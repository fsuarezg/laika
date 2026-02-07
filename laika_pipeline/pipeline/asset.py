from typing import Any

from laika_pipeline.pipeline.asset_type import AssetType
from laika_pipeline.validation.operation_result import OperationResult


class Asset():
    """
    A class representing an asset in the pipeline.
    """

    def __init__(self, name: str,
                 asset_type: str | AssetType):
        """
        Initialise an Asset instance.

        Args:
            name (str): The name of the asset
            asset_type (str | AssetType): The type of the asset

        Returns:
            _type_: _description_
        """
        self._name = name.strip()
        if isinstance(asset_type, str):
            asset_type = AssetType.from_string(asset_type)
        self._asset_type = asset_type
        # Generate a unique code for the asset based on its name and type
        self._code = self.generate_code(name, asset_type)

    def __eq__(self, other: Any) -> bool:
        """Check if Asset is equal to another Asset.
        Args:
            other: Another Asset instance to compare against.
        Returns:
            bool: True if both Assets have the same code,
                  False otherwise.
        """
        if isinstance(other, Asset):
            return self.code == other.code
        return False

    def __repr__(self) -> str:
        """Return a string representation of the Asset."""
        return (
            f"Asset(name='{self.name}', "
            f"asset_type='{self.asset_type.value}', "
            f"code='{self.code}')"
        )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Asset name must be a string.")
        self._name = value

    @property
    def asset_type(self):
        return self._asset_type

    @asset_type.setter
    def asset_type(self, value: AssetType):
        if not isinstance(value, AssetType):
            raise TypeError("Asset type must be a valid AssetType.")
        self._asset_type = value

    @property
    def code(self):
        return self._code

    def generate_code(self, name, asset_type):
        return f"{name.lower().replace(' ', '_')}_{asset_type.value}"

    def validate(self) -> OperationResult:
        """
        Validate the asset's properties.

        Returns:
            OperationResult: An object indicating success or failure of
                             validation, and an error message if validation
                             fails.
        """
        if not self.name or not self.name.strip():
            return OperationResult(
                success=False,
                error_message="Asset name must be a non-empty string"
            )
        if not isinstance(self.asset_type, AssetType):
            valid = ", ".join([t.value for t in AssetType])
            return OperationResult(
                success=False,
                error_message=(
                    f"Invalid asset type '{self.asset_type}'."
                    f"Must be one of: {valid}"
                )
            )
        return OperationResult(success=True)

    def to_dict(self) -> dict:
        """
        Convert the Asset instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Asset.
        """
        return {
            "name": self.name,
            "type": self.asset_type.value,
            "code": self.code
        }

    def from_dict(data: dict):
        """
        Create an Asset instance from a dictionary.

        Args:
            data (dict): A dictionary containing the asset's properties.

        Returns:
            Asset: A new Asset instance created from the dictionary.
        """
        name = data["name"]
        asset_type = AssetType.from_string(data["type"])
        return Asset(name=name, asset_type=asset_type)
