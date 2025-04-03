from typing import List

from sqlalchemy import and_, select

from ..models.chat import ChatMember
from ..models.user import User, UserProfilePhoto
from .base import BaseService


class UserService(BaseService):
    def get_user_profile_photos(
        self, user_id: int, offset: int = 0, limit: int = 100
    ) -> List[UserProfilePhoto]:
        return (
            self.session.query(UserProfilePhoto)
            .filter(UserProfilePhoto.user_id == user_id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_user_chats(self, user_id: int, offset: int = 0, limit: int = 100):
        return (
            self.session.query(select(ChatMember.chat))
            .filter(
                and_(ChatMember.user_id == user_id, ChatMember.deleted_at.is_(None))
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).where(User.id == user_id).first()

    def get_user_by_username(
        self, username: str, offset: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            self.session.query(User)
            .filter(User.username.contains(username))
            .offset(offset)
            .limit(limit)
            .all()
        )
