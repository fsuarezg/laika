import unittest

from laika_pipeline import api
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion


class TestListAssetVersions(unittest.TestCase):
    """Tests for the list_asset_versions() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()
        self.asset = Asset("hero", "character")

    def tearDown(self):
        """Clean up after each test."""
        api.clear()

    def test_list_asset_versions_empty(self):
        """Test listing versions when asset has none."""
        versions = api.list_asset_versions("hero", "character")

        self.assertIsInstance(versions, list)
        self.assertEqual(len(versions), 0)

    def test_list_asset_versions_returns_asset_version_objects(self):
        """Test that list_asset_versions returns AssetVersion objects."""
        v1 = AssetVersion(self.asset.code, "modeling", 1, "active")
        v2 = AssetVersion(self.asset.code, "texturing", 1, "active")

        api.add_asset_version(v1)
        api.add_asset_version(v2)

        api.add_asset(self.asset)

        versions = api.list_asset_versions("hero", "character")

        self.assertEqual(len(versions), 2)
        self.assertIsInstance(versions[0], AssetVersion)
        self.assertIsInstance(versions[1], AssetVersion)

    def test_list_asset_versions_nonexistent_asset(self):
        """Test listing versions for nonexistent asset."""
        versions = api.list_asset_versions("nonexistent", "character")

        self.assertIsInstance(versions, list)
        self.assertEqual(len(versions), 0)

    def test_list_asset_versions_different_types(self):
        """Test listing versions with different departments."""
        v1 = AssetVersion(self.asset.code, "modeling", 1, "active")
        v2 = AssetVersion(self.asset.code, "texturing", 1, "inactive")
        v3 = AssetVersion(self.asset.code, "rigging", 1, "active")

        api.add_asset_version(v1)
        api.add_asset_version(v2)
        api.add_asset_version(v3)

        api.add_asset(self.asset)

        versions = api.list_asset_versions("hero", "character")

        self.assertEqual(len(versions), 3)
        departments = [v.department for v in versions]
        self.assertIn("modeling", departments)
        self.assertIn("texturing", departments)
        self.assertIn("rigging", departments)
