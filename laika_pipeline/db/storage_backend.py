from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Avoid circular imports for type hints
    from laika_pipeline.pipeline.asset import Asset
    from laika_pipeline.pipeline.asset_version import AssetVersion


class StorageBackend(ABC):
    """
    Abstract class representing a storage backend for the Project.
    This class defines the interface for saving and retrieving assets and
    asset versions.
    """
    @abstractmethod
    def save_asset(self, asset: 'Asset'):
        # Implement logic to save an asset to the storage backend
        pass

    @abstractmethod
    def load_asset(self):
        # Implement logic to retrieve asset from the storage backend
        pass

    @abstractmethod
    def save_assets(self, assets: list['Asset']):
        # Implement logic to save assets to the storage backend
        pass

    @abstractmethod
    def load_assets(self):
        # Implement logic to retrieve assets from the storage backend
        pass

    @abstractmethod
    def save_asset_version(self, asset_version: 'AssetVersion'):
        # Implement logic to save an asset version to the storage backend
        pass

    @abstractmethod
    def load_asset_version(self):
        # Implement logic to retrieve an asset version from the storage backend
        pass

    @abstractmethod
    def save_asset_versions(self, asset_versions: list['AssetVersion']):
        # Implement logic to save asset versions to the storage backend
        pass

    @abstractmethod
    def load_asset_versions(self):
        # Implement logic to retrieve asset versions from the storage backend
        pass
