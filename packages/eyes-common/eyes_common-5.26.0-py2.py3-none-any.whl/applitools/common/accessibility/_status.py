# GENERATED FILE #
from enum import Enum

from applitools.common.utils.general_utils import DeprecatedEnumVariant


class AccessibilityStatus(Enum):
    """
    Accessibility status.
    """

    # Session has passed accessibility validation.
    Passed = "Passed"
    # Session hasn't passed accessibility validation.
    Failed = "Failed"
