"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._4169 import AbstractAssemblyCompoundPowerFlow
    from ._4170 import AbstractShaftCompoundPowerFlow
    from ._4171 import AbstractShaftOrHousingCompoundPowerFlow
    from ._4172 import AbstractShaftToMountableComponentConnectionCompoundPowerFlow
    from ._4173 import AGMAGleasonConicalGearCompoundPowerFlow
    from ._4174 import AGMAGleasonConicalGearMeshCompoundPowerFlow
    from ._4175 import AGMAGleasonConicalGearSetCompoundPowerFlow
    from ._4176 import AssemblyCompoundPowerFlow
    from ._4177 import BearingCompoundPowerFlow
    from ._4178 import BeltConnectionCompoundPowerFlow
    from ._4179 import BeltDriveCompoundPowerFlow
    from ._4180 import BevelDifferentialGearCompoundPowerFlow
    from ._4181 import BevelDifferentialGearMeshCompoundPowerFlow
    from ._4182 import BevelDifferentialGearSetCompoundPowerFlow
    from ._4183 import BevelDifferentialPlanetGearCompoundPowerFlow
    from ._4184 import BevelDifferentialSunGearCompoundPowerFlow
    from ._4185 import BevelGearCompoundPowerFlow
    from ._4186 import BevelGearMeshCompoundPowerFlow
    from ._4187 import BevelGearSetCompoundPowerFlow
    from ._4188 import BoltCompoundPowerFlow
    from ._4189 import BoltedJointCompoundPowerFlow
    from ._4190 import ClutchCompoundPowerFlow
    from ._4191 import ClutchConnectionCompoundPowerFlow
    from ._4192 import ClutchHalfCompoundPowerFlow
    from ._4193 import CoaxialConnectionCompoundPowerFlow
    from ._4194 import ComponentCompoundPowerFlow
    from ._4195 import ConceptCouplingCompoundPowerFlow
    from ._4196 import ConceptCouplingConnectionCompoundPowerFlow
    from ._4197 import ConceptCouplingHalfCompoundPowerFlow
    from ._4198 import ConceptGearCompoundPowerFlow
    from ._4199 import ConceptGearMeshCompoundPowerFlow
    from ._4200 import ConceptGearSetCompoundPowerFlow
    from ._4201 import ConicalGearCompoundPowerFlow
    from ._4202 import ConicalGearMeshCompoundPowerFlow
    from ._4203 import ConicalGearSetCompoundPowerFlow
    from ._4204 import ConnectionCompoundPowerFlow
    from ._4205 import ConnectorCompoundPowerFlow
    from ._4206 import CouplingCompoundPowerFlow
    from ._4207 import CouplingConnectionCompoundPowerFlow
    from ._4208 import CouplingHalfCompoundPowerFlow
    from ._4209 import CVTBeltConnectionCompoundPowerFlow
    from ._4210 import CVTCompoundPowerFlow
    from ._4211 import CVTPulleyCompoundPowerFlow
    from ._4212 import CycloidalAssemblyCompoundPowerFlow
    from ._4213 import CycloidalDiscCentralBearingConnectionCompoundPowerFlow
    from ._4214 import CycloidalDiscCompoundPowerFlow
    from ._4215 import CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow
    from ._4216 import CylindricalGearCompoundPowerFlow
    from ._4217 import CylindricalGearMeshCompoundPowerFlow
    from ._4218 import CylindricalGearSetCompoundPowerFlow
    from ._4219 import CylindricalPlanetGearCompoundPowerFlow
    from ._4220 import DatumCompoundPowerFlow
    from ._4221 import ExternalCADModelCompoundPowerFlow
    from ._4222 import FaceGearCompoundPowerFlow
    from ._4223 import FaceGearMeshCompoundPowerFlow
    from ._4224 import FaceGearSetCompoundPowerFlow
    from ._4225 import FEPartCompoundPowerFlow
    from ._4226 import FlexiblePinAssemblyCompoundPowerFlow
    from ._4227 import GearCompoundPowerFlow
    from ._4228 import GearMeshCompoundPowerFlow
    from ._4229 import GearSetCompoundPowerFlow
    from ._4230 import GuideDxfModelCompoundPowerFlow
    from ._4231 import HypoidGearCompoundPowerFlow
    from ._4232 import HypoidGearMeshCompoundPowerFlow
    from ._4233 import HypoidGearSetCompoundPowerFlow
    from ._4234 import InterMountableComponentConnectionCompoundPowerFlow
    from ._4235 import KlingelnbergCycloPalloidConicalGearCompoundPowerFlow
    from ._4236 import KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow
    from ._4237 import KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow
    from ._4238 import KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow
    from ._4239 import KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow
    from ._4240 import KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow
    from ._4241 import KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow
    from ._4242 import KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow
    from ._4243 import KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow
    from ._4244 import MassDiscCompoundPowerFlow
    from ._4245 import MeasurementComponentCompoundPowerFlow
    from ._4246 import MountableComponentCompoundPowerFlow
    from ._4247 import OilSealCompoundPowerFlow
    from ._4248 import PartCompoundPowerFlow
    from ._4249 import PartToPartShearCouplingCompoundPowerFlow
    from ._4250 import PartToPartShearCouplingConnectionCompoundPowerFlow
    from ._4251 import PartToPartShearCouplingHalfCompoundPowerFlow
    from ._4252 import PlanetaryConnectionCompoundPowerFlow
    from ._4253 import PlanetaryGearSetCompoundPowerFlow
    from ._4254 import PlanetCarrierCompoundPowerFlow
    from ._4255 import PointLoadCompoundPowerFlow
    from ._4256 import PowerLoadCompoundPowerFlow
    from ._4257 import PulleyCompoundPowerFlow
    from ._4258 import RingPinsCompoundPowerFlow
    from ._4259 import RingPinsToDiscConnectionCompoundPowerFlow
    from ._4260 import RollingRingAssemblyCompoundPowerFlow
    from ._4261 import RollingRingCompoundPowerFlow
    from ._4262 import RollingRingConnectionCompoundPowerFlow
    from ._4263 import RootAssemblyCompoundPowerFlow
    from ._4264 import ShaftCompoundPowerFlow
    from ._4265 import ShaftHubConnectionCompoundPowerFlow
    from ._4266 import ShaftToMountableComponentConnectionCompoundPowerFlow
    from ._4267 import SpecialisedAssemblyCompoundPowerFlow
    from ._4268 import SpiralBevelGearCompoundPowerFlow
    from ._4269 import SpiralBevelGearMeshCompoundPowerFlow
    from ._4270 import SpiralBevelGearSetCompoundPowerFlow
    from ._4271 import SpringDamperCompoundPowerFlow
    from ._4272 import SpringDamperConnectionCompoundPowerFlow
    from ._4273 import SpringDamperHalfCompoundPowerFlow
    from ._4274 import StraightBevelDiffGearCompoundPowerFlow
    from ._4275 import StraightBevelDiffGearMeshCompoundPowerFlow
    from ._4276 import StraightBevelDiffGearSetCompoundPowerFlow
    from ._4277 import StraightBevelGearCompoundPowerFlow
    from ._4278 import StraightBevelGearMeshCompoundPowerFlow
    from ._4279 import StraightBevelGearSetCompoundPowerFlow
    from ._4280 import StraightBevelPlanetGearCompoundPowerFlow
    from ._4281 import StraightBevelSunGearCompoundPowerFlow
    from ._4282 import SynchroniserCompoundPowerFlow
    from ._4283 import SynchroniserHalfCompoundPowerFlow
    from ._4284 import SynchroniserPartCompoundPowerFlow
    from ._4285 import SynchroniserSleeveCompoundPowerFlow
    from ._4286 import TorqueConverterCompoundPowerFlow
    from ._4287 import TorqueConverterConnectionCompoundPowerFlow
    from ._4288 import TorqueConverterPumpCompoundPowerFlow
    from ._4289 import TorqueConverterTurbineCompoundPowerFlow
    from ._4290 import UnbalancedMassCompoundPowerFlow
    from ._4291 import VirtualComponentCompoundPowerFlow
    from ._4292 import WormGearCompoundPowerFlow
    from ._4293 import WormGearMeshCompoundPowerFlow
    from ._4294 import WormGearSetCompoundPowerFlow
    from ._4295 import ZerolBevelGearCompoundPowerFlow
    from ._4296 import ZerolBevelGearMeshCompoundPowerFlow
    from ._4297 import ZerolBevelGearSetCompoundPowerFlow
