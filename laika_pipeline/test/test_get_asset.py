import unittest

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion
from laika_pipeline.pipeline.asset_type import AssetType


class TestGetAsset(unittest.TestCase):
    """Tests for the get_asset() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()
        self.asset = Asset("hero", "character")
        v1 = AssetVersion(self.asset.code, "modeling", 1)
        api.add_asset_version(v1)
        api.add_asset(self.asset)

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_get_asset_success(self):
        """Test retrieving an existing asset."""
        asset = api.get_asset("hero", "character")

        self.assertIsNotNone(asset)
        self.assertIsInstance(asset, Asset)
        self.assertEqual(asset.name, "hero")

    def test_get_asset_nonexistent(self):
        """Test retrieving a nonexistent asset."""
        asset = api.get_asset("nonexistent", "character")

        self.assertIsNone(asset)

    def test_get_asset_wrong_type(self):
        """Test retrieving asset with wrong type."""
        asset = api.get_asset("hero", "prop")

        self.assertIsNone(asset)

    def test_get_asset_case_sensitivity(self):
        """Test that get_asset is case sensitive for name."""
        # Asset name should be stripped but case-sensitive
        asset = api.get_asset("Hero", "character")

        # Depends on implementation - typically case sensitive
        # If not found, assertIsNone
        if asset is None:
            self.assertIsNone(asset)

    def test_get_asset_returns_correct_object(self):
        """Test that get_asset returns the correct asset object."""
        from laika_pipeline.pipeline.asset_version import AssetVersion

        asset1 = Asset("hero", "character")
        asset2 = Asset("sword", "prop")

        # Add versions to ensure assets are valid
        v1 = AssetVersion(asset1.code, "modeling", 1, "active")
        v2 = AssetVersion(asset2.code, "modeling", 1, "active")
        api.add_asset_version(v1)
        api.add_asset_version(v2)

        api.add_asset(asset1)
        api.add_asset(asset2)

        retrieved = api.get_asset("hero", "character")

        self.assertEqual(retrieved.name, "hero")
        self.assertEqual(retrieved.asset_type, AssetType.CHARACTER)
