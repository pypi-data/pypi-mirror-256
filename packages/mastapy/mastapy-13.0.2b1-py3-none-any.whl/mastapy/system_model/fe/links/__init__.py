"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2420 import FELink
    from ._2421 import ElectricMachineStatorFELink
    from ._2422 import FELinkWithSelection
    from ._2423 import GearMeshFELink
    from ._2424 import GearWithDuplicatedMeshesFELink
    from ._2425 import MultiAngleConnectionFELink
    from ._2426 import MultiNodeConnectorFELink
    from ._2427 import MultiNodeFELink
    from ._2428 import PlanetaryConnectorMultiNodeFELink
    from ._2429 import PlanetBasedFELink
    from ._2430 import PlanetCarrierFELink
    from ._2431 import PointLoadFELink
    from ._2432 import RollingRingConnectionFELink
    from ._2433 import ShaftHubConnectionFELink
    from ._2434 import SingleNodeFELink
else:
    import_structure = {
        "_2420": ["FELink"],
        "_2421": ["ElectricMachineStatorFELink"],
        "_2422": ["FELinkWithSelection"],
        "_2423": ["GearMeshFELink"],
        "_2424": ["GearWithDuplicatedMeshesFELink"],
        "_2425": ["MultiAngleConnectionFELink"],
        "_2426": ["MultiNodeConnectorFELink"],
        "_2427": ["MultiNodeFELink"],
        "_2428": ["PlanetaryConnectorMultiNodeFELink"],
        "_2429": ["PlanetBasedFELink"],
        "_2430": ["PlanetCarrierFELink"],
        "_2431": ["PointLoadFELink"],
        "_2432": ["RollingRingConnectionFELink"],
        "_2433": ["ShaftHubConnectionFELink"],
        "_2434": ["SingleNodeFELink"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "FELink",
    "ElectricMachineStatorFELink",
    "FELinkWithSelection",
    "GearMeshFELink",
    "GearWithDuplicatedMeshesFELink",
    "MultiAngleConnectionFELink",
    "MultiNodeConnectorFELink",
    "MultiNodeFELink",
    "PlanetaryConnectorMultiNodeFELink",
    "PlanetBasedFELink",
    "PlanetCarrierFELink",
    "PointLoadFELink",
    "RollingRingConnectionFELink",
    "ShaftHubConnectionFELink",
    "SingleNodeFELink",
)
