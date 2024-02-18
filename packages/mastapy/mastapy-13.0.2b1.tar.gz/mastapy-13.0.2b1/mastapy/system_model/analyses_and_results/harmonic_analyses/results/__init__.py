"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5846 import ConnectedComponentType
    from ._5847 import ExcitationSourceSelection
    from ._5848 import ExcitationSourceSelectionBase
    from ._5849 import ExcitationSourceSelectionGroup
    from ._5850 import HarmonicSelection
    from ._5851 import ModalContributionDisplayMethod
    from ._5852 import ModalContributionFilteringMethod
    from ._5853 import ResultLocationSelectionGroup
    from ._5854 import ResultLocationSelectionGroups
    from ._5855 import ResultNodeSelection
else:
    import_structure = {
        "_5846": ["ConnectedComponentType"],
        "_5847": ["ExcitationSourceSelection"],
        "_5848": ["ExcitationSourceSelectionBase"],
        "_5849": ["ExcitationSourceSelectionGroup"],
        "_5850": ["HarmonicSelection"],
        "_5851": ["ModalContributionDisplayMethod"],
        "_5852": ["ModalContributionFilteringMethod"],
        "_5853": ["ResultLocationSelectionGroup"],
        "_5854": ["ResultLocationSelectionGroups"],
        "_5855": ["ResultNodeSelection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ConnectedComponentType",
    "ExcitationSourceSelection",
    "ExcitationSourceSelectionBase",
    "ExcitationSourceSelectionGroup",
    "HarmonicSelection",
    "ModalContributionDisplayMethod",
    "ModalContributionFilteringMethod",
    "ResultLocationSelectionGroup",
    "ResultLocationSelectionGroups",
    "ResultNodeSelection",
)
