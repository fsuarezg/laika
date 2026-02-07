from pprint import pprint

from laika_pipeline.pipeline.asset import Asset
from laika_pipeline.pipeline.asset_version import AssetVersion
from laika_pipeline.pipeline.project import Project


def main(filepath: str = 'sample_data/asset_data.json'):
    project = Project(name="Sample Project")
    project.load_assets(filepath)

    pprint(project.assets)
    pprint(project.asset_versions)
    pprint(project.validation_errors)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
