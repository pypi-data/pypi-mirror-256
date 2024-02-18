"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._3377 import AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3378 import AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3379 import (
        AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3380 import (
        AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3381 import (
        AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3382 import (
        AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3383 import (
        AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3384 import AssemblyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3385 import BearingCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3386 import BeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3387 import BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3388 import (
        BevelDifferentialGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3389 import (
        BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3390 import (
        BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3391 import (
        BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3392 import (
        BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3393 import BevelGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3394 import BevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3395 import BevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3396 import BoltCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3397 import BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3398 import ClutchCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3399 import ClutchConnectionCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3400 import ClutchHalfCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3401 import CoaxialConnectionCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3402 import ComponentCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3403 import ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3404 import (
        ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3405 import ConceptCouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3406 import ConceptGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3407 import ConceptGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3408 import ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3409 import ConicalGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3410 import ConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3411 import ConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3412 import ConnectionCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3413 import ConnectorCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3414 import CouplingCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3415 import CouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3416 import CouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3417 import CVTBeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3418 import CVTCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3419 import CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3420 import CycloidalAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3421 import (
        CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3422 import CycloidalDiscCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3423 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3424 import CylindricalGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3425 import CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3426 import CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3427 import (
        CylindricalPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3428 import DatumCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3429 import ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3430 import FaceGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3431 import FaceGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3432 import FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3433 import FEPartCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3434 import FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3435 import GearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3436 import GearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3437 import GearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3438 import GuideDxfModelCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3439 import HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3440 import HypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3441 import HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3442 import (
        InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3443 import (
        KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3444 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3445 import (
        KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3446 import (
        KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3447 import (
        KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3448 import (
        KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3449 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3450 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3451 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3452 import MassDiscCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3453 import (
        MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3454 import MountableComponentCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3455 import OilSealCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3456 import PartCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3457 import (
        PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3458 import (
        PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3459 import (
        PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3460 import PlanetaryConnectionCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3461 import PlanetaryGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3462 import PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3463 import PointLoadCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3464 import PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3465 import PulleyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3466 import RingPinsCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3467 import (
        RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3468 import RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3469 import RollingRingCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3470 import (
        RollingRingConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3471 import RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3472 import ShaftCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3473 import ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3474 import (
        ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3475 import SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3476 import SpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3477 import SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3478 import SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3479 import SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3480 import (
        SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3481 import SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3482 import (
        StraightBevelDiffGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3483 import (
        StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3484 import (
        StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3485 import StraightBevelGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3486 import (
        StraightBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3487 import (
        StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3488 import (
        StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3489 import (
        StraightBevelSunGearCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3490 import SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3491 import SynchroniserHalfCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3492 import SynchroniserPartCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3493 import SynchroniserSleeveCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3494 import TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3495 import (
        TorqueConverterConnectionCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3496 import TorqueConverterPumpCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3497 import (
        TorqueConverterTurbineCompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from ._3498 import UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3499 import VirtualComponentCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3500 import WormGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3501 import WormGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3502 import WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3503 import ZerolBevelGearCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3504 import ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft
    from ._3505 import ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft
else:
    import_structure = {
        "_3377": ["AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3378": ["AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3379": [
            "AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3380": [
            "AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3381": [
            "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3382": [
            "AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3383": [
            "AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3384": ["AssemblyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3385": ["BearingCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3386": ["BeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3387": ["BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3388": [
            "BevelDifferentialGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3389": [
            "BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3390": [
            "BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3391": [
            "BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3392": [
            "BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3393": ["BevelGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3394": ["BevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3395": ["BevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3396": ["BoltCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3397": ["BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3398": ["ClutchCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3399": ["ClutchConnectionCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3400": ["ClutchHalfCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3401": ["CoaxialConnectionCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3402": ["ComponentCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3403": ["ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3404": [
            "ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3405": ["ConceptCouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3406": ["ConceptGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3407": ["ConceptGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3408": ["ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3409": ["ConicalGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3410": ["ConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3411": ["ConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3412": ["ConnectionCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3413": ["ConnectorCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3414": ["CouplingCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3415": ["CouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3416": ["CouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3417": ["CVTBeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3418": ["CVTCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3419": ["CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3420": ["CycloidalAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3421": [
            "CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3422": ["CycloidalDiscCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3423": [
            "CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3424": ["CylindricalGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3425": ["CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3426": ["CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3427": [
            "CylindricalPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3428": ["DatumCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3429": ["ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3430": ["FaceGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3431": ["FaceGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3432": ["FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3433": ["FEPartCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3434": ["FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3435": ["GearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3436": ["GearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3437": ["GearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3438": ["GuideDxfModelCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3439": ["HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3440": ["HypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3441": ["HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3442": [
            "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3443": [
            "KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3444": [
            "KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3445": [
            "KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3446": [
            "KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3447": [
            "KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3448": [
            "KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3449": [
            "KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3450": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3451": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3452": ["MassDiscCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3453": ["MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3454": ["MountableComponentCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3455": ["OilSealCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3456": ["PartCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3457": [
            "PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3458": [
            "PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3459": [
            "PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3460": ["PlanetaryConnectionCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3461": ["PlanetaryGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3462": ["PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3463": ["PointLoadCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3464": ["PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3465": ["PulleyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3466": ["RingPinsCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3467": [
            "RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3468": ["RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3469": ["RollingRingCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3470": [
            "RollingRingConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3471": ["RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3472": ["ShaftCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3473": ["ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3474": [
            "ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3475": ["SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3476": ["SpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3477": ["SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3478": ["SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3479": ["SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3480": [
            "SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3481": ["SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3482": [
            "StraightBevelDiffGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3483": [
            "StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3484": [
            "StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3485": ["StraightBevelGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3486": [
            "StraightBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3487": ["StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3488": [
            "StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3489": ["StraightBevelSunGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3490": ["SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3491": ["SynchroniserHalfCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3492": ["SynchroniserPartCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3493": ["SynchroniserSleeveCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3494": ["TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3495": [
            "TorqueConverterConnectionCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3496": ["TorqueConverterPumpCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3497": [
            "TorqueConverterTurbineCompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_3498": ["UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3499": ["VirtualComponentCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3500": ["WormGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3501": ["WormGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3502": ["WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3503": ["ZerolBevelGearCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3504": ["ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft"],
        "_3505": ["ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    "AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft",
    "AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseOnAShaft",
    "AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "AssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    "BearingCompoundSteadyStateSynchronousResponseOnAShaft",
    "BeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft",
    "BevelDifferentialGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "BevelGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "BevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "BevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "BoltCompoundSteadyStateSynchronousResponseOnAShaft",
    "BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft",
    "ClutchCompoundSteadyStateSynchronousResponseOnAShaft",
    "ClutchConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "ClutchHalfCompoundSteadyStateSynchronousResponseOnAShaft",
    "CoaxialConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "ComponentCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConceptCouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConceptGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConceptGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConicalGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "ConnectorCompoundSteadyStateSynchronousResponseOnAShaft",
    "CouplingCompoundSteadyStateSynchronousResponseOnAShaft",
    "CouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "CouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft",
    "CVTBeltConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "CVTCompoundSteadyStateSynchronousResponseOnAShaft",
    "CVTPulleyCompoundSteadyStateSynchronousResponseOnAShaft",
    "CycloidalAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    "CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "CycloidalDiscCompoundSteadyStateSynchronousResponseOnAShaft",
    "CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "CylindricalGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "CylindricalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "CylindricalPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "DatumCompoundSteadyStateSynchronousResponseOnAShaft",
    "ExternalCADModelCompoundSteadyStateSynchronousResponseOnAShaft",
    "FaceGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "FaceGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "FEPartCompoundSteadyStateSynchronousResponseOnAShaft",
    "FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    "GearCompoundSteadyStateSynchronousResponseOnAShaft",
    "GearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "GearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "GuideDxfModelCompoundSteadyStateSynchronousResponseOnAShaft",
    "HypoidGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "HypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "MassDiscCompoundSteadyStateSynchronousResponseOnAShaft",
    "MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft",
    "MountableComponentCompoundSteadyStateSynchronousResponseOnAShaft",
    "OilSealCompoundSteadyStateSynchronousResponseOnAShaft",
    "PartCompoundSteadyStateSynchronousResponseOnAShaft",
    "PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft",
    "PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponseOnAShaft",
    "PlanetaryConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "PlanetaryGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft",
    "PointLoadCompoundSteadyStateSynchronousResponseOnAShaft",
    "PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft",
    "PulleyCompoundSteadyStateSynchronousResponseOnAShaft",
    "RingPinsCompoundSteadyStateSynchronousResponseOnAShaft",
    "RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    "RollingRingCompoundSteadyStateSynchronousResponseOnAShaft",
    "RollingRingConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "RootAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    "ShaftCompoundSteadyStateSynchronousResponseOnAShaft",
    "ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseOnAShaft",
    "SpiralBevelGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft",
    "SpringDamperConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "SpringDamperHalfCompoundSteadyStateSynchronousResponseOnAShaft",
    "StraightBevelDiffGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "StraightBevelGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "StraightBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "StraightBevelSunGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft",
    "SynchroniserHalfCompoundSteadyStateSynchronousResponseOnAShaft",
    "SynchroniserPartCompoundSteadyStateSynchronousResponseOnAShaft",
    "SynchroniserSleeveCompoundSteadyStateSynchronousResponseOnAShaft",
    "TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft",
    "TorqueConverterConnectionCompoundSteadyStateSynchronousResponseOnAShaft",
    "TorqueConverterPumpCompoundSteadyStateSynchronousResponseOnAShaft",
    "TorqueConverterTurbineCompoundSteadyStateSynchronousResponseOnAShaft",
    "UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft",
    "VirtualComponentCompoundSteadyStateSynchronousResponseOnAShaft",
    "WormGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "WormGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
    "ZerolBevelGearCompoundSteadyStateSynchronousResponseOnAShaft",
    "ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseOnAShaft",
    "ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft",
)
