from __future__ import annotations
from enum import Enum


class AssetType(Enum):
    """
    A class representing the type of an asset in the pipeline.
    """

    CHARACTER = 'character'
    PROP = 'prop'
    SET = 'set'
    ENVIRONMENT = 'environment'
    VEHICLE = 'vehicle'
    DRESSING = 'dressing'
    FX = 'fx'

    @classmethod
    def list_values(cls):
        """
        Return a list of all enum values as strings.
        """
        return [item.value for item in cls]

    @classmethod
    def from_string(cls, value: str) -> tuple[AssetType | None, str]:
        """
        Convert a string to an AssetType (case insensitive).
        To not raise an error, if this fails it will return None and the
        original string, we validate the value in the Asset class.

        Args:
            value (str): The string to convert.

        Returns:
            tuple: A tuple of (AssetType or None, original string).
        """
        normalized = value.strip().lower()
        for item in cls:
            if item.value == normalized:
                return item, value
        return None, value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """
        Check if a string is a valid asset type.
        """
        try:
            cls.from_string(value)
            return True
        except ValueError:
            return False
