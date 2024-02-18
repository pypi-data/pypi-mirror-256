"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5249 import AbstractAssemblyCompoundModalAnalysisAtASpeed
    from ._5250 import AbstractShaftCompoundModalAnalysisAtASpeed
    from ._5251 import AbstractShaftOrHousingCompoundModalAnalysisAtASpeed
    from ._5252 import (
        AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed,
    )
    from ._5253 import AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed
    from ._5254 import AGMAGleasonConicalGearMeshCompoundModalAnalysisAtASpeed
    from ._5255 import AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed
    from ._5256 import AssemblyCompoundModalAnalysisAtASpeed
    from ._5257 import BearingCompoundModalAnalysisAtASpeed
    from ._5258 import BeltConnectionCompoundModalAnalysisAtASpeed
    from ._5259 import BeltDriveCompoundModalAnalysisAtASpeed
    from ._5260 import BevelDifferentialGearCompoundModalAnalysisAtASpeed
    from ._5261 import BevelDifferentialGearMeshCompoundModalAnalysisAtASpeed
    from ._5262 import BevelDifferentialGearSetCompoundModalAnalysisAtASpeed
    from ._5263 import BevelDifferentialPlanetGearCompoundModalAnalysisAtASpeed
    from ._5264 import BevelDifferentialSunGearCompoundModalAnalysisAtASpeed
    from ._5265 import BevelGearCompoundModalAnalysisAtASpeed
    from ._5266 import BevelGearMeshCompoundModalAnalysisAtASpeed
    from ._5267 import BevelGearSetCompoundModalAnalysisAtASpeed
    from ._5268 import BoltCompoundModalAnalysisAtASpeed
    from ._5269 import BoltedJointCompoundModalAnalysisAtASpeed
    from ._5270 import ClutchCompoundModalAnalysisAtASpeed
    from ._5271 import ClutchConnectionCompoundModalAnalysisAtASpeed
    from ._5272 import ClutchHalfCompoundModalAnalysisAtASpeed
    from ._5273 import CoaxialConnectionCompoundModalAnalysisAtASpeed
    from ._5274 import ComponentCompoundModalAnalysisAtASpeed
    from ._5275 import ConceptCouplingCompoundModalAnalysisAtASpeed
    from ._5276 import ConceptCouplingConnectionCompoundModalAnalysisAtASpeed
    from ._5277 import ConceptCouplingHalfCompoundModalAnalysisAtASpeed
    from ._5278 import ConceptGearCompoundModalAnalysisAtASpeed
    from ._5279 import ConceptGearMeshCompoundModalAnalysisAtASpeed
    from ._5280 import ConceptGearSetCompoundModalAnalysisAtASpeed
    from ._5281 import ConicalGearCompoundModalAnalysisAtASpeed
    from ._5282 import ConicalGearMeshCompoundModalAnalysisAtASpeed
    from ._5283 import ConicalGearSetCompoundModalAnalysisAtASpeed
    from ._5284 import ConnectionCompoundModalAnalysisAtASpeed
    from ._5285 import ConnectorCompoundModalAnalysisAtASpeed
    from ._5286 import CouplingCompoundModalAnalysisAtASpeed
    from ._5287 import CouplingConnectionCompoundModalAnalysisAtASpeed
    from ._5288 import CouplingHalfCompoundModalAnalysisAtASpeed
    from ._5289 import CVTBeltConnectionCompoundModalAnalysisAtASpeed
    from ._5290 import CVTCompoundModalAnalysisAtASpeed
    from ._5291 import CVTPulleyCompoundModalAnalysisAtASpeed
    from ._5292 import CycloidalAssemblyCompoundModalAnalysisAtASpeed
    from ._5293 import (
        CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtASpeed,
    )
    from ._5294 import CycloidalDiscCompoundModalAnalysisAtASpeed
    from ._5295 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed,
    )
    from ._5296 import CylindricalGearCompoundModalAnalysisAtASpeed
    from ._5297 import CylindricalGearMeshCompoundModalAnalysisAtASpeed
    from ._5298 import CylindricalGearSetCompoundModalAnalysisAtASpeed
    from ._5299 import CylindricalPlanetGearCompoundModalAnalysisAtASpeed
    from ._5300 import DatumCompoundModalAnalysisAtASpeed
    from ._5301 import ExternalCADModelCompoundModalAnalysisAtASpeed
    from ._5302 import FaceGearCompoundModalAnalysisAtASpeed
    from ._5303 import FaceGearMeshCompoundModalAnalysisAtASpeed
    from ._5304 import FaceGearSetCompoundModalAnalysisAtASpeed
    from ._5305 import FEPartCompoundModalAnalysisAtASpeed
    from ._5306 import FlexiblePinAssemblyCompoundModalAnalysisAtASpeed
    from ._5307 import GearCompoundModalAnalysisAtASpeed
    from ._5308 import GearMeshCompoundModalAnalysisAtASpeed
    from ._5309 import GearSetCompoundModalAnalysisAtASpeed
    from ._5310 import GuideDxfModelCompoundModalAnalysisAtASpeed
    from ._5311 import HypoidGearCompoundModalAnalysisAtASpeed
    from ._5312 import HypoidGearMeshCompoundModalAnalysisAtASpeed
    from ._5313 import HypoidGearSetCompoundModalAnalysisAtASpeed
    from ._5314 import InterMountableComponentConnectionCompoundModalAnalysisAtASpeed
    from ._5315 import KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtASpeed
    from ._5316 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtASpeed,
    )
    from ._5317 import (
        KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed,
    )
    from ._5318 import KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed
    from ._5319 import (
        KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtASpeed,
    )
    from ._5320 import (
        KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed,
    )
    from ._5321 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed,
    )
    from ._5322 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed,
    )
    from ._5323 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed,
    )
    from ._5324 import MassDiscCompoundModalAnalysisAtASpeed
    from ._5325 import MeasurementComponentCompoundModalAnalysisAtASpeed
    from ._5326 import MountableComponentCompoundModalAnalysisAtASpeed
    from ._5327 import OilSealCompoundModalAnalysisAtASpeed
    from ._5328 import PartCompoundModalAnalysisAtASpeed
    from ._5329 import PartToPartShearCouplingCompoundModalAnalysisAtASpeed
    from ._5330 import PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed
    from ._5331 import PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed
    from ._5332 import PlanetaryConnectionCompoundModalAnalysisAtASpeed
    from ._5333 import PlanetaryGearSetCompoundModalAnalysisAtASpeed
    from ._5334 import PlanetCarrierCompoundModalAnalysisAtASpeed
    from ._5335 import PointLoadCompoundModalAnalysisAtASpeed
    from ._5336 import PowerLoadCompoundModalAnalysisAtASpeed
    from ._5337 import PulleyCompoundModalAnalysisAtASpeed
    from ._5338 import RingPinsCompoundModalAnalysisAtASpeed
    from ._5339 import RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed
    from ._5340 import RollingRingAssemblyCompoundModalAnalysisAtASpeed
    from ._5341 import RollingRingCompoundModalAnalysisAtASpeed
    from ._5342 import RollingRingConnectionCompoundModalAnalysisAtASpeed
    from ._5343 import RootAssemblyCompoundModalAnalysisAtASpeed
    from ._5344 import ShaftCompoundModalAnalysisAtASpeed
    from ._5345 import ShaftHubConnectionCompoundModalAnalysisAtASpeed
    from ._5346 import ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed
    from ._5347 import SpecialisedAssemblyCompoundModalAnalysisAtASpeed
    from ._5348 import SpiralBevelGearCompoundModalAnalysisAtASpeed
    from ._5349 import SpiralBevelGearMeshCompoundModalAnalysisAtASpeed
    from ._5350 import SpiralBevelGearSetCompoundModalAnalysisAtASpeed
    from ._5351 import SpringDamperCompoundModalAnalysisAtASpeed
    from ._5352 import SpringDamperConnectionCompoundModalAnalysisAtASpeed
    from ._5353 import SpringDamperHalfCompoundModalAnalysisAtASpeed
    from ._5354 import StraightBevelDiffGearCompoundModalAnalysisAtASpeed
    from ._5355 import StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed
    from ._5356 import StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed
    from ._5357 import StraightBevelGearCompoundModalAnalysisAtASpeed
    from ._5358 import StraightBevelGearMeshCompoundModalAnalysisAtASpeed
    from ._5359 import StraightBevelGearSetCompoundModalAnalysisAtASpeed
    from ._5360 import StraightBevelPlanetGearCompoundModalAnalysisAtASpeed
    from ._5361 import StraightBevelSunGearCompoundModalAnalysisAtASpeed
    from ._5362 import SynchroniserCompoundModalAnalysisAtASpeed
    from ._5363 import SynchroniserHalfCompoundModalAnalysisAtASpeed
    from ._5364 import SynchroniserPartCompoundModalAnalysisAtASpeed
    from ._5365 import SynchroniserSleeveCompoundModalAnalysisAtASpeed
    from ._5366 import TorqueConverterCompoundModalAnalysisAtASpeed
    from ._5367 import TorqueConverterConnectionCompoundModalAnalysisAtASpeed
    from ._5368 import TorqueConverterPumpCompoundModalAnalysisAtASpeed
    from ._5369 import TorqueConverterTurbineCompoundModalAnalysisAtASpeed
    from ._5370 import UnbalancedMassCompoundModalAnalysisAtASpeed
    from ._5371 import VirtualComponentCompoundModalAnalysisAtASpeed
    from ._5372 import WormGearCompoundModalAnalysisAtASpeed
    from ._5373 import WormGearMeshCompoundModalAnalysisAtASpeed
    from ._5374 import WormGearSetCompoundModalAnalysisAtASpeed
    from ._5375 import ZerolBevelGearCompoundModalAnalysisAtASpeed
    from ._5376 import ZerolBevelGearMeshCompoundModalAnalysisAtASpeed
    from ._5377 import ZerolBevelGearSetCompoundModalAnalysisAtASpeed
