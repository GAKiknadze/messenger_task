from datetime import datetime

from ..models.enums import ContentType
from ..models.file import File
from ..models.message import Message
from .base import BaseService


class MediaService(BaseService):
    def _send_media(
        self,
        chat_id: int,
        sender_id: int,
        content_type: ContentType,
        file_data: bytes,
        mime_type: str,
        file_name: str,
    ):
        file_id = f"file_{datetime.now().timestamp()}"
        new_file = File(
            id=file_id, content=file_data, mime_type=mime_type, file_path=file_name
        )

        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            content_type=content_type,
            file_id=file_id,
        )

        self.session.add_all([new_file, message])
        return message

    def send_photo(
        self,
        chat_id: int,
        sender_id: int,
        image_data: bytes,
        mime_type: str = "image/jpeg",
        file_name: str = "photo.jpg",
    ):
        return self._send_media(
            chat_id, sender_id, ContentType.PHOTO, image_data, mime_type, file_name
        )

    def send_audio(
        self,
        chat_id: int,
        sender_id: int,
        audio_data: bytes,
        mime_type: str = "audio/mpeg",
        file_name: str = "audio.mp3",
    ):
        return self._send_media(
            chat_id, sender_id, ContentType.AUDIO, audio_data, mime_type, file_name
        )

    def send_location(
        self, chat_id: int, sender_id: int, latitude: float, longitude: float
    ):
        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            content_type=ContentType.LOCATION,
            location_data={"latitude": latitude, "longitude": longitude},
        )
        self.session.add(message)
        return message

    def send_venue(
        self,
        chat_id: int,
        sender_id: int,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
    ):
        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            content_type=ContentType.VENUE,
            venue_data={
                "latitude": latitude,
                "longitude": longitude,
                "title": title,
                "address": address,
            },
        )
        self.session.add(message)
        return message

    def send_contact(
        self,
        chat_id: int,
        sender_id: int,
        phone_number: str,
        first_name: str,
        last_name: str = None,
    ):
        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            content_type=ContentType.CONTACT,
            contact_data={
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        self.session.add(message)
        return message

    def get_file(self, file_id: str):
        return self.session.query(File).get(file_id)
