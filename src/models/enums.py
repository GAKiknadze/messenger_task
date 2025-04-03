from enum import Enum


class Role(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class ContentType(str, Enum):
    TEXT = "TEXT"
    PHOTO = "PHOTO"
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"
    VIDEO = "VIDEO"
    ANIMATION = "ANIMATION"
    VOICE = "VOICE"
    LOCATION = "LOCATION"
    VENUE = "VENUE"
    CONTACT = "CONTACT"
    POLL = "POLL"


class PollType(str, Enum):
    REGULAR = "regular"
    QUIZ = "quiz"


class DeletionType(str, Enum):
    SOFT = "soft"
    HARD = "hard"
