"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._3636 import AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3637 import AbstractShaftCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3638 import (
        AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3639 import (
        AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3640 import (
        AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3641 import (
        AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3642 import (
        AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3643 import AssemblyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3644 import BearingCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3645 import BeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3646 import BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3647 import (
        BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3648 import (
        BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3649 import (
        BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3650 import (
        BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3651 import (
        BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3652 import BevelGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3653 import BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3654 import BevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3655 import BoltCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3656 import BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3657 import ClutchCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3658 import ClutchConnectionCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3659 import ClutchHalfCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3660 import CoaxialConnectionCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3661 import ComponentCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3662 import ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3663 import (
        ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3664 import ConceptCouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3665 import ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3666 import ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3667 import ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3668 import ConicalGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3669 import ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3670 import ConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3671 import ConnectionCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3672 import ConnectorCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3673 import CouplingCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3674 import CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3675 import CouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3676 import CVTBeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3677 import CVTCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3678 import CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3679 import CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3680 import (
        CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3681 import CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3682 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3683 import CylindricalGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3684 import CylindricalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3685 import CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3686 import (
        CylindricalPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3687 import DatumCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3688 import ExternalCADModelCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3689 import FaceGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3690 import FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3691 import FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3692 import FEPartCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3693 import FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3694 import GearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3695 import GearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3696 import GearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3697 import GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3698 import HypoidGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3699 import HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3700 import HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3701 import (
        InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3702 import (
        KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3703 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3704 import (
        KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3705 import (
        KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3706 import (
        KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3707 import (
        KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3708 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3709 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3710 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3711 import MassDiscCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3712 import (
        MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3713 import MountableComponentCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3714 import OilSealCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3715 import PartCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3716 import (
        PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3717 import (
        PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3718 import (
        PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3719 import PlanetaryConnectionCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3720 import PlanetaryGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3721 import PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3722 import PointLoadCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3723 import PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3724 import PulleyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3725 import RingPinsCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3726 import (
        RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3727 import RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3728 import RollingRingCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3729 import (
        RollingRingConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3730 import RootAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3731 import ShaftCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3732 import ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3733 import (
        ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3734 import SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3735 import SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3736 import SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3737 import SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3738 import SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3739 import (
        SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3740 import SpringDamperHalfCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3741 import (
        StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3742 import (
        StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3743 import (
        StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3744 import StraightBevelGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3745 import (
        StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3746 import (
        StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3747 import (
        StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3748 import (
        StraightBevelSunGearCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3749 import SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3750 import SynchroniserHalfCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3751 import SynchroniserPartCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3752 import SynchroniserSleeveCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3753 import TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3754 import (
        TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3755 import TorqueConverterPumpCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3756 import (
        TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from ._3757 import UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3758 import VirtualComponentCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3759 import WormGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3760 import WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3761 import WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3762 import ZerolBevelGearCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3763 import ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
    from ._3764 import ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed
else:
    import_structure = {
        "_3636": ["AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3637": ["AbstractShaftCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3638": [
            "AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3639": [
            "AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3640": [
            "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3641": [
            "AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3642": [
            "AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3643": ["AssemblyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3644": ["BearingCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3645": ["BeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3646": ["BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3647": [
            "BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3648": [
            "BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3649": [
            "BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3650": [
            "BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3651": [
            "BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3652": ["BevelGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3653": ["BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3654": ["BevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3655": ["BoltCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3656": ["BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3657": ["ClutchCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3658": ["ClutchConnectionCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3659": ["ClutchHalfCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3660": ["CoaxialConnectionCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3661": ["ComponentCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3662": ["ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3663": [
            "ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3664": ["ConceptCouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3665": ["ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3666": ["ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3667": ["ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3668": ["ConicalGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3669": ["ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3670": ["ConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3671": ["ConnectionCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3672": ["ConnectorCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3673": ["CouplingCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3674": ["CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3675": ["CouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3676": ["CVTBeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3677": ["CVTCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3678": ["CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3679": ["CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3680": [
            "CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3681": ["CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3682": [
            "CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3683": ["CylindricalGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3684": ["CylindricalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3685": ["CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3686": [
            "CylindricalPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3687": ["DatumCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3688": ["ExternalCADModelCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3689": ["FaceGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3690": ["FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3691": ["FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3692": ["FEPartCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3693": ["FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3694": ["GearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3695": ["GearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3696": ["GearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3697": ["GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3698": ["HypoidGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3699": ["HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3700": ["HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3701": [
            "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3702": [
            "KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3703": [
            "KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3704": [
            "KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3705": [
            "KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3706": [
            "KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3707": [
            "KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3708": [
            "KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3709": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3710": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3711": ["MassDiscCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3712": ["MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3713": ["MountableComponentCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3714": ["OilSealCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3715": ["PartCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3716": [
            "PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3717": [
            "PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3718": [
            "PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3719": ["PlanetaryConnectionCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3720": ["PlanetaryGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3721": ["PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3722": ["PointLoadCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3723": ["PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3724": ["PulleyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3725": ["RingPinsCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3726": [
            "RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3727": ["RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3728": ["RollingRingCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3729": [
            "RollingRingConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3730": ["RootAssemblyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3731": ["ShaftCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3732": ["ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3733": [
            "ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3734": ["SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3735": ["SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3736": ["SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3737": ["SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3738": ["SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3739": [
            "SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3740": ["SpringDamperHalfCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3741": [
            "StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3742": [
            "StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3743": [
            "StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3744": ["StraightBevelGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3745": [
            "StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3746": ["StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3747": [
            "StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3748": ["StraightBevelSunGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3749": ["SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3750": ["SynchroniserHalfCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3751": ["SynchroniserPartCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3752": ["SynchroniserSleeveCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3753": ["TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3754": [
            "TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3755": ["TorqueConverterPumpCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3756": [
            "TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_3757": ["UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3758": ["VirtualComponentCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3759": ["WormGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3760": ["WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3761": ["WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3762": ["ZerolBevelGearCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3763": ["ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"],
        "_3764": ["ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    "AbstractShaftCompoundSteadyStateSynchronousResponseAtASpeed",
    "AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseAtASpeed",
    "AbstractShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "AssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    "BearingCompoundSteadyStateSynchronousResponseAtASpeed",
    "BeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "BevelGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "BevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "BoltCompoundSteadyStateSynchronousResponseAtASpeed",
    "BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed",
    "ClutchCompoundSteadyStateSynchronousResponseAtASpeed",
    "ClutchConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "ClutchHalfCompoundSteadyStateSynchronousResponseAtASpeed",
    "CoaxialConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "ComponentCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConceptCouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConceptGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "ConnectorCompoundSteadyStateSynchronousResponseAtASpeed",
    "CouplingCompoundSteadyStateSynchronousResponseAtASpeed",
    "CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "CouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed",
    "CVTBeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "CVTCompoundSteadyStateSynchronousResponseAtASpeed",
    "CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed",
    "CycloidalAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    "CycloidalDiscCentralBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "CycloidalDiscCompoundSteadyStateSynchronousResponseAtASpeed",
    "CycloidalDiscPlanetaryBearingConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "CylindricalGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "CylindricalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "CylindricalPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "DatumCompoundSteadyStateSynchronousResponseAtASpeed",
    "ExternalCADModelCompoundSteadyStateSynchronousResponseAtASpeed",
    "FaceGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "FEPartCompoundSteadyStateSynchronousResponseAtASpeed",
    "FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    "GearCompoundSteadyStateSynchronousResponseAtASpeed",
    "GearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "GearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "GuideDxfModelCompoundSteadyStateSynchronousResponseAtASpeed",
    "HypoidGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "MassDiscCompoundSteadyStateSynchronousResponseAtASpeed",
    "MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed",
    "MountableComponentCompoundSteadyStateSynchronousResponseAtASpeed",
    "OilSealCompoundSteadyStateSynchronousResponseAtASpeed",
    "PartCompoundSteadyStateSynchronousResponseAtASpeed",
    "PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed",
    "PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "PartToPartShearCouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed",
    "PlanetaryConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "PlanetaryGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed",
    "PointLoadCompoundSteadyStateSynchronousResponseAtASpeed",
    "PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed",
    "PulleyCompoundSteadyStateSynchronousResponseAtASpeed",
    "RingPinsCompoundSteadyStateSynchronousResponseAtASpeed",
    "RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    "RollingRingCompoundSteadyStateSynchronousResponseAtASpeed",
    "RollingRingConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "RootAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    "ShaftCompoundSteadyStateSynchronousResponseAtASpeed",
    "ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "ShaftToMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed",
    "SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed",
    "SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "SpringDamperHalfCompoundSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "StraightBevelSunGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed",
    "SynchroniserHalfCompoundSteadyStateSynchronousResponseAtASpeed",
    "SynchroniserPartCompoundSteadyStateSynchronousResponseAtASpeed",
    "SynchroniserSleeveCompoundSteadyStateSynchronousResponseAtASpeed",
    "TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed",
    "TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    "TorqueConverterPumpCompoundSteadyStateSynchronousResponseAtASpeed",
    "TorqueConverterTurbineCompoundSteadyStateSynchronousResponseAtASpeed",
    "UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed",
    "VirtualComponentCompoundSteadyStateSynchronousResponseAtASpeed",
    "WormGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    "ZerolBevelGearCompoundSteadyStateSynchronousResponseAtASpeed",
    "ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed",
    "ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
)
