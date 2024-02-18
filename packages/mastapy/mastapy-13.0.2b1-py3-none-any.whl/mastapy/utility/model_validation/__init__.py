"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1793 import Fix
    from ._1794 import Severity
    from ._1795 import Status
    from ._1796 import StatusItem
    from ._1797 import StatusItemSeverity
else:
    import_structure = {
        "_1793": ["Fix"],
        "_1794": ["Severity"],
        "_1795": ["Status"],
        "_1796": ["StatusItem"],
        "_1797": ["StatusItemSeverity"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Fix",
    "Severity",
    "Status",
    "StatusItem",
    "StatusItemSeverity",
)
