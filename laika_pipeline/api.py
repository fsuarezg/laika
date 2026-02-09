"""
Public Python API

This module provides module-level functions for interacting with assets,
asset versions, and the validation/storage system. It abstracts away the
complexity of Project management and provides a clean interface. I still
allow to access the underlying Project instance for advanced use cases.
"""

from typing import Optional
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion
from laika_pipeline.pipeline.project import Project
from laika_pipeline.db.storage_backend import StorageBackend


# Global project instance
_project: Project = None


def initialize(
    name: str = "Default Project",
    storage_backend: Optional[StorageBackend] = None
) -> None:
    """
    Initialize the API with a project instance and optional storage backend.

    Args:
        name (str): Name of the project. Defaults to "Default Project".
        storage_backend (StorageBackend, optional): Storage backend to use.
            If None, assets are stored in memory only.

    Example:
        >>> from laika_pipeline.db.storage_json import StorageJSON
        >>> from laika_pipeline.api import initialize
        >>> storage = StorageJSON('path/to/storage')
        >>> initialize("MyProject", storage)
    """
    global _project
    _project = Project(name=name, storage_backend=storage_backend)


def _ensure_initialized() -> None:
    """Ensure the API is initialized, raise error if not."""
    global _project
    if _project is None:
        initialize()


def load_assets(
        file_path: str
) -> dict:
    """
    Load assets and versions from a JSON file.

    This function reads asset metadata and version information from a JSON file,
    validates each entry, and stores valid assets. Invalid entries are skipped
    and logged in the validation errors.

    Args:
        file_path (str): Path to the JSON file containing assets.

    Returns:
        dict: Report containing:
            - 'total': Total entries processed
            - 'valid': Number of valid entries
            - 'errors': List of error messages

    Example:
        >>> from laika_pipeline.api import load_assets
        >>> report = load_assets('sample_data/assets.json')
        >>> print(f"Loaded {report['valid']} valid assets")
    """
    _ensure_initialized()
    _project.load_assets(file_path)

    # Return a report-style dict
    return {
        'total': len(_project.assets) + len(_project.validation_errors),
        'valid': len(_project.assets),
        'errors': _project.validation_errors
    }


def add_asset(
    asset: Asset
) -> dict:
    # TODO
    pass


def add_asset_version(
    asset_version: AssetVersion
) -> dict:
    # TODO
    pass


def list_assets() -> list:
    # TODO
    pass


def list_asset_versions(
        asset_name: str,
        asset_type: str
) -> list[AssetVersion]:
    # TODO
    pass


def get_asset(
        asset_name: str,
        asset_type: str
) -> Asset | None:
    # TODO
    pass


def get_asset_version(
    asset_name: str,
    asset_type: str,
    version_num: int
) -> AssetVersion | None:
    # TODO
    pass


def save():
    # TODO
    pass


def load():
    # TODO
    pass


def get_project() -> Project:
    """
    Get the underlying Project instance (for advanced usage).

    Returns:
        Project: The current project instance.

    Note:
        This is exposed for advanced use cases. Prefer using the module-level
        functions above for standard operations.
    """
    _ensure_initialized()
    return _project
