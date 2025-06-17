from enum import Enum

class GenericScopes(Enum):
    OPENID = 'openid'


class UserInfoScopes(Enum):
    PROFILE = "https://www.googleapis.com/auth/userinfo.profile"
    EMAIL = "https://www.googleapis.com/auth/userinfo.email"


class CalendarScopes(Enum):
    READONLY = "https://www.googleapis.com/auth/calendar.readonly"


class TaskScopes(Enum):
    READONLY = "https://www.googleapis.com/auth/tasks.readonly"


class DriveScopes(Enum):

    VIEW_MANAGE = "https://www.googleapis.com/auth/drive"
    METADATA_READONLY = "https://www.googleapis.com/auth/drive.metadata.readonly"

class SheetScopes(Enum):

    RAEDONLY = "https://www.googleapis.com/auth/spreadsheets.readonly"