"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1489 import LicenceServer
    from ._7574 import LicenceServerDetails
    from ._7575 import ModuleDetails
    from ._7576 import ModuleLicenceStatus
else:
    import_structure = {
        "_1489": ["LicenceServer"],
        "_7574": ["LicenceServerDetails"],
        "_7575": ["ModuleDetails"],
        "_7576": ["ModuleLicenceStatus"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "LicenceServer",
    "LicenceServerDetails",
    "ModuleDetails",
    "ModuleLicenceStatus",
)
