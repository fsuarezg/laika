from typing import Any

from laika_pipeline.pipeline.status import Status


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
        if isinstance(status, str):
            status = Status.from_string(status)
        self._status = status

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
