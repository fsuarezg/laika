import unittest
import json
import tempfile
import os

from laika_pipeline import api


class TestLoadAssets(unittest.TestCase):
    """Tests for the load_assets() function."""

    def setUp(self):
        """Set up test fixtures."""
        api.initialize()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = self.temp_dir.name

    def tearDown(self):
        """Clean up after each test."""
        api.clear()
        self.temp_dir.cleanup()

    def test_load_assets_valid_file(self):
        """Test loading valid assets from JSON file."""
        # Create a temporary JSON file with valid assets
        asset_data = [
            {
                "asset": {"name": "hero", "type": "character"},
                "department": "modeling",
                "version": 1,
                "status": "active"
            },
            {
                "asset": {"name": "sword", "type": "prop"},
                "department": "modeling",
                "version": 1,
                "status": "active"
            }
        ]

        json_file = os.path.join(self.temp_path, "assets.json")
        with open(json_file, 'w') as f:
            json.dump(asset_data, f)

        report = api.load_assets(json_file)

        self.assertIsInstance(report, dict)
        self.assertIn('total', report)
        self.assertIn('valid', report)
        self.assertIn('errors', report)
        self.assertEqual(report['valid'], 2)

    def test_load_assets_empty_file(self):
        """Test loading from an empty JSON file."""
        json_file = os.path.join(self.temp_path, "empty.json")
        with open(json_file, 'w') as f:
            json.dump([], f)

        report = api.load_assets(json_file)

        self.assertEqual(report['valid'], 0)
        self.assertEqual(report['total'], 0)

    def test_load_assets_returns_report_dict(self):
        """Test that load_assets returns proper report structure."""
        json_file = os.path.join(self.temp_path, "test.json")
        with open(json_file, 'w') as f:
            json.dump([], f)

        report = api.load_assets(json_file)

        self.assertIsInstance(report, dict)
        self.assertTrue('total' in report)
        self.assertTrue('valid' in report)
        self.assertTrue('errors' in report)

    def test_load_assets_invalid_json(self):
        """Test loading from an invalid JSON file."""
        json_file = os.path.join(self.temp_path, "invalid.json")
        with open(json_file, 'w') as f:
            f.write("not valid json {")

        with self.assertRaises(Exception):
            api.load_assets(json_file)

    def test_load_assets_nonexistent_file(self):
        """Test loading from a nonexistent file."""
        with self.assertRaises(Exception):
            api.load_assets("/nonexistent/path/to/file.json")
