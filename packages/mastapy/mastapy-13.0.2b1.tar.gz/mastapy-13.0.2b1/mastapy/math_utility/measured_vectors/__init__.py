"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1561 import AbstractForceAndDisplacementResults
    from ._1562 import ForceAndDisplacementResults
    from ._1563 import ForceResults
    from ._1564 import NodeResults
    from ._1565 import OverridableDisplacementBoundaryCondition
    from ._1566 import VectorWithLinearAndAngularComponents
else:
    import_structure = {
        "_1561": ["AbstractForceAndDisplacementResults"],
        "_1562": ["ForceAndDisplacementResults"],
        "_1563": ["ForceResults"],
        "_1564": ["NodeResults"],
        "_1565": ["OverridableDisplacementBoundaryCondition"],
        "_1566": ["VectorWithLinearAndAngularComponents"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractForceAndDisplacementResults",
    "ForceAndDisplacementResults",
    "ForceResults",
    "NodeResults",
    "OverridableDisplacementBoundaryCondition",
    "VectorWithLinearAndAngularComponents",
)
