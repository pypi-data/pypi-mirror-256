"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1388 import DetailedRigidConnectorDesign
    from ._1389 import DetailedRigidConnectorHalfDesign
else:
    import_structure = {
        "_1388": ["DetailedRigidConnectorDesign"],
        "_1389": ["DetailedRigidConnectorHalfDesign"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "DetailedRigidConnectorDesign",
    "DetailedRigidConnectorHalfDesign",
)
