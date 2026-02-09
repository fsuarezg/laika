from typing import Any

from laika_pipeline.pipeline.status import Status
from laika_pipeline.validation.operation_result import OperationResult


class AssetVersion():
    """
    A class representing an asset version in the pipeline
    """

    def __init__(self,
                 asset: str,
                 department: str,
                 version: int,
                 status: str | Status = Status.ACTIVE):
        """
        Initialize an AssetVersion instance.

        Args:
            asset (str): The code of the asset this version belongs to.
            department (str): The department that created the asset version.
            version (int): The version number of the asset (e.g., 1, 2, 3).
            status (str | Status, optional): The status of the asset version.
                                             Defaults to 'active'.
        """
        self._asset = asset
        self._department = department
        self._version = version
        self._status = self._normalize_status(status)

    def __eq__(self, other: Any) -> bool:
        """
        Check if AssetVersion is equal to another AssetVersion.

        Args:
            other: Another AssetVersion instance to compare against.

        Returns:
            bool: True if both AssetVersions have the same asset, department,
                  version, False otherwise.
        """
        if isinstance(other, AssetVersion):
            return (self.asset == other.asset and
                    self.department == other.department and
                    self.version == other.version)
        return False

    def __repr__(self) -> str:
        """
        Return a string representation of the AssetVersion.
        """
        return (
            f"AssetVersion(asset_code='{self._asset}', "
            f"department='{self.department}', "
            f"version='{self.version}'), "
            f"status='{self.status.value}')"
        )

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Asset must be a string.")
        self._asset = value

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Department must be a string.")
        self._department = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Version must be an integer.")
        if not value > 0:
            raise ValueError("Version must be a positive integer.")
        self._version = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str | Status):
        if isinstance(value, str):
            value = Status.from_string(value)
        if not isinstance(value, Status):
            raise TypeError("Status must be a valid Status.")
        self._status = value

    def _normalize_status(self, value: str | Status) -> Status | str:
        if isinstance(value, Status):
            return value
        enum_value, raw = Status.from_string(value)
        return enum_value if enum_value is not None else raw

    def validate(self) -> OperationResult:
        """ Validate the asset version's properties.

        Returns:
            OperationResult: An object indicating success or failure of
                             validation, and an error message if validation
                             fails.
        """
        if not self.asset or not self.asset.strip():
            return OperationResult(
                success=False,
                error_message="Asset code must be a non-empty string"
            )
        if not self.department or not self.department.strip():
            return OperationResult(
                success=False,
                error_message="Department must be a non-empty string"
            )
        if not isinstance(self.version, int):
            return OperationResult(
                success=False,
                error_message="Version must be an integer"
            )
        if not self.version > 0:
            return OperationResult(
                success=False,
                error_message="Version must be a positive integer"
            )
        if not isinstance(self.status, Status):
            valid = ", ".join([s.value for s in Status])
            return OperationResult(
                success=False,
                error_message=(
                    f"Invalid status '{self.status}'. Must be one of: {valid}"
                )
            )
        return OperationResult(success=True)

    def to_dict(self) -> dict:
        """
        Convert the AssetVersion instance to a dictionary.
        """
        return {
            "asset": self.asset,
            "department": self.department,
            "version": self.version,
            "status": self.status.value
        }

    def from_dict(data: dict):
        """
        Create an AssetVersion instance from a dictionary.

        Args:
            data (dict): A dictionary with keys 'asset', 'department',
                         'version', and 'status'.
        Returns:
            AssetVersion: An instance of AssetVersion created from the
                          dictionary data.
        """
        asset = data["asset"]
        department = data["department"]
        version = data["version"]
        status, _ = Status.from_string(data["status"])
        return AssetVersion(
            asset=asset,
            department=department,
            version=version,
            status=status
        )
