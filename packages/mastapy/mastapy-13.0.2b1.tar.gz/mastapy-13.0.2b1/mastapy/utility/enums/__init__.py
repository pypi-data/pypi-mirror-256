"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1821 import BearingForceArrowOption
    from ._1822 import TableAndChartOptions
    from ._1823 import ThreeDViewContourOption
    from ._1824 import ThreeDViewContourOptionFirstSelection
    from ._1825 import ThreeDViewContourOptionSecondSelection
else:
    import_structure = {
        "_1821": ["BearingForceArrowOption"],
        "_1822": ["TableAndChartOptions"],
        "_1823": ["ThreeDViewContourOption"],
        "_1824": ["ThreeDViewContourOptionFirstSelection"],
        "_1825": ["ThreeDViewContourOptionSecondSelection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BearingForceArrowOption",
    "TableAndChartOptions",
    "ThreeDViewContourOption",
    "ThreeDViewContourOptionFirstSelection",
    "ThreeDViewContourOptionSecondSelection",
)
