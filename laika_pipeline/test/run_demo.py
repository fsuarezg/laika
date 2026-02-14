from pprint import pprint

from laika_pipeline.pipeline.project import Project
from laika_pipeline.db.storage_json import StorageJSON

SAMPLE_DATA_FILEPATH = 'sample_data/asset_data_02.json'
TEST_PROJECT_FILEPATH = 'sample_data/test_project'


def main(filepath: str = SAMPLE_DATA_FILEPATH):
    storage_backend = StorageJSON(file_path=TEST_PROJECT_FILEPATH)
    project = Project(name="Default Project", storage_backend=storage_backend)
    project.load_assets(filepath)

    print("=" * 70)
    print("ASSETS")
    print("=" * 70)
    pprint(project.assets)
    print("=" * 70)
    print("ASSET VERSIONS")
    print("=" * 70)
    pprint(project.asset_versions)
    print("=" * 70)
    print("VALIDATION ERRORS")
    print("=" * 70)
    pprint(project.validation_errors)

    project.save()
    project.load()

    print("=" * 70)
    print("ASSETS ATER LOAD")
    print("=" * 70)
    pprint(project.assets)
    print("=" * 70)
    print("ASSET VERSIONS ATER LOAD")
    print("=" * 70)
    pprint(project.asset_versions)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
