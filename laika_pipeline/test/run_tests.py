from pprint import pprint

from laika_pipeline.lib.load_json import load_json
from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion


def main(filepath: str = 'sample_data/asset_data.json'):
    data = load_json(filepath)

    for entry in data:
        asset_entry = entry['asset']
        asset = Asset(
                    name=asset_entry['name'],
                    asset_type=asset_entry['type']
                )
        asset_version = AssetVersion(
                    asset=asset.code,
                    department=entry['department'],
                    version=entry['version'],
                    status=entry['status']
                )


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
