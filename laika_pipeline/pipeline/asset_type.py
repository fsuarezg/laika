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
    def from_string(cls, value: str):
        """
        Convert a string to an AssetType (case insensitive).
        Raises ValueError if no match is found.
        """
        normalized = value.strip().lower()
        for item in cls:
            if item.value == normalized:
                return item
        raise ValueError(f"Unknown AssetType: {value}")

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
