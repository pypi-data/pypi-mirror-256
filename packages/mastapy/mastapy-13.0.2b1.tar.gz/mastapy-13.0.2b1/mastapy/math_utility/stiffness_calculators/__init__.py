"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1538 import IndividualContactPosition
    from ._1539 import SurfaceToSurfaceContact
else:
    import_structure = {
        "_1538": ["IndividualContactPosition"],
        "_1539": ["SurfaceToSurfaceContact"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "IndividualContactPosition",
    "SurfaceToSurfaceContact",
)
