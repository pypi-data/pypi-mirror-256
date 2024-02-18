"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1790 import CellValuePosition
    from ._1791 import CustomChartType
else:
    import_structure = {
        "_1790": ["CellValuePosition"],
        "_1791": ["CustomChartType"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "CellValuePosition",
    "CustomChartType",
)
