from enum import Enum


class CloudStorageType(str, Enum):
    STANDARD: str = 'STANDARD'
    NEARLINE: str = 'NEARLINE'
    COLDLINE: str = 'COLDLINE'
    ARCHIVE: str = 'ARCHIVE'
