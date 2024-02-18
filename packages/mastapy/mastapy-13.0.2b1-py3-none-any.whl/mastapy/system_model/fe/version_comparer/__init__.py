"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2414 import DesignResults
    from ._2415 import FESubstructureResults
    from ._2416 import FESubstructureVersionComparer
    from ._2417 import LoadCaseResults
    from ._2418 import LoadCasesToRun
    from ._2419 import NodeComparisonResult
else:
    import_structure = {
        "_2414": ["DesignResults"],
        "_2415": ["FESubstructureResults"],
        "_2416": ["FESubstructureVersionComparer"],
        "_2417": ["LoadCaseResults"],
        "_2418": ["LoadCasesToRun"],
        "_2419": ["NodeComparisonResult"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "DesignResults",
    "FESubstructureResults",
    "FESubstructureVersionComparer",
    "LoadCaseResults",
    "LoadCasesToRun",
    "NodeComparisonResult",
)
