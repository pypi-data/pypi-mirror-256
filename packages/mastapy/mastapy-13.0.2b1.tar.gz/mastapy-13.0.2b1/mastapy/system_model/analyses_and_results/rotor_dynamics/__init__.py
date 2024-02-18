"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._4028 import RotorDynamicsDrawStyle
    from ._4029 import ShaftComplexShape
    from ._4030 import ShaftForcedComplexShape
    from ._4031 import ShaftModalComplexShape
    from ._4032 import ShaftModalComplexShapeAtSpeeds
    from ._4033 import ShaftModalComplexShapeAtStiffness
else:
    import_structure = {
        "_4028": ["RotorDynamicsDrawStyle"],
        "_4029": ["ShaftComplexShape"],
        "_4030": ["ShaftForcedComplexShape"],
        "_4031": ["ShaftModalComplexShape"],
        "_4032": ["ShaftModalComplexShapeAtSpeeds"],
        "_4033": ["ShaftModalComplexShapeAtStiffness"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "RotorDynamicsDrawStyle",
    "ShaftComplexShape",
    "ShaftForcedComplexShape",
    "ShaftModalComplexShape",
    "ShaftModalComplexShapeAtSpeeds",
    "ShaftModalComplexShapeAtStiffness",
)
