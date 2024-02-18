"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2112 import InnerRingFittingThermalResults
    from ._2113 import InterferenceComponents
    from ._2114 import OuterRingFittingThermalResults
    from ._2115 import RingFittingThermalResults
else:
    import_structure = {
        "_2112": ["InnerRingFittingThermalResults"],
        "_2113": ["InterferenceComponents"],
        "_2114": ["OuterRingFittingThermalResults"],
        "_2115": ["RingFittingThermalResults"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "InnerRingFittingThermalResults",
    "InterferenceComponents",
    "OuterRingFittingThermalResults",
    "RingFittingThermalResults",
)
