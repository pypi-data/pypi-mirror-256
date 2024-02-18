"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1810 import Logger
    from ._1811 import Message
else:
    import_structure = {
        "_1810": ["Logger"],
        "_1811": ["Message"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Logger",
    "Message",
)
