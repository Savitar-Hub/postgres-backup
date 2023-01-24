from enum import StrEnum


class CloudStorageType(StrEnum):
    STANDARD = 'STANDARD'
    NEARLINE = 'NEARLINE'
    COLDLINE = 'COLDLINE'
    ARCHIVE = 'ARCHIVE'
