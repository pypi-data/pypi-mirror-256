"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._4034 import AbstractAssemblyPowerFlow
    from ._4035 import AbstractShaftOrHousingPowerFlow
    from ._4036 import AbstractShaftPowerFlow
    from ._4037 import AbstractShaftToMountableComponentConnectionPowerFlow
    from ._4038 import AGMAGleasonConicalGearMeshPowerFlow
    from ._4039 import AGMAGleasonConicalGearPowerFlow
    from ._4040 import AGMAGleasonConicalGearSetPowerFlow
    from ._4041 import AssemblyPowerFlow
    from ._4042 import BearingPowerFlow
    from ._4043 import BeltConnectionPowerFlow
    from ._4044 import BeltDrivePowerFlow
    from ._4045 import BevelDifferentialGearMeshPowerFlow
    from ._4046 import BevelDifferentialGearPowerFlow
    from ._4047 import BevelDifferentialGearSetPowerFlow
    from ._4048 import BevelDifferentialPlanetGearPowerFlow
    from ._4049 import BevelDifferentialSunGearPowerFlow
    from ._4050 import BevelGearMeshPowerFlow
    from ._4051 import BevelGearPowerFlow
    from ._4052 import BevelGearSetPowerFlow
    from ._4053 import BoltedJointPowerFlow
    from ._4054 import BoltPowerFlow
    from ._4055 import ClutchConnectionPowerFlow
    from ._4056 import ClutchHalfPowerFlow
    from ._4057 import ClutchPowerFlow
    from ._4058 import CoaxialConnectionPowerFlow
    from ._4059 import ComponentPowerFlow
    from ._4060 import ConceptCouplingConnectionPowerFlow
    from ._4061 import ConceptCouplingHalfPowerFlow
    from ._4062 import ConceptCouplingPowerFlow
    from ._4063 import ConceptGearMeshPowerFlow
    from ._4064 import ConceptGearPowerFlow
    from ._4065 import ConceptGearSetPowerFlow
    from ._4066 import ConicalGearMeshPowerFlow
    from ._4067 import ConicalGearPowerFlow
    from ._4068 import ConicalGearSetPowerFlow
    from ._4069 import ConnectionPowerFlow
    from ._4070 import ConnectorPowerFlow
    from ._4071 import CouplingConnectionPowerFlow
    from ._4072 import CouplingHalfPowerFlow
    from ._4073 import CouplingPowerFlow
    from ._4074 import CVTBeltConnectionPowerFlow
    from ._4075 import CVTPowerFlow
    from ._4076 import CVTPulleyPowerFlow
    from ._4077 import CycloidalAssemblyPowerFlow
    from ._4078 import CycloidalDiscCentralBearingConnectionPowerFlow
    from ._4079 import CycloidalDiscPlanetaryBearingConnectionPowerFlow
    from ._4080 import CycloidalDiscPowerFlow
    from ._4081 import CylindricalGearGeometricEntityDrawStyle
    from ._4082 import CylindricalGearMeshPowerFlow
    from ._4083 import CylindricalGearPowerFlow
    from ._4084 import CylindricalGearSetPowerFlow
    from ._4085 import CylindricalPlanetGearPowerFlow
    from ._4086 import DatumPowerFlow
    from ._4087 import ExternalCADModelPowerFlow
    from ._4088 import FaceGearMeshPowerFlow
    from ._4089 import FaceGearPowerFlow
    from ._4090 import FaceGearSetPowerFlow
    from ._4091 import FastPowerFlow
    from ._4092 import FastPowerFlowSolution
    from ._4093 import FEPartPowerFlow
    from ._4094 import FlexiblePinAssemblyPowerFlow
    from ._4095 import GearMeshPowerFlow
    from ._4096 import GearPowerFlow
    from ._4097 import GearSetPowerFlow
    from ._4098 import GuideDxfModelPowerFlow
    from ._4099 import HypoidGearMeshPowerFlow
    from ._4100 import HypoidGearPowerFlow
    from ._4101 import HypoidGearSetPowerFlow
    from ._4102 import InterMountableComponentConnectionPowerFlow
    from ._4103 import KlingelnbergCycloPalloidConicalGearMeshPowerFlow
    from ._4104 import KlingelnbergCycloPalloidConicalGearPowerFlow
    from ._4105 import KlingelnbergCycloPalloidConicalGearSetPowerFlow
    from ._4106 import KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
    from ._4107 import KlingelnbergCycloPalloidHypoidGearPowerFlow
    from ._4108 import KlingelnbergCycloPalloidHypoidGearSetPowerFlow
    from ._4109 import KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
    from ._4110 import KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
    from ._4111 import KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
    from ._4112 import MassDiscPowerFlow
    from ._4113 import MeasurementComponentPowerFlow
    from ._4114 import MountableComponentPowerFlow
    from ._4115 import OilSealPowerFlow
    from ._4116 import PartPowerFlow
    from ._4117 import PartToPartShearCouplingConnectionPowerFlow
    from ._4118 import PartToPartShearCouplingHalfPowerFlow
    from ._4119 import PartToPartShearCouplingPowerFlow
    from ._4120 import PlanetaryConnectionPowerFlow
    from ._4121 import PlanetaryGearSetPowerFlow
    from ._4122 import PlanetCarrierPowerFlow
    from ._4123 import PointLoadPowerFlow
    from ._4124 import PowerFlow
    from ._4125 import PowerFlowDrawStyle
    from ._4126 import PowerLoadPowerFlow
    from ._4127 import PulleyPowerFlow
    from ._4128 import RingPinsPowerFlow
    from ._4129 import RingPinsToDiscConnectionPowerFlow
    from ._4130 import RollingRingAssemblyPowerFlow
    from ._4131 import RollingRingConnectionPowerFlow
    from ._4132 import RollingRingPowerFlow
    from ._4133 import RootAssemblyPowerFlow
    from ._4134 import ShaftHubConnectionPowerFlow
    from ._4135 import ShaftPowerFlow
    from ._4136 import ShaftToMountableComponentConnectionPowerFlow
    from ._4137 import SpecialisedAssemblyPowerFlow
    from ._4138 import SpiralBevelGearMeshPowerFlow
    from ._4139 import SpiralBevelGearPowerFlow
    from ._4140 import SpiralBevelGearSetPowerFlow
    from ._4141 import SpringDamperConnectionPowerFlow
    from ._4142 import SpringDamperHalfPowerFlow
    from ._4143 import SpringDamperPowerFlow
    from ._4144 import StraightBevelDiffGearMeshPowerFlow
    from ._4145 import StraightBevelDiffGearPowerFlow
    from ._4146 import StraightBevelDiffGearSetPowerFlow
    from ._4147 import StraightBevelGearMeshPowerFlow
    from ._4148 import StraightBevelGearPowerFlow
    from ._4149 import StraightBevelGearSetPowerFlow
    from ._4150 import StraightBevelPlanetGearPowerFlow
    from ._4151 import StraightBevelSunGearPowerFlow
    from ._4152 import SynchroniserHalfPowerFlow
    from ._4153 import SynchroniserPartPowerFlow
    from ._4154 import SynchroniserPowerFlow
    from ._4155 import SynchroniserSleevePowerFlow
    from ._4156 import ToothPassingHarmonic
    from ._4157 import TorqueConverterConnectionPowerFlow
    from ._4158 import TorqueConverterPowerFlow
    from ._4159 import TorqueConverterPumpPowerFlow
    from ._4160 import TorqueConverterTurbinePowerFlow
    from ._4161 import UnbalancedMassPowerFlow
    from ._4162 import VirtualComponentPowerFlow
    from ._4163 import WormGearMeshPowerFlow
    from ._4164 import WormGearPowerFlow
    from ._4165 import WormGearSetPowerFlow
    from ._4166 import ZerolBevelGearMeshPowerFlow
    from ._4167 import ZerolBevelGearPowerFlow
    from ._4168 import ZerolBevelGearSetPowerFlow
