"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._7537 import AnalysisCase
    from ._7538 import AbstractAnalysisOptions
    from ._7539 import CompoundAnalysisCase
    from ._7540 import ConnectionAnalysisCase
    from ._7541 import ConnectionCompoundAnalysis
    from ._7542 import ConnectionFEAnalysis
    from ._7543 import ConnectionStaticLoadAnalysisCase
    from ._7544 import ConnectionTimeSeriesLoadAnalysisCase
    from ._7545 import DesignEntityCompoundAnalysis
    from ._7546 import FEAnalysis
    from ._7547 import PartAnalysisCase
    from ._7548 import PartCompoundAnalysis
    from ._7549 import PartFEAnalysis
    from ._7550 import PartStaticLoadAnalysisCase
    from ._7551 import PartTimeSeriesLoadAnalysisCase
    from ._7552 import StaticLoadAnalysisCase
    from ._7553 import TimeSeriesLoadAnalysisCase
else:
    import_structure = {
        "_7537": ["AnalysisCase"],
        "_7538": ["AbstractAnalysisOptions"],
        "_7539": ["CompoundAnalysisCase"],
        "_7540": ["ConnectionAnalysisCase"],
        "_7541": ["ConnectionCompoundAnalysis"],
        "_7542": ["ConnectionFEAnalysis"],
        "_7543": ["ConnectionStaticLoadAnalysisCase"],
        "_7544": ["ConnectionTimeSeriesLoadAnalysisCase"],
        "_7545": ["DesignEntityCompoundAnalysis"],
        "_7546": ["FEAnalysis"],
        "_7547": ["PartAnalysisCase"],
        "_7548": ["PartCompoundAnalysis"],
        "_7549": ["PartFEAnalysis"],
        "_7550": ["PartStaticLoadAnalysisCase"],
        "_7551": ["PartTimeSeriesLoadAnalysisCase"],
        "_7552": ["StaticLoadAnalysisCase"],
        "_7553": ["TimeSeriesLoadAnalysisCase"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AnalysisCase",
    "AbstractAnalysisOptions",
    "CompoundAnalysisCase",
    "ConnectionAnalysisCase",
    "ConnectionCompoundAnalysis",
    "ConnectionFEAnalysis",
    "ConnectionStaticLoadAnalysisCase",
    "ConnectionTimeSeriesLoadAnalysisCase",
    "DesignEntityCompoundAnalysis",
    "FEAnalysis",
    "PartAnalysisCase",
    "PartCompoundAnalysis",
    "PartFEAnalysis",
    "PartStaticLoadAnalysisCase",
    "PartTimeSeriesLoadAnalysisCase",
    "StaticLoadAnalysisCase",
    "TimeSeriesLoadAnalysisCase",
)
