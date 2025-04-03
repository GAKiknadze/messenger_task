import uuid
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy.exc import SQLAlchemyError

from ..models.chat import Chat, ChatMember, ChatPermissions
from ..models.enums import Role
from ..models.invite import InviteLink
from .base import BaseService


class ChatService(BaseService):
    def create_chat(self, creator_id: int, title: str, description: str = None):
        try:
            new_chat = Chat(title=title, description=description)
            self.session.add(new_chat)
            self.session.flush()

            self.add_member(new_chat.id, creator_id, Role.OWNER)
            return new_chat
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def update_chat_settings(self, chat_id: int, user_id: int, **settings):
        self._check_permission(chat_id, user_id, Role.OWNER)
        chat = self.session.query(Chat).get(chat_id)
        for key, value in settings.items():
            setattr(chat, key, value)
        return chat

    def get_chat(self, chat_id: int):
        return self.session.query(Chat).get(chat_id)

    def get_chat_administrators(self, chat_id: int):
        return (
            self.session.query(ChatMember)
            .filter(
                ChatMember.chat_id == chat_id,
                ChatMember.role.in_([Role.OWNER, Role.ADMIN]),
                ChatMember.deleted_at.is_(None),
            )
            .all()
        )

    def set_chat_permissions(self, chat_id: int, user_id: int, permissions: Dict):
        self._check_permission(chat_id, user_id, Role.OWNER)
        chat_perms = self.session.query(ChatPermissions).get(
            chat_id
        ) or ChatPermissions(chat_id=chat_id)
        for key, value in permissions.items():
            setattr(chat_perms, key, value)
        self.session.add(chat_perms)
        return chat_perms

    def create_invite_link(
        self,
        chat_id: int,
        creator_id: int,
        expires: Optional[datetime] = None,
        member_limit: int = None,
    ):
        link = f"https://chat.example/invite/{uuid.uuid4()}"
        new_link = InviteLink(
            chat_id=chat_id,
            creator_id=creator_id,
            link=link,
            expire_date=expires,
            member_limit=member_limit,
        )
        self.session.add(new_link)
        return new_link

    def revoke_invite_link(self, link_id: int, user_id: int):
        link = self.session.query(InviteLink).get(link_id)
        self._check_permission(link.chat_id, user_id)
        link.is_revoked = True
        return link

    def export_chat_invite_link(self, chat_id: int, user_id: int):
        self._check_permission(chat_id, user_id)
        return (
            self.session.query(InviteLink)
            .filter(InviteLink.chat_id == chat_id, InviteLink.is_revoked == False)
            .order_by(InviteLink.created_at.desc())
            .first()
        )

    def ban_chat_member(self, chat_id: int, moderator_id: int, user_id: int):
        self._check_permission(chat_id, moderator_id)
        member = self._get_chat_member(chat_id, user_id)
        member.deleted_at = datetime.utcnow()
        return member

    def unban_chat_member(self, chat_id: int, moderator_id: int, user_id: int):
        self._check_permission(chat_id, moderator_id)
        member = self._get_chat_member(chat_id, user_id)
        member.deleted_at = None
        return member

    def restrict_chat_member(
        self, chat_id: int, moderator_id: int, user_id: int, permissions: Dict
    ):
        self._check_permission(chat_id, moderator_id)
        member = self._get_chat_member(chat_id, user_id)
        member.restrictions = permissions
        return member

    def promote_chat_member(
        self, chat_id: int, promoter_id: int, user_id: int, role: Role
    ):
        self._check_permission(chat_id, promoter_id, Role.OWNER)
        member = self._get_chat_member(chat_id, user_id)
        member.role = role
        return member

    def leave_chat(self, chat_id: int, user_id: int):
        member = self._get_chat_member(chat_id, user_id)
        member.deleted_at = datetime.utcnow()
        return member

    def _get_chat_member(self, chat_id: int, user_id: int):
        return (
            self.session.query(ChatMember)
            .filter(ChatMember.chat_id == chat_id, ChatMember.user_id == user_id)
            .first()
        )
