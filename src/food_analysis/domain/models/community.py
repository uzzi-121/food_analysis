from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class CommunityComment(BaseModel):
    """Community comment and cooking know-how model for a recipe."""
    comment_id: str = Field(description="고유 댓글 식별자 (UUID)")
    recipe_id: str = Field(description="대상 레시피 식별자 (예: spicy-braised-tofu)")
    user_id: str = Field(description="작성자 고유 ID (Firebase UID)")
    user_name: str = Field(description="작성자 표시 이름")
    user_photo_url: Optional[str] = Field(default=None, description="작성자 구글 프로필 사진 URL")
    content: str = Field(description="댓글 및 조리 꿀팁 내용")
    upvotes: int = Field(default=0, description="추천 수")
    downvotes: int = Field(default=0, description="비추천 수")
    voters: Dict[str, str] = Field(default_factory=dict, description="투표한 사용자 맵 (user_id -> 'up' | 'down')")
    is_knowhow: bool = Field(default=False, description="베스트 조리 노하우 선정 여부")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"), description="작성 일시")


class CommentCreateRequest(BaseModel):
    """Request payload for posting a new comment."""
    recipe_id: str
    user_id: str
    user_name: str
    user_photo_url: Optional[str] = None
    content: str
    completed: bool = Field(default=True, description="조리 완료 여부 인증 플래그")


class VoteRequest(BaseModel):
    """Request payload for voting on a comment."""
    user_id: str
    vote_type: str = Field(description="'up' 또는 'down'")


class FirebaseConfigResponse(BaseModel):
    """Public Firebase configuration for frontend client initialization."""
    api_key: str = ""
    auth_domain: str = ""
    project_id: str = ""
    storage_bucket: str = ""
    messaging_sender_id: str = ""
    app_id: str = ""
    is_configured: bool = False
