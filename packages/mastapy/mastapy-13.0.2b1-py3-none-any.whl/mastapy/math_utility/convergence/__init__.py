"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1576 import ConvergenceLogger
    from ._1577 import DataLogger
else:
    import_structure = {
        "_1576": ["ConvergenceLogger"],
        "_1577": ["DataLogger"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ConvergenceLogger",
    "DataLogger",
)