else:
    import_structure = {
        "_4034": ["AbstractAssemblyPowerFlow"],
        "_4035": ["AbstractShaftOrHousingPowerFlow"],
        "_4036": ["AbstractShaftPowerFlow"],
        "_4037": ["AbstractShaftToMountableComponentConnectionPowerFlow"],
        "_4038": ["AGMAGleasonConicalGearMeshPowerFlow"],
        "_4039": ["AGMAGleasonConicalGearPowerFlow"],
        "_4040": ["AGMAGleasonConicalGearSetPowerFlow"],
        "_4041": ["AssemblyPowerFlow"],
        "_4042": ["BearingPowerFlow"],
        "_4043": ["BeltConnectionPowerFlow"],
        "_4044": ["BeltDrivePowerFlow"],
        "_4045": ["BevelDifferentialGearMeshPowerFlow"],
        "_4046": ["BevelDifferentialGearPowerFlow"],
        "_4047": ["BevelDifferentialGearSetPowerFlow"],
        "_4048": ["BevelDifferentialPlanetGearPowerFlow"],
        "_4049": ["BevelDifferentialSunGearPowerFlow"],
        "_4050": ["BevelGearMeshPowerFlow"],
        "_4051": ["BevelGearPowerFlow"],
        "_4052": ["BevelGearSetPowerFlow"],
        "_4053": ["BoltedJointPowerFlow"],
        "_4054": ["BoltPowerFlow"],
        "_4055": ["ClutchConnectionPowerFlow"],
        "_4056": ["ClutchHalfPowerFlow"],
        "_4057": ["ClutchPowerFlow"],
        "_4058": ["CoaxialConnectionPowerFlow"],
        "_4059": ["ComponentPowerFlow"],
        "_4060": ["ConceptCouplingConnectionPowerFlow"],
        "_4061": ["ConceptCouplingHalfPowerFlow"],
        "_4062": ["ConceptCouplingPowerFlow"],
        "_4063": ["ConceptGearMeshPowerFlow"],
        "_4064": ["ConceptGearPowerFlow"],
        "_4065": ["ConceptGearSetPowerFlow"],
        "_4066": ["ConicalGearMeshPowerFlow"],
        "_4067": ["ConicalGearPowerFlow"],
        "_4068": ["ConicalGearSetPowerFlow"],
        "_4069": ["ConnectionPowerFlow"],
        "_4070": ["ConnectorPowerFlow"],
        "_4071": ["CouplingConnectionPowerFlow"],
        "_4072": ["CouplingHalfPowerFlow"],
        "_4073": ["CouplingPowerFlow"],
        "_4074": ["CVTBeltConnectionPowerFlow"],
        "_4075": ["CVTPowerFlow"],
        "_4076": ["CVTPulleyPowerFlow"],
        "_4077": ["CycloidalAssemblyPowerFlow"],
        "_4078": ["CycloidalDiscCentralBearingConnectionPowerFlow"],
        "_4079": ["CycloidalDiscPlanetaryBearingConnectionPowerFlow"],
        "_4080": ["CycloidalDiscPowerFlow"],
        "_4081": ["CylindricalGearGeometricEntityDrawStyle"],
        "_4082": ["CylindricalGearMeshPowerFlow"],
        "_4083": ["CylindricalGearPowerFlow"],
        "_4084": ["CylindricalGearSetPowerFlow"],
        "_4085": ["CylindricalPlanetGearPowerFlow"],
        "_4086": ["DatumPowerFlow"],
        "_4087": ["ExternalCADModelPowerFlow"],
        "_4088": ["FaceGearMeshPowerFlow"],
        "_4089": ["FaceGearPowerFlow"],
        "_4090": ["FaceGearSetPowerFlow"],
        "_4091": ["FastPowerFlow"],
        "_4092": ["FastPowerFlowSolution"],
        "_4093": ["FEPartPowerFlow"],
        "_4094": ["FlexiblePinAssemblyPowerFlow"],
        "_4095": ["GearMeshPowerFlow"],
        "_4096": ["GearPowerFlow"],
        "_4097": ["GearSetPowerFlow"],
        "_4098": ["GuideDxfModelPowerFlow"],
        "_4099": ["HypoidGearMeshPowerFlow"],
        "_4100": ["HypoidGearPowerFlow"],
        "_4101": ["HypoidGearSetPowerFlow"],
        "_4102": ["InterMountableComponentConnectionPowerFlow"],
        "_4103": ["KlingelnbergCycloPalloidConicalGearMeshPowerFlow"],
        "_4104": ["KlingelnbergCycloPalloidConicalGearPowerFlow"],
        "_4105": ["KlingelnbergCycloPalloidConicalGearSetPowerFlow"],
        "_4106": ["KlingelnbergCycloPalloidHypoidGearMeshPowerFlow"],
        "_4107": ["KlingelnbergCycloPalloidHypoidGearPowerFlow"],
        "_4108": ["KlingelnbergCycloPalloidHypoidGearSetPowerFlow"],
        "_4109": ["KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow"],
        "_4110": ["KlingelnbergCycloPalloidSpiralBevelGearPowerFlow"],
        "_4111": ["KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow"],
        "_4112": ["MassDiscPowerFlow"],
        "_4113": ["MeasurementComponentPowerFlow"],
        "_4114": ["MountableComponentPowerFlow"],
        "_4115": ["OilSealPowerFlow"],
        "_4116": ["PartPowerFlow"],
        "_4117": ["PartToPartShearCouplingConnectionPowerFlow"],
        "_4118": ["PartToPartShearCouplingHalfPowerFlow"],
        "_4119": ["PartToPartShearCouplingPowerFlow"],
        "_4120": ["PlanetaryConnectionPowerFlow"],
        "_4121": ["PlanetaryGearSetPowerFlow"],
        "_4122": ["PlanetCarrierPowerFlow"],
        "_4123": ["PointLoadPowerFlow"],
        "_4124": ["PowerFlow"],
        "_4125": ["PowerFlowDrawStyle"],
        "_4126": ["PowerLoadPowerFlow"],
        "_4127": ["PulleyPowerFlow"],
        "_4128": ["RingPinsPowerFlow"],
        "_4129": ["RingPinsToDiscConnectionPowerFlow"],
        "_4130": ["RollingRingAssemblyPowerFlow"],
        "_4131": ["RollingRingConnectionPowerFlow"],
        "_4132": ["RollingRingPowerFlow"],
        "_4133": ["RootAssemblyPowerFlow"],
        "_4134": ["ShaftHubConnectionPowerFlow"],
        "_4135": ["ShaftPowerFlow"],
        "_4136": ["ShaftToMountableComponentConnectionPowerFlow"],
        "_4137": ["SpecialisedAssemblyPowerFlow"],
        "_4138": ["SpiralBevelGearMeshPowerFlow"],
        "_4139": ["SpiralBevelGearPowerFlow"],
        "_4140": ["SpiralBevelGearSetPowerFlow"],
        "_4141": ["SpringDamperConnectionPowerFlow"],
        "_4142": ["SpringDamperHalfPowerFlow"],
        "_4143": ["SpringDamperPowerFlow"],
        "_4144": ["StraightBevelDiffGearMeshPowerFlow"],
        "_4145": ["StraightBevelDiffGearPowerFlow"],
        "_4146": ["StraightBevelDiffGearSetPowerFlow"],
        "_4147": ["StraightBevelGearMeshPowerFlow"],
        "_4148": ["StraightBevelGearPowerFlow"],
        "_4149": ["StraightBevelGearSetPowerFlow"],
        "_4150": ["StraightBevelPlanetGearPowerFlow"],
        "_4151": ["StraightBevelSunGearPowerFlow"],
        "_4152": ["SynchroniserHalfPowerFlow"],
        "_4153": ["SynchroniserPartPowerFlow"],
        "_4154": ["SynchroniserPowerFlow"],
        "_4155": ["SynchroniserSleevePowerFlow"],
        "_4156": ["ToothPassingHarmonic"],
        "_4157": ["TorqueConverterConnectionPowerFlow"],
        "_4158": ["TorqueConverterPowerFlow"],
        "_4159": ["TorqueConverterPumpPowerFlow"],
        "_4160": ["TorqueConverterTurbinePowerFlow"],
        "_4161": ["UnbalancedMassPowerFlow"],
        "_4162": ["VirtualComponentPowerFlow"],
        "_4163": ["WormGearMeshPowerFlow"],
        "_4164": ["WormGearPowerFlow"],
        "_4165": ["WormGearSetPowerFlow"],
        "_4166": ["ZerolBevelGearMeshPowerFlow"],
        "_4167": ["ZerolBevelGearPowerFlow"],
        "_4168": ["ZerolBevelGearSetPowerFlow"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyPowerFlow",
    "AbstractShaftOrHousingPowerFlow",
    "AbstractShaftPowerFlow",
    "AbstractShaftToMountableComponentConnectionPowerFlow",
    "AGMAGleasonConicalGearMeshPowerFlow",
    "AGMAGleasonConicalGearPowerFlow",
    "AGMAGleasonConicalGearSetPowerFlow",
    "AssemblyPowerFlow",
    "BearingPowerFlow",
    "BeltConnectionPowerFlow",
    "BeltDrivePowerFlow",
    "BevelDifferentialGearMeshPowerFlow",
    "BevelDifferentialGearPowerFlow",
    "BevelDifferentialGearSetPowerFlow",
    "BevelDifferentialPlanetGearPowerFlow",
    "BevelDifferentialSunGearPowerFlow",
    "BevelGearMeshPowerFlow",
    "BevelGearPowerFlow",
    "BevelGearSetPowerFlow",
    "BoltedJointPowerFlow",
    "BoltPowerFlow",
    "ClutchConnectionPowerFlow",
    "ClutchHalfPowerFlow",
    "ClutchPowerFlow",
    "CoaxialConnectionPowerFlow",
    "ComponentPowerFlow",
    "ConceptCouplingConnectionPowerFlow",
    "ConceptCouplingHalfPowerFlow",
    "ConceptCouplingPowerFlow",
    "ConceptGearMeshPowerFlow",
    "ConceptGearPowerFlow",
    "ConceptGearSetPowerFlow",
    "ConicalGearMeshPowerFlow",
    "ConicalGearPowerFlow",
    "ConicalGearSetPowerFlow",
    "ConnectionPowerFlow",
    "ConnectorPowerFlow",
    "CouplingConnectionPowerFlow",
    "CouplingHalfPowerFlow",
    "CouplingPowerFlow",
    "CVTBeltConnectionPowerFlow",
    "CVTPowerFlow",
    "CVTPulleyPowerFlow",
    "CycloidalAssemblyPowerFlow",
    "CycloidalDiscCentralBearingConnectionPowerFlow",
    "CycloidalDiscPlanetaryBearingConnectionPowerFlow",
    "CycloidalDiscPowerFlow",
    "CylindricalGearGeometricEntityDrawStyle",
    "CylindricalGearMeshPowerFlow",
    "CylindricalGearPowerFlow",
    "CylindricalGearSetPowerFlow",
    "CylindricalPlanetGearPowerFlow",
    "DatumPowerFlow",
    "ExternalCADModelPowerFlow",
    "FaceGearMeshPowerFlow",
    "FaceGearPowerFlow",
    "FaceGearSetPowerFlow",
    "FastPowerFlow",
    "FastPowerFlowSolution",
    "FEPartPowerFlow",
    "FlexiblePinAssemblyPowerFlow",
    "GearMeshPowerFlow",
    "GearPowerFlow",
    "GearSetPowerFlow",
    "GuideDxfModelPowerFlow",
    "HypoidGearMeshPowerFlow",
    "HypoidGearPowerFlow",
    "HypoidGearSetPowerFlow",
    "InterMountableComponentConnectionPowerFlow",
    "KlingelnbergCycloPalloidConicalGearMeshPowerFlow",
    "KlingelnbergCycloPalloidConicalGearPowerFlow",
    "KlingelnbergCycloPalloidConicalGearSetPowerFlow",
    "KlingelnbergCycloPalloidHypoidGearMeshPowerFlow",
    "KlingelnbergCycloPalloidHypoidGearPowerFlow",
    "KlingelnbergCycloPalloidHypoidGearSetPowerFlow",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow",
    "KlingelnbergCycloPalloidSpiralBevelGearPowerFlow",
    "KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow",
    "MassDiscPowerFlow",
    "MeasurementComponentPowerFlow",
    "MountableComponentPowerFlow",
    "OilSealPowerFlow",
    "PartPowerFlow",
    "PartToPartShearCouplingConnectionPowerFlow",
    "PartToPartShearCouplingHalfPowerFlow",
    "PartToPartShearCouplingPowerFlow",
    "PlanetaryConnectionPowerFlow",
    "PlanetaryGearSetPowerFlow",
    "PlanetCarrierPowerFlow",
    "PointLoadPowerFlow",
    "PowerFlow",
    "PowerFlowDrawStyle",
    "PowerLoadPowerFlow",
    "PulleyPowerFlow",
    "RingPinsPowerFlow",
    "RingPinsToDiscConnectionPowerFlow",
    "RollingRingAssemblyPowerFlow",
    "RollingRingConnectionPowerFlow",
    "RollingRingPowerFlow",
    "RootAssemblyPowerFlow",
    "ShaftHubConnectionPowerFlow",
    "ShaftPowerFlow",
    "ShaftToMountableComponentConnectionPowerFlow",
    "SpecialisedAssemblyPowerFlow",
    "SpiralBevelGearMeshPowerFlow",
    "SpiralBevelGearPowerFlow",
    "SpiralBevelGearSetPowerFlow",
    "SpringDamperConnectionPowerFlow",
    "SpringDamperHalfPowerFlow",
    "SpringDamperPowerFlow",
    "StraightBevelDiffGearMeshPowerFlow",
    "StraightBevelDiffGearPowerFlow",
    "StraightBevelDiffGearSetPowerFlow",
    "StraightBevelGearMeshPowerFlow",
    "StraightBevelGearPowerFlow",
    "StraightBevelGearSetPowerFlow",
    "StraightBevelPlanetGearPowerFlow",
    "StraightBevelSunGearPowerFlow",
    "SynchroniserHalfPowerFlow",
    "SynchroniserPartPowerFlow",
    "SynchroniserPowerFlow",
    "SynchroniserSleevePowerFlow",
    "ToothPassingHarmonic",
    "TorqueConverterConnectionPowerFlow",
    "TorqueConverterPowerFlow",
    "TorqueConverterPumpPowerFlow",
    "TorqueConverterTurbinePowerFlow",
    "UnbalancedMassPowerFlow",
    "VirtualComponentPowerFlow",
    "WormGearMeshPowerFlow",
    "WormGearPowerFlow",
    "WormGearSetPowerFlow",
    "ZerolBevelGearMeshPowerFlow",
    "ZerolBevelGearPowerFlow",
    "ZerolBevelGearSetPowerFlow",
)
