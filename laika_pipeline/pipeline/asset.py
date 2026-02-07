from laika_pipeline.pipeline.asset_type import AssetType


class Asset():
    """
    A class representing an asset in the pipeline.
    """

    def __init__(self, name: str,
                 asset_type: str | AssetType):
        self._name = name
        if isinstance(asset_type, str):
            asset_type = AssetType.from_string(asset_type)
        self._asset_type = asset_type
        # Generate a unique code for the asset based on its name and type
        self._code = self.generate_code(name, asset_type)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Asset name must be a string.")
        self._name = value

    @property
    def asset_type(self):
        return self._asset_type

    @asset_type.setter
    def asset_type(self, value):
        if not isinstance(value, AssetType):
            raise TypeError("Asset type must be a valid AssetType.")
        self._asset_type = value

    @property
    def code(self):
        return self._code

    def generate_code(self, name, asset_type):
        return f"{name.lower().replace(' ', '_')}_{asset_type.value}"