from pprint import pprint

from laika_pipeline.pipeline.project import Project
from laika_pipeline.db.storage_json import StorageJSON

SAMPLE_DATA_FILEPATH = 'sample_data/asset_data.json'
TEST_PROJECT_FILEPATH = 'sample_data/test_project'


def main(filepath: str = SAMPLE_DATA_FILEPATH):
    storage_backend = StorageJSON(file_path=TEST_PROJECT_FILEPATH)
    project = Project(name="Sample Project", storage_backend=storage_backend)
    project.load_assets(filepath)

    pprint(project.assets)
    pprint(project.asset_versions)
    pprint(project.validation_errors)

    project.save()
    project.load()

    pprint(project.assets)
    pprint(project.asset_versions)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
