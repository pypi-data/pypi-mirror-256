"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2116 import DynamicBearingAnalysisOptions
else:
    import_structure = {
        "_2116": ["DynamicBearingAnalysisOptions"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = ("DynamicBearingAnalysisOptions",)
