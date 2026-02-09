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

    This function reads asset metadata and version information from a JSON
    file, validates each entry, and stores valid assets. Invalid entries are
    skipped and logged in the validation errors.

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


def add_asset(asset: Asset) -> dict:
    """
    Add a single asset to the project.

    Args:
        asset (Asset): The asset to add.

    Returns:
        dict: Operation result with:
            - 'success': Whether the operation succeeded
            - 'asset_code': The generated code for the asset (if successful)
            - 'error': Error message (if failed)

    Example:
        >>> from laika_pipeline.pipeline.asset import Asset
        >>> from laika_pipeline.api import add_asset
        >>> asset = Asset("hero", "character")
        >>> result = add_asset(asset)
        >>> if result['success']:
        ...     print(f"Asset code: {result['asset_code']}")
    """
    _ensure_initialized()
    result = _project.add_asset(asset)

    return {
        'success': result.success,
        'asset_code': result.data.get('asset_code') if result.data else None,
        'error': result.error_message
    }


def add_asset_version(asset_version: AssetVersion) -> dict:
    """
    Add a single asset version to the project.

    Args:
        asset_version (AssetVersion): The asset version to add.

    Returns:
        dict: Operation result with:
            - 'success': Whether the operation succeeded
            - 'asset_code': The asset code (if successful)
            - 'version': The version number (if successful)
            - 'error': Error message (if failed)

    Example:
        >>> from laika_pipeline.pipeline.asset_version import AssetVersion
        >>> from laika_pipeline.api import add_asset_version
        >>> version = AssetVersion("hero_character", "modeling", 1, "active")
        >>> result = add_asset_version(version)
    """
    _ensure_initialized()
    result = _project.add_asset_version(asset_version)

    return {
        'success': result.success,
        'asset_code': result.data.get('asset_code') if result.data else None,
        'version': result.data.get('version') if result.data else None,
        'error': result.error_message
    }


def list_assets() -> list[Asset]:
    """
    List all assets in the project.

    Returns:
        list[Asset]: List of all loaded assets.

    Example:
        >>> from laika_pipeline.api import list_assets
        >>> assets = list_assets()
        >>> for asset in assets:
        ...     print(f"{asset.name}: {asset.asset_type.value}")
    """
    _ensure_initialized()
    return _project.list_assets()


def list_asset_versions(
        asset_name: str,
        asset_type: str
) -> list[AssetVersion]:
    """
    List all versions of a specific asset.

    Args:
        asset_name (str): Name of the asset.
        asset_type (str): Type of the asset.

    Returns:
        list[AssetVersion]: List of all versions for the asset, or empty list
            if asset not found.

    Example:
        >>> from laika_pipeline.api import list_asset_versions
        >>> versions = list_asset_versions("hero", "character")
        >>> for version in versions:
        ...     print(f"v{version.version}: {version.status.value}")
    """
    _ensure_initialized()
    asset = _project.get_asset(asset_name, asset_type)
    if not asset:
        return []

    return [
        av for av in _project.asset_versions
        if av.asset == asset.code
    ]


def get_asset(
    asset_name: str,
    asset_type: str
) -> Asset | None:
    """
    Retrieve a specific asset by name and type.

    Args:
        asset_name (str): Name of the asset.
        asset_type (str): Type of the asset.

    Returns:
        Asset | None: The asset if found, None otherwise.

    Example:
        >>> from laika_pipeline.api import get_asset
        >>> asset = get_asset("hero", "character")
        >>> if asset:
        ...     print(f"Found: {asset.name}")
    """
    _ensure_initialized()
    return _project.get_asset(asset_name, asset_type)


def get_asset_version(
    asset_name: str,
    asset_type: str,
    version_num: int
) -> AssetVersion | None:
    """
    Retrieve a specific asset version.

    Args:
        asset_name (str): Name of the asset.
        asset_type (str): Type of the asset.
        version_num (int): Version number to retrieve.

    Returns:
        AssetVersion | None: The asset version if found, None otherwise.

    Example:
        >>> from laika_pipeline.api import get_asset_version
        >>> version = get_asset_version("hero", "character", 2)
        >>> if version:
        ...     print(f"Status: {version.status.value}")
    """
    _ensure_initialized()
    return _project.get_asset_version(asset_name, asset_type, version_num)


def save() -> dict:
    """
    Save the project to the configured storage backend.

    Returns:
        dict: Operation result with:
            - 'success': Whether the save succeeded
            - 'error': Error message (if failed)

    Example:
        >>> from laika_pipeline.api import save
        >>> result = save()
        >>> if result['success']:
        ...     print("Project saved!")
    """
    _ensure_initialized()
    try:
        _project.save()
        return {'success': True, 'error': None}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def load() -> dict:
    """
    Load the project from the configured storage backend.

    Returns:
        dict: Operation result with:
            - 'success': Whether the load succeeded
            - 'error': Error message (if failed)

    Example:
        >>> from laika_pipeline.api import load
        >>> result = load()
        >>> if result['success']:
        ...     assets = list_assets()
    """
    _ensure_initialized()
    try:
        _project.load()
        return {'success': True, 'error': None}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_validation_errors() -> list[str]:
    """
    Get all validation errors from the current session.

    Returns:
        list[str]: List of validation error messages.

    Example:
        >>> from laika_pipeline.api import get_validation_errors
        >>> errors = get_validation_errors()
        >>> for error in errors:
        ...     print(f"Error: {error}")
    """
    _ensure_initialized()
    return _project.validation_errors


def clear() -> None:
    """
    Clear the current project and reset to uninitialized state.

    Example:
        >>> from laika_pipeline.api import clear
        >>> clear()
        >>> initialize("New Project")
    """
    global _project
    _project = None


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
