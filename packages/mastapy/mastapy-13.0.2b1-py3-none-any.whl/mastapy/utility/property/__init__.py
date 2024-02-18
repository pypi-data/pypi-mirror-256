"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1836 import EnumWithSelectedValue
    from ._1838 import DeletableCollectionMember
    from ._1839 import DutyCyclePropertySummary
    from ._1840 import DutyCyclePropertySummaryForce
    from ._1841 import DutyCyclePropertySummaryPercentage
    from ._1842 import DutyCyclePropertySummarySmallAngle
    from ._1843 import DutyCyclePropertySummaryStress
    from ._1844 import DutyCyclePropertySummaryVeryShortLength
    from ._1845 import EnumWithBoolean
    from ._1846 import NamedRangeWithOverridableMinAndMax
    from ._1847 import TypedObjectsWithOption
else:
    import_structure = {
        "_1836": ["EnumWithSelectedValue"],
        "_1838": ["DeletableCollectionMember"],
        "_1839": ["DutyCyclePropertySummary"],
        "_1840": ["DutyCyclePropertySummaryForce"],
        "_1841": ["DutyCyclePropertySummaryPercentage"],
        "_1842": ["DutyCyclePropertySummarySmallAngle"],
        "_1843": ["DutyCyclePropertySummaryStress"],
        "_1844": ["DutyCyclePropertySummaryVeryShortLength"],
        "_1845": ["EnumWithBoolean"],
        "_1846": ["NamedRangeWithOverridableMinAndMax"],
        "_1847": ["TypedObjectsWithOption"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "EnumWithSelectedValue",
    "DeletableCollectionMember",
    "DutyCyclePropertySummary",
    "DutyCyclePropertySummaryForce",
    "DutyCyclePropertySummaryPercentage",
    "DutyCyclePropertySummarySmallAngle",
    "DutyCyclePropertySummaryStress",
    "DutyCyclePropertySummaryVeryShortLength",
    "EnumWithBoolean",
    "NamedRangeWithOverridableMinAndMax",
    "TypedObjectsWithOption",
)
