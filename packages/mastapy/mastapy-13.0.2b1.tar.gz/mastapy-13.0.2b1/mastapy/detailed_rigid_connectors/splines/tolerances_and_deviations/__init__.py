"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1422 import FitAndTolerance
    from ._1423 import SAESplineTolerances
else:
    import_structure = {
        "_1422": ["FitAndTolerance"],
        "_1423": ["SAESplineTolerances"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "FitAndTolerance",
    "SAESplineTolerances",
)
