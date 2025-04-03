from sqlalchemy.orm import Session

from ..models.chat import ChatMember
from ..models.enums import Role


class BaseService:
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def _check_permission(
        self, chat_id: int, user_id: int, required_role: Role = Role.ADMIN
    ) -> bool:
        member = (
            self.session.query(ChatMember)
            .filter(
                ChatMember.chat_id == chat_id,
                ChatMember.user_id == user_id,
                ChatMember.deleted_at.is_(None),
            )
            .first()
        )

        if not member or (required_role == Role.OWNER and member.role != Role.OWNER):
            raise PermissionError("Insufficient permissions")
        return True
