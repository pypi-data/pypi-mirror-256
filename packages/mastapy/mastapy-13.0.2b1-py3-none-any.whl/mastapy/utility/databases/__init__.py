"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1826 import Database
    from ._1827 import DatabaseConnectionSettings
    from ._1828 import DatabaseKey
    from ._1829 import DatabaseSettings
    from ._1830 import NamedDatabase
    from ._1831 import NamedDatabaseItem
    from ._1832 import NamedKey
    from ._1833 import SQLDatabase
else:
    import_structure = {
        "_1826": ["Database"],
        "_1827": ["DatabaseConnectionSettings"],
        "_1828": ["DatabaseKey"],
        "_1829": ["DatabaseSettings"],
        "_1830": ["NamedDatabase"],
        "_1831": ["NamedDatabaseItem"],
        "_1832": ["NamedKey"],
        "_1833": ["SQLDatabase"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Database",
    "DatabaseConnectionSettings",
    "DatabaseKey",
    "DatabaseSettings",
    "NamedDatabase",
    "NamedDatabaseItem",
    "NamedKey",
    "SQLDatabase",
)
