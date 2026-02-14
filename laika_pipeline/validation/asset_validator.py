from laika_pipeline.validation.operation_result import OperationResult
from laika_pipeline.pipeline.asset import Asset

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Avoid circular imports for type hints
    from laika_pipeline.pipeline.project import Project


class AssetValidator:
    """
    Validator for contextual asset rules that depend on the Project.
    """

    def validate_asset_has_version(
            self,
            asset: Asset,
            project: 'Project'
    ) -> OperationResult:
        """
        Ensure that the given asset has at least one AssetVersion in the
        project.

        Args:
            asset (Asset): The asset to validate.
            project (Project): The project containing assets and versions.

        Returns:
            OperationResult: success=True if valid, otherwise False with
            message.
        """
        versions = [
            av for av in project.asset_versions
            if av.asset == asset.code
        ]

        if not versions:
            return OperationResult(
                success=False,
                error_message=(
                    f"Asset '{asset.name}' of type '{asset.asset_type.value}' "
                    f"has no versions in the project."
                )
            )

        return OperationResult(success=True)

    def validate_asset_is_unique(
            self,
            asset: Asset,
            project: 'Project'
    ) -> OperationResult:
        """
        Ensure a given asset is not already existing in the project.

        Args:
            asset (Asset): The asset to validate.
            project (Project): The project containing assets.

        Returns:
            OperationResult: success=True if valid, otherwise False with
            message.
        """
        if asset in project.assets:
            return OperationResult(
                success=False,
                error_message=(
                    f"Asset '{asset.name}' of type '{asset.asset_type}' "
                    f"already exists"
                )
            )

        return OperationResult(success=True)
