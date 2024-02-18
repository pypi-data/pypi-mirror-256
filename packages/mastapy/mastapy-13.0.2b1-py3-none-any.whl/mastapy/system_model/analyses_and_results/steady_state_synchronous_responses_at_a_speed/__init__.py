"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._3506 import AbstractAssemblySteadyStateSynchronousResponseAtASpeed
    from ._3507 import AbstractShaftOrHousingSteadyStateSynchronousResponseAtASpeed
    from ._3508 import AbstractShaftSteadyStateSynchronousResponseAtASpeed
    from ._3509 import (
        AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3510 import AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3511 import AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3512 import AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed
    from ._3513 import AssemblySteadyStateSynchronousResponseAtASpeed
    from ._3514 import BearingSteadyStateSynchronousResponseAtASpeed
    from ._3515 import BeltConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3516 import BeltDriveSteadyStateSynchronousResponseAtASpeed
    from ._3517 import BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3518 import BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3519 import BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed
    from ._3520 import BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed
    from ._3521 import BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed
    from ._3522 import BevelGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3523 import BevelGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3524 import BevelGearSteadyStateSynchronousResponseAtASpeed
    from ._3525 import BoltedJointSteadyStateSynchronousResponseAtASpeed
    from ._3526 import BoltSteadyStateSynchronousResponseAtASpeed
    from ._3527 import ClutchConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3528 import ClutchHalfSteadyStateSynchronousResponseAtASpeed
    from ._3529 import ClutchSteadyStateSynchronousResponseAtASpeed
    from ._3530 import CoaxialConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3531 import ComponentSteadyStateSynchronousResponseAtASpeed
    from ._3532 import ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3533 import ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed
    from ._3534 import ConceptCouplingSteadyStateSynchronousResponseAtASpeed
    from ._3535 import ConceptGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3536 import ConceptGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3537 import ConceptGearSteadyStateSynchronousResponseAtASpeed
    from ._3538 import ConicalGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3539 import ConicalGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3540 import ConicalGearSteadyStateSynchronousResponseAtASpeed
    from ._3541 import ConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3542 import ConnectorSteadyStateSynchronousResponseAtASpeed
    from ._3543 import CouplingConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3544 import CouplingHalfSteadyStateSynchronousResponseAtASpeed
    from ._3545 import CouplingSteadyStateSynchronousResponseAtASpeed
    from ._3546 import CVTBeltConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3547 import CVTPulleySteadyStateSynchronousResponseAtASpeed
    from ._3548 import CVTSteadyStateSynchronousResponseAtASpeed
    from ._3549 import CycloidalAssemblySteadyStateSynchronousResponseAtASpeed
    from ._3550 import (
        CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3551 import (
        CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3552 import CycloidalDiscSteadyStateSynchronousResponseAtASpeed
    from ._3553 import CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3554 import CylindricalGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3555 import CylindricalGearSteadyStateSynchronousResponseAtASpeed
    from ._3556 import CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed
    from ._3557 import DatumSteadyStateSynchronousResponseAtASpeed
    from ._3558 import ExternalCADModelSteadyStateSynchronousResponseAtASpeed
    from ._3559 import FaceGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3560 import FaceGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3561 import FaceGearSteadyStateSynchronousResponseAtASpeed
    from ._3562 import FEPartSteadyStateSynchronousResponseAtASpeed
    from ._3563 import FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed
    from ._3564 import GearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3565 import GearSetSteadyStateSynchronousResponseAtASpeed
    from ._3566 import GearSteadyStateSynchronousResponseAtASpeed
    from ._3567 import GuideDxfModelSteadyStateSynchronousResponseAtASpeed
    from ._3568 import HypoidGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3569 import HypoidGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3570 import HypoidGearSteadyStateSynchronousResponseAtASpeed
    from ._3571 import (
        InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3572 import (
        KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3573 import (
        KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3574 import (
        KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3575 import (
        KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3576 import (
        KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3577 import (
        KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3578 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3579 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3580 import (
        KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3581 import MassDiscSteadyStateSynchronousResponseAtASpeed
    from ._3582 import MeasurementComponentSteadyStateSynchronousResponseAtASpeed
    from ._3583 import MountableComponentSteadyStateSynchronousResponseAtASpeed
    from ._3584 import OilSealSteadyStateSynchronousResponseAtASpeed
    from ._3585 import PartSteadyStateSynchronousResponseAtASpeed
    from ._3586 import (
        PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3587 import PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed
    from ._3588 import PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed
    from ._3589 import PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3590 import PlanetaryGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3591 import PlanetCarrierSteadyStateSynchronousResponseAtASpeed
    from ._3592 import PointLoadSteadyStateSynchronousResponseAtASpeed
    from ._3593 import PowerLoadSteadyStateSynchronousResponseAtASpeed
    from ._3594 import PulleySteadyStateSynchronousResponseAtASpeed
    from ._3595 import RingPinsSteadyStateSynchronousResponseAtASpeed
    from ._3596 import RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3597 import RollingRingAssemblySteadyStateSynchronousResponseAtASpeed
    from ._3598 import RollingRingConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3599 import RollingRingSteadyStateSynchronousResponseAtASpeed
    from ._3600 import RootAssemblySteadyStateSynchronousResponseAtASpeed
    from ._3601 import ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3602 import ShaftSteadyStateSynchronousResponseAtASpeed
    from ._3603 import (
        ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3604 import SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed
    from ._3605 import SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3606 import SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3607 import SpiralBevelGearSteadyStateSynchronousResponseAtASpeed
    from ._3608 import SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3609 import SpringDamperHalfSteadyStateSynchronousResponseAtASpeed
    from ._3610 import SpringDamperSteadyStateSynchronousResponseAtASpeed
    from ._3611 import SteadyStateSynchronousResponseAtASpeed
    from ._3612 import StraightBevelDiffGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3613 import StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3614 import StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed
    from ._3615 import StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3616 import StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3617 import StraightBevelGearSteadyStateSynchronousResponseAtASpeed
    from ._3618 import StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed
    from ._3619 import StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed
    from ._3620 import SynchroniserHalfSteadyStateSynchronousResponseAtASpeed
    from ._3621 import SynchroniserPartSteadyStateSynchronousResponseAtASpeed
    from ._3622 import SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed
    from ._3623 import SynchroniserSteadyStateSynchronousResponseAtASpeed
    from ._3624 import TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed
    from ._3625 import TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed
    from ._3626 import TorqueConverterSteadyStateSynchronousResponseAtASpeed
    from ._3627 import TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed
    from ._3628 import UnbalancedMassSteadyStateSynchronousResponseAtASpeed
    from ._3629 import VirtualComponentSteadyStateSynchronousResponseAtASpeed
    from ._3630 import WormGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3631 import WormGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3632 import WormGearSteadyStateSynchronousResponseAtASpeed
    from ._3633 import ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed
    from ._3634 import ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed
    from ._3635 import ZerolBevelGearSteadyStateSynchronousResponseAtASpeed
else:
    import_structure = {
        "_3506": ["AbstractAssemblySteadyStateSynchronousResponseAtASpeed"],
        "_3507": ["AbstractShaftOrHousingSteadyStateSynchronousResponseAtASpeed"],
        "_3508": ["AbstractShaftSteadyStateSynchronousResponseAtASpeed"],
        "_3509": [
            "AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3510": ["AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3511": ["AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3512": ["AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed"],
        "_3513": ["AssemblySteadyStateSynchronousResponseAtASpeed"],
        "_3514": ["BearingSteadyStateSynchronousResponseAtASpeed"],
        "_3515": ["BeltConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3516": ["BeltDriveSteadyStateSynchronousResponseAtASpeed"],
        "_3517": ["BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3518": ["BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3519": ["BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed"],
        "_3520": ["BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed"],
        "_3521": ["BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed"],
        "_3522": ["BevelGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3523": ["BevelGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3524": ["BevelGearSteadyStateSynchronousResponseAtASpeed"],
        "_3525": ["BoltedJointSteadyStateSynchronousResponseAtASpeed"],
        "_3526": ["BoltSteadyStateSynchronousResponseAtASpeed"],
        "_3527": ["ClutchConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3528": ["ClutchHalfSteadyStateSynchronousResponseAtASpeed"],
        "_3529": ["ClutchSteadyStateSynchronousResponseAtASpeed"],
        "_3530": ["CoaxialConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3531": ["ComponentSteadyStateSynchronousResponseAtASpeed"],
        "_3532": ["ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3533": ["ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed"],
        "_3534": ["ConceptCouplingSteadyStateSynchronousResponseAtASpeed"],
        "_3535": ["ConceptGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3536": ["ConceptGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3537": ["ConceptGearSteadyStateSynchronousResponseAtASpeed"],
        "_3538": ["ConicalGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3539": ["ConicalGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3540": ["ConicalGearSteadyStateSynchronousResponseAtASpeed"],
        "_3541": ["ConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3542": ["ConnectorSteadyStateSynchronousResponseAtASpeed"],
        "_3543": ["CouplingConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3544": ["CouplingHalfSteadyStateSynchronousResponseAtASpeed"],
        "_3545": ["CouplingSteadyStateSynchronousResponseAtASpeed"],
        "_3546": ["CVTBeltConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3547": ["CVTPulleySteadyStateSynchronousResponseAtASpeed"],
        "_3548": ["CVTSteadyStateSynchronousResponseAtASpeed"],
        "_3549": ["CycloidalAssemblySteadyStateSynchronousResponseAtASpeed"],
        "_3550": [
            "CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3551": [
            "CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3552": ["CycloidalDiscSteadyStateSynchronousResponseAtASpeed"],
        "_3553": ["CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3554": ["CylindricalGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3555": ["CylindricalGearSteadyStateSynchronousResponseAtASpeed"],
        "_3556": ["CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed"],
        "_3557": ["DatumSteadyStateSynchronousResponseAtASpeed"],
        "_3558": ["ExternalCADModelSteadyStateSynchronousResponseAtASpeed"],
        "_3559": ["FaceGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3560": ["FaceGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3561": ["FaceGearSteadyStateSynchronousResponseAtASpeed"],
        "_3562": ["FEPartSteadyStateSynchronousResponseAtASpeed"],
        "_3563": ["FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed"],
        "_3564": ["GearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3565": ["GearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3566": ["GearSteadyStateSynchronousResponseAtASpeed"],
        "_3567": ["GuideDxfModelSteadyStateSynchronousResponseAtASpeed"],
        "_3568": ["HypoidGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3569": ["HypoidGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3570": ["HypoidGearSteadyStateSynchronousResponseAtASpeed"],
        "_3571": [
            "InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3572": [
            "KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3573": [
            "KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3574": [
            "KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3575": [
            "KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3576": [
            "KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3577": [
            "KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3578": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3579": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3580": [
            "KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3581": ["MassDiscSteadyStateSynchronousResponseAtASpeed"],
        "_3582": ["MeasurementComponentSteadyStateSynchronousResponseAtASpeed"],
        "_3583": ["MountableComponentSteadyStateSynchronousResponseAtASpeed"],
        "_3584": ["OilSealSteadyStateSynchronousResponseAtASpeed"],
        "_3585": ["PartSteadyStateSynchronousResponseAtASpeed"],
        "_3586": [
            "PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3587": ["PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed"],
        "_3588": ["PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed"],
        "_3589": ["PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3590": ["PlanetaryGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3591": ["PlanetCarrierSteadyStateSynchronousResponseAtASpeed"],
        "_3592": ["PointLoadSteadyStateSynchronousResponseAtASpeed"],
        "_3593": ["PowerLoadSteadyStateSynchronousResponseAtASpeed"],
        "_3594": ["PulleySteadyStateSynchronousResponseAtASpeed"],
        "_3595": ["RingPinsSteadyStateSynchronousResponseAtASpeed"],
        "_3596": ["RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3597": ["RollingRingAssemblySteadyStateSynchronousResponseAtASpeed"],
        "_3598": ["RollingRingConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3599": ["RollingRingSteadyStateSynchronousResponseAtASpeed"],
        "_3600": ["RootAssemblySteadyStateSynchronousResponseAtASpeed"],
        "_3601": ["ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3602": ["ShaftSteadyStateSynchronousResponseAtASpeed"],
        "_3603": [
            "ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3604": ["SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed"],
        "_3605": ["SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3606": ["SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3607": ["SpiralBevelGearSteadyStateSynchronousResponseAtASpeed"],
        "_3608": ["SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3609": ["SpringDamperHalfSteadyStateSynchronousResponseAtASpeed"],
        "_3610": ["SpringDamperSteadyStateSynchronousResponseAtASpeed"],
        "_3611": ["SteadyStateSynchronousResponseAtASpeed"],
        "_3612": ["StraightBevelDiffGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3613": ["StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3614": ["StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed"],
        "_3615": ["StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3616": ["StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3617": ["StraightBevelGearSteadyStateSynchronousResponseAtASpeed"],
        "_3618": ["StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed"],
        "_3619": ["StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed"],
        "_3620": ["SynchroniserHalfSteadyStateSynchronousResponseAtASpeed"],
        "_3621": ["SynchroniserPartSteadyStateSynchronousResponseAtASpeed"],
        "_3622": ["SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed"],
        "_3623": ["SynchroniserSteadyStateSynchronousResponseAtASpeed"],
        "_3624": ["TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed"],
        "_3625": ["TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed"],
        "_3626": ["TorqueConverterSteadyStateSynchronousResponseAtASpeed"],
        "_3627": ["TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed"],
        "_3628": ["UnbalancedMassSteadyStateSynchronousResponseAtASpeed"],
        "_3629": ["VirtualComponentSteadyStateSynchronousResponseAtASpeed"],
        "_3630": ["WormGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3631": ["WormGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3632": ["WormGearSteadyStateSynchronousResponseAtASpeed"],
        "_3633": ["ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed"],
        "_3634": ["ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed"],
        "_3635": ["ZerolBevelGearSteadyStateSynchronousResponseAtASpeed"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblySteadyStateSynchronousResponseAtASpeed",
    "AbstractShaftOrHousingSteadyStateSynchronousResponseAtASpeed",
    "AbstractShaftSteadyStateSynchronousResponseAtASpeed",
    "AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed",
    "AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseAtASpeed",
    "AGMAGleasonConicalGearSetSteadyStateSynchronousResponseAtASpeed",
    "AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed",
    "AssemblySteadyStateSynchronousResponseAtASpeed",
    "BearingSteadyStateSynchronousResponseAtASpeed",
    "BeltConnectionSteadyStateSynchronousResponseAtASpeed",
    "BeltDriveSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialGearMeshSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed",
    "BevelGearMeshSteadyStateSynchronousResponseAtASpeed",
    "BevelGearSetSteadyStateSynchronousResponseAtASpeed",
    "BevelGearSteadyStateSynchronousResponseAtASpeed",
    "BoltedJointSteadyStateSynchronousResponseAtASpeed",
    "BoltSteadyStateSynchronousResponseAtASpeed",
    "ClutchConnectionSteadyStateSynchronousResponseAtASpeed",
    "ClutchHalfSteadyStateSynchronousResponseAtASpeed",
    "ClutchSteadyStateSynchronousResponseAtASpeed",
    "CoaxialConnectionSteadyStateSynchronousResponseAtASpeed",
    "ComponentSteadyStateSynchronousResponseAtASpeed",
    "ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed",
    "ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed",
    "ConceptCouplingSteadyStateSynchronousResponseAtASpeed",
    "ConceptGearMeshSteadyStateSynchronousResponseAtASpeed",
    "ConceptGearSetSteadyStateSynchronousResponseAtASpeed",
    "ConceptGearSteadyStateSynchronousResponseAtASpeed",
    "ConicalGearMeshSteadyStateSynchronousResponseAtASpeed",
    "ConicalGearSetSteadyStateSynchronousResponseAtASpeed",
    "ConicalGearSteadyStateSynchronousResponseAtASpeed",
    "ConnectionSteadyStateSynchronousResponseAtASpeed",
    "ConnectorSteadyStateSynchronousResponseAtASpeed",
    "CouplingConnectionSteadyStateSynchronousResponseAtASpeed",
    "CouplingHalfSteadyStateSynchronousResponseAtASpeed",
    "CouplingSteadyStateSynchronousResponseAtASpeed",
    "CVTBeltConnectionSteadyStateSynchronousResponseAtASpeed",
    "CVTPulleySteadyStateSynchronousResponseAtASpeed",
    "CVTSteadyStateSynchronousResponseAtASpeed",
    "CycloidalAssemblySteadyStateSynchronousResponseAtASpeed",
    "CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed",
    "CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseAtASpeed",
    "CycloidalDiscSteadyStateSynchronousResponseAtASpeed",
    "CylindricalGearMeshSteadyStateSynchronousResponseAtASpeed",
    "CylindricalGearSetSteadyStateSynchronousResponseAtASpeed",
    "CylindricalGearSteadyStateSynchronousResponseAtASpeed",
    "CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed",
    "DatumSteadyStateSynchronousResponseAtASpeed",
    "ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
    "FaceGearMeshSteadyStateSynchronousResponseAtASpeed",
    "FaceGearSetSteadyStateSynchronousResponseAtASpeed",
    "FaceGearSteadyStateSynchronousResponseAtASpeed",
    "FEPartSteadyStateSynchronousResponseAtASpeed",
    "FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed",
    "GearMeshSteadyStateSynchronousResponseAtASpeed",
    "GearSetSteadyStateSynchronousResponseAtASpeed",
    "GearSteadyStateSynchronousResponseAtASpeed",
    "GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
    "HypoidGearMeshSteadyStateSynchronousResponseAtASpeed",
    "HypoidGearSetSteadyStateSynchronousResponseAtASpeed",
    "HypoidGearSteadyStateSynchronousResponseAtASpeed",
    "InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed",
    "MassDiscSteadyStateSynchronousResponseAtASpeed",
    "MeasurementComponentSteadyStateSynchronousResponseAtASpeed",
    "MountableComponentSteadyStateSynchronousResponseAtASpeed",
    "OilSealSteadyStateSynchronousResponseAtASpeed",
    "PartSteadyStateSynchronousResponseAtASpeed",
    "PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed",
    "PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed",
    "PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed",
    "PlanetaryConnectionSteadyStateSynchronousResponseAtASpeed",
    "PlanetaryGearSetSteadyStateSynchronousResponseAtASpeed",
    "PlanetCarrierSteadyStateSynchronousResponseAtASpeed",
    "PointLoadSteadyStateSynchronousResponseAtASpeed",
    "PowerLoadSteadyStateSynchronousResponseAtASpeed",
    "PulleySteadyStateSynchronousResponseAtASpeed",
    "RingPinsSteadyStateSynchronousResponseAtASpeed",
    "RingPinsToDiscConnectionSteadyStateSynchronousResponseAtASpeed",
    "RollingRingAssemblySteadyStateSynchronousResponseAtASpeed",
    "RollingRingConnectionSteadyStateSynchronousResponseAtASpeed",
    "RollingRingSteadyStateSynchronousResponseAtASpeed",
    "RootAssemblySteadyStateSynchronousResponseAtASpeed",
    "ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed",
    "ShaftSteadyStateSynchronousResponseAtASpeed",
    "ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed",
    "SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed",
    "SpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed",
    "SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed",
    "SpiralBevelGearSteadyStateSynchronousResponseAtASpeed",
    "SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed",
    "SpringDamperHalfSteadyStateSynchronousResponseAtASpeed",
    "SpringDamperSteadyStateSynchronousResponseAtASpeed",
    "SteadyStateSynchronousResponseAtASpeed",
    "StraightBevelDiffGearMeshSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelGearMeshSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelGearSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed",
    "SynchroniserHalfSteadyStateSynchronousResponseAtASpeed",
    "SynchroniserPartSteadyStateSynchronousResponseAtASpeed",
    "SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed",
    "SynchroniserSteadyStateSynchronousResponseAtASpeed",
    "TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed",
    "TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed",
    "TorqueConverterSteadyStateSynchronousResponseAtASpeed",
    "TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed",
    "UnbalancedMassSteadyStateSynchronousResponseAtASpeed",
    "VirtualComponentSteadyStateSynchronousResponseAtASpeed",
    "WormGearMeshSteadyStateSynchronousResponseAtASpeed",
    "WormGearSetSteadyStateSynchronousResponseAtASpeed",
    "WormGearSteadyStateSynchronousResponseAtASpeed",
    "ZerolBevelGearMeshSteadyStateSynchronousResponseAtASpeed",
    "ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed",
    "ZerolBevelGearSteadyStateSynchronousResponseAtASpeed",
)
