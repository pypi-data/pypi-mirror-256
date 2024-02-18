"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2132 import BearingDesign
    from ._2133 import DetailedBearing
    from ._2134 import DummyRollingBearing
    from ._2135 import LinearBearing
    from ._2136 import NonLinearBearing
else:
    import_structure = {
        "_2132": ["BearingDesign"],
        "_2133": ["DetailedBearing"],
        "_2134": ["DummyRollingBearing"],
        "_2135": ["LinearBearing"],
        "_2136": ["NonLinearBearing"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BearingDesign",
    "DetailedBearing",
    "DummyRollingBearing",
    "LinearBearing",
    "NonLinearBearing",
)
