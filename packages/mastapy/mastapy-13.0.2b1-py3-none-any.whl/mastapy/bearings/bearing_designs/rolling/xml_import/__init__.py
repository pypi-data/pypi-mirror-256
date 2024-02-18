"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2178 import AbstractXmlVariableAssignment
    from ._2179 import BearingImportFile
    from ._2180 import RollingBearingImporter
    from ._2181 import XmlBearingTypeMapping
    from ._2182 import XMLVariableAssignment
else:
    import_structure = {
        "_2178": ["AbstractXmlVariableAssignment"],
        "_2179": ["BearingImportFile"],
        "_2180": ["RollingBearingImporter"],
        "_2181": ["XmlBearingTypeMapping"],
        "_2182": ["XMLVariableAssignment"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractXmlVariableAssignment",
    "BearingImportFile",
    "RollingBearingImporter",
    "XmlBearingTypeMapping",
    "XMLVariableAssignment",
)
