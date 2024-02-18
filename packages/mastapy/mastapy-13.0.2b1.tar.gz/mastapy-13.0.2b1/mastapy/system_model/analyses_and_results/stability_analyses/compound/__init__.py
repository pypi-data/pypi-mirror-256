"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._3899 import AbstractAssemblyCompoundStabilityAnalysis
    from ._3900 import AbstractShaftCompoundStabilityAnalysis
    from ._3901 import AbstractShaftOrHousingCompoundStabilityAnalysis
    from ._3902 import (
        AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis,
    )
    from ._3903 import AGMAGleasonConicalGearCompoundStabilityAnalysis
    from ._3904 import AGMAGleasonConicalGearMeshCompoundStabilityAnalysis
    from ._3905 import AGMAGleasonConicalGearSetCompoundStabilityAnalysis
    from ._3906 import AssemblyCompoundStabilityAnalysis
    from ._3907 import BearingCompoundStabilityAnalysis
    from ._3908 import BeltConnectionCompoundStabilityAnalysis
    from ._3909 import BeltDriveCompoundStabilityAnalysis
    from ._3910 import BevelDifferentialGearCompoundStabilityAnalysis
    from ._3911 import BevelDifferentialGearMeshCompoundStabilityAnalysis
    from ._3912 import BevelDifferentialGearSetCompoundStabilityAnalysis
    from ._3913 import BevelDifferentialPlanetGearCompoundStabilityAnalysis
    from ._3914 import BevelDifferentialSunGearCompoundStabilityAnalysis
    from ._3915 import BevelGearCompoundStabilityAnalysis
    from ._3916 import BevelGearMeshCompoundStabilityAnalysis
    from ._3917 import BevelGearSetCompoundStabilityAnalysis
    from ._3918 import BoltCompoundStabilityAnalysis
    from ._3919 import BoltedJointCompoundStabilityAnalysis
    from ._3920 import ClutchCompoundStabilityAnalysis
    from ._3921 import ClutchConnectionCompoundStabilityAnalysis
    from ._3922 import ClutchHalfCompoundStabilityAnalysis
    from ._3923 import CoaxialConnectionCompoundStabilityAnalysis
    from ._3924 import ComponentCompoundStabilityAnalysis
    from ._3925 import ConceptCouplingCompoundStabilityAnalysis
    from ._3926 import ConceptCouplingConnectionCompoundStabilityAnalysis
    from ._3927 import ConceptCouplingHalfCompoundStabilityAnalysis
    from ._3928 import ConceptGearCompoundStabilityAnalysis
    from ._3929 import ConceptGearMeshCompoundStabilityAnalysis
    from ._3930 import ConceptGearSetCompoundStabilityAnalysis
    from ._3931 import ConicalGearCompoundStabilityAnalysis
    from ._3932 import ConicalGearMeshCompoundStabilityAnalysis
    from ._3933 import ConicalGearSetCompoundStabilityAnalysis
    from ._3934 import ConnectionCompoundStabilityAnalysis
    from ._3935 import ConnectorCompoundStabilityAnalysis
    from ._3936 import CouplingCompoundStabilityAnalysis
    from ._3937 import CouplingConnectionCompoundStabilityAnalysis
    from ._3938 import CouplingHalfCompoundStabilityAnalysis
    from ._3939 import CVTBeltConnectionCompoundStabilityAnalysis
    from ._3940 import CVTCompoundStabilityAnalysis
    from ._3941 import CVTPulleyCompoundStabilityAnalysis
    from ._3942 import CycloidalAssemblyCompoundStabilityAnalysis
    from ._3943 import CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis
    from ._3944 import CycloidalDiscCompoundStabilityAnalysis
    from ._3945 import CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis
    from ._3946 import CylindricalGearCompoundStabilityAnalysis
    from ._3947 import CylindricalGearMeshCompoundStabilityAnalysis
    from ._3948 import CylindricalGearSetCompoundStabilityAnalysis
    from ._3949 import CylindricalPlanetGearCompoundStabilityAnalysis
    from ._3950 import DatumCompoundStabilityAnalysis
    from ._3951 import ExternalCADModelCompoundStabilityAnalysis
    from ._3952 import FaceGearCompoundStabilityAnalysis
    from ._3953 import FaceGearMeshCompoundStabilityAnalysis
    from ._3954 import FaceGearSetCompoundStabilityAnalysis
    from ._3955 import FEPartCompoundStabilityAnalysis
    from ._3956 import FlexiblePinAssemblyCompoundStabilityAnalysis
    from ._3957 import GearCompoundStabilityAnalysis
    from ._3958 import GearMeshCompoundStabilityAnalysis
    from ._3959 import GearSetCompoundStabilityAnalysis
    from ._3960 import GuideDxfModelCompoundStabilityAnalysis
    from ._3961 import HypoidGearCompoundStabilityAnalysis
    from ._3962 import HypoidGearMeshCompoundStabilityAnalysis
    from ._3963 import HypoidGearSetCompoundStabilityAnalysis
    from ._3964 import InterMountableComponentConnectionCompoundStabilityAnalysis
    from ._3965 import KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis
    from ._3966 import KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis
    from ._3967 import KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis
    from ._3968 import KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis
    from ._3969 import KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis
    from ._3970 import KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis
    from ._3971 import KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis
    from ._3972 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis,
    )
    from ._3973 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis,
    )
    from ._3974 import MassDiscCompoundStabilityAnalysis
    from ._3975 import MeasurementComponentCompoundStabilityAnalysis
    from ._3976 import MountableComponentCompoundStabilityAnalysis
    from ._3977 import OilSealCompoundStabilityAnalysis
    from ._3978 import PartCompoundStabilityAnalysis
    from ._3979 import PartToPartShearCouplingCompoundStabilityAnalysis
    from ._3980 import PartToPartShearCouplingConnectionCompoundStabilityAnalysis
    from ._3981 import PartToPartShearCouplingHalfCompoundStabilityAnalysis
    from ._3982 import PlanetaryConnectionCompoundStabilityAnalysis
    from ._3983 import PlanetaryGearSetCompoundStabilityAnalysis
    from ._3984 import PlanetCarrierCompoundStabilityAnalysis
    from ._3985 import PointLoadCompoundStabilityAnalysis
    from ._3986 import PowerLoadCompoundStabilityAnalysis
    from ._3987 import PulleyCompoundStabilityAnalysis
    from ._3988 import RingPinsCompoundStabilityAnalysis
    from ._3989 import RingPinsToDiscConnectionCompoundStabilityAnalysis
    from ._3990 import RollingRingAssemblyCompoundStabilityAnalysis
    from ._3991 import RollingRingCompoundStabilityAnalysis
    from ._3992 import RollingRingConnectionCompoundStabilityAnalysis
    from ._3993 import RootAssemblyCompoundStabilityAnalysis
    from ._3994 import ShaftCompoundStabilityAnalysis
    from ._3995 import ShaftHubConnectionCompoundStabilityAnalysis
    from ._3996 import ShaftToMountableComponentConnectionCompoundStabilityAnalysis
    from ._3997 import SpecialisedAssemblyCompoundStabilityAnalysis
    from ._3998 import SpiralBevelGearCompoundStabilityAnalysis
    from ._3999 import SpiralBevelGearMeshCompoundStabilityAnalysis
    from ._4000 import SpiralBevelGearSetCompoundStabilityAnalysis
    from ._4001 import SpringDamperCompoundStabilityAnalysis
    from ._4002 import SpringDamperConnectionCompoundStabilityAnalysis
    from ._4003 import SpringDamperHalfCompoundStabilityAnalysis
    from ._4004 import StraightBevelDiffGearCompoundStabilityAnalysis
    from ._4005 import StraightBevelDiffGearMeshCompoundStabilityAnalysis
    from ._4006 import StraightBevelDiffGearSetCompoundStabilityAnalysis
    from ._4007 import StraightBevelGearCompoundStabilityAnalysis
    from ._4008 import StraightBevelGearMeshCompoundStabilityAnalysis
    from ._4009 import StraightBevelGearSetCompoundStabilityAnalysis
    from ._4010 import StraightBevelPlanetGearCompoundStabilityAnalysis
    from ._4011 import StraightBevelSunGearCompoundStabilityAnalysis
    from ._4012 import SynchroniserCompoundStabilityAnalysis
    from ._4013 import SynchroniserHalfCompoundStabilityAnalysis
    from ._4014 import SynchroniserPartCompoundStabilityAnalysis
    from ._4015 import SynchroniserSleeveCompoundStabilityAnalysis
    from ._4016 import TorqueConverterCompoundStabilityAnalysis
    from ._4017 import TorqueConverterConnectionCompoundStabilityAnalysis
    from ._4018 import TorqueConverterPumpCompoundStabilityAnalysis
    from ._4019 import TorqueConverterTurbineCompoundStabilityAnalysis
    from ._4020 import UnbalancedMassCompoundStabilityAnalysis
    from ._4021 import VirtualComponentCompoundStabilityAnalysis
    from ._4022 import WormGearCompoundStabilityAnalysis
    from ._4023 import WormGearMeshCompoundStabilityAnalysis
    from ._4024 import WormGearSetCompoundStabilityAnalysis
    from ._4025 import ZerolBevelGearCompoundStabilityAnalysis
    from ._4026 import ZerolBevelGearMeshCompoundStabilityAnalysis
    from ._4027 import ZerolBevelGearSetCompoundStabilityAnalysis
