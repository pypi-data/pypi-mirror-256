"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1438 import KeyedJointDesign
    from ._1439 import KeyTypes
    from ._1440 import KeywayJointHalfDesign
    from ._1441 import NumberOfKeys
else:
    import_structure = {
        "_1438": ["KeyedJointDesign"],
        "_1439": ["KeyTypes"],
        "_1440": ["KeywayJointHalfDesign"],
        "_1441": ["NumberOfKeys"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "KeyedJointDesign",
    "KeyTypes",
    "KeywayJointHalfDesign",
    "NumberOfKeys",
)
