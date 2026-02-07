from dataclasses import dataclass
from typing import Optional


@dataclass
class OperationResult:
    """
    A class to represent an operation result from a function.
    To avoid raising errors and stop code execution, use a validation-as-data
    pattern: we return OperationResult which can be discarded or logged.
    """
    success: bool
    error_message: Optional[str] = None
    data: Optional[dict] = None
