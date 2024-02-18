"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2488 import ConcentricOrParallelPartGroup
    from ._2489 import ConcentricPartGroup
    from ._2490 import ConcentricPartGroupParallelToThis
    from ._2491 import DesignMeasurements
    from ._2492 import ParallelPartGroup
    from ._2493 import ParallelPartGroupSelection
    from ._2494 import PartGroup
else:
    import_structure = {
        "_2488": ["ConcentricOrParallelPartGroup"],
        "_2489": ["ConcentricPartGroup"],
        "_2490": ["ConcentricPartGroupParallelToThis"],
        "_2491": ["DesignMeasurements"],
        "_2492": ["ParallelPartGroup"],
        "_2493": ["ParallelPartGroupSelection"],
        "_2494": ["PartGroup"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ConcentricOrParallelPartGroup",
    "ConcentricPartGroup",
    "ConcentricPartGroupParallelToThis",
    "DesignMeasurements",
    "ParallelPartGroup",
    "ParallelPartGroupSelection",
    "PartGroup",
)
