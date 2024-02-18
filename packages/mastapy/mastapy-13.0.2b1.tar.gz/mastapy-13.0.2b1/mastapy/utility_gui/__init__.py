"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1849 import ColumnInputOptions
    from ._1850 import DataInputFileOptions
    from ._1851 import DataLoggerItem
    from ._1852 import DataLoggerWithCharts
    from ._1853 import ScalingDrawStyle
else:
    import_structure = {
        "_1849": ["ColumnInputOptions"],
        "_1850": ["DataInputFileOptions"],
        "_1851": ["DataLoggerItem"],
        "_1852": ["DataLoggerWithCharts"],
        "_1853": ["ScalingDrawStyle"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ColumnInputOptions",
    "DataInputFileOptions",
    "DataLoggerItem",
    "DataLoggerWithCharts",
    "ScalingDrawStyle",
)
