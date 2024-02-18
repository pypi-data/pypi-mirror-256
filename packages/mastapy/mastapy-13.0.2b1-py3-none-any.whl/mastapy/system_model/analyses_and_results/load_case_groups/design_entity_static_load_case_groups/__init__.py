"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5674 import AbstractAssemblyStaticLoadCaseGroup
    from ._5675 import ComponentStaticLoadCaseGroup
    from ._5676 import ConnectionStaticLoadCaseGroup
    from ._5677 import DesignEntityStaticLoadCaseGroup
    from ._5678 import GearSetStaticLoadCaseGroup
    from ._5679 import PartStaticLoadCaseGroup
else:
    import_structure = {
        "_5674": ["AbstractAssemblyStaticLoadCaseGroup"],
        "_5675": ["ComponentStaticLoadCaseGroup"],
        "_5676": ["ConnectionStaticLoadCaseGroup"],
        "_5677": ["DesignEntityStaticLoadCaseGroup"],
        "_5678": ["GearSetStaticLoadCaseGroup"],
        "_5679": ["PartStaticLoadCaseGroup"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyStaticLoadCaseGroup",
    "ComponentStaticLoadCaseGroup",
    "ConnectionStaticLoadCaseGroup",
    "DesignEntityStaticLoadCaseGroup",
    "GearSetStaticLoadCaseGroup",
    "PartStaticLoadCaseGroup",
)
