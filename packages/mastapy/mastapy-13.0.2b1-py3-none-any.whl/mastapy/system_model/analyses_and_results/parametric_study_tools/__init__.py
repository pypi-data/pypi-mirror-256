"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._4298 import AbstractAssemblyParametricStudyTool
    from ._4299 import AbstractShaftOrHousingParametricStudyTool
    from ._4300 import AbstractShaftParametricStudyTool
    from ._4301 import AbstractShaftToMountableComponentConnectionParametricStudyTool
    from ._4302 import AGMAGleasonConicalGearMeshParametricStudyTool
    from ._4303 import AGMAGleasonConicalGearParametricStudyTool
    from ._4304 import AGMAGleasonConicalGearSetParametricStudyTool
    from ._4305 import AssemblyParametricStudyTool
    from ._4306 import BearingParametricStudyTool
    from ._4307 import BeltConnectionParametricStudyTool
    from ._4308 import BeltDriveParametricStudyTool
    from ._4309 import BevelDifferentialGearMeshParametricStudyTool
    from ._4310 import BevelDifferentialGearParametricStudyTool
    from ._4311 import BevelDifferentialGearSetParametricStudyTool
    from ._4312 import BevelDifferentialPlanetGearParametricStudyTool
    from ._4313 import BevelDifferentialSunGearParametricStudyTool
    from ._4314 import BevelGearMeshParametricStudyTool
    from ._4315 import BevelGearParametricStudyTool
    from ._4316 import BevelGearSetParametricStudyTool
    from ._4317 import BoltedJointParametricStudyTool
    from ._4318 import BoltParametricStudyTool
    from ._4319 import ClutchConnectionParametricStudyTool
    from ._4320 import ClutchHalfParametricStudyTool
    from ._4321 import ClutchParametricStudyTool
    from ._4322 import CoaxialConnectionParametricStudyTool
    from ._4323 import ComponentParametricStudyTool
    from ._4324 import ConceptCouplingConnectionParametricStudyTool
    from ._4325 import ConceptCouplingHalfParametricStudyTool
    from ._4326 import ConceptCouplingParametricStudyTool
    from ._4327 import ConceptGearMeshParametricStudyTool
    from ._4328 import ConceptGearParametricStudyTool
    from ._4329 import ConceptGearSetParametricStudyTool
    from ._4330 import ConicalGearMeshParametricStudyTool
    from ._4331 import ConicalGearParametricStudyTool
    from ._4332 import ConicalGearSetParametricStudyTool
    from ._4333 import ConnectionParametricStudyTool
    from ._4334 import ConnectorParametricStudyTool
    from ._4335 import CouplingConnectionParametricStudyTool
    from ._4336 import CouplingHalfParametricStudyTool
    from ._4337 import CouplingParametricStudyTool
    from ._4338 import CVTBeltConnectionParametricStudyTool
    from ._4339 import CVTParametricStudyTool
    from ._4340 import CVTPulleyParametricStudyTool
    from ._4341 import CycloidalAssemblyParametricStudyTool
    from ._4342 import CycloidalDiscCentralBearingConnectionParametricStudyTool
    from ._4343 import CycloidalDiscParametricStudyTool
    from ._4344 import CycloidalDiscPlanetaryBearingConnectionParametricStudyTool
    from ._4345 import CylindricalGearMeshParametricStudyTool
    from ._4346 import CylindricalGearParametricStudyTool
    from ._4347 import CylindricalGearSetParametricStudyTool
    from ._4348 import CylindricalPlanetGearParametricStudyTool
    from ._4349 import DatumParametricStudyTool
    from ._4350 import DesignOfExperimentsVariableSetter
    from ._4351 import DoeValueSpecificationOption
    from ._4352 import DutyCycleResultsForAllComponents
    from ._4353 import DutyCycleResultsForAllGearSets
    from ._4354 import DutyCycleResultsForRootAssembly
    from ._4355 import DutyCycleResultsForSingleBearing
    from ._4356 import DutyCycleResultsForSingleShaft
    from ._4357 import ExternalCADModelParametricStudyTool
    from ._4358 import FaceGearMeshParametricStudyTool
    from ._4359 import FaceGearParametricStudyTool
    from ._4360 import FaceGearSetParametricStudyTool
    from ._4361 import FEPartParametricStudyTool
    from ._4362 import FlexiblePinAssemblyParametricStudyTool
    from ._4363 import GearMeshParametricStudyTool
    from ._4364 import GearParametricStudyTool
    from ._4365 import GearSetParametricStudyTool
    from ._4366 import GuideDxfModelParametricStudyTool
    from ._4367 import HypoidGearMeshParametricStudyTool
    from ._4368 import HypoidGearParametricStudyTool
    from ._4369 import HypoidGearSetParametricStudyTool
    from ._4370 import InterMountableComponentConnectionParametricStudyTool
    from ._4371 import KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
    from ._4372 import KlingelnbergCycloPalloidConicalGearParametricStudyTool
    from ._4373 import KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
    from ._4374 import KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool
    from ._4375 import KlingelnbergCycloPalloidHypoidGearParametricStudyTool
    from ._4376 import KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
    from ._4377 import KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool
    from ._4378 import KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
    from ._4379 import KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
    from ._4380 import MassDiscParametricStudyTool
    from ._4381 import MeasurementComponentParametricStudyTool
    from ._4382 import MonteCarloDistribution
    from ._4383 import MountableComponentParametricStudyTool
    from ._4384 import OilSealParametricStudyTool
    from ._4385 import ParametricStudyDimension
    from ._4386 import ParametricStudyDOEResultVariable
    from ._4387 import ParametricStudyDOEResultVariableForParallelCoordinatesPlot
    from ._4388 import ParametricStudyHistogram
    from ._4389 import ParametricStudyStaticLoad
    from ._4390 import ParametricStudyTool
    from ._4391 import ParametricStudyToolOptions
    from ._4392 import ParametricStudyToolResultsForReporting
    from ._4393 import ParametricStudyToolStepResult
    from ._4394 import ParametricStudyVariable
    from ._4395 import PartParametricStudyTool
    from ._4396 import PartToPartShearCouplingConnectionParametricStudyTool
    from ._4397 import PartToPartShearCouplingHalfParametricStudyTool
    from ._4398 import PartToPartShearCouplingParametricStudyTool
    from ._4399 import PlanetaryConnectionParametricStudyTool
    from ._4400 import PlanetaryGearSetParametricStudyTool
    from ._4401 import PlanetCarrierParametricStudyTool
    from ._4402 import PointLoadParametricStudyTool
    from ._4403 import PowerLoadParametricStudyTool
    from ._4404 import PulleyParametricStudyTool
    from ._4405 import RingPinsParametricStudyTool
    from ._4406 import RingPinsToDiscConnectionParametricStudyTool
    from ._4407 import RollingRingAssemblyParametricStudyTool
    from ._4408 import RollingRingConnectionParametricStudyTool
    from ._4409 import RollingRingParametricStudyTool
    from ._4410 import RootAssemblyParametricStudyTool
    from ._4411 import ShaftHubConnectionParametricStudyTool
    from ._4412 import ShaftParametricStudyTool
    from ._4413 import ShaftToMountableComponentConnectionParametricStudyTool
    from ._4414 import SpecialisedAssemblyParametricStudyTool
    from ._4415 import SpiralBevelGearMeshParametricStudyTool
    from ._4416 import SpiralBevelGearParametricStudyTool
    from ._4417 import SpiralBevelGearSetParametricStudyTool
    from ._4418 import SpringDamperConnectionParametricStudyTool
    from ._4419 import SpringDamperHalfParametricStudyTool
    from ._4420 import SpringDamperParametricStudyTool
    from ._4421 import StraightBevelDiffGearMeshParametricStudyTool
    from ._4422 import StraightBevelDiffGearParametricStudyTool
    from ._4423 import StraightBevelDiffGearSetParametricStudyTool
    from ._4424 import StraightBevelGearMeshParametricStudyTool
    from ._4425 import StraightBevelGearParametricStudyTool
    from ._4426 import StraightBevelGearSetParametricStudyTool
    from ._4427 import StraightBevelPlanetGearParametricStudyTool
    from ._4428 import StraightBevelSunGearParametricStudyTool
    from ._4429 import SynchroniserHalfParametricStudyTool
    from ._4430 import SynchroniserParametricStudyTool
    from ._4431 import SynchroniserPartParametricStudyTool
    from ._4432 import SynchroniserSleeveParametricStudyTool
    from ._4433 import TorqueConverterConnectionParametricStudyTool
    from ._4434 import TorqueConverterParametricStudyTool
    from ._4435 import TorqueConverterPumpParametricStudyTool
    from ._4436 import TorqueConverterTurbineParametricStudyTool
    from ._4437 import UnbalancedMassParametricStudyTool
    from ._4438 import VirtualComponentParametricStudyTool
    from ._4439 import WormGearMeshParametricStudyTool
    from ._4440 import WormGearParametricStudyTool
    from ._4441 import WormGearSetParametricStudyTool
    from ._4442 import ZerolBevelGearMeshParametricStudyTool
    from ._4443 import ZerolBevelGearParametricStudyTool
    from ._4444 import ZerolBevelGearSetParametricStudyTool
