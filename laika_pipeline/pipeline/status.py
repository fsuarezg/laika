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
    def from_string(cls, value: str):
        """
        Convert a string to a Status (case insensitive).
        Raises ValueError if no match is found.
        """
        normalized = value.strip().lower()
        for item in cls:
            if item.value == normalized:
                return item
        raise ValueError(f"Unknown Status: {value}")

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
