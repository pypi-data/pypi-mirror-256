"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2267 import AbstractShaftToMountableComponentConnection
    from ._2268 import BearingInnerSocket
    from ._2269 import BearingOuterSocket
    from ._2270 import BeltConnection
    from ._2271 import CoaxialConnection
    from ._2272 import ComponentConnection
    from ._2273 import ComponentMeasurer
    from ._2274 import Connection
    from ._2275 import CVTBeltConnection
    from ._2276 import CVTPulleySocket
    from ._2277 import CylindricalComponentConnection
    from ._2278 import CylindricalSocket
    from ._2279 import DatumMeasurement
    from ._2280 import ElectricMachineStatorSocket
    from ._2281 import InnerShaftSocket
    from ._2282 import InnerShaftSocketBase
    from ._2283 import InterMountableComponentConnection
    from ._2284 import MountableComponentInnerSocket
    from ._2285 import MountableComponentOuterSocket
    from ._2286 import MountableComponentSocket
    from ._2287 import OuterShaftSocket
    from ._2288 import OuterShaftSocketBase
    from ._2289 import PlanetaryConnection
    from ._2290 import PlanetarySocket
    from ._2291 import PlanetarySocketBase
    from ._2292 import PulleySocket
    from ._2293 import RealignmentResult
    from ._2294 import RollingRingConnection
    from ._2295 import RollingRingSocket
    from ._2296 import ShaftSocket
    from ._2297 import ShaftToMountableComponentConnection
    from ._2298 import Socket
    from ._2299 import SocketConnectionOptions
    from ._2300 import SocketConnectionSelection
else:
    import_structure = {
        "_2267": ["AbstractShaftToMountableComponentConnection"],
        "_2268": ["BearingInnerSocket"],
        "_2269": ["BearingOuterSocket"],
        "_2270": ["BeltConnection"],
        "_2271": ["CoaxialConnection"],
        "_2272": ["ComponentConnection"],
        "_2273": ["ComponentMeasurer"],
        "_2274": ["Connection"],
        "_2275": ["CVTBeltConnection"],
        "_2276": ["CVTPulleySocket"],
        "_2277": ["CylindricalComponentConnection"],
        "_2278": ["CylindricalSocket"],
        "_2279": ["DatumMeasurement"],
        "_2280": ["ElectricMachineStatorSocket"],
        "_2281": ["InnerShaftSocket"],
        "_2282": ["InnerShaftSocketBase"],
        "_2283": ["InterMountableComponentConnection"],
        "_2284": ["MountableComponentInnerSocket"],
        "_2285": ["MountableComponentOuterSocket"],
        "_2286": ["MountableComponentSocket"],
        "_2287": ["OuterShaftSocket"],
        "_2288": ["OuterShaftSocketBase"],
        "_2289": ["PlanetaryConnection"],
        "_2290": ["PlanetarySocket"],
        "_2291": ["PlanetarySocketBase"],
        "_2292": ["PulleySocket"],
        "_2293": ["RealignmentResult"],
        "_2294": ["RollingRingConnection"],
        "_2295": ["RollingRingSocket"],
        "_2296": ["ShaftSocket"],
        "_2297": ["ShaftToMountableComponentConnection"],
        "_2298": ["Socket"],
        "_2299": ["SocketConnectionOptions"],
        "_2300": ["SocketConnectionSelection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractShaftToMountableComponentConnection",
    "BearingInnerSocket",
    "BearingOuterSocket",
    "BeltConnection",
    "CoaxialConnection",
    "ComponentConnection",
    "ComponentMeasurer",
    "Connection",
    "CVTBeltConnection",
    "CVTPulleySocket",
    "CylindricalComponentConnection",
    "CylindricalSocket",
    "DatumMeasurement",
    "ElectricMachineStatorSocket",
    "InnerShaftSocket",
    "InnerShaftSocketBase",
    "InterMountableComponentConnection",
    "MountableComponentInnerSocket",
    "MountableComponentOuterSocket",
    "MountableComponentSocket",
    "OuterShaftSocket",
    "OuterShaftSocketBase",
    "PlanetaryConnection",
    "PlanetarySocket",
    "PlanetarySocketBase",
    "PulleySocket",
    "RealignmentResult",
    "RollingRingConnection",
    "RollingRingSocket",
    "ShaftSocket",
    "ShaftToMountableComponentConnection",
    "Socket",
    "SocketConnectionOptions",
    "SocketConnectionSelection",
)
