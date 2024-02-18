"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2573 import BeltCreationOptions
    from ._2574 import CycloidalAssemblyCreationOptions
    from ._2575 import CylindricalGearLinearTrainCreationOptions
    from ._2576 import PlanetCarrierCreationOptions
    from ._2577 import ShaftCreationOptions
else:
    import_structure = {
        "_2573": ["BeltCreationOptions"],
        "_2574": ["CycloidalAssemblyCreationOptions"],
        "_2575": ["CylindricalGearLinearTrainCreationOptions"],
        "_2576": ["PlanetCarrierCreationOptions"],
        "_2577": ["ShaftCreationOptions"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BeltCreationOptions",
    "CycloidalAssemblyCreationOptions",
    "CylindricalGearLinearTrainCreationOptions",
    "PlanetCarrierCreationOptions",
    "ShaftCreationOptions",
)
