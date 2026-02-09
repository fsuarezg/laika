"""
LAIKA Asset Pipeline

A Python library for validating and managing versioned assets in a pipeline.
"""

# Import core API functions for easy access
from laika_pipeline.api import (
    initialize,
    load_assets,
    add_asset,
    add_asset_version,
    list_assets,
    list_asset_versions,
    get_asset,
    get_asset_version,
    save,
    load,
    get_validation_errors,
    clear,
    get_project,
)

# Import core models for users who want to work directly
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion
from laika_pipeline.pipeline.asset_type import AssetType
from laika_pipeline.pipeline.status import Status
from laika_pipeline.pipeline.project import Project

__version__ = "0.1.0"

__all__ = [
    # API functions
    "initialize",
    "load_assets",
    "add_asset",
    "add_asset_version",
    "list_assets",
    "list_asset_versions",
    "get_asset",
    "get_asset_version",
    "save",
    "load",
    "get_validation_errors",
    "clear",
    "get_project",
    # Models
    "Asset",
    "AssetVersion",
    "AssetType",
    "Status",
    "Project"
]
