import pytest
import tempfile
from pathlib import Path
from food_analysis.storage.community_storage import CommunityStorage
from food_analysis.domain.models.community import CommunityComment


def test_community_storage_initialization():
    with tempfile.TemporaryDirectory() as tmp_dir:
        storage_file = Path(tmp_dir) / "comments.json"
        storage = CommunityStorage(storage_file)

        # Check default seed comments loaded
        comments = storage.get_comments("spicy-braised-tofu")
        assert len(comments) >= 1
        # Top comment should have is_knowhow = True
        assert comments[0].is_knowhow is True
        assert "들기름" in comments[0].content


def test_community_add_comment():
    with tempfile.TemporaryDirectory() as tmp_dir:
        storage_file = Path(tmp_dir) / "comments.json"
        storage = CommunityStorage(storage_file)

        new_c = storage.add_comment(
            recipe_id="test-recipe",
            user_id="user-123",
            user_name="홍길동",
            content="정말 간편하고 맛있는 레시피입니다!",
            user_photo_url=None
        )
        assert new_c.recipe_id == "test-recipe"
        assert new_c.user_name == "홍길동"
        assert new_c.upvotes == 0
        assert new_c.is_knowhow is False

        comments = storage.get_comments("test-recipe")
        assert len(comments) == 1
        assert comments[0].comment_id == new_c.comment_id


def test_community_vote_and_knowhow_promotion():
    with tempfile.TemporaryDirectory() as tmp_dir:
        storage_file = Path(tmp_dir) / "comments.json"
        storage = CommunityStorage(storage_file)

        c = storage.add_comment(
            recipe_id="test-recipe",
            user_id="user-1",
            user_name="요리왕",
            content="비법 양념 공개합니다."
        )

        # Upvote 5 times from different users
        for i in range(5):
            updated = storage.vote(c.comment_id, f"voter-{i}", "up")

        assert updated.upvotes == 5
        assert updated.downvotes == 0
        assert updated.is_knowhow is True

        # Toggle vote off for voter-0
        updated = storage.vote(c.comment_id, "voter-0", "up")
        assert updated.upvotes == 4
        # Since upvotes < 5, knowhow drops
        assert updated.is_knowhow is False
