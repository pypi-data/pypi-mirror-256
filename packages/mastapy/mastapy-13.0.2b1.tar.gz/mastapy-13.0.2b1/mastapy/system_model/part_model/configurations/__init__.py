"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2613 import ActiveFESubstructureSelection
    from ._2614 import ActiveFESubstructureSelectionGroup
    from ._2615 import ActiveShaftDesignSelection
    from ._2616 import ActiveShaftDesignSelectionGroup
    from ._2617 import BearingDetailConfiguration
    from ._2618 import BearingDetailSelection
    from ._2619 import PartDetailConfiguration
    from ._2620 import PartDetailSelection
else:
    import_structure = {
        "_2613": ["ActiveFESubstructureSelection"],
        "_2614": ["ActiveFESubstructureSelectionGroup"],
        "_2615": ["ActiveShaftDesignSelection"],
        "_2616": ["ActiveShaftDesignSelectionGroup"],
        "_2617": ["BearingDetailConfiguration"],
        "_2618": ["BearingDetailSelection"],
        "_2619": ["PartDetailConfiguration"],
        "_2620": ["PartDetailSelection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ActiveFESubstructureSelection",
    "ActiveFESubstructureSelectionGroup",
    "ActiveShaftDesignSelection",
    "ActiveShaftDesignSelectionGroup",
    "BearingDetailConfiguration",
    "BearingDetailSelection",
    "PartDetailConfiguration",
    "PartDetailSelection",
)
