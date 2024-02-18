"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2335 import CycloidalDiscAxialLeftSocket
    from ._2336 import CycloidalDiscAxialRightSocket
    from ._2337 import CycloidalDiscCentralBearingConnection
    from ._2338 import CycloidalDiscInnerSocket
    from ._2339 import CycloidalDiscOuterSocket
    from ._2340 import CycloidalDiscPlanetaryBearingConnection
    from ._2341 import CycloidalDiscPlanetaryBearingSocket
    from ._2342 import RingPinsSocket
    from ._2343 import RingPinsToDiscConnection
else:
    import_structure = {
        "_2335": ["CycloidalDiscAxialLeftSocket"],
        "_2336": ["CycloidalDiscAxialRightSocket"],
        "_2337": ["CycloidalDiscCentralBearingConnection"],
        "_2338": ["CycloidalDiscInnerSocket"],
        "_2339": ["CycloidalDiscOuterSocket"],
        "_2340": ["CycloidalDiscPlanetaryBearingConnection"],
        "_2341": ["CycloidalDiscPlanetaryBearingSocket"],
        "_2342": ["RingPinsSocket"],
        "_2343": ["RingPinsToDiscConnection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "CycloidalDiscAxialLeftSocket",
    "CycloidalDiscAxialRightSocket",
    "CycloidalDiscCentralBearingConnection",
    "CycloidalDiscInnerSocket",
    "CycloidalDiscOuterSocket",
    "CycloidalDiscPlanetaryBearingConnection",
    "CycloidalDiscPlanetaryBearingSocket",
    "RingPinsSocket",
    "RingPinsToDiscConnection",
)
