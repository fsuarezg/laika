from __future__ import annotations
from enum import Enum


class Status(Enum):
    """
    A class representing the status of an asset in the pipeline.
    """

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DEPRECATED = 'deprecated'

    @classmethod
    def list_values(cls):
        """
        Return a list of all enum values as strings.
        """
        return [item.value for item in cls]

    @classmethod
    def from_string(cls, value: str) -> tuple[Status | None, str]:
        """
        Convert a string to a Status (case insensitive).
        To not raise an error if this fails it will return None and the
        original string, we validate the value in the AssetVersion class.
        """
        normalized = value.strip().lower()
        for item in cls:
            if item.value == normalized:
                return item, value
        return None, value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """
        Check if a string is a valid status.
        """
        try:
            cls.from_string(value)
            return True
        except ValueError:
            return False
