import unittest

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion
from laika_pipeline.pipeline.status import Status


class TestGetAssetVersion(unittest.TestCase):
    """Tests for the get_asset_version() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()
        self.asset = Asset("hero", "character")

        v1 = AssetVersion(self.asset.code, "modeling", 1, "active")
        v2 = AssetVersion(self.asset.code, "modeling", 2, "active")
        api.add_asset_version(v1)
        api.add_asset_version(v2)
        api.add_asset(self.asset)

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_get_asset_version_success(self):
        """Test retrieving an existing asset version."""
        version = api.get_asset_version("hero", "character", 1)

        self.assertIsNotNone(version)
        self.assertIsInstance(version, AssetVersion)
        self.assertEqual(version.version, 1)

    def test_get_asset_version_nonexistent_version(self):
        """Test retrieving a nonexistent version number."""
        version = api.get_asset_version("hero", "character", 99)

        self.assertIsNone(version)

    def test_get_asset_version_nonexistent_asset(self):
        """Test retrieving version from nonexistent asset."""
        version = api.get_asset_version("nonexistent", "character", 1)

        self.assertIsNone(version)

    def test_get_asset_version_multiple_versions(self):
        """Test retrieving specific versions from multiple."""
        v1 = api.get_asset_version("hero", "character", 1)
        v2 = api.get_asset_version("hero", "character", 2)

        self.assertIsNotNone(v1)
        self.assertIsNotNone(v2)
        self.assertEqual(v1.version, 1)
        self.assertEqual(v2.version, 2)

    def test_get_asset_version_returns_correct_status(self):
        """Test that returned version has correct status."""
        version = api.get_asset_version("hero", "character", 1)

        self.assertEqual(version.status, Status.ACTIVE)
