"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2570 import CycloidalAssembly
    from ._2571 import CycloidalDisc
    from ._2572 import RingPins
else:
    import_structure = {
        "_2570": ["CycloidalAssembly"],
        "_2571": ["CycloidalDisc"],
        "_2572": ["RingPins"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "CycloidalAssembly",
    "CycloidalDisc",
    "RingPins",
)
