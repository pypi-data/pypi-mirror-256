"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._7564 import ApiEnumForAttribute
    from ._7565 import ApiVersion
    from ._7566 import SMTBitmap
    from ._7568 import MastaPropertyAttribute
    from ._7569 import PythonCommand
    from ._7570 import ScriptingCommand
    from ._7571 import ScriptingExecutionCommand
    from ._7572 import ScriptingObjectCommand
    from ._7573 import ApiVersioning
else:
    import_structure = {
        "_7564": ["ApiEnumForAttribute"],
        "_7565": ["ApiVersion"],
        "_7566": ["SMTBitmap"],
        "_7568": ["MastaPropertyAttribute"],
        "_7569": ["PythonCommand"],
        "_7570": ["ScriptingCommand"],
        "_7571": ["ScriptingExecutionCommand"],
        "_7572": ["ScriptingObjectCommand"],
        "_7573": ["ApiVersioning"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
