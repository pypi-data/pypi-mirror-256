"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1799 import GearMeshForTE
    from ._1800 import GearOrderForTE
    from ._1801 import GearPositions
    from ._1802 import HarmonicOrderForTE
    from ._1803 import LabelOnlyOrder
    from ._1804 import OrderForTE
    from ._1805 import OrderSelector
    from ._1806 import OrderWithRadius
    from ._1807 import RollingBearingOrder
    from ._1808 import ShaftOrderForTE
    from ._1809 import UserDefinedOrderForTE
else:
    import_structure = {
        "_1799": ["GearMeshForTE"],
        "_1800": ["GearOrderForTE"],
        "_1801": ["GearPositions"],
        "_1802": ["HarmonicOrderForTE"],
        "_1803": ["LabelOnlyOrder"],
        "_1804": ["OrderForTE"],
        "_1805": ["OrderSelector"],
        "_1806": ["OrderWithRadius"],
        "_1807": ["RollingBearingOrder"],
        "_1808": ["ShaftOrderForTE"],
        "_1809": ["UserDefinedOrderForTE"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "GearMeshForTE",
    "GearOrderForTE",
    "GearPositions",
    "HarmonicOrderForTE",
    "LabelOnlyOrder",
    "OrderForTE",
    "OrderSelector",
    "OrderWithRadius",
    "RollingBearingOrder",
    "ShaftOrderForTE",
    "UserDefinedOrderForTE",
)
