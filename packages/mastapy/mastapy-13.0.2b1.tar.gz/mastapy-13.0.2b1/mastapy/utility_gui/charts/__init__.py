"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1854 import BubbleChartDefinition
    from ._1855 import ConstantLine
    from ._1856 import CustomLineChart
    from ._1857 import CustomTableAndChart
    from ._1858 import LegacyChartMathChartDefinition
    from ._1859 import MatrixVisualisationDefinition
    from ._1860 import ModeConstantLine
    from ._1861 import NDChartDefinition
    from ._1862 import ParallelCoordinatesChartDefinition
    from ._1863 import PointsForSurface
    from ._1864 import ScatterChartDefinition
    from ._1865 import Series2D
    from ._1866 import SMTAxis
    from ._1867 import ThreeDChartDefinition
    from ._1868 import ThreeDVectorChartDefinition
    from ._1869 import TwoDChartDefinition
else:
    import_structure = {
        "_1854": ["BubbleChartDefinition"],
        "_1855": ["ConstantLine"],
        "_1856": ["CustomLineChart"],
        "_1857": ["CustomTableAndChart"],
        "_1858": ["LegacyChartMathChartDefinition"],
        "_1859": ["MatrixVisualisationDefinition"],
        "_1860": ["ModeConstantLine"],
        "_1861": ["NDChartDefinition"],
        "_1862": ["ParallelCoordinatesChartDefinition"],
        "_1863": ["PointsForSurface"],
        "_1864": ["ScatterChartDefinition"],
        "_1865": ["Series2D"],
        "_1866": ["SMTAxis"],
        "_1867": ["ThreeDChartDefinition"],
        "_1868": ["ThreeDVectorChartDefinition"],
        "_1869": ["TwoDChartDefinition"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BubbleChartDefinition",
    "ConstantLine",
    "CustomLineChart",
    "CustomTableAndChart",
    "LegacyChartMathChartDefinition",
    "MatrixVisualisationDefinition",
    "ModeConstantLine",
    "NDChartDefinition",
    "ParallelCoordinatesChartDefinition",
    "PointsForSurface",
    "ScatterChartDefinition",
    "Series2D",
    "SMTAxis",
    "ThreeDChartDefinition",
    "ThreeDVectorChartDefinition",
    "TwoDChartDefinition",
)
