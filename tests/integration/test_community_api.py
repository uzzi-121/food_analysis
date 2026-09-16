from fastapi.testclient import TestClient
from food_analysis.api.app import app

client = TestClient(app)


def test_get_firebase_config():
    response = client.get("/api/v1/community/auth/config")
    assert response.status_code == 200
    data = response.json()
    assert "is_configured" in data
    assert "api_key" in data


def test_get_recipe_comments_unauthenticated():
    # Anyone (guests included) can read recipe comments
    response = client.get("/api/v1/community/recipes/spicy-braised-tofu/comments")
    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) >= 1
    # Check that the first comment has is_knowhow = True
    assert comments[0]["is_knowhow"] is True


def test_create_comment_requires_login():
    response = client.post(
        "/api/v1/community/recipes/spicy-braised-tofu/comments",
        json={
            "recipe_id": "spicy-braised-tofu",
            "user_id": "",
            "user_name": "",
            "content": "맛있어요!",
            "completed": True
        }
    )
    assert response.status_code == 401


def test_create_comment_requires_completion():
    response = client.post(
        "/api/v1/community/recipes/spicy-braised-tofu/comments",
        json={
            "recipe_id": "spicy-braised-tofu",
            "user_id": "test-user-1",
            "user_name": "홍길동",
            "content": "맛있어요!",
            "completed": False
        }
    )
    assert response.status_code == 403


def test_create_comment_and_vote_success():
    # 1. Post comment as a completed user
    response = client.post(
        "/api/v1/community/recipes/spicy-braised-tofu/comments",
        json={
            "recipe_id": "spicy-braised-tofu",
            "user_id": "google-uid-777",
            "user_name": "구글유저",
            "user_photo_url": "https://example.com/photo.jpg",
            "content": "청양고추 반 개 넣으면 칼칼함이 배가 됩니다!",
            "completed": True
        }
    )
    assert response.status_code == 201
    created = response.json()
    comment_id = created["comment_id"]
    assert created["user_name"] == "구글유저"

    # 2. Vote on this comment
    vote_res = client.post(
        f"/api/v1/community/comments/{comment_id}/vote",
        json={
            "user_id": "voter-user-999",
            "vote_type": "up"
        }
    )
    assert vote_res.status_code == 200
    voted = vote_res.json()
    assert voted["upvotes"] == 1
