"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._6270 import CombinationAnalysis
    from ._6271 import FlexiblePinAnalysis
    from ._6272 import FlexiblePinAnalysisConceptLevel
    from ._6273 import FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass
    from ._6274 import FlexiblePinAnalysisGearAndBearingRating
    from ._6275 import FlexiblePinAnalysisManufactureLevel
    from ._6276 import FlexiblePinAnalysisOptions
    from ._6277 import FlexiblePinAnalysisStopStartAnalysis
    from ._6278 import WindTurbineCertificationReport
else:
    import_structure = {
        "_6270": ["CombinationAnalysis"],
        "_6271": ["FlexiblePinAnalysis"],
        "_6272": ["FlexiblePinAnalysisConceptLevel"],
        "_6273": ["FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass"],
        "_6274": ["FlexiblePinAnalysisGearAndBearingRating"],
        "_6275": ["FlexiblePinAnalysisManufactureLevel"],
        "_6276": ["FlexiblePinAnalysisOptions"],
        "_6277": ["FlexiblePinAnalysisStopStartAnalysis"],
        "_6278": ["WindTurbineCertificationReport"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "CombinationAnalysis",
    "FlexiblePinAnalysis",
    "FlexiblePinAnalysisConceptLevel",
    "FlexiblePinAnalysisDetailLevelAndPinFatigueOneToothPass",
    "FlexiblePinAnalysisGearAndBearingRating",
    "FlexiblePinAnalysisManufactureLevel",
    "FlexiblePinAnalysisOptions",
    "FlexiblePinAnalysisStopStartAnalysis",
    "WindTurbineCertificationReport",
)
