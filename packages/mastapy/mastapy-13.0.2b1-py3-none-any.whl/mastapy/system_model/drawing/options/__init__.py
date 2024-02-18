"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2263 import AdvancedTimeSteppingAnalysisForModulationModeViewOptions
    from ._2264 import ExcitationAnalysisViewOption
    from ._2265 import ModalContributionViewOptions
else:
    import_structure = {
        "_2263": ["AdvancedTimeSteppingAnalysisForModulationModeViewOptions"],
        "_2264": ["ExcitationAnalysisViewOption"],
        "_2265": ["ModalContributionViewOptions"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AdvancedTimeSteppingAnalysisForModulationModeViewOptions",
    "ExcitationAnalysisViewOption",
    "ModalContributionViewOptions",
)
