"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1741 import ScriptingSetup
    from ._1742 import UserDefinedPropertyKey
    from ._1743 import UserSpecifiedData
else:
    import_structure = {
        "_1741": ["ScriptingSetup"],
        "_1742": ["UserDefinedPropertyKey"],
        "_1743": ["UserSpecifiedData"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ScriptingSetup",
    "UserDefinedPropertyKey",
    "UserSpecifiedData",
)