else:
    import_structure = {
        "_4169": ["AbstractAssemblyCompoundPowerFlow"],
        "_4170": ["AbstractShaftCompoundPowerFlow"],
        "_4171": ["AbstractShaftOrHousingCompoundPowerFlow"],
        "_4172": ["AbstractShaftToMountableComponentConnectionCompoundPowerFlow"],
        "_4173": ["AGMAGleasonConicalGearCompoundPowerFlow"],
        "_4174": ["AGMAGleasonConicalGearMeshCompoundPowerFlow"],
        "_4175": ["AGMAGleasonConicalGearSetCompoundPowerFlow"],
        "_4176": ["AssemblyCompoundPowerFlow"],
        "_4177": ["BearingCompoundPowerFlow"],
        "_4178": ["BeltConnectionCompoundPowerFlow"],
        "_4179": ["BeltDriveCompoundPowerFlow"],
        "_4180": ["BevelDifferentialGearCompoundPowerFlow"],
        "_4181": ["BevelDifferentialGearMeshCompoundPowerFlow"],
        "_4182": ["BevelDifferentialGearSetCompoundPowerFlow"],
        "_4183": ["BevelDifferentialPlanetGearCompoundPowerFlow"],
        "_4184": ["BevelDifferentialSunGearCompoundPowerFlow"],
        "_4185": ["BevelGearCompoundPowerFlow"],
        "_4186": ["BevelGearMeshCompoundPowerFlow"],
        "_4187": ["BevelGearSetCompoundPowerFlow"],
        "_4188": ["BoltCompoundPowerFlow"],
        "_4189": ["BoltedJointCompoundPowerFlow"],
        "_4190": ["ClutchCompoundPowerFlow"],
        "_4191": ["ClutchConnectionCompoundPowerFlow"],
        "_4192": ["ClutchHalfCompoundPowerFlow"],
        "_4193": ["CoaxialConnectionCompoundPowerFlow"],
        "_4194": ["ComponentCompoundPowerFlow"],
        "_4195": ["ConceptCouplingCompoundPowerFlow"],
        "_4196": ["ConceptCouplingConnectionCompoundPowerFlow"],
        "_4197": ["ConceptCouplingHalfCompoundPowerFlow"],
        "_4198": ["ConceptGearCompoundPowerFlow"],
        "_4199": ["ConceptGearMeshCompoundPowerFlow"],
        "_4200": ["ConceptGearSetCompoundPowerFlow"],
        "_4201": ["ConicalGearCompoundPowerFlow"],
        "_4202": ["ConicalGearMeshCompoundPowerFlow"],
        "_4203": ["ConicalGearSetCompoundPowerFlow"],
        "_4204": ["ConnectionCompoundPowerFlow"],
        "_4205": ["ConnectorCompoundPowerFlow"],
        "_4206": ["CouplingCompoundPowerFlow"],
        "_4207": ["CouplingConnectionCompoundPowerFlow"],
        "_4208": ["CouplingHalfCompoundPowerFlow"],
        "_4209": ["CVTBeltConnectionCompoundPowerFlow"],
        "_4210": ["CVTCompoundPowerFlow"],
        "_4211": ["CVTPulleyCompoundPowerFlow"],
        "_4212": ["CycloidalAssemblyCompoundPowerFlow"],
        "_4213": ["CycloidalDiscCentralBearingConnectionCompoundPowerFlow"],
        "_4214": ["CycloidalDiscCompoundPowerFlow"],
        "_4215": ["CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow"],
        "_4216": ["CylindricalGearCompoundPowerFlow"],
        "_4217": ["CylindricalGearMeshCompoundPowerFlow"],
        "_4218": ["CylindricalGearSetCompoundPowerFlow"],
        "_4219": ["CylindricalPlanetGearCompoundPowerFlow"],
        "_4220": ["DatumCompoundPowerFlow"],
        "_4221": ["ExternalCADModelCompoundPowerFlow"],
        "_4222": ["FaceGearCompoundPowerFlow"],
        "_4223": ["FaceGearMeshCompoundPowerFlow"],
        "_4224": ["FaceGearSetCompoundPowerFlow"],
        "_4225": ["FEPartCompoundPowerFlow"],
        "_4226": ["FlexiblePinAssemblyCompoundPowerFlow"],
        "_4227": ["GearCompoundPowerFlow"],
        "_4228": ["GearMeshCompoundPowerFlow"],
        "_4229": ["GearSetCompoundPowerFlow"],
        "_4230": ["GuideDxfModelCompoundPowerFlow"],
        "_4231": ["HypoidGearCompoundPowerFlow"],
        "_4232": ["HypoidGearMeshCompoundPowerFlow"],
        "_4233": ["HypoidGearSetCompoundPowerFlow"],
        "_4234": ["InterMountableComponentConnectionCompoundPowerFlow"],
        "_4235": ["KlingelnbergCycloPalloidConicalGearCompoundPowerFlow"],
        "_4236": ["KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow"],
        "_4237": ["KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow"],
        "_4238": ["KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow"],
        "_4239": ["KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow"],
        "_4240": ["KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow"],
        "_4241": ["KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow"],
        "_4242": ["KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow"],
        "_4243": ["KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow"],
        "_4244": ["MassDiscCompoundPowerFlow"],
        "_4245": ["MeasurementComponentCompoundPowerFlow"],
        "_4246": ["MountableComponentCompoundPowerFlow"],
        "_4247": ["OilSealCompoundPowerFlow"],
        "_4248": ["PartCompoundPowerFlow"],
        "_4249": ["PartToPartShearCouplingCompoundPowerFlow"],
        "_4250": ["PartToPartShearCouplingConnectionCompoundPowerFlow"],
        "_4251": ["PartToPartShearCouplingHalfCompoundPowerFlow"],
        "_4252": ["PlanetaryConnectionCompoundPowerFlow"],
        "_4253": ["PlanetaryGearSetCompoundPowerFlow"],
        "_4254": ["PlanetCarrierCompoundPowerFlow"],
        "_4255": ["PointLoadCompoundPowerFlow"],
        "_4256": ["PowerLoadCompoundPowerFlow"],
        "_4257": ["PulleyCompoundPowerFlow"],
        "_4258": ["RingPinsCompoundPowerFlow"],
        "_4259": ["RingPinsToDiscConnectionCompoundPowerFlow"],
        "_4260": ["RollingRingAssemblyCompoundPowerFlow"],
        "_4261": ["RollingRingCompoundPowerFlow"],
        "_4262": ["RollingRingConnectionCompoundPowerFlow"],
        "_4263": ["RootAssemblyCompoundPowerFlow"],
        "_4264": ["ShaftCompoundPowerFlow"],
        "_4265": ["ShaftHubConnectionCompoundPowerFlow"],
        "_4266": ["ShaftToMountableComponentConnectionCompoundPowerFlow"],
        "_4267": ["SpecialisedAssemblyCompoundPowerFlow"],
        "_4268": ["SpiralBevelGearCompoundPowerFlow"],
        "_4269": ["SpiralBevelGearMeshCompoundPowerFlow"],
        "_4270": ["SpiralBevelGearSetCompoundPowerFlow"],
        "_4271": ["SpringDamperCompoundPowerFlow"],
        "_4272": ["SpringDamperConnectionCompoundPowerFlow"],
        "_4273": ["SpringDamperHalfCompoundPowerFlow"],
        "_4274": ["StraightBevelDiffGearCompoundPowerFlow"],
        "_4275": ["StraightBevelDiffGearMeshCompoundPowerFlow"],
        "_4276": ["StraightBevelDiffGearSetCompoundPowerFlow"],
        "_4277": ["StraightBevelGearCompoundPowerFlow"],
        "_4278": ["StraightBevelGearMeshCompoundPowerFlow"],
        "_4279": ["StraightBevelGearSetCompoundPowerFlow"],
        "_4280": ["StraightBevelPlanetGearCompoundPowerFlow"],
        "_4281": ["StraightBevelSunGearCompoundPowerFlow"],
        "_4282": ["SynchroniserCompoundPowerFlow"],
        "_4283": ["SynchroniserHalfCompoundPowerFlow"],
        "_4284": ["SynchroniserPartCompoundPowerFlow"],
        "_4285": ["SynchroniserSleeveCompoundPowerFlow"],
        "_4286": ["TorqueConverterCompoundPowerFlow"],
        "_4287": ["TorqueConverterConnectionCompoundPowerFlow"],
        "_4288": ["TorqueConverterPumpCompoundPowerFlow"],
        "_4289": ["TorqueConverterTurbineCompoundPowerFlow"],
        "_4290": ["UnbalancedMassCompoundPowerFlow"],
        "_4291": ["VirtualComponentCompoundPowerFlow"],
        "_4292": ["WormGearCompoundPowerFlow"],
        "_4293": ["WormGearMeshCompoundPowerFlow"],
        "_4294": ["WormGearSetCompoundPowerFlow"],
        "_4295": ["ZerolBevelGearCompoundPowerFlow"],
        "_4296": ["ZerolBevelGearMeshCompoundPowerFlow"],
        "_4297": ["ZerolBevelGearSetCompoundPowerFlow"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundPowerFlow",
    "AbstractShaftCompoundPowerFlow",
    "AbstractShaftOrHousingCompoundPowerFlow",
    "AbstractShaftToMountableComponentConnectionCompoundPowerFlow",
    "AGMAGleasonConicalGearCompoundPowerFlow",
    "AGMAGleasonConicalGearMeshCompoundPowerFlow",
    "AGMAGleasonConicalGearSetCompoundPowerFlow",
    "AssemblyCompoundPowerFlow",
    "BearingCompoundPowerFlow",
    "BeltConnectionCompoundPowerFlow",
    "BeltDriveCompoundPowerFlow",
    "BevelDifferentialGearCompoundPowerFlow",
    "BevelDifferentialGearMeshCompoundPowerFlow",
    "BevelDifferentialGearSetCompoundPowerFlow",
    "BevelDifferentialPlanetGearCompoundPowerFlow",
    "BevelDifferentialSunGearCompoundPowerFlow",
    "BevelGearCompoundPowerFlow",
    "BevelGearMeshCompoundPowerFlow",
    "BevelGearSetCompoundPowerFlow",
    "BoltCompoundPowerFlow",
    "BoltedJointCompoundPowerFlow",
    "ClutchCompoundPowerFlow",
    "ClutchConnectionCompoundPowerFlow",
    "ClutchHalfCompoundPowerFlow",
    "CoaxialConnectionCompoundPowerFlow",
    "ComponentCompoundPowerFlow",
    "ConceptCouplingCompoundPowerFlow",
    "ConceptCouplingConnectionCompoundPowerFlow",
    "ConceptCouplingHalfCompoundPowerFlow",
    "ConceptGearCompoundPowerFlow",
    "ConceptGearMeshCompoundPowerFlow",
    "ConceptGearSetCompoundPowerFlow",
    "ConicalGearCompoundPowerFlow",
    "ConicalGearMeshCompoundPowerFlow",
    "ConicalGearSetCompoundPowerFlow",
    "ConnectionCompoundPowerFlow",
    "ConnectorCompoundPowerFlow",
    "CouplingCompoundPowerFlow",
    "CouplingConnectionCompoundPowerFlow",
    "CouplingHalfCompoundPowerFlow",
    "CVTBeltConnectionCompoundPowerFlow",
    "CVTCompoundPowerFlow",
    "CVTPulleyCompoundPowerFlow",
    "CycloidalAssemblyCompoundPowerFlow",
    "CycloidalDiscCentralBearingConnectionCompoundPowerFlow",
    "CycloidalDiscCompoundPowerFlow",
    "CycloidalDiscPlanetaryBearingConnectionCompoundPowerFlow",
    "CylindricalGearCompoundPowerFlow",
    "CylindricalGearMeshCompoundPowerFlow",
    "CylindricalGearSetCompoundPowerFlow",
    "CylindricalPlanetGearCompoundPowerFlow",
    "DatumCompoundPowerFlow",
    "ExternalCADModelCompoundPowerFlow",
    "FaceGearCompoundPowerFlow",
    "FaceGearMeshCompoundPowerFlow",
    "FaceGearSetCompoundPowerFlow",
    "FEPartCompoundPowerFlow",
    "FlexiblePinAssemblyCompoundPowerFlow",
    "GearCompoundPowerFlow",
    "GearMeshCompoundPowerFlow",
    "GearSetCompoundPowerFlow",
    "GuideDxfModelCompoundPowerFlow",
    "HypoidGearCompoundPowerFlow",
    "HypoidGearMeshCompoundPowerFlow",
    "HypoidGearSetCompoundPowerFlow",
    "InterMountableComponentConnectionCompoundPowerFlow",
    "KlingelnbergCycloPalloidConicalGearCompoundPowerFlow",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow",
    "KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow",
    "KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow",
    "MassDiscCompoundPowerFlow",
    "MeasurementComponentCompoundPowerFlow",
    "MountableComponentCompoundPowerFlow",
    "OilSealCompoundPowerFlow",
    "PartCompoundPowerFlow",
    "PartToPartShearCouplingCompoundPowerFlow",
    "PartToPartShearCouplingConnectionCompoundPowerFlow",
    "PartToPartShearCouplingHalfCompoundPowerFlow",
    "PlanetaryConnectionCompoundPowerFlow",
    "PlanetaryGearSetCompoundPowerFlow",
    "PlanetCarrierCompoundPowerFlow",
    "PointLoadCompoundPowerFlow",
    "PowerLoadCompoundPowerFlow",
    "PulleyCompoundPowerFlow",
    "RingPinsCompoundPowerFlow",
    "RingPinsToDiscConnectionCompoundPowerFlow",
    "RollingRingAssemblyCompoundPowerFlow",
    "RollingRingCompoundPowerFlow",
    "RollingRingConnectionCompoundPowerFlow",
    "RootAssemblyCompoundPowerFlow",
    "ShaftCompoundPowerFlow",
    "ShaftHubConnectionCompoundPowerFlow",
    "ShaftToMountableComponentConnectionCompoundPowerFlow",
    "SpecialisedAssemblyCompoundPowerFlow",
    "SpiralBevelGearCompoundPowerFlow",
    "SpiralBevelGearMeshCompoundPowerFlow",
    "SpiralBevelGearSetCompoundPowerFlow",
    "SpringDamperCompoundPowerFlow",
    "SpringDamperConnectionCompoundPowerFlow",
    "SpringDamperHalfCompoundPowerFlow",
    "StraightBevelDiffGearCompoundPowerFlow",
    "StraightBevelDiffGearMeshCompoundPowerFlow",
    "StraightBevelDiffGearSetCompoundPowerFlow",
    "StraightBevelGearCompoundPowerFlow",
    "StraightBevelGearMeshCompoundPowerFlow",
    "StraightBevelGearSetCompoundPowerFlow",
    "StraightBevelPlanetGearCompoundPowerFlow",
    "StraightBevelSunGearCompoundPowerFlow",
    "SynchroniserCompoundPowerFlow",
    "SynchroniserHalfCompoundPowerFlow",
    "SynchroniserPartCompoundPowerFlow",
    "SynchroniserSleeveCompoundPowerFlow",
    "TorqueConverterCompoundPowerFlow",
    "TorqueConverterConnectionCompoundPowerFlow",
    "TorqueConverterPumpCompoundPowerFlow",
    "TorqueConverterTurbineCompoundPowerFlow",
    "UnbalancedMassCompoundPowerFlow",
    "VirtualComponentCompoundPowerFlow",
    "WormGearCompoundPowerFlow",
    "WormGearMeshCompoundPowerFlow",
    "WormGearSetCompoundPowerFlow",
    "ZerolBevelGearCompoundPowerFlow",
    "ZerolBevelGearMeshCompoundPowerFlow",
    "ZerolBevelGearSetCompoundPowerFlow",
)
