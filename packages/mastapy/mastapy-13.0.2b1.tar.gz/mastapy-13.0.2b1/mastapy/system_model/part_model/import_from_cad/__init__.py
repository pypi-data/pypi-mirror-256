"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2495 import AbstractShaftFromCAD
    from ._2496 import ClutchFromCAD
    from ._2497 import ComponentFromCAD
    from ._2498 import ConceptBearingFromCAD
    from ._2499 import ConnectorFromCAD
    from ._2500 import CylindricalGearFromCAD
    from ._2501 import CylindricalGearInPlanetarySetFromCAD
    from ._2502 import CylindricalPlanetGearFromCAD
    from ._2503 import CylindricalRingGearFromCAD
    from ._2504 import CylindricalSunGearFromCAD
    from ._2505 import HousedOrMounted
    from ._2506 import MountableComponentFromCAD
    from ._2507 import PlanetShaftFromCAD
    from ._2508 import PulleyFromCAD
    from ._2509 import RigidConnectorFromCAD
    from ._2510 import RollingBearingFromCAD
    from ._2511 import ShaftFromCAD
else:
    import_structure = {
        "_2495": ["AbstractShaftFromCAD"],
        "_2496": ["ClutchFromCAD"],
        "_2497": ["ComponentFromCAD"],
        "_2498": ["ConceptBearingFromCAD"],
        "_2499": ["ConnectorFromCAD"],
        "_2500": ["CylindricalGearFromCAD"],
        "_2501": ["CylindricalGearInPlanetarySetFromCAD"],
        "_2502": ["CylindricalPlanetGearFromCAD"],
        "_2503": ["CylindricalRingGearFromCAD"],
        "_2504": ["CylindricalSunGearFromCAD"],
        "_2505": ["HousedOrMounted"],
        "_2506": ["MountableComponentFromCAD"],
        "_2507": ["PlanetShaftFromCAD"],
        "_2508": ["PulleyFromCAD"],
        "_2509": ["RigidConnectorFromCAD"],
        "_2510": ["RollingBearingFromCAD"],
        "_2511": ["ShaftFromCAD"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractShaftFromCAD",
    "ClutchFromCAD",
    "ComponentFromCAD",
    "ConceptBearingFromCAD",
    "ConnectorFromCAD",
    "CylindricalGearFromCAD",
    "CylindricalGearInPlanetarySetFromCAD",
    "CylindricalPlanetGearFromCAD",
    "CylindricalRingGearFromCAD",
    "CylindricalSunGearFromCAD",
    "HousedOrMounted",
    "MountableComponentFromCAD",
    "PlanetShaftFromCAD",
    "PulleyFromCAD",
    "RigidConnectorFromCAD",
    "RollingBearingFromCAD",
    "ShaftFromCAD",
)
