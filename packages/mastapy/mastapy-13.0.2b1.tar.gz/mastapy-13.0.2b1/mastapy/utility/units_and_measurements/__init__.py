"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1604 import DegreesMinutesSeconds
    from ._1605 import EnumUnit
    from ._1606 import InverseUnit
    from ._1607 import MeasurementBase
    from ._1608 import MeasurementSettings
    from ._1609 import MeasurementSystem
    from ._1610 import SafetyFactorUnit
    from ._1611 import TimeUnit
    from ._1612 import Unit
    from ._1613 import UnitGradient
else:
    import_structure = {
        "_1604": ["DegreesMinutesSeconds"],
        "_1605": ["EnumUnit"],
        "_1606": ["InverseUnit"],
        "_1607": ["MeasurementBase"],
        "_1608": ["MeasurementSettings"],
        "_1609": ["MeasurementSystem"],
        "_1610": ["SafetyFactorUnit"],
        "_1611": ["TimeUnit"],
        "_1612": ["Unit"],
        "_1613": ["UnitGradient"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "DegreesMinutesSeconds",
    "EnumUnit",
    "InverseUnit",
    "MeasurementBase",
    "MeasurementSettings",
    "MeasurementSystem",
    "SafetyFactorUnit",
    "TimeUnit",
    "Unit",
    "UnitGradient",
)
