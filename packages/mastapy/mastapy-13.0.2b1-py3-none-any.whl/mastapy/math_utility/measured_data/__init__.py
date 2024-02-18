"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1567 import GriddedSurfaceAccessor
    from ._1568 import LookupTableBase
    from ._1569 import OnedimensionalFunctionLookupTable
    from ._1570 import TwodimensionalFunctionLookupTable
else:
    import_structure = {
        "_1567": ["GriddedSurfaceAccessor"],
        "_1568": ["LookupTableBase"],
        "_1569": ["OnedimensionalFunctionLookupTable"],
        "_1570": ["TwodimensionalFunctionLookupTable"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "GriddedSurfaceAccessor",
    "LookupTableBase",
    "OnedimensionalFunctionLookupTable",
    "TwodimensionalFunctionLookupTable",
)
