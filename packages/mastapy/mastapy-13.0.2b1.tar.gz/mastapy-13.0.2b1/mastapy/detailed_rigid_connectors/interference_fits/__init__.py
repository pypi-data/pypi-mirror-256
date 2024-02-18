"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1444 import AssemblyMethods
    from ._1445 import CalculationMethods
    from ._1446 import InterferenceFitDesign
    from ._1447 import InterferenceFitHalfDesign
    from ._1448 import StressRegions
    from ._1449 import Table4JointInterfaceTypes
else:
    import_structure = {
        "_1444": ["AssemblyMethods"],
        "_1445": ["CalculationMethods"],
        "_1446": ["InterferenceFitDesign"],
        "_1447": ["InterferenceFitHalfDesign"],
        "_1448": ["StressRegions"],
        "_1449": ["Table4JointInterfaceTypes"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AssemblyMethods",
    "CalculationMethods",
    "InterferenceFitDesign",
    "InterferenceFitHalfDesign",
    "StressRegions",
    "Table4JointInterfaceTypes",
)
