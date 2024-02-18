"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2228 import ConicalGearOptimisationStrategy
    from ._2229 import ConicalGearOptimizationStep
    from ._2230 import ConicalGearOptimizationStrategyDatabase
    from ._2231 import CylindricalGearOptimisationStrategy
    from ._2232 import CylindricalGearOptimizationStep
    from ._2233 import MeasuredAndFactorViewModel
    from ._2234 import MicroGeometryOptimisationTarget
    from ._2235 import OptimizationStep
    from ._2236 import OptimizationStrategy
    from ._2237 import OptimizationStrategyBase
    from ._2238 import OptimizationStrategyDatabase
else:
    import_structure = {
        "_2228": ["ConicalGearOptimisationStrategy"],
        "_2229": ["ConicalGearOptimizationStep"],
        "_2230": ["ConicalGearOptimizationStrategyDatabase"],
        "_2231": ["CylindricalGearOptimisationStrategy"],
        "_2232": ["CylindricalGearOptimizationStep"],
        "_2233": ["MeasuredAndFactorViewModel"],
        "_2234": ["MicroGeometryOptimisationTarget"],
        "_2235": ["OptimizationStep"],
        "_2236": ["OptimizationStrategy"],
        "_2237": ["OptimizationStrategyBase"],
        "_2238": ["OptimizationStrategyDatabase"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ConicalGearOptimisationStrategy",
    "ConicalGearOptimizationStep",
    "ConicalGearOptimizationStrategyDatabase",
    "CylindricalGearOptimisationStrategy",
    "CylindricalGearOptimizationStep",
    "MeasuredAndFactorViewModel",
    "MicroGeometryOptimisationTarget",
    "OptimizationStep",
    "OptimizationStrategy",
    "OptimizationStrategyBase",
    "OptimizationStrategyDatabase",
)
