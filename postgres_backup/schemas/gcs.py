from enum import Enum


class CloudStorageType(str, Enum):
    STANDARD = 'STANDARD'
    NEARLINE = 'NEARLINE'
    COLDLINE = 'COLDLINE'
    ARCHIVE = 'ARCHIVE'
