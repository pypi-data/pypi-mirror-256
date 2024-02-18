"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1571 import DataScalingOptions
    from ._1572 import DataScalingReferenceValues
    from ._1573 import DataScalingReferenceValuesBase
else:
    import_structure = {
        "_1571": ["DataScalingOptions"],
        "_1572": ["DataScalingReferenceValues"],
        "_1573": ["DataScalingReferenceValuesBase"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "DataScalingOptions",
    "DataScalingReferenceValues",
    "DataScalingReferenceValuesBase",
)
