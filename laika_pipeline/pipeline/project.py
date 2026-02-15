from laika_pipeline.lib.load_json import load_json

from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion
from laika_pipeline.validation.operation_result import OperationResult
from laika_pipeline.validation.asset_validator import AssetValidator
from laika_pipeline.validation.asset_version_validator import (
    AssetVersionValidator)
from laika_pipeline.db.storage_backend import StorageBackend


class Project():
    """
    A class representing a project in the pipeline.
    """
    def __init__(
            self,
            name: str,
            storage_backend: StorageBackend = None
            ):
        self._name = name
        self._assets = []
        self._asset_versions = []
        self.validation_errors = []
        self.storage_backend = storage_backend

    @property
    def name(self):
        return self._name

    @property
    def assets(self):
        return self._assets

    @property
    def asset_versions(self):
        return self._asset_versions

    def load_assets(
            self,
            file_path: str
    ) -> None:
        """
        Load Assets and Asset Versions from a given json file.

        Args:
            file_path (str): the path to the json file containing the asset and
                             asset version data
        """
        data = load_json(file_path)
        for entry in data:
            asset_entry = entry['asset']
            asset = Asset(
                        name=asset_entry['name'],
                        asset_type=asset_entry['type']
                    )

            asset_version = AssetVersion(
                        asset=asset.code,
                        department=entry['department'],
                        version=entry['version'],
                        status=entry['status']
                    )
            validation_result = self.add_asset_version(asset_version)
            if not validation_result.success:
                self.validation_errors.append(validation_result.error_message)
            validation_result = self.add_asset(asset)
            if not validation_result.success:
                self.validation_errors.append(validation_result.error_message)

    def add_asset(
        self,
        asset: Asset
    ) -> OperationResult:
        """
        Add an asset to the project context. This method validates the asset
        and checks for duplicates before adding it to the project.

        Args:
            asset (Asset): Asset object to be added in the project context

        Raises:
            TypeError: if the provided asset is not an instance of Asset

        Returns:
            OperationResult: The result of the operation, indicating success or
                             failure.
        """
        if not isinstance(asset, Asset):
            raise TypeError("Asset must be an instance of Asset.")
        valid_asset = asset.validate()
        if valid_asset.success is False:
            return valid_asset

        validator = AssetValidator()
        result = validator.validate_asset_has_version(asset, self)
        if result.success is False:
            return result
        result = validator.validate_asset_is_unique(asset, self)
        if result.success is False:
            return result

        self.assets.append(asset)
        return OperationResult(
            success=True,
            data={"asset_code": asset.code}
        )

    def add_asset_version(
            self,
            asset_version: AssetVersion
    ) -> OperationResult:
        """ Add an asset version to the project context. This method validates
        the asset version and checks for duplicates before adding it to the
        project.

        Args:
            asset_version (AssetVersion): The Asset Version to be added in the
                                          project context

        Raises:
            TypeError: if the provided asset version is not an instance of
                       AssetVersion

        Returns:
            OperationResult: The result of the operation, indicating success or
                             failure.
        """
        if not isinstance(asset_version, AssetVersion):
            raise TypeError(
                "Asset version must be an instance of AssetVersion.")
        valid_asset_version = asset_version.validate()
        if valid_asset_version.success is False:
            return valid_asset_version

        validator = AssetVersionValidator()
        result = validator.validate_linear_versioning(asset_version, self)
        if result.success is False:
            return result
        result = validator.validate_version_is_unique(asset_version, self)
        if result.success is False:
            return result

        self.asset_versions.append(asset_version)
        return OperationResult(
            success=True,
            data={
                "asset_code": asset_version.asset,
                "version": asset_version.version
            }
        )

    def list_assets(self) -> list[Asset]:
        """ List all the assets in the project

        Returns:
            list[Asset]: list of assets
        """
        return self.assets

    def list_asset_versions(self) -> list[AssetVersion]:
        """ List all the asset versions in the project

        Returns:
            list[AssetVersion]: list all asset versions
        """
        return self.asset_versions

    def get_asset(self, asset_name: str, asset_type: str) -> Asset | None:
        """
        Retrieve an asset from the project, if not found a validation error
        is logged and None is returned.

        Args:
            asset_name (str): name of the asset
            asset_type (str): type of the asset

        Returns:
            Asset | None: The retrieved asset or None if not found
        """
        for asset in self.assets:
            if (asset.name == asset_name
               and asset.asset_type.value == asset_type):
                return asset
        validation_result = OperationResult(
            success=False,
            error_message=(
                f"Asset '{asset_name}' of type '{asset_type}' not found in "
                f"project."
            )
        )
        self.validation_errors.append(validation_result.error_message)
        return None

    def get_asset_version(
            self,
            asset_name: str,
            asset_type: str,
            version_num: int
    ) -> AssetVersion | None:
        """
        Retrieve an asset version from the project, if not found a validation
        error is logged and None is returned.

        Args:
            asset_name (str): name of the asset
            asset_type (str): type of the asset
            version_num (int): version number of the asset version
        """
        asset = self.get_asset(asset_name, asset_type)
        if not asset:
            return None
        for asset_version in self.asset_versions:
            if (asset_version.asset == asset.code
               and asset_version.version == version_num):
                return asset_version
        validation_result = OperationResult(
            success=False,
            error_message=(
                f"Asset version '{version_num}' for asset '{asset_name}' of "
                f"type '{asset_type}' not found in project."
            )
        )
        self.validation_errors.append(validation_result.error_message)
        return None

    # --------------------------------------------------------------------------
    # Backend storage methods
    # --------------------------------------------------------------------------

    def save(self):
        """ Save the project data to the storage backend if it exists,
            otherwise do nothing.
        """
        if self.storage_backend:
            self.storage_backend.save_assets(self.assets)
            self.storage_backend.save_asset_versions(self.asset_versions)

    def load(self):
        """ Load the project data from the storage backend if it exists,
            otherwise do nothing.
        """
        if self.storage_backend:
            self._assets = self.storage_backend.load_assets()
            self._asset_versions = self.storage_backend.load_asset_versions()
