"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2239 import DesignStateTargetRatio
    from ._2240 import PlanetGearOptions
    from ._2241 import SystemOptimiser
    from ._2242 import SystemOptimiserDetails
    from ._2243 import ToothNumberFinder
else:
    import_structure = {
        "_2239": ["DesignStateTargetRatio"],
        "_2240": ["PlanetGearOptions"],
        "_2241": ["SystemOptimiser"],
        "_2242": ["SystemOptimiserDetails"],
        "_2243": ["ToothNumberFinder"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "DesignStateTargetRatio",
    "PlanetGearOptions",
    "SystemOptimiser",
    "SystemOptimiserDetails",
    "ToothNumberFinder",
)
