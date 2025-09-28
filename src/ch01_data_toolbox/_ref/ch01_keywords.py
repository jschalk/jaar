# from src.ch00_purpose._ref.ch00_keywords import *
from enum import Enum


def INSERT_str() -> str:
    return "INSERT"


def UPDATE_str() -> str:
    return "UPDATE"


def sqlite_datatype_str() -> str:
    return "sqlite_datatype"


class Ch01Keywords(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    sqlite_datatype = "sqlite_datatype"
