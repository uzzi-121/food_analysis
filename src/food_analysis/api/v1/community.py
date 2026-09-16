from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from ...core.config import settings
from ...core.logger import setup_logger
from ...domain.models.community import (
    CommunityComment,
    CommentCreateRequest,
    VoteRequest,
    FirebaseConfigResponse,
)
from ...storage.community_storage import community_storage

logger = setup_logger("CommunityRouter")
router = APIRouter(prefix="/community", tags=["Community"])


@router.get("/auth/config", response_model=FirebaseConfigResponse)
async def get_firebase_config() -> FirebaseConfigResponse:
    """Provide public Firebase configuration for client-side Google Auth."""
    is_configured = bool(
        settings.FIREBASE_API_KEY
        and settings.FIREBASE_PROJECT_ID
        and settings.FIREBASE_APP_ID
    )
    return FirebaseConfigResponse(
        api_key=settings.FIREBASE_API_KEY,
        auth_domain=settings.FIREBASE_AUTH_DOMAIN,
        project_id=settings.FIREBASE_PROJECT_ID,
        storage_bucket=settings.FIREBASE_STORAGE_BUCKET,
        messaging_sender_id=settings.FIREBASE_MESSAGING_SENDER_ID,
        app_id=settings.FIREBASE_APP_ID,
        is_configured=is_configured,
    )


@router.get("/recipes/{recipe_id}/comments", response_model=List[CommunityComment])
async def get_recipe_comments(
    recipe_id: str,
    current_user_id: Optional[str] = Query(None, description="현재 로그인한 사용자 ID (투표 상태 확인용)")
) -> List[CommunityComment]:
    """
    Get all community comments for a recipe.
    Publicly accessible (non-logged-in users can view).
    Ranked with Best Know-How comments pinned at the top.
    """
    comments = community_storage.get_comments(recipe_id)
    return comments


@router.post("/recipes/{recipe_id}/comments", response_model=CommunityComment, status_code=status.HTTP_201_CREATED)
async def create_recipe_comment(
    recipe_id: str,
    payload: CommentCreateRequest
) -> CommunityComment:
    """
    Post a cooking tip/comment on a recipe.
    Requires user to be logged in (Firebase Auth) and have completed the recipe.
    """
    if not payload.user_id or not payload.user_name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요한 서비스입니다. 구글 로그인 후 이용해주세요."
        )

    if not payload.completed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="레시피 조리를 완료한 사용자만 후기 및 노하우 댓글을 작성할 수 있습니다."
        )

    content = payload.content.strip()
    if not content or len(content) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="댓글 내용을 3자 이상 입력해주세요."
        )

    new_comment = community_storage.add_comment(
        recipe_id=recipe_id,
        user_id=payload.user_id,
        user_name=payload.user_name,
        content=content,
        user_photo_url=payload.user_photo_url,
    )
    return new_comment


@router.post("/comments/{comment_id}/vote", response_model=CommunityComment)
async def vote_comment(
    comment_id: str,
    payload: VoteRequest
) -> CommunityComment:
    """
    Upvote or downvote a comment.
    Requires login. Toggle if voted again, or switch vote.
    """
    if not payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="추천/비추천 투표는 구글 로그인 후 가능합니다."
        )

    if payload.vote_type not in ("up", "down"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="올바르지 않은 투표 유형입니다. ('up' 또는 'down')"
        )

    updated_comment = community_storage.vote(
        comment_id=comment_id,
        user_id=payload.user_id,
        vote_type=payload.vote_type,
    )

    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다."
        )

    return updated_comment
