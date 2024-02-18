"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1424 import AGMA6123SplineHalfRating
    from ._1425 import AGMA6123SplineJointRating
    from ._1426 import DIN5466SplineHalfRating
    from ._1427 import DIN5466SplineRating
    from ._1428 import GBT17855SplineHalfRating
    from ._1429 import GBT17855SplineJointRating
    from ._1430 import SAESplineHalfRating
    from ._1431 import SAESplineJointRating
    from ._1432 import SplineHalfRating
    from ._1433 import SplineJointRating
else:
    import_structure = {
        "_1424": ["AGMA6123SplineHalfRating"],
        "_1425": ["AGMA6123SplineJointRating"],
        "_1426": ["DIN5466SplineHalfRating"],
        "_1427": ["DIN5466SplineRating"],
        "_1428": ["GBT17855SplineHalfRating"],
        "_1429": ["GBT17855SplineJointRating"],
        "_1430": ["SAESplineHalfRating"],
        "_1431": ["SAESplineJointRating"],
        "_1432": ["SplineHalfRating"],
        "_1433": ["SplineJointRating"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AGMA6123SplineHalfRating",
    "AGMA6123SplineJointRating",
    "DIN5466SplineHalfRating",
    "DIN5466SplineRating",
    "GBT17855SplineHalfRating",
    "GBT17855SplineJointRating",
    "SAESplineHalfRating",
    "SAESplineJointRating",
    "SplineHalfRating",
    "SplineJointRating",
)
