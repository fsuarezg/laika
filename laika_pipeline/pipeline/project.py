from laika_pipeline.lib.load_json import load_json

from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion
from laika_pipeline.validation.operation_result import OperationResult


class Project():
    """
    A class representing a project in the pipeline.
    """
    def __init__(self, name: str):
        self._name = name
        self._assets = []
        self._asset_versions = []
        self.validation_errors = []

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
        data = load_json(file_path)
        for entry in data:
            asset_entry = entry['asset']
            # TODO handle type not being in the enum
            asset = Asset(
                        name=asset_entry['name'],
                        asset_type=asset_entry['type']
                    )
            validation_result = self.add_asset(asset)
            if not validation_result.success:
                self.validation_errors.append(validation_result.error_message)
            # TODO handle status not being in the enum
            asset_version = AssetVersion(
                        asset=asset.code,
                        department=entry['department'],
                        version=entry['version'],
                        status=entry['status']
                    )
            validation_result = self.add_asset_version(asset_version)
            if not validation_result.success:
                self.validation_errors.append(validation_result.error_message)

    def add_asset(
        self,
        asset: Asset
    ) -> OperationResult:
        if not isinstance(asset, Asset):
            raise TypeError("Asset must be an instance of Asset.")
        valid_asset = asset.validate()
        if valid_asset.success is False:
            return valid_asset
        if asset in self.assets:
            return OperationResult(
                success=False,
                error_message=(
                    f"Asset '{asset.name}' of type '{asset.asset_type}' "
                    f"already exists"
                )
            )

        self.assets.append(asset)
        return OperationResult(
            success=True,
            data={"asset_code": asset.code}
        )

    def add_asset_version(
            self,
            asset_version: AssetVersion
    ) -> OperationResult:
        if not isinstance(asset_version, AssetVersion):
            raise TypeError(
                "Asset version must be an instance of AssetVersion.")
        valid_asset_version = asset_version.validate()
        if valid_asset_version.success is False:
            return valid_asset_version
        if asset_version in self.asset_versions:
            return OperationResult(
                success=False,
                error_message=(
                    f"Asset version for asset '{asset_version.asset}' "
                    f"version '{asset_version.version}' already exists in the "
                    f"project."
                )
            )

        self.asset_versions.append(asset_version)
        return OperationResult(
            success=True,
            data={
                "asset_code": asset_version.asset,
                "version": asset_version.version
            }
        )

    # # list all assets
    def list_assets(self) -> list[Asset]:
        return self.assets

    # # list versions of an asset
    def list_asset_versions(self) -> list[AssetVersion]:
        return self.asset_versions

    # # retrieve asset by name
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

    # # retrieve asset version by version number
    # get_asset_version(asset_name, type, version_num)