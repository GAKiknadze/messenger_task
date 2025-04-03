from datetime import datetime
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from ..models.enums import ContentType, DeletionType, PollType
from ..models.message import DeletedMessage, Message
from ..models.poll import Poll, PollOption
from .base import BaseService


class MessageService(BaseService):
    def send_message(
        self,
        chat_id: int,
        sender_id: int,
        content: str | None = None,
        content_type: ContentType = ContentType.TEXT,
        original_message_id: int = None,
    ) -> Message:
        try:
            if original_message_id:
                original = self.session.query(Message).where(Message.id == original_message_id).one()
                if not original.chat.allow_forwarding:
                    raise PermissionError("Forwarding not allowed in source chat")

            message = Message(
                chat_id=chat_id,
                sender_id=sender_id,
                content=content,
                content_type=content_type,
                original_message_id=original_message_id,
            )
            self.session.add(message)
            return message
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

    def edit_message_text(self, message_id: int, user_id: int, new_text: str) -> Message:
        message = self.session.query(Message).where(Message.id == message_id).one()
        if message.sender_id != user_id:
            self._check_permission(message.chat_id, user_id)

        message.content = new_text
        message.edited_at = datetime.utcnow()
        return message

    def delete_message(self, message_id: int, user_id: int, hard_delete: bool = False) -> Message:
        message = self.session.query(Message).where(Message.id == message_id).one()

        if message.sender_id != user_id:
            self._check_permission(message.chat_id, user_id)

        if hard_delete:
            deleted_msg = DeletedMessage(
                message_id=message_id, deletion_type=DeletionType.HARD
            )
            self.session.add(deleted_msg)
            self.session.delete(message)
        else:
            message.deleted_at = datetime.utcnow()
        return message

    def forward_message(
        self, source_message_id: int, target_chat_id: int, sender_id: int
    ) -> Message:
        return self.send_message(
            chat_id=target_chat_id,
            sender_id=sender_id,
            content="Forwarded message",
            original_message_id=source_message_id,
        )

    def copy_message(self, source_message_id: int, target_chat_id: int, sender_id: int) -> Message:
        source = self.session.query(Message).where(Message.id == source_message_id).one()
        return self.send_message(
            chat_id=target_chat_id,
            sender_id=sender_id,
            content=source.content,
            content_type=source.content_type,
            original_message_id=source.id,
        )

    def send_poll(
        self,
        chat_id: int,
        sender_id: int,
        question: str,
        options: List[str],
        poll_type: PollType = PollType.REGULAR,
    ) -> Message:
        poll = Poll(
            question=question,
            type=poll_type,
            options=[PollOption(text=text) for text in options],
        )

        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            content_type=ContentType.POLL,
            poll=poll,
        )
        self.session.add(message)
        return message

    def stop_poll(self, message_id: int, user_id: int) -> Message:
        message = self.session.query(Message).where(Message.id == message_id).one()
        if message.sender_id != user_id:
            self._check_permission(message.chat_id, user_id)

        message.poll.is_closed = True
        return message
