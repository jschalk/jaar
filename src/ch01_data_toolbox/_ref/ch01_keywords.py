from enum import Enum


class Ch01Keywords(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    sqlite_datatype = "sqlite_datatype"

    def __str__(self):
        return self.value
