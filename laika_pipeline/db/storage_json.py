from pathlib import Path
import os
import json

from laika_pipeline.db.storage_backend import StorageBackend


from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion


class StorageJSON(StorageBackend):
    """
    A class representing a JSON storage backend for the Project.
    This class implements the StorageBackend interface to save and retrieve
    assets and asset versions from a JSON file.
    """
    def __init__(self, file_path: str):
        """
        Initialize a storage JSON handler

        Args:
            file_path (str): the root filepath in which we will save
                             and retrieve the JSON files.
        """
        self.file_path = file_path
        self.asset_path = os.path.join(self.file_path, 'assets')
        self.asset_version_path = os.path.join(self.file_path, 'asset_versions')
        # Ensure the directory structure exists
        if not Path(self.file_path).exists():
            os.makedirs(self.file_path, exist_ok=True)
        if not Path(self.asset_path).exists():
            os.makedirs(self.asset_path, exist_ok=True)
        if not Path(self.asset_version_path).exists():
            os.makedirs(self.asset_version_path, exist_ok=True)

    def save_asset(self, asset: Asset):
        data = asset.to_dict()
        publish_path = os.path.join(self.asset_path, asset.code + '.json')
        with open(publish_path, 'w') as fp:
            json.dump(data, fp, indent=4)

    def load_asset(self, asset_code: str):
        file_path = os.path.join(self.asset_path, asset_code + '.json')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Asset file not found: {file_path}")
        with open(file_path, 'r') as fp:
            data = json.load(fp)
            return Asset.from_dict(data)

    def save_assets(self, assets: list[Asset]):
        for asset in assets:
            self.save_asset(asset)

    def load_assets(self):
        assets = []
        for file_name in os.listdir(self.asset_path):
            if file_name.endswith('.json'):
                with open(os.path.join(self.asset_path, file_name), 'r') as fp:
                    data = json.load(fp)
                    asset = Asset.from_dict(data)
                    assets.append(asset)
        return assets

    def save_asset_version(self, asset_version: AssetVersion):
        data = asset_version.to_dict()
        department_path = os.path.join(self.asset_version_path,
                                       asset_version.department)
        if not Path(department_path).exists():
            os.makedirs(department_path, exist_ok=True)
        publish_path = os.path.join(
                        department_path,    
                        f"{asset_version.asset}.{asset_version.version}.json"
                    )

        with open(publish_path, 'w') as fp:
            json.dump(data, fp, indent=4)

    def load_asset_version(self,
                           asset_code: str,
                           department: str,
                           version: int):
        file_path = os.path.join(
            self.asset_version_path,
            department,
            f"{asset_code}.{version}.json"
        )
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Asset Version file not found: {file_path}")
        with open(file_path, 'r') as fp:
            data = json.load(fp)
            return AssetVersion.from_dict(data)

    def save_asset_versions(self, asset_versions: list[AssetVersion]):
        for asset_version in asset_versions:
            self.save_asset_version(asset_version)

    def load_asset_versions(self):
        asset_versions = []
        for root, dirs, files in os.walk(self.asset_version_path):
            for file_name in files:
                if file_name.endswith('.json'):
                    with open(os.path.join(root, file_name), 'r') as fp:
                        data = json.load(fp)
                        asset_version = AssetVersion.from_dict(data)
                        asset_versions.append(asset_version)
        return asset_versions
