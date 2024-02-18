"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2578 import BeltDrive
    from ._2579 import BeltDriveType
    from ._2580 import Clutch
    from ._2581 import ClutchHalf
    from ._2582 import ClutchType
    from ._2583 import ConceptCoupling
    from ._2584 import ConceptCouplingHalf
    from ._2585 import Coupling
    from ._2586 import CouplingHalf
    from ._2587 import CrowningSpecification
    from ._2588 import CVT
    from ._2589 import CVTPulley
    from ._2590 import PartToPartShearCoupling
    from ._2591 import PartToPartShearCouplingHalf
    from ._2592 import Pulley
    from ._2593 import RigidConnectorStiffnessType
    from ._2594 import RigidConnectorTiltStiffnessTypes
    from ._2595 import RigidConnectorToothLocation
    from ._2596 import RigidConnectorToothSpacingType
    from ._2597 import RigidConnectorTypes
    from ._2598 import RollingRing
    from ._2599 import RollingRingAssembly
    from ._2600 import ShaftHubConnection
    from ._2601 import SplineLeadRelief
    from ._2602 import SpringDamper
    from ._2603 import SpringDamperHalf
    from ._2604 import Synchroniser
    from ._2605 import SynchroniserCone
    from ._2606 import SynchroniserHalf
    from ._2607 import SynchroniserPart
    from ._2608 import SynchroniserSleeve
    from ._2609 import TorqueConverter
    from ._2610 import TorqueConverterPump
    from ._2611 import TorqueConverterSpeedRatio
    from ._2612 import TorqueConverterTurbine
else:
    import_structure = {
        "_2578": ["BeltDrive"],
        "_2579": ["BeltDriveType"],
        "_2580": ["Clutch"],
        "_2581": ["ClutchHalf"],
        "_2582": ["ClutchType"],
        "_2583": ["ConceptCoupling"],
        "_2584": ["ConceptCouplingHalf"],
        "_2585": ["Coupling"],
        "_2586": ["CouplingHalf"],
        "_2587": ["CrowningSpecification"],
        "_2588": ["CVT"],
        "_2589": ["CVTPulley"],
        "_2590": ["PartToPartShearCoupling"],
        "_2591": ["PartToPartShearCouplingHalf"],
        "_2592": ["Pulley"],
        "_2593": ["RigidConnectorStiffnessType"],
        "_2594": ["RigidConnectorTiltStiffnessTypes"],
        "_2595": ["RigidConnectorToothLocation"],
        "_2596": ["RigidConnectorToothSpacingType"],
        "_2597": ["RigidConnectorTypes"],
        "_2598": ["RollingRing"],
        "_2599": ["RollingRingAssembly"],
        "_2600": ["ShaftHubConnection"],
        "_2601": ["SplineLeadRelief"],
        "_2602": ["SpringDamper"],
        "_2603": ["SpringDamperHalf"],
        "_2604": ["Synchroniser"],
        "_2605": ["SynchroniserCone"],
        "_2606": ["SynchroniserHalf"],
        "_2607": ["SynchroniserPart"],
        "_2608": ["SynchroniserSleeve"],
        "_2609": ["TorqueConverter"],
        "_2610": ["TorqueConverterPump"],
        "_2611": ["TorqueConverterSpeedRatio"],
        "_2612": ["TorqueConverterTurbine"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "Pulley",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineLeadRelief",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