else:
    import_structure = {
        "_4298": ["AbstractAssemblyParametricStudyTool"],
        "_4299": ["AbstractShaftOrHousingParametricStudyTool"],
        "_4300": ["AbstractShaftParametricStudyTool"],
        "_4301": ["AbstractShaftToMountableComponentConnectionParametricStudyTool"],
        "_4302": ["AGMAGleasonConicalGearMeshParametricStudyTool"],
        "_4303": ["AGMAGleasonConicalGearParametricStudyTool"],
        "_4304": ["AGMAGleasonConicalGearSetParametricStudyTool"],
        "_4305": ["AssemblyParametricStudyTool"],
        "_4306": ["BearingParametricStudyTool"],
        "_4307": ["BeltConnectionParametricStudyTool"],
        "_4308": ["BeltDriveParametricStudyTool"],
        "_4309": ["BevelDifferentialGearMeshParametricStudyTool"],
        "_4310": ["BevelDifferentialGearParametricStudyTool"],
        "_4311": ["BevelDifferentialGearSetParametricStudyTool"],
        "_4312": ["BevelDifferentialPlanetGearParametricStudyTool"],
        "_4313": ["BevelDifferentialSunGearParametricStudyTool"],
        "_4314": ["BevelGearMeshParametricStudyTool"],
        "_4315": ["BevelGearParametricStudyTool"],
        "_4316": ["BevelGearSetParametricStudyTool"],
        "_4317": ["BoltedJointParametricStudyTool"],
        "_4318": ["BoltParametricStudyTool"],
        "_4319": ["ClutchConnectionParametricStudyTool"],
        "_4320": ["ClutchHalfParametricStudyTool"],
        "_4321": ["ClutchParametricStudyTool"],
        "_4322": ["CoaxialConnectionParametricStudyTool"],
        "_4323": ["ComponentParametricStudyTool"],
        "_4324": ["ConceptCouplingConnectionParametricStudyTool"],
        "_4325": ["ConceptCouplingHalfParametricStudyTool"],
        "_4326": ["ConceptCouplingParametricStudyTool"],
        "_4327": ["ConceptGearMeshParametricStudyTool"],
        "_4328": ["ConceptGearParametricStudyTool"],
        "_4329": ["ConceptGearSetParametricStudyTool"],
        "_4330": ["ConicalGearMeshParametricStudyTool"],
        "_4331": ["ConicalGearParametricStudyTool"],
        "_4332": ["ConicalGearSetParametricStudyTool"],
        "_4333": ["ConnectionParametricStudyTool"],
        "_4334": ["ConnectorParametricStudyTool"],
        "_4335": ["CouplingConnectionParametricStudyTool"],
        "_4336": ["CouplingHalfParametricStudyTool"],
        "_4337": ["CouplingParametricStudyTool"],
        "_4338": ["CVTBeltConnectionParametricStudyTool"],
        "_4339": ["CVTParametricStudyTool"],
        "_4340": ["CVTPulleyParametricStudyTool"],
        "_4341": ["CycloidalAssemblyParametricStudyTool"],
        "_4342": ["CycloidalDiscCentralBearingConnectionParametricStudyTool"],
        "_4343": ["CycloidalDiscParametricStudyTool"],
        "_4344": ["CycloidalDiscPlanetaryBearingConnectionParametricStudyTool"],
        "_4345": ["CylindricalGearMeshParametricStudyTool"],
        "_4346": ["CylindricalGearParametricStudyTool"],
        "_4347": ["CylindricalGearSetParametricStudyTool"],
        "_4348": ["CylindricalPlanetGearParametricStudyTool"],
        "_4349": ["DatumParametricStudyTool"],
        "_4350": ["DesignOfExperimentsVariableSetter"],
        "_4351": ["DoeValueSpecificationOption"],
        "_4352": ["DutyCycleResultsForAllComponents"],
        "_4353": ["DutyCycleResultsForAllGearSets"],
        "_4354": ["DutyCycleResultsForRootAssembly"],
        "_4355": ["DutyCycleResultsForSingleBearing"],
        "_4356": ["DutyCycleResultsForSingleShaft"],
        "_4357": ["ExternalCADModelParametricStudyTool"],
        "_4358": ["FaceGearMeshParametricStudyTool"],
        "_4359": ["FaceGearParametricStudyTool"],
        "_4360": ["FaceGearSetParametricStudyTool"],
        "_4361": ["FEPartParametricStudyTool"],
        "_4362": ["FlexiblePinAssemblyParametricStudyTool"],
        "_4363": ["GearMeshParametricStudyTool"],
        "_4364": ["GearParametricStudyTool"],
        "_4365": ["GearSetParametricStudyTool"],
        "_4366": ["GuideDxfModelParametricStudyTool"],
        "_4367": ["HypoidGearMeshParametricStudyTool"],
        "_4368": ["HypoidGearParametricStudyTool"],
        "_4369": ["HypoidGearSetParametricStudyTool"],
        "_4370": ["InterMountableComponentConnectionParametricStudyTool"],
        "_4371": ["KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool"],
        "_4372": ["KlingelnbergCycloPalloidConicalGearParametricStudyTool"],
        "_4373": ["KlingelnbergCycloPalloidConicalGearSetParametricStudyTool"],
        "_4374": ["KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool"],
        "_4375": ["KlingelnbergCycloPalloidHypoidGearParametricStudyTool"],
        "_4376": ["KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool"],
        "_4377": ["KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool"],
        "_4378": ["KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool"],
        "_4379": ["KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool"],
        "_4380": ["MassDiscParametricStudyTool"],
        "_4381": ["MeasurementComponentParametricStudyTool"],
        "_4382": ["MonteCarloDistribution"],
        "_4383": ["MountableComponentParametricStudyTool"],
        "_4384": ["OilSealParametricStudyTool"],
        "_4385": ["ParametricStudyDimension"],
        "_4386": ["ParametricStudyDOEResultVariable"],
        "_4387": ["ParametricStudyDOEResultVariableForParallelCoordinatesPlot"],
        "_4388": ["ParametricStudyHistogram"],
        "_4389": ["ParametricStudyStaticLoad"],
        "_4390": ["ParametricStudyTool"],
        "_4391": ["ParametricStudyToolOptions"],
        "_4392": ["ParametricStudyToolResultsForReporting"],
        "_4393": ["ParametricStudyToolStepResult"],
        "_4394": ["ParametricStudyVariable"],
        "_4395": ["PartParametricStudyTool"],
        "_4396": ["PartToPartShearCouplingConnectionParametricStudyTool"],
        "_4397": ["PartToPartShearCouplingHalfParametricStudyTool"],
        "_4398": ["PartToPartShearCouplingParametricStudyTool"],
        "_4399": ["PlanetaryConnectionParametricStudyTool"],
        "_4400": ["PlanetaryGearSetParametricStudyTool"],
        "_4401": ["PlanetCarrierParametricStudyTool"],
        "_4402": ["PointLoadParametricStudyTool"],
        "_4403": ["PowerLoadParametricStudyTool"],
        "_4404": ["PulleyParametricStudyTool"],
        "_4405": ["RingPinsParametricStudyTool"],
        "_4406": ["RingPinsToDiscConnectionParametricStudyTool"],
        "_4407": ["RollingRingAssemblyParametricStudyTool"],
        "_4408": ["RollingRingConnectionParametricStudyTool"],
        "_4409": ["RollingRingParametricStudyTool"],
        "_4410": ["RootAssemblyParametricStudyTool"],
        "_4411": ["ShaftHubConnectionParametricStudyTool"],
        "_4412": ["ShaftParametricStudyTool"],
        "_4413": ["ShaftToMountableComponentConnectionParametricStudyTool"],
        "_4414": ["SpecialisedAssemblyParametricStudyTool"],
        "_4415": ["SpiralBevelGearMeshParametricStudyTool"],
        "_4416": ["SpiralBevelGearParametricStudyTool"],
        "_4417": ["SpiralBevelGearSetParametricStudyTool"],
        "_4418": ["SpringDamperConnectionParametricStudyTool"],
        "_4419": ["SpringDamperHalfParametricStudyTool"],
        "_4420": ["SpringDamperParametricStudyTool"],
        "_4421": ["StraightBevelDiffGearMeshParametricStudyTool"],
        "_4422": ["StraightBevelDiffGearParametricStudyTool"],
        "_4423": ["StraightBevelDiffGearSetParametricStudyTool"],
        "_4424": ["StraightBevelGearMeshParametricStudyTool"],
        "_4425": ["StraightBevelGearParametricStudyTool"],
        "_4426": ["StraightBevelGearSetParametricStudyTool"],
        "_4427": ["StraightBevelPlanetGearParametricStudyTool"],
        "_4428": ["StraightBevelSunGearParametricStudyTool"],
        "_4429": ["SynchroniserHalfParametricStudyTool"],
        "_4430": ["SynchroniserParametricStudyTool"],
        "_4431": ["SynchroniserPartParametricStudyTool"],
        "_4432": ["SynchroniserSleeveParametricStudyTool"],
        "_4433": ["TorqueConverterConnectionParametricStudyTool"],
        "_4434": ["TorqueConverterParametricStudyTool"],
        "_4435": ["TorqueConverterPumpParametricStudyTool"],
        "_4436": ["TorqueConverterTurbineParametricStudyTool"],
        "_4437": ["UnbalancedMassParametricStudyTool"],
        "_4438": ["VirtualComponentParametricStudyTool"],
        "_4439": ["WormGearMeshParametricStudyTool"],
        "_4440": ["WormGearParametricStudyTool"],
        "_4441": ["WormGearSetParametricStudyTool"],
        "_4442": ["ZerolBevelGearMeshParametricStudyTool"],
        "_4443": ["ZerolBevelGearParametricStudyTool"],
        "_4444": ["ZerolBevelGearSetParametricStudyTool"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyParametricStudyTool",
    "AbstractShaftOrHousingParametricStudyTool",
    "AbstractShaftParametricStudyTool",
    "AbstractShaftToMountableComponentConnectionParametricStudyTool",
    "AGMAGleasonConicalGearMeshParametricStudyTool",
    "AGMAGleasonConicalGearParametricStudyTool",
    "AGMAGleasonConicalGearSetParametricStudyTool",
    "AssemblyParametricStudyTool",
    "BearingParametricStudyTool",
    "BeltConnectionParametricStudyTool",
    "BeltDriveParametricStudyTool",
    "BevelDifferentialGearMeshParametricStudyTool",
    "BevelDifferentialGearParametricStudyTool",
    "BevelDifferentialGearSetParametricStudyTool",
    "BevelDifferentialPlanetGearParametricStudyTool",
    "BevelDifferentialSunGearParametricStudyTool",
    "BevelGearMeshParametricStudyTool",
    "BevelGearParametricStudyTool",
    "BevelGearSetParametricStudyTool",
    "BoltedJointParametricStudyTool",
    "BoltParametricStudyTool",
    "ClutchConnectionParametricStudyTool",
    "ClutchHalfParametricStudyTool",
    "ClutchParametricStudyTool",
    "CoaxialConnectionParametricStudyTool",
    "ComponentParametricStudyTool",
    "ConceptCouplingConnectionParametricStudyTool",
    "ConceptCouplingHalfParametricStudyTool",
    "ConceptCouplingParametricStudyTool",
    "ConceptGearMeshParametricStudyTool",
    "ConceptGearParametricStudyTool",
    "ConceptGearSetParametricStudyTool",
    "ConicalGearMeshParametricStudyTool",
    "ConicalGearParametricStudyTool",
    "ConicalGearSetParametricStudyTool",
    "ConnectionParametricStudyTool",
    "ConnectorParametricStudyTool",
    "CouplingConnectionParametricStudyTool",
    "CouplingHalfParametricStudyTool",
    "CouplingParametricStudyTool",
    "CVTBeltConnectionParametricStudyTool",
    "CVTParametricStudyTool",
    "CVTPulleyParametricStudyTool",
    "CycloidalAssemblyParametricStudyTool",
    "CycloidalDiscCentralBearingConnectionParametricStudyTool",
    "CycloidalDiscParametricStudyTool",
    "CycloidalDiscPlanetaryBearingConnectionParametricStudyTool",
    "CylindricalGearMeshParametricStudyTool",
    "CylindricalGearParametricStudyTool",
    "CylindricalGearSetParametricStudyTool",
    "CylindricalPlanetGearParametricStudyTool",
    "DatumParametricStudyTool",
    "DesignOfExperimentsVariableSetter",
    "DoeValueSpecificationOption",
    "DutyCycleResultsForAllComponents",
    "DutyCycleResultsForAllGearSets",
    "DutyCycleResultsForRootAssembly",
    "DutyCycleResultsForSingleBearing",
    "DutyCycleResultsForSingleShaft",
    "ExternalCADModelParametricStudyTool",
    "FaceGearMeshParametricStudyTool",
    "FaceGearParametricStudyTool",
    "FaceGearSetParametricStudyTool",
    "FEPartParametricStudyTool",
    "FlexiblePinAssemblyParametricStudyTool",
    "GearMeshParametricStudyTool",
    "GearParametricStudyTool",
    "GearSetParametricStudyTool",
    "GuideDxfModelParametricStudyTool",
    "HypoidGearMeshParametricStudyTool",
    "HypoidGearParametricStudyTool",
    "HypoidGearSetParametricStudyTool",
    "InterMountableComponentConnectionParametricStudyTool",
    "KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool",
    "KlingelnbergCycloPalloidConicalGearParametricStudyTool",
    "KlingelnbergCycloPalloidConicalGearSetParametricStudyTool",
    "KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool",
    "KlingelnbergCycloPalloidHypoidGearParametricStudyTool",
    "KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool",
    "KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool",
    "KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool",
    "MassDiscParametricStudyTool",
    "MeasurementComponentParametricStudyTool",
    "MonteCarloDistribution",
    "MountableComponentParametricStudyTool",
    "OilSealParametricStudyTool",
    "ParametricStudyDimension",
    "ParametricStudyDOEResultVariable",
    "ParametricStudyDOEResultVariableForParallelCoordinatesPlot",
    "ParametricStudyHistogram",
    "ParametricStudyStaticLoad",
    "ParametricStudyTool",
    "ParametricStudyToolOptions",
    "ParametricStudyToolResultsForReporting",
    "ParametricStudyToolStepResult",
    "ParametricStudyVariable",
    "PartParametricStudyTool",
    "PartToPartShearCouplingConnectionParametricStudyTool",
    "PartToPartShearCouplingHalfParametricStudyTool",
    "PartToPartShearCouplingParametricStudyTool",
    "PlanetaryConnectionParametricStudyTool",
    "PlanetaryGearSetParametricStudyTool",
    "PlanetCarrierParametricStudyTool",
    "PointLoadParametricStudyTool",
    "PowerLoadParametricStudyTool",
    "PulleyParametricStudyTool",
    "RingPinsParametricStudyTool",
    "RingPinsToDiscConnectionParametricStudyTool",
    "RollingRingAssemblyParametricStudyTool",
    "RollingRingConnectionParametricStudyTool",
    "RollingRingParametricStudyTool",
    "RootAssemblyParametricStudyTool",
    "ShaftHubConnectionParametricStudyTool",
    "ShaftParametricStudyTool",
    "ShaftToMountableComponentConnectionParametricStudyTool",
    "SpecialisedAssemblyParametricStudyTool",
    "SpiralBevelGearMeshParametricStudyTool",
    "SpiralBevelGearParametricStudyTool",
    "SpiralBevelGearSetParametricStudyTool",
    "SpringDamperConnectionParametricStudyTool",
    "SpringDamperHalfParametricStudyTool",
    "SpringDamperParametricStudyTool",
    "StraightBevelDiffGearMeshParametricStudyTool",
    "StraightBevelDiffGearParametricStudyTool",
    "StraightBevelDiffGearSetParametricStudyTool",
    "StraightBevelGearMeshParametricStudyTool",
    "StraightBevelGearParametricStudyTool",
    "StraightBevelGearSetParametricStudyTool",
    "StraightBevelPlanetGearParametricStudyTool",
    "StraightBevelSunGearParametricStudyTool",
    "SynchroniserHalfParametricStudyTool",
    "SynchroniserParametricStudyTool",
    "SynchroniserPartParametricStudyTool",
    "SynchroniserSleeveParametricStudyTool",
    "TorqueConverterConnectionParametricStudyTool",
    "TorqueConverterParametricStudyTool",
    "TorqueConverterPumpParametricStudyTool",
    "TorqueConverterTurbineParametricStudyTool",
    "UnbalancedMassParametricStudyTool",
    "VirtualComponentParametricStudyTool",
    "WormGearMeshParametricStudyTool",
    "WormGearParametricStudyTool",
    "WormGearSetParametricStudyTool",
    "ZerolBevelGearMeshParametricStudyTool",
    "ZerolBevelGearParametricStudyTool",
    "ZerolBevelGearSetParametricStudyTool",
)