else:
    import_structure = {
        "_3899": ["AbstractAssemblyCompoundStabilityAnalysis"],
        "_3900": ["AbstractShaftCompoundStabilityAnalysis"],
        "_3901": ["AbstractShaftOrHousingCompoundStabilityAnalysis"],
        "_3902": [
            "AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis"
        ],
        "_3903": ["AGMAGleasonConicalGearCompoundStabilityAnalysis"],
        "_3904": ["AGMAGleasonConicalGearMeshCompoundStabilityAnalysis"],
        "_3905": ["AGMAGleasonConicalGearSetCompoundStabilityAnalysis"],
        "_3906": ["AssemblyCompoundStabilityAnalysis"],
        "_3907": ["BearingCompoundStabilityAnalysis"],
        "_3908": ["BeltConnectionCompoundStabilityAnalysis"],
        "_3909": ["BeltDriveCompoundStabilityAnalysis"],
        "_3910": ["BevelDifferentialGearCompoundStabilityAnalysis"],
        "_3911": ["BevelDifferentialGearMeshCompoundStabilityAnalysis"],
        "_3912": ["BevelDifferentialGearSetCompoundStabilityAnalysis"],
        "_3913": ["BevelDifferentialPlanetGearCompoundStabilityAnalysis"],
        "_3914": ["BevelDifferentialSunGearCompoundStabilityAnalysis"],
        "_3915": ["BevelGearCompoundStabilityAnalysis"],
        "_3916": ["BevelGearMeshCompoundStabilityAnalysis"],
        "_3917": ["BevelGearSetCompoundStabilityAnalysis"],
        "_3918": ["BoltCompoundStabilityAnalysis"],
        "_3919": ["BoltedJointCompoundStabilityAnalysis"],
        "_3920": ["ClutchCompoundStabilityAnalysis"],
        "_3921": ["ClutchConnectionCompoundStabilityAnalysis"],
        "_3922": ["ClutchHalfCompoundStabilityAnalysis"],
        "_3923": ["CoaxialConnectionCompoundStabilityAnalysis"],
        "_3924": ["ComponentCompoundStabilityAnalysis"],
        "_3925": ["ConceptCouplingCompoundStabilityAnalysis"],
        "_3926": ["ConceptCouplingConnectionCompoundStabilityAnalysis"],
        "_3927": ["ConceptCouplingHalfCompoundStabilityAnalysis"],
        "_3928": ["ConceptGearCompoundStabilityAnalysis"],
        "_3929": ["ConceptGearMeshCompoundStabilityAnalysis"],
        "_3930": ["ConceptGearSetCompoundStabilityAnalysis"],
        "_3931": ["ConicalGearCompoundStabilityAnalysis"],
        "_3932": ["ConicalGearMeshCompoundStabilityAnalysis"],
        "_3933": ["ConicalGearSetCompoundStabilityAnalysis"],
        "_3934": ["ConnectionCompoundStabilityAnalysis"],
        "_3935": ["ConnectorCompoundStabilityAnalysis"],
        "_3936": ["CouplingCompoundStabilityAnalysis"],
        "_3937": ["CouplingConnectionCompoundStabilityAnalysis"],
        "_3938": ["CouplingHalfCompoundStabilityAnalysis"],
        "_3939": ["CVTBeltConnectionCompoundStabilityAnalysis"],
        "_3940": ["CVTCompoundStabilityAnalysis"],
        "_3941": ["CVTPulleyCompoundStabilityAnalysis"],
        "_3942": ["CycloidalAssemblyCompoundStabilityAnalysis"],
        "_3943": ["CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis"],
        "_3944": ["CycloidalDiscCompoundStabilityAnalysis"],
        "_3945": ["CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis"],
        "_3946": ["CylindricalGearCompoundStabilityAnalysis"],
        "_3947": ["CylindricalGearMeshCompoundStabilityAnalysis"],
        "_3948": ["CylindricalGearSetCompoundStabilityAnalysis"],
        "_3949": ["CylindricalPlanetGearCompoundStabilityAnalysis"],
        "_3950": ["DatumCompoundStabilityAnalysis"],
        "_3951": ["ExternalCADModelCompoundStabilityAnalysis"],
        "_3952": ["FaceGearCompoundStabilityAnalysis"],
        "_3953": ["FaceGearMeshCompoundStabilityAnalysis"],
        "_3954": ["FaceGearSetCompoundStabilityAnalysis"],
        "_3955": ["FEPartCompoundStabilityAnalysis"],
        "_3956": ["FlexiblePinAssemblyCompoundStabilityAnalysis"],
        "_3957": ["GearCompoundStabilityAnalysis"],
        "_3958": ["GearMeshCompoundStabilityAnalysis"],
        "_3959": ["GearSetCompoundStabilityAnalysis"],
        "_3960": ["GuideDxfModelCompoundStabilityAnalysis"],
        "_3961": ["HypoidGearCompoundStabilityAnalysis"],
        "_3962": ["HypoidGearMeshCompoundStabilityAnalysis"],
        "_3963": ["HypoidGearSetCompoundStabilityAnalysis"],
        "_3964": ["InterMountableComponentConnectionCompoundStabilityAnalysis"],
        "_3965": ["KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis"],
        "_3966": ["KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis"],
        "_3967": ["KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis"],
        "_3968": ["KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis"],
        "_3969": ["KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis"],
        "_3970": ["KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis"],
        "_3971": ["KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis"],
        "_3972": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis"
        ],
        "_3973": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis"
        ],
        "_3974": ["MassDiscCompoundStabilityAnalysis"],
        "_3975": ["MeasurementComponentCompoundStabilityAnalysis"],
        "_3976": ["MountableComponentCompoundStabilityAnalysis"],
        "_3977": ["OilSealCompoundStabilityAnalysis"],
        "_3978": ["PartCompoundStabilityAnalysis"],
        "_3979": ["PartToPartShearCouplingCompoundStabilityAnalysis"],
        "_3980": ["PartToPartShearCouplingConnectionCompoundStabilityAnalysis"],
        "_3981": ["PartToPartShearCouplingHalfCompoundStabilityAnalysis"],
        "_3982": ["PlanetaryConnectionCompoundStabilityAnalysis"],
        "_3983": ["PlanetaryGearSetCompoundStabilityAnalysis"],
        "_3984": ["PlanetCarrierCompoundStabilityAnalysis"],
        "_3985": ["PointLoadCompoundStabilityAnalysis"],
        "_3986": ["PowerLoadCompoundStabilityAnalysis"],
        "_3987": ["PulleyCompoundStabilityAnalysis"],
        "_3988": ["RingPinsCompoundStabilityAnalysis"],
        "_3989": ["RingPinsToDiscConnectionCompoundStabilityAnalysis"],
        "_3990": ["RollingRingAssemblyCompoundStabilityAnalysis"],
        "_3991": ["RollingRingCompoundStabilityAnalysis"],
        "_3992": ["RollingRingConnectionCompoundStabilityAnalysis"],
        "_3993": ["RootAssemblyCompoundStabilityAnalysis"],
        "_3994": ["ShaftCompoundStabilityAnalysis"],
        "_3995": ["ShaftHubConnectionCompoundStabilityAnalysis"],
        "_3996": ["ShaftToMountableComponentConnectionCompoundStabilityAnalysis"],
        "_3997": ["SpecialisedAssemblyCompoundStabilityAnalysis"],
        "_3998": ["SpiralBevelGearCompoundStabilityAnalysis"],
        "_3999": ["SpiralBevelGearMeshCompoundStabilityAnalysis"],
        "_4000": ["SpiralBevelGearSetCompoundStabilityAnalysis"],
        "_4001": ["SpringDamperCompoundStabilityAnalysis"],
        "_4002": ["SpringDamperConnectionCompoundStabilityAnalysis"],
        "_4003": ["SpringDamperHalfCompoundStabilityAnalysis"],
        "_4004": ["StraightBevelDiffGearCompoundStabilityAnalysis"],
        "_4005": ["StraightBevelDiffGearMeshCompoundStabilityAnalysis"],
        "_4006": ["StraightBevelDiffGearSetCompoundStabilityAnalysis"],
        "_4007": ["StraightBevelGearCompoundStabilityAnalysis"],
        "_4008": ["StraightBevelGearMeshCompoundStabilityAnalysis"],
        "_4009": ["StraightBevelGearSetCompoundStabilityAnalysis"],
        "_4010": ["StraightBevelPlanetGearCompoundStabilityAnalysis"],
        "_4011": ["StraightBevelSunGearCompoundStabilityAnalysis"],
        "_4012": ["SynchroniserCompoundStabilityAnalysis"],
        "_4013": ["SynchroniserHalfCompoundStabilityAnalysis"],
        "_4014": ["SynchroniserPartCompoundStabilityAnalysis"],
        "_4015": ["SynchroniserSleeveCompoundStabilityAnalysis"],
        "_4016": ["TorqueConverterCompoundStabilityAnalysis"],
        "_4017": ["TorqueConverterConnectionCompoundStabilityAnalysis"],
        "_4018": ["TorqueConverterPumpCompoundStabilityAnalysis"],
        "_4019": ["TorqueConverterTurbineCompoundStabilityAnalysis"],
        "_4020": ["UnbalancedMassCompoundStabilityAnalysis"],
        "_4021": ["VirtualComponentCompoundStabilityAnalysis"],
        "_4022": ["WormGearCompoundStabilityAnalysis"],
        "_4023": ["WormGearMeshCompoundStabilityAnalysis"],
        "_4024": ["WormGearSetCompoundStabilityAnalysis"],
        "_4025": ["ZerolBevelGearCompoundStabilityAnalysis"],
        "_4026": ["ZerolBevelGearMeshCompoundStabilityAnalysis"],
        "_4027": ["ZerolBevelGearSetCompoundStabilityAnalysis"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundStabilityAnalysis",
    "AbstractShaftCompoundStabilityAnalysis",
    "AbstractShaftOrHousingCompoundStabilityAnalysis",
    "AbstractShaftToMountableComponentConnectionCompoundStabilityAnalysis",
    "AGMAGleasonConicalGearCompoundStabilityAnalysis",
    "AGMAGleasonConicalGearMeshCompoundStabilityAnalysis",
    "AGMAGleasonConicalGearSetCompoundStabilityAnalysis",
    "AssemblyCompoundStabilityAnalysis",
    "BearingCompoundStabilityAnalysis",
    "BeltConnectionCompoundStabilityAnalysis",
    "BeltDriveCompoundStabilityAnalysis",
    "BevelDifferentialGearCompoundStabilityAnalysis",
    "BevelDifferentialGearMeshCompoundStabilityAnalysis",
    "BevelDifferentialGearSetCompoundStabilityAnalysis",
    "BevelDifferentialPlanetGearCompoundStabilityAnalysis",
    "BevelDifferentialSunGearCompoundStabilityAnalysis",
    "BevelGearCompoundStabilityAnalysis",
    "BevelGearMeshCompoundStabilityAnalysis",
    "BevelGearSetCompoundStabilityAnalysis",
    "BoltCompoundStabilityAnalysis",
    "BoltedJointCompoundStabilityAnalysis",
    "ClutchCompoundStabilityAnalysis",
    "ClutchConnectionCompoundStabilityAnalysis",
    "ClutchHalfCompoundStabilityAnalysis",
    "CoaxialConnectionCompoundStabilityAnalysis",
    "ComponentCompoundStabilityAnalysis",
    "ConceptCouplingCompoundStabilityAnalysis",
    "ConceptCouplingConnectionCompoundStabilityAnalysis",
    "ConceptCouplingHalfCompoundStabilityAnalysis",
    "ConceptGearCompoundStabilityAnalysis",
    "ConceptGearMeshCompoundStabilityAnalysis",
    "ConceptGearSetCompoundStabilityAnalysis",
    "ConicalGearCompoundStabilityAnalysis",
    "ConicalGearMeshCompoundStabilityAnalysis",
    "ConicalGearSetCompoundStabilityAnalysis",
    "ConnectionCompoundStabilityAnalysis",
    "ConnectorCompoundStabilityAnalysis",
    "CouplingCompoundStabilityAnalysis",
    "CouplingConnectionCompoundStabilityAnalysis",
    "CouplingHalfCompoundStabilityAnalysis",
    "CVTBeltConnectionCompoundStabilityAnalysis",
    "CVTCompoundStabilityAnalysis",
    "CVTPulleyCompoundStabilityAnalysis",
    "CycloidalAssemblyCompoundStabilityAnalysis",
    "CycloidalDiscCentralBearingConnectionCompoundStabilityAnalysis",
    "CycloidalDiscCompoundStabilityAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionCompoundStabilityAnalysis",
    "CylindricalGearCompoundStabilityAnalysis",
    "CylindricalGearMeshCompoundStabilityAnalysis",
    "CylindricalGearSetCompoundStabilityAnalysis",
    "CylindricalPlanetGearCompoundStabilityAnalysis",
    "DatumCompoundStabilityAnalysis",
    "ExternalCADModelCompoundStabilityAnalysis",
    "FaceGearCompoundStabilityAnalysis",
    "FaceGearMeshCompoundStabilityAnalysis",
    "FaceGearSetCompoundStabilityAnalysis",
    "FEPartCompoundStabilityAnalysis",
    "FlexiblePinAssemblyCompoundStabilityAnalysis",
    "GearCompoundStabilityAnalysis",
    "GearMeshCompoundStabilityAnalysis",
    "GearSetCompoundStabilityAnalysis",
    "GuideDxfModelCompoundStabilityAnalysis",
    "HypoidGearCompoundStabilityAnalysis",
    "HypoidGearMeshCompoundStabilityAnalysis",
    "HypoidGearSetCompoundStabilityAnalysis",
    "InterMountableComponentConnectionCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis",
    "MassDiscCompoundStabilityAnalysis",
    "MeasurementComponentCompoundStabilityAnalysis",
    "MountableComponentCompoundStabilityAnalysis",
    "OilSealCompoundStabilityAnalysis",
    "PartCompoundStabilityAnalysis",
    "PartToPartShearCouplingCompoundStabilityAnalysis",
    "PartToPartShearCouplingConnectionCompoundStabilityAnalysis",
    "PartToPartShearCouplingHalfCompoundStabilityAnalysis",
    "PlanetaryConnectionCompoundStabilityAnalysis",
    "PlanetaryGearSetCompoundStabilityAnalysis",
    "PlanetCarrierCompoundStabilityAnalysis",
    "PointLoadCompoundStabilityAnalysis",
    "PowerLoadCompoundStabilityAnalysis",
    "PulleyCompoundStabilityAnalysis",
    "RingPinsCompoundStabilityAnalysis",
    "RingPinsToDiscConnectionCompoundStabilityAnalysis",
    "RollingRingAssemblyCompoundStabilityAnalysis",
    "RollingRingCompoundStabilityAnalysis",
    "RollingRingConnectionCompoundStabilityAnalysis",
    "RootAssemblyCompoundStabilityAnalysis",
    "ShaftCompoundStabilityAnalysis",
    "ShaftHubConnectionCompoundStabilityAnalysis",
    "ShaftToMountableComponentConnectionCompoundStabilityAnalysis",
    "SpecialisedAssemblyCompoundStabilityAnalysis",
    "SpiralBevelGearCompoundStabilityAnalysis",
    "SpiralBevelGearMeshCompoundStabilityAnalysis",
    "SpiralBevelGearSetCompoundStabilityAnalysis",
    "SpringDamperCompoundStabilityAnalysis",
    "SpringDamperConnectionCompoundStabilityAnalysis",
    "SpringDamperHalfCompoundStabilityAnalysis",
    "StraightBevelDiffGearCompoundStabilityAnalysis",
    "StraightBevelDiffGearMeshCompoundStabilityAnalysis",
    "StraightBevelDiffGearSetCompoundStabilityAnalysis",
    "StraightBevelGearCompoundStabilityAnalysis",
    "StraightBevelGearMeshCompoundStabilityAnalysis",
    "StraightBevelGearSetCompoundStabilityAnalysis",
    "StraightBevelPlanetGearCompoundStabilityAnalysis",
    "StraightBevelSunGearCompoundStabilityAnalysis",
    "SynchroniserCompoundStabilityAnalysis",
    "SynchroniserHalfCompoundStabilityAnalysis",
    "SynchroniserPartCompoundStabilityAnalysis",
    "SynchroniserSleeveCompoundStabilityAnalysis",
    "TorqueConverterCompoundStabilityAnalysis",
    "TorqueConverterConnectionCompoundStabilityAnalysis",
    "TorqueConverterPumpCompoundStabilityAnalysis",
    "TorqueConverterTurbineCompoundStabilityAnalysis",
    "UnbalancedMassCompoundStabilityAnalysis",
    "VirtualComponentCompoundStabilityAnalysis",
    "WormGearCompoundStabilityAnalysis",
    "WormGearMeshCompoundStabilityAnalysis",
    "WormGearSetCompoundStabilityAnalysis",
    "ZerolBevelGearCompoundStabilityAnalysis",
    "ZerolBevelGearMeshCompoundStabilityAnalysis",
    "ZerolBevelGearSetCompoundStabilityAnalysis",
)
