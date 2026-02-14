from laika_pipeline.validation.operation_result import OperationResult
from laika_pipeline.pipeline.asset_version import AssetVersion

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Avoid circular imports for type hints
    from laika_pipeline.pipeline.project import Project


class AssetVersionValidator:
    """
    Validator for contextual rules related to AssetVersion objects.
    Ensures that versions for a given asset increase linearly (1, 2, 3, ...).
    """

    def validate_linear_versioning(
            self,
            asset_version: AssetVersion,
            project: 'Project'
    ) -> OperationResult:
        """
        Ensure that the version numbers for the given asset increase linearly.

        Rules:
        - Version numbers must start at 1.
        - No gaps are allowed (e.g., cannot add v3 if v2 is missing).

        Args:
            asset_version (AssetVersion): The version being added.
            project (Project): The project containing existing versions.

        Returns:
            OperationResult: success=True if valid, otherwise False with
                             message.
        """

        # Collect all existing versions for this asset
        existing_versions = sorted(
            av.version for av in project.asset_versions
            if av.asset == asset_version.asset
        )

        # If no versions exist yet, the first version must be 1
        if not existing_versions:
            if asset_version.version != 1:
                return OperationResult(
                    success=False,
                    error_message=(
                        f"Asset '{asset_version.asset}' has no versions yet. "
                        f"The first version must be 1, not "
                        f"{asset_version.version}."
                    )
                )
            return OperationResult(success=True)

        # Determine the expected next version
        expected_next = existing_versions[-1] + 1

        if asset_version.version != expected_next:
            return OperationResult(
                success=False,
                error_message=(
                    f"Invalid version sequence for asset "
                    f"'{asset_version.asset}'. "
                    f"Expected version {expected_next}, got "
                    f"{asset_version.version}."
                )
            )

        return OperationResult(success=True)

    def validate_version_is_unique(
            self,
            asset_version: AssetVersion,
            project: 'Project'
    ) -> OperationResult:
        if asset_version in project.asset_versions:
            return OperationResult(
                success=False,
                error_message=(
                    f"Asset version for asset '{asset_version.asset}' "
                    f"version '{asset_version.version}' already exists in the "
                    f"project."
                )
            )

        return OperationResult(success=True)
