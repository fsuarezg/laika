from laika_pipeline.pipeline.status import Status


class AssetVersion():
    """
    A class representing an asset version in the pipeline
    """

    def __init__(self, asset: str,
                 department: str,
                 version: int,
                 status: str | Status = Status.ACTIVE):
        self._asset = asset
        self._department = department
        self._version = version
        if isinstance(status, str):
            status = Status.from_string(status)
        self._status = status

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Asset must be a string.")
        self._asset = value

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Department must be a string.")
        self._department = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Version must be an integer.")
        if not value > 0:
            raise ValueError("Version must be a positive integer.")
        self._version = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str | Status):
        if isinstance(value, str):
            value = Status.from_string(value)
        if not isinstance(value, Status):
            raise TypeError("Status must be a valid Status.")
        self._status = value
