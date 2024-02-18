"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2103 import BallISO2812007Results
    from ._2104 import BallISOTS162812008Results
    from ._2105 import ISO2812007Results
    from ._2106 import ISO762006Results
    from ._2107 import ISOResults
    from ._2108 import ISOTS162812008Results
    from ._2109 import RollerISO2812007Results
    from ._2110 import RollerISOTS162812008Results
    from ._2111 import StressConcentrationMethod
else:
    import_structure = {
        "_2103": ["BallISO2812007Results"],
        "_2104": ["BallISOTS162812008Results"],
        "_2105": ["ISO2812007Results"],
        "_2106": ["ISO762006Results"],
        "_2107": ["ISOResults"],
        "_2108": ["ISOTS162812008Results"],
        "_2109": ["RollerISO2812007Results"],
        "_2110": ["RollerISOTS162812008Results"],
        "_2111": ["StressConcentrationMethod"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BallISO2812007Results",
    "BallISOTS162812008Results",
    "ISO2812007Results",
    "ISO762006Results",
    "ISOResults",
    "ISOTS162812008Results",
    "RollerISO2812007Results",
    "RollerISOTS162812008Results",
    "StressConcentrationMethod",
)