else:
    import_structure = {
        "_5249": ["AbstractAssemblyCompoundModalAnalysisAtASpeed"],
        "_5250": ["AbstractShaftCompoundModalAnalysisAtASpeed"],
        "_5251": ["AbstractShaftOrHousingCompoundModalAnalysisAtASpeed"],
        "_5252": [
            "AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed"
        ],
        "_5253": ["AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed"],
        "_5254": ["AGMAGleasonConicalGearMeshCompoundModalAnalysisAtASpeed"],
        "_5255": ["AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed"],
        "_5256": ["AssemblyCompoundModalAnalysisAtASpeed"],
        "_5257": ["BearingCompoundModalAnalysisAtASpeed"],
        "_5258": ["BeltConnectionCompoundModalAnalysisAtASpeed"],
        "_5259": ["BeltDriveCompoundModalAnalysisAtASpeed"],
        "_5260": ["BevelDifferentialGearCompoundModalAnalysisAtASpeed"],
        "_5261": ["BevelDifferentialGearMeshCompoundModalAnalysisAtASpeed"],
        "_5262": ["BevelDifferentialGearSetCompoundModalAnalysisAtASpeed"],
        "_5263": ["BevelDifferentialPlanetGearCompoundModalAnalysisAtASpeed"],
        "_5264": ["BevelDifferentialSunGearCompoundModalAnalysisAtASpeed"],
        "_5265": ["BevelGearCompoundModalAnalysisAtASpeed"],
        "_5266": ["BevelGearMeshCompoundModalAnalysisAtASpeed"],
        "_5267": ["BevelGearSetCompoundModalAnalysisAtASpeed"],
        "_5268": ["BoltCompoundModalAnalysisAtASpeed"],
        "_5269": ["BoltedJointCompoundModalAnalysisAtASpeed"],
        "_5270": ["ClutchCompoundModalAnalysisAtASpeed"],
        "_5271": ["ClutchConnectionCompoundModalAnalysisAtASpeed"],
        "_5272": ["ClutchHalfCompoundModalAnalysisAtASpeed"],
        "_5273": ["CoaxialConnectionCompoundModalAnalysisAtASpeed"],
        "_5274": ["ComponentCompoundModalAnalysisAtASpeed"],
        "_5275": ["ConceptCouplingCompoundModalAnalysisAtASpeed"],
        "_5276": ["ConceptCouplingConnectionCompoundModalAnalysisAtASpeed"],
        "_5277": ["ConceptCouplingHalfCompoundModalAnalysisAtASpeed"],
        "_5278": ["ConceptGearCompoundModalAnalysisAtASpeed"],
        "_5279": ["ConceptGearMeshCompoundModalAnalysisAtASpeed"],
        "_5280": ["ConceptGearSetCompoundModalAnalysisAtASpeed"],
        "_5281": ["ConicalGearCompoundModalAnalysisAtASpeed"],
        "_5282": ["ConicalGearMeshCompoundModalAnalysisAtASpeed"],
        "_5283": ["ConicalGearSetCompoundModalAnalysisAtASpeed"],
        "_5284": ["ConnectionCompoundModalAnalysisAtASpeed"],
        "_5285": ["ConnectorCompoundModalAnalysisAtASpeed"],
        "_5286": ["CouplingCompoundModalAnalysisAtASpeed"],
        "_5287": ["CouplingConnectionCompoundModalAnalysisAtASpeed"],
        "_5288": ["CouplingHalfCompoundModalAnalysisAtASpeed"],
        "_5289": ["CVTBeltConnectionCompoundModalAnalysisAtASpeed"],
        "_5290": ["CVTCompoundModalAnalysisAtASpeed"],
        "_5291": ["CVTPulleyCompoundModalAnalysisAtASpeed"],
        "_5292": ["CycloidalAssemblyCompoundModalAnalysisAtASpeed"],
        "_5293": ["CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtASpeed"],
        "_5294": ["CycloidalDiscCompoundModalAnalysisAtASpeed"],
        "_5295": [
            "CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed"
        ],
        "_5296": ["CylindricalGearCompoundModalAnalysisAtASpeed"],
        "_5297": ["CylindricalGearMeshCompoundModalAnalysisAtASpeed"],
        "_5298": ["CylindricalGearSetCompoundModalAnalysisAtASpeed"],
        "_5299": ["CylindricalPlanetGearCompoundModalAnalysisAtASpeed"],
        "_5300": ["DatumCompoundModalAnalysisAtASpeed"],
        "_5301": ["ExternalCADModelCompoundModalAnalysisAtASpeed"],
        "_5302": ["FaceGearCompoundModalAnalysisAtASpeed"],
        "_5303": ["FaceGearMeshCompoundModalAnalysisAtASpeed"],
        "_5304": ["FaceGearSetCompoundModalAnalysisAtASpeed"],
        "_5305": ["FEPartCompoundModalAnalysisAtASpeed"],
        "_5306": ["FlexiblePinAssemblyCompoundModalAnalysisAtASpeed"],
        "_5307": ["GearCompoundModalAnalysisAtASpeed"],
        "_5308": ["GearMeshCompoundModalAnalysisAtASpeed"],
        "_5309": ["GearSetCompoundModalAnalysisAtASpeed"],
        "_5310": ["GuideDxfModelCompoundModalAnalysisAtASpeed"],
        "_5311": ["HypoidGearCompoundModalAnalysisAtASpeed"],
        "_5312": ["HypoidGearMeshCompoundModalAnalysisAtASpeed"],
        "_5313": ["HypoidGearSetCompoundModalAnalysisAtASpeed"],
        "_5314": ["InterMountableComponentConnectionCompoundModalAnalysisAtASpeed"],
        "_5315": ["KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtASpeed"],
        "_5316": [
            "KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtASpeed"
        ],
        "_5317": [
            "KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed"
        ],
        "_5318": ["KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed"],
        "_5319": [
            "KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtASpeed"
        ],
        "_5320": ["KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed"],
        "_5321": [
            "KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed"
        ],
        "_5322": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed"
        ],
        "_5323": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed"
        ],
        "_5324": ["MassDiscCompoundModalAnalysisAtASpeed"],
        "_5325": ["MeasurementComponentCompoundModalAnalysisAtASpeed"],
        "_5326": ["MountableComponentCompoundModalAnalysisAtASpeed"],
        "_5327": ["OilSealCompoundModalAnalysisAtASpeed"],
        "_5328": ["PartCompoundModalAnalysisAtASpeed"],
        "_5329": ["PartToPartShearCouplingCompoundModalAnalysisAtASpeed"],
        "_5330": ["PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed"],
        "_5331": ["PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed"],
        "_5332": ["PlanetaryConnectionCompoundModalAnalysisAtASpeed"],
        "_5333": ["PlanetaryGearSetCompoundModalAnalysisAtASpeed"],
        "_5334": ["PlanetCarrierCompoundModalAnalysisAtASpeed"],
        "_5335": ["PointLoadCompoundModalAnalysisAtASpeed"],
        "_5336": ["PowerLoadCompoundModalAnalysisAtASpeed"],
        "_5337": ["PulleyCompoundModalAnalysisAtASpeed"],
        "_5338": ["RingPinsCompoundModalAnalysisAtASpeed"],
        "_5339": ["RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed"],
        "_5340": ["RollingRingAssemblyCompoundModalAnalysisAtASpeed"],
        "_5341": ["RollingRingCompoundModalAnalysisAtASpeed"],
        "_5342": ["RollingRingConnectionCompoundModalAnalysisAtASpeed"],
        "_5343": ["RootAssemblyCompoundModalAnalysisAtASpeed"],
        "_5344": ["ShaftCompoundModalAnalysisAtASpeed"],
        "_5345": ["ShaftHubConnectionCompoundModalAnalysisAtASpeed"],
        "_5346": ["ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed"],
        "_5347": ["SpecialisedAssemblyCompoundModalAnalysisAtASpeed"],
        "_5348": ["SpiralBevelGearCompoundModalAnalysisAtASpeed"],
        "_5349": ["SpiralBevelGearMeshCompoundModalAnalysisAtASpeed"],
        "_5350": ["SpiralBevelGearSetCompoundModalAnalysisAtASpeed"],
        "_5351": ["SpringDamperCompoundModalAnalysisAtASpeed"],
        "_5352": ["SpringDamperConnectionCompoundModalAnalysisAtASpeed"],
        "_5353": ["SpringDamperHalfCompoundModalAnalysisAtASpeed"],
        "_5354": ["StraightBevelDiffGearCompoundModalAnalysisAtASpeed"],
        "_5355": ["StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed"],
        "_5356": ["StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed"],
        "_5357": ["StraightBevelGearCompoundModalAnalysisAtASpeed"],
        "_5358": ["StraightBevelGearMeshCompoundModalAnalysisAtASpeed"],
        "_5359": ["StraightBevelGearSetCompoundModalAnalysisAtASpeed"],
        "_5360": ["StraightBevelPlanetGearCompoundModalAnalysisAtASpeed"],
        "_5361": ["StraightBevelSunGearCompoundModalAnalysisAtASpeed"],
        "_5362": ["SynchroniserCompoundModalAnalysisAtASpeed"],
        "_5363": ["SynchroniserHalfCompoundModalAnalysisAtASpeed"],
        "_5364": ["SynchroniserPartCompoundModalAnalysisAtASpeed"],
        "_5365": ["SynchroniserSleeveCompoundModalAnalysisAtASpeed"],
        "_5366": ["TorqueConverterCompoundModalAnalysisAtASpeed"],
        "_5367": ["TorqueConverterConnectionCompoundModalAnalysisAtASpeed"],
        "_5368": ["TorqueConverterPumpCompoundModalAnalysisAtASpeed"],
        "_5369": ["TorqueConverterTurbineCompoundModalAnalysisAtASpeed"],
        "_5370": ["UnbalancedMassCompoundModalAnalysisAtASpeed"],
        "_5371": ["VirtualComponentCompoundModalAnalysisAtASpeed"],
        "_5372": ["WormGearCompoundModalAnalysisAtASpeed"],
        "_5373": ["WormGearMeshCompoundModalAnalysisAtASpeed"],
        "_5374": ["WormGearSetCompoundModalAnalysisAtASpeed"],
        "_5375": ["ZerolBevelGearCompoundModalAnalysisAtASpeed"],
        "_5376": ["ZerolBevelGearMeshCompoundModalAnalysisAtASpeed"],
        "_5377": ["ZerolBevelGearSetCompoundModalAnalysisAtASpeed"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundModalAnalysisAtASpeed",
    "AbstractShaftCompoundModalAnalysisAtASpeed",
    "AbstractShaftOrHousingCompoundModalAnalysisAtASpeed",
    "AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed",
    "AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed",
    "AGMAGleasonConicalGearMeshCompoundModalAnalysisAtASpeed",
    "AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed",
    "AssemblyCompoundModalAnalysisAtASpeed",
    "BearingCompoundModalAnalysisAtASpeed",
    "BeltConnectionCompoundModalAnalysisAtASpeed",
    "BeltDriveCompoundModalAnalysisAtASpeed",
    "BevelDifferentialGearCompoundModalAnalysisAtASpeed",
    "BevelDifferentialGearMeshCompoundModalAnalysisAtASpeed",
    "BevelDifferentialGearSetCompoundModalAnalysisAtASpeed",
    "BevelDifferentialPlanetGearCompoundModalAnalysisAtASpeed",
    "BevelDifferentialSunGearCompoundModalAnalysisAtASpeed",
    "BevelGearCompoundModalAnalysisAtASpeed",
    "BevelGearMeshCompoundModalAnalysisAtASpeed",
    "BevelGearSetCompoundModalAnalysisAtASpeed",
    "BoltCompoundModalAnalysisAtASpeed",
    "BoltedJointCompoundModalAnalysisAtASpeed",
    "ClutchCompoundModalAnalysisAtASpeed",
    "ClutchConnectionCompoundModalAnalysisAtASpeed",
    "ClutchHalfCompoundModalAnalysisAtASpeed",
    "CoaxialConnectionCompoundModalAnalysisAtASpeed",
    "ComponentCompoundModalAnalysisAtASpeed",
    "ConceptCouplingCompoundModalAnalysisAtASpeed",
    "ConceptCouplingConnectionCompoundModalAnalysisAtASpeed",
    "ConceptCouplingHalfCompoundModalAnalysisAtASpeed",
    "ConceptGearCompoundModalAnalysisAtASpeed",
    "ConceptGearMeshCompoundModalAnalysisAtASpeed",
    "ConceptGearSetCompoundModalAnalysisAtASpeed",
    "ConicalGearCompoundModalAnalysisAtASpeed",
    "ConicalGearMeshCompoundModalAnalysisAtASpeed",
    "ConicalGearSetCompoundModalAnalysisAtASpeed",
    "ConnectionCompoundModalAnalysisAtASpeed",
    "ConnectorCompoundModalAnalysisAtASpeed",
    "CouplingCompoundModalAnalysisAtASpeed",
    "CouplingConnectionCompoundModalAnalysisAtASpeed",
    "CouplingHalfCompoundModalAnalysisAtASpeed",
    "CVTBeltConnectionCompoundModalAnalysisAtASpeed",
    "CVTCompoundModalAnalysisAtASpeed",
    "CVTPulleyCompoundModalAnalysisAtASpeed",
    "CycloidalAssemblyCompoundModalAnalysisAtASpeed",
    "CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtASpeed",
    "CycloidalDiscCompoundModalAnalysisAtASpeed",
    "CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtASpeed",
    "CylindricalGearCompoundModalAnalysisAtASpeed",
    "CylindricalGearMeshCompoundModalAnalysisAtASpeed",
    "CylindricalGearSetCompoundModalAnalysisAtASpeed",
    "CylindricalPlanetGearCompoundModalAnalysisAtASpeed",
    "DatumCompoundModalAnalysisAtASpeed",
    "ExternalCADModelCompoundModalAnalysisAtASpeed",
    "FaceGearCompoundModalAnalysisAtASpeed",
    "FaceGearMeshCompoundModalAnalysisAtASpeed",
    "FaceGearSetCompoundModalAnalysisAtASpeed",
    "FEPartCompoundModalAnalysisAtASpeed",
    "FlexiblePinAssemblyCompoundModalAnalysisAtASpeed",
    "GearCompoundModalAnalysisAtASpeed",
    "GearMeshCompoundModalAnalysisAtASpeed",
    "GearSetCompoundModalAnalysisAtASpeed",
    "GuideDxfModelCompoundModalAnalysisAtASpeed",
    "HypoidGearCompoundModalAnalysisAtASpeed",
    "HypoidGearMeshCompoundModalAnalysisAtASpeed",
    "HypoidGearSetCompoundModalAnalysisAtASpeed",
    "InterMountableComponentConnectionCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed",
    "MassDiscCompoundModalAnalysisAtASpeed",
    "MeasurementComponentCompoundModalAnalysisAtASpeed",
    "MountableComponentCompoundModalAnalysisAtASpeed",
    "OilSealCompoundModalAnalysisAtASpeed",
    "PartCompoundModalAnalysisAtASpeed",
    "PartToPartShearCouplingCompoundModalAnalysisAtASpeed",
    "PartToPartShearCouplingConnectionCompoundModalAnalysisAtASpeed",
    "PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed",
    "PlanetaryConnectionCompoundModalAnalysisAtASpeed",
    "PlanetaryGearSetCompoundModalAnalysisAtASpeed",
    "PlanetCarrierCompoundModalAnalysisAtASpeed",
    "PointLoadCompoundModalAnalysisAtASpeed",
    "PowerLoadCompoundModalAnalysisAtASpeed",
    "PulleyCompoundModalAnalysisAtASpeed",
    "RingPinsCompoundModalAnalysisAtASpeed",
    "RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed",
    "RollingRingAssemblyCompoundModalAnalysisAtASpeed",
    "RollingRingCompoundModalAnalysisAtASpeed",
    "RollingRingConnectionCompoundModalAnalysisAtASpeed",
    "RootAssemblyCompoundModalAnalysisAtASpeed",
    "ShaftCompoundModalAnalysisAtASpeed",
    "ShaftHubConnectionCompoundModalAnalysisAtASpeed",
    "ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed",
    "SpecialisedAssemblyCompoundModalAnalysisAtASpeed",
    "SpiralBevelGearCompoundModalAnalysisAtASpeed",
    "SpiralBevelGearMeshCompoundModalAnalysisAtASpeed",
    "SpiralBevelGearSetCompoundModalAnalysisAtASpeed",
    "SpringDamperCompoundModalAnalysisAtASpeed",
    "SpringDamperConnectionCompoundModalAnalysisAtASpeed",
    "SpringDamperHalfCompoundModalAnalysisAtASpeed",
    "StraightBevelDiffGearCompoundModalAnalysisAtASpeed",
    "StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed",
    "StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed",
    "StraightBevelGearCompoundModalAnalysisAtASpeed",
    "StraightBevelGearMeshCompoundModalAnalysisAtASpeed",
    "StraightBevelGearSetCompoundModalAnalysisAtASpeed",
    "StraightBevelPlanetGearCompoundModalAnalysisAtASpeed",
    "StraightBevelSunGearCompoundModalAnalysisAtASpeed",
    "SynchroniserCompoundModalAnalysisAtASpeed",
    "SynchroniserHalfCompoundModalAnalysisAtASpeed",
    "SynchroniserPartCompoundModalAnalysisAtASpeed",
    "SynchroniserSleeveCompoundModalAnalysisAtASpeed",
    "TorqueConverterCompoundModalAnalysisAtASpeed",
    "TorqueConverterConnectionCompoundModalAnalysisAtASpeed",
    "TorqueConverterPumpCompoundModalAnalysisAtASpeed",
    "TorqueConverterTurbineCompoundModalAnalysisAtASpeed",
    "UnbalancedMassCompoundModalAnalysisAtASpeed",
    "VirtualComponentCompoundModalAnalysisAtASpeed",
    "WormGearCompoundModalAnalysisAtASpeed",
    "WormGearMeshCompoundModalAnalysisAtASpeed",
    "WormGearSetCompoundModalAnalysisAtASpeed",
    "ZerolBevelGearCompoundModalAnalysisAtASpeed",
    "ZerolBevelGearMeshCompoundModalAnalysisAtASpeed",
    "ZerolBevelGearSetCompoundModalAnalysisAtASpeed",
)
