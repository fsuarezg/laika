from laika_pipeline.lib.load_json import load_json

from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion


class Project():
    """
    A class representing a project in the pipeline.
    """
    def __init__(self, name: str):
        self._name = name
        self._assets = []
        self._asset_versions = []

    @property
    def name(self):
        return self._name

    @property
    def assets(self):
        return self._assets

    @property
    def asset_versions(self):
        return self._asset_versions

    def load_assets(self, file_path: str):
        data = load_json(file_path)
        for entry in data:
            asset_entry = entry['asset']
            asset = Asset(
                        name=asset_entry['name'],
                        asset_type=asset_entry['type']
                    )
            self.add_asset(asset)
            asset_version = AssetVersion(
                        asset=asset.code,
                        department=entry['department'],
                        version=entry['version'],
                        status=entry['status']
                    )
            self.add_asset_version(asset_version)

    def add_asset(self, asset: Asset):
        if not isinstance(asset, Asset):
            raise TypeError("Asset must be an instance of Asset.")
        if asset in self.assets:
            raise ValueError(f"Asset with code '{asset.code}' already exists in the project.")
        self.assets.append(asset)

    def add_asset_version(self, asset_version: AssetVersion):
        if not isinstance(asset_version, AssetVersion):
            raise TypeError("Asset version must be an instance of AssetVersion.")
        if asset_version in self.asset_versions:
            raise ValueError(
                f"Asset version for asset '{asset_version.asset}' "
                f"version '{asset_version.version}' already exists in the "
                f"project."
            )
        self.asset_versions.append(asset_version)

    # # list all assets
    # list_assets()

    # # list versions of an asset
    # list_asset_versions(asset_name, type)

    # # retrieve asset by name
    # get_asset(asset_name, type)

    # # retrieve asset version by version number
    # get_asset_version(asset_name, type, version_num)