import json
import uuid
import threading
from pathlib import Path
from typing import List, Optional, Dict
from ..core.config import settings
from ..core.logger import setup_logger
from ..domain.models.community import CommunityComment

logger = setup_logger("CommunityStorage")


class CommunityStorage:
    """Thread-safe persistent storage for community comments and know-how reviews."""

    def __init__(self, storage_file: Optional[Path] = None):
        self.storage_file = storage_file or (settings.COMMUNITY_DIR / "comments.json")
        self._lock = threading.Lock()
        self._init_storage()

    def _init_storage(self) -> None:
        """Initialize storage file with default seed comments if it doesn't exist."""
        with self._lock:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            if not self.storage_file.exists():
                seed_comments = self._generate_seed_comments()
                self._save_raw(seed_comments)

    def _generate_seed_comments(self) -> Dict[str, List[dict]]:
        """Default seed comments showcasing the best know-how pinned at top."""
        return {
            "spicy-braised-tofu": [
                {
                    "comment_id": "knowhow-tofu-001",
                    "recipe_id": "spicy-braised-tofu",
                    "user_id": "chef_master_99",
                    "user_name": "들기름매니아",
                    "user_photo_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80",
                    "content": "💡 핵심 꿀팁: 양념장 붓기 전에 들기름 1스푼을 냄비 바닥에 살짝 둘러 두부 앞뒤를 30초씩만 애벌 부치고 양념을 부어보세요! 고소한 풍미가 두부 속까지 배어서 밥 두 공기 순식간에 비웁니다. 백종원 셰프 팁대로 숟가락으로 국물 끼얹는 게 진짜 신의 한 수예요!",
                    "upvotes": 48,
                    "downvotes": 1,
                    "voters": {"seed_user_1": "up", "seed_user_2": "up"},
                    "is_knowhow": True,
                    "created_at": "2026-09-15 19:40"
                },
                {
                    "comment_id": "review-tofu-002",
                    "recipe_id": "spicy-braised-tofu",
                    "user_id": "home_cook_24",
                    "user_name": "자취요리왕",
                    "user_photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80",
                    "content": "양파를 냄비 바닥에 도톰하게 깔고 두부를 올렸더니 전혀 눌어붙지 않고 양파 단맛이 배어서 너무 맛있게 완성됐어요. 핸즈프리 음성 가이드 들으면서 하니까 손에 양념 묻은 채로 스마트폰 안 만져도 돼서 너무 편합니다!",
                    "upvotes": 25,
                    "downvotes": 0,
                    "voters": {"seed_user_3": "up"},
                    "is_knowhow": False,
                    "created_at": "2026-09-16 11:15"
                },
                {
                    "comment_id": "review-tofu-003",
                    "recipe_id": "spicy-braised-tofu",
                    "user_id": "spicy_lover",
                    "user_name": "청양고추팍팍",
                    "user_photo_url": None,
                    "content": "매콤한 거 좋아하시는 분들은 청양고추 1개 송송 썰어 넣으세요. 칼칼한 맛이 더해져서 술안주로도 최고입니다!",
                    "upvotes": 14,
                    "downvotes": 2,
                    "voters": {},
                    "is_knowhow": False,
                    "created_at": "2026-09-16 15:30"
                }
            ],
            "pork-kimchi-jjigae": [
                {
                    "comment_id": "knowhow-jjigae-001",
                    "recipe_id": "pork-kimchi-jjigae",
                    "user_id": "kimchi_king",
                    "user_name": "찌개장인",
                    "user_photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80",
                    "content": "돼지고기를 참기름에 달달 볶다가 새우젓 반 스푼을 고기에 먼저 넣고 볶으면 고기 누린내가 싹 잡히고 육수 깊이가 달라집니다!",
                    "upvotes": 52,
                    "downvotes": 1,
                    "voters": {},
                    "is_knowhow": True,
                    "created_at": "2026-09-14 18:20"
                }
            ]
        }

    def _read_raw(self) -> Dict[str, List[dict]]:
        """Read comments raw dictionary from file."""
        try:
            if not self.storage_file.exists():
                return {}
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading community comments: {e}")
            return {}

    def _save_raw(self, data: Dict[str, List[dict]]) -> None:
        """Save comments dictionary to file."""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving community comments: {e}")

    def get_comments(self, recipe_id: str) -> List[CommunityComment]:
        """Fetch all comments for a recipe, sorted with Know-How first then by popularity."""
        with self._lock:
            data = self._read_raw()
            raw_list = data.get(recipe_id, [])

            # Convert to models and recalculate is_knowhow
            comments: List[CommunityComment] = [CommunityComment(**item) for item in raw_list]
            if comments:
                # Find maximum net upvotes
                max_net = max(c.upvotes - c.downvotes for c in comments)
                for c in comments:
                    net_score = c.upvotes - c.downvotes
                    # Selected as best know-how if highest net votes and at least 5 upvotes
                    c.is_knowhow = (net_score == max_net and c.upvotes >= 5)

            # Sort: is_knowhow first (descending), then by net score (descending), then created_at (descending)
            comments.sort(key=lambda c: (1 if c.is_knowhow else 0, c.upvotes - c.downvotes, c.created_at), reverse=True)
            return comments

    def add_comment(
        self,
        recipe_id: str,
        user_id: str,
        user_name: str,
        content: str,
        user_photo_url: Optional[str] = None
    ) -> CommunityComment:
        """Add a new comment for a completed recipe."""
        with self._lock:
            data = self._read_raw()
            if recipe_id not in data:
                data[recipe_id] = []

            new_comment = CommunityComment(
                comment_id=f"comment-{uuid.uuid4().hex[:8]}",
                recipe_id=recipe_id,
                user_id=user_id,
                user_name=user_name,
                user_photo_url=user_photo_url,
                content=content,
                upvotes=0,
                downvotes=0,
                voters={},
                is_knowhow=False
            )

            data[recipe_id].append(new_comment.model_dump())
            self._save_raw(data)
            logger.info(f"Added comment {new_comment.comment_id} to recipe {recipe_id} by {user_name}")
            return new_comment

    def vote(self, comment_id: str, user_id: str, vote_type: str) -> Optional[CommunityComment]:
        """Process upvote or downvote with toggle & switch logic."""
        if vote_type not in ("up", "down"):
            return None

        with self._lock:
            data = self._read_raw()
            target_recipe = None
            target_item = None

            for recipe_id, comments in data.items():
                for item in comments:
                    if item.get("comment_id") == comment_id:
                        target_recipe = recipe_id
                        target_item = item
                        break
                if target_item:
                    break

            if not target_item:
                return None

            voters = target_item.setdefault("voters", {})
            current_vote = voters.get(user_id)

            if current_vote == vote_type:
                # Cancel existing vote
                if vote_type == "up":
                    target_item["upvotes"] = max(0, target_item.get("upvotes", 0) - 1)
                else:
                    target_item["downvotes"] = max(0, target_item.get("downvotes", 0) - 1)
                del voters[user_id]
            elif current_vote is not None:
                # Switch vote (e.g. from down to up or up to down)
                if current_vote == "up":
                    target_item["upvotes"] = max(0, target_item.get("upvotes", 0) - 1)
                else:
                    target_item["downvotes"] = max(0, target_item.get("downvotes", 0) - 1)

                if vote_type == "up":
                    target_item["upvotes"] = target_item.get("upvotes", 0) + 1
                else:
                    target_item["downvotes"] = target_item.get("downvotes", 0) + 1
                voters[user_id] = vote_type
            else:
                # New vote
                if vote_type == "up":
                    target_item["upvotes"] = target_item.get("upvotes", 0) + 1
                else:
                    target_item["downvotes"] = target_item.get("downvotes", 0) + 1
                voters[user_id] = vote_type

            # Recalculate know-how for this recipe's comments
            recipe_comments = data[target_recipe]
            if recipe_comments:
                max_net = max(c.get("upvotes", 0) - c.get("downvotes", 0) for c in recipe_comments)
                for c in recipe_comments:
                    net = c.get("upvotes", 0) - c.get("downvotes", 0)
                    c["is_knowhow"] = (net == max_net and c.get("upvotes", 0) >= 5)

            self._save_raw(data)
            return CommunityComment(**target_item)


# Global storage singleton
community_storage = CommunityStorage()
