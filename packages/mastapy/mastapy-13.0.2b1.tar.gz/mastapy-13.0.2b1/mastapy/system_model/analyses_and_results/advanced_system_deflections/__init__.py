"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._7272 import AbstractAssemblyAdvancedSystemDeflection
    from ._7273 import AbstractShaftAdvancedSystemDeflection
    from ._7274 import AbstractShaftOrHousingAdvancedSystemDeflection
    from ._7275 import (
        AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection,
    )
    from ._7276 import AdvancedSystemDeflection
    from ._7277 import AdvancedSystemDeflectionOptions
    from ._7278 import AdvancedSystemDeflectionSubAnalysis
    from ._7279 import AGMAGleasonConicalGearAdvancedSystemDeflection
    from ._7280 import AGMAGleasonConicalGearMeshAdvancedSystemDeflection
    from ._7281 import AGMAGleasonConicalGearSetAdvancedSystemDeflection
    from ._7282 import AssemblyAdvancedSystemDeflection
    from ._7283 import BearingAdvancedSystemDeflection
    from ._7284 import BeltConnectionAdvancedSystemDeflection
    from ._7285 import BeltDriveAdvancedSystemDeflection
    from ._7286 import BevelDifferentialGearAdvancedSystemDeflection
    from ._7287 import BevelDifferentialGearMeshAdvancedSystemDeflection
    from ._7288 import BevelDifferentialGearSetAdvancedSystemDeflection
    from ._7289 import BevelDifferentialPlanetGearAdvancedSystemDeflection
    from ._7290 import BevelDifferentialSunGearAdvancedSystemDeflection
    from ._7291 import BevelGearAdvancedSystemDeflection
    from ._7292 import BevelGearMeshAdvancedSystemDeflection
    from ._7293 import BevelGearSetAdvancedSystemDeflection
    from ._7294 import BoltAdvancedSystemDeflection
    from ._7295 import BoltedJointAdvancedSystemDeflection
    from ._7296 import ClutchAdvancedSystemDeflection
    from ._7297 import ClutchConnectionAdvancedSystemDeflection
    from ._7298 import ClutchHalfAdvancedSystemDeflection
    from ._7299 import CoaxialConnectionAdvancedSystemDeflection
    from ._7300 import ComponentAdvancedSystemDeflection
    from ._7301 import ConceptCouplingAdvancedSystemDeflection
    from ._7302 import ConceptCouplingConnectionAdvancedSystemDeflection
    from ._7303 import ConceptCouplingHalfAdvancedSystemDeflection
    from ._7304 import ConceptGearAdvancedSystemDeflection
    from ._7305 import ConceptGearMeshAdvancedSystemDeflection
    from ._7306 import ConceptGearSetAdvancedSystemDeflection
    from ._7307 import ConicalGearAdvancedSystemDeflection
    from ._7308 import ConicalGearMeshAdvancedSystemDeflection
    from ._7309 import ConicalGearSetAdvancedSystemDeflection
    from ._7310 import ConnectionAdvancedSystemDeflection
    from ._7311 import ConnectorAdvancedSystemDeflection
    from ._7312 import ContactChartPerToothPass
    from ._7313 import CouplingAdvancedSystemDeflection
    from ._7314 import CouplingConnectionAdvancedSystemDeflection
    from ._7315 import CouplingHalfAdvancedSystemDeflection
    from ._7316 import CVTAdvancedSystemDeflection
    from ._7317 import CVTBeltConnectionAdvancedSystemDeflection
    from ._7318 import CVTPulleyAdvancedSystemDeflection
    from ._7319 import CycloidalAssemblyAdvancedSystemDeflection
    from ._7320 import CycloidalDiscAdvancedSystemDeflection
    from ._7321 import CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection
    from ._7322 import CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection
    from ._7323 import CylindricalGearAdvancedSystemDeflection
    from ._7324 import CylindricalGearMeshAdvancedSystemDeflection
    from ._7325 import CylindricalGearSetAdvancedSystemDeflection
    from ._7326 import CylindricalMeshedGearAdvancedSystemDeflection
    from ._7327 import CylindricalPlanetGearAdvancedSystemDeflection
    from ._7328 import DatumAdvancedSystemDeflection
    from ._7329 import ExternalCADModelAdvancedSystemDeflection
    from ._7330 import FaceGearAdvancedSystemDeflection
    from ._7331 import FaceGearMeshAdvancedSystemDeflection
    from ._7332 import FaceGearSetAdvancedSystemDeflection
    from ._7333 import FEPartAdvancedSystemDeflection
    from ._7334 import FlexiblePinAssemblyAdvancedSystemDeflection
    from ._7335 import GearAdvancedSystemDeflection
    from ._7336 import GearMeshAdvancedSystemDeflection
    from ._7337 import GearSetAdvancedSystemDeflection
    from ._7338 import GuideDxfModelAdvancedSystemDeflection
    from ._7339 import HypoidGearAdvancedSystemDeflection
    from ._7340 import HypoidGearMeshAdvancedSystemDeflection
    from ._7341 import HypoidGearSetAdvancedSystemDeflection
    from ._7342 import InterMountableComponentConnectionAdvancedSystemDeflection
    from ._7343 import KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
    from ._7344 import KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
    from ._7345 import KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
    from ._7346 import KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
    from ._7347 import KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
    from ._7348 import KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
    from ._7349 import KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
    from ._7350 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection,
    )
    from ._7351 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection,
    )
    from ._7352 import UseLtcaInAsdOption
    from ._7353 import MassDiscAdvancedSystemDeflection
    from ._7354 import MeasurementComponentAdvancedSystemDeflection
    from ._7355 import MountableComponentAdvancedSystemDeflection
    from ._7356 import OilSealAdvancedSystemDeflection
    from ._7357 import PartAdvancedSystemDeflection
    from ._7358 import PartToPartShearCouplingAdvancedSystemDeflection
    from ._7359 import PartToPartShearCouplingConnectionAdvancedSystemDeflection
    from ._7360 import PartToPartShearCouplingHalfAdvancedSystemDeflection
    from ._7361 import PlanetaryConnectionAdvancedSystemDeflection
    from ._7362 import PlanetaryGearSetAdvancedSystemDeflection
    from ._7363 import PlanetCarrierAdvancedSystemDeflection
    from ._7364 import PointLoadAdvancedSystemDeflection
    from ._7365 import PowerLoadAdvancedSystemDeflection
    from ._7366 import PulleyAdvancedSystemDeflection
    from ._7367 import RingPinsAdvancedSystemDeflection
    from ._7368 import RingPinsToDiscConnectionAdvancedSystemDeflection
    from ._7369 import RollingRingAdvancedSystemDeflection
    from ._7370 import RollingRingAssemblyAdvancedSystemDeflection
    from ._7371 import RollingRingConnectionAdvancedSystemDeflection
    from ._7372 import RootAssemblyAdvancedSystemDeflection
    from ._7373 import ShaftAdvancedSystemDeflection
    from ._7374 import ShaftHubConnectionAdvancedSystemDeflection
    from ._7375 import ShaftToMountableComponentConnectionAdvancedSystemDeflection
    from ._7376 import SpecialisedAssemblyAdvancedSystemDeflection
    from ._7377 import SpiralBevelGearAdvancedSystemDeflection
    from ._7378 import SpiralBevelGearMeshAdvancedSystemDeflection
    from ._7379 import SpiralBevelGearSetAdvancedSystemDeflection
    from ._7380 import SpringDamperAdvancedSystemDeflection
    from ._7381 import SpringDamperConnectionAdvancedSystemDeflection
    from ._7382 import SpringDamperHalfAdvancedSystemDeflection
    from ._7383 import StraightBevelDiffGearAdvancedSystemDeflection
    from ._7384 import StraightBevelDiffGearMeshAdvancedSystemDeflection
    from ._7385 import StraightBevelDiffGearSetAdvancedSystemDeflection
    from ._7386 import StraightBevelGearAdvancedSystemDeflection
    from ._7387 import StraightBevelGearMeshAdvancedSystemDeflection
    from ._7388 import StraightBevelGearSetAdvancedSystemDeflection
    from ._7389 import StraightBevelPlanetGearAdvancedSystemDeflection
    from ._7390 import StraightBevelSunGearAdvancedSystemDeflection
    from ._7391 import SynchroniserAdvancedSystemDeflection
    from ._7392 import SynchroniserHalfAdvancedSystemDeflection
    from ._7393 import SynchroniserPartAdvancedSystemDeflection
    from ._7394 import SynchroniserSleeveAdvancedSystemDeflection
    from ._7395 import TorqueConverterAdvancedSystemDeflection
    from ._7396 import TorqueConverterConnectionAdvancedSystemDeflection
    from ._7397 import TorqueConverterPumpAdvancedSystemDeflection
    from ._7398 import TorqueConverterTurbineAdvancedSystemDeflection
    from ._7399 import TransmissionErrorToOtherPowerLoad
    from ._7400 import UnbalancedMassAdvancedSystemDeflection
    from ._7401 import VirtualComponentAdvancedSystemDeflection
    from ._7402 import WormGearAdvancedSystemDeflection
    from ._7403 import WormGearMeshAdvancedSystemDeflection
    from ._7404 import WormGearSetAdvancedSystemDeflection
    from ._7405 import ZerolBevelGearAdvancedSystemDeflection
    from ._7406 import ZerolBevelGearMeshAdvancedSystemDeflection
    from ._7407 import ZerolBevelGearSetAdvancedSystemDeflection
else:
    import_structure = {
        "_7272": ["AbstractAssemblyAdvancedSystemDeflection"],
        "_7273": ["AbstractShaftAdvancedSystemDeflection"],
        "_7274": ["AbstractShaftOrHousingAdvancedSystemDeflection"],
        "_7275": [
            "AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection"
        ],
        "_7276": ["AdvancedSystemDeflection"],
        "_7277": ["AdvancedSystemDeflectionOptions"],
        "_7278": ["AdvancedSystemDeflectionSubAnalysis"],
        "_7279": ["AGMAGleasonConicalGearAdvancedSystemDeflection"],
        "_7280": ["AGMAGleasonConicalGearMeshAdvancedSystemDeflection"],
        "_7281": ["AGMAGleasonConicalGearSetAdvancedSystemDeflection"],
        "_7282": ["AssemblyAdvancedSystemDeflection"],
        "_7283": ["BearingAdvancedSystemDeflection"],
        "_7284": ["BeltConnectionAdvancedSystemDeflection"],
        "_7285": ["BeltDriveAdvancedSystemDeflection"],
        "_7286": ["BevelDifferentialGearAdvancedSystemDeflection"],
        "_7287": ["BevelDifferentialGearMeshAdvancedSystemDeflection"],
        "_7288": ["BevelDifferentialGearSetAdvancedSystemDeflection"],
        "_7289": ["BevelDifferentialPlanetGearAdvancedSystemDeflection"],
        "_7290": ["BevelDifferentialSunGearAdvancedSystemDeflection"],
        "_7291": ["BevelGearAdvancedSystemDeflection"],
        "_7292": ["BevelGearMeshAdvancedSystemDeflection"],
        "_7293": ["BevelGearSetAdvancedSystemDeflection"],
        "_7294": ["BoltAdvancedSystemDeflection"],
        "_7295": ["BoltedJointAdvancedSystemDeflection"],
        "_7296": ["ClutchAdvancedSystemDeflection"],
        "_7297": ["ClutchConnectionAdvancedSystemDeflection"],
        "_7298": ["ClutchHalfAdvancedSystemDeflection"],
        "_7299": ["CoaxialConnectionAdvancedSystemDeflection"],
        "_7300": ["ComponentAdvancedSystemDeflection"],
        "_7301": ["ConceptCouplingAdvancedSystemDeflection"],
        "_7302": ["ConceptCouplingConnectionAdvancedSystemDeflection"],
        "_7303": ["ConceptCouplingHalfAdvancedSystemDeflection"],
        "_7304": ["ConceptGearAdvancedSystemDeflection"],
        "_7305": ["ConceptGearMeshAdvancedSystemDeflection"],
        "_7306": ["ConceptGearSetAdvancedSystemDeflection"],
        "_7307": ["ConicalGearAdvancedSystemDeflection"],
        "_7308": ["ConicalGearMeshAdvancedSystemDeflection"],
        "_7309": ["ConicalGearSetAdvancedSystemDeflection"],
        "_7310": ["ConnectionAdvancedSystemDeflection"],
        "_7311": ["ConnectorAdvancedSystemDeflection"],
        "_7312": ["ContactChartPerToothPass"],
        "_7313": ["CouplingAdvancedSystemDeflection"],
        "_7314": ["CouplingConnectionAdvancedSystemDeflection"],
        "_7315": ["CouplingHalfAdvancedSystemDeflection"],
        "_7316": ["CVTAdvancedSystemDeflection"],
        "_7317": ["CVTBeltConnectionAdvancedSystemDeflection"],
        "_7318": ["CVTPulleyAdvancedSystemDeflection"],
        "_7319": ["CycloidalAssemblyAdvancedSystemDeflection"],
        "_7320": ["CycloidalDiscAdvancedSystemDeflection"],
        "_7321": ["CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection"],
        "_7322": ["CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection"],
        "_7323": ["CylindricalGearAdvancedSystemDeflection"],
        "_7324": ["CylindricalGearMeshAdvancedSystemDeflection"],
        "_7325": ["CylindricalGearSetAdvancedSystemDeflection"],
        "_7326": ["CylindricalMeshedGearAdvancedSystemDeflection"],
        "_7327": ["CylindricalPlanetGearAdvancedSystemDeflection"],
        "_7328": ["DatumAdvancedSystemDeflection"],
        "_7329": ["ExternalCADModelAdvancedSystemDeflection"],
        "_7330": ["FaceGearAdvancedSystemDeflection"],
        "_7331": ["FaceGearMeshAdvancedSystemDeflection"],
        "_7332": ["FaceGearSetAdvancedSystemDeflection"],
        "_7333": ["FEPartAdvancedSystemDeflection"],
        "_7334": ["FlexiblePinAssemblyAdvancedSystemDeflection"],
        "_7335": ["GearAdvancedSystemDeflection"],
        "_7336": ["GearMeshAdvancedSystemDeflection"],
        "_7337": ["GearSetAdvancedSystemDeflection"],
        "_7338": ["GuideDxfModelAdvancedSystemDeflection"],
        "_7339": ["HypoidGearAdvancedSystemDeflection"],
        "_7340": ["HypoidGearMeshAdvancedSystemDeflection"],
        "_7341": ["HypoidGearSetAdvancedSystemDeflection"],
        "_7342": ["InterMountableComponentConnectionAdvancedSystemDeflection"],
        "_7343": ["KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection"],
        "_7344": ["KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection"],
        "_7345": ["KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection"],
        "_7346": ["KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection"],
        "_7347": ["KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection"],
        "_7348": ["KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection"],
        "_7349": ["KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection"],
        "_7350": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection"
        ],
        "_7351": ["KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection"],
        "_7352": ["UseLtcaInAsdOption"],
        "_7353": ["MassDiscAdvancedSystemDeflection"],
        "_7354": ["MeasurementComponentAdvancedSystemDeflection"],
        "_7355": ["MountableComponentAdvancedSystemDeflection"],
        "_7356": ["OilSealAdvancedSystemDeflection"],
        "_7357": ["PartAdvancedSystemDeflection"],
        "_7358": ["PartToPartShearCouplingAdvancedSystemDeflection"],
        "_7359": ["PartToPartShearCouplingConnectionAdvancedSystemDeflection"],
        "_7360": ["PartToPartShearCouplingHalfAdvancedSystemDeflection"],
        "_7361": ["PlanetaryConnectionAdvancedSystemDeflection"],
        "_7362": ["PlanetaryGearSetAdvancedSystemDeflection"],
        "_7363": ["PlanetCarrierAdvancedSystemDeflection"],
        "_7364": ["PointLoadAdvancedSystemDeflection"],
        "_7365": ["PowerLoadAdvancedSystemDeflection"],
        "_7366": ["PulleyAdvancedSystemDeflection"],
        "_7367": ["RingPinsAdvancedSystemDeflection"],
        "_7368": ["RingPinsToDiscConnectionAdvancedSystemDeflection"],
        "_7369": ["RollingRingAdvancedSystemDeflection"],
        "_7370": ["RollingRingAssemblyAdvancedSystemDeflection"],
        "_7371": ["RollingRingConnectionAdvancedSystemDeflection"],
        "_7372": ["RootAssemblyAdvancedSystemDeflection"],
        "_7373": ["ShaftAdvancedSystemDeflection"],
        "_7374": ["ShaftHubConnectionAdvancedSystemDeflection"],
        "_7375": ["ShaftToMountableComponentConnectionAdvancedSystemDeflection"],
        "_7376": ["SpecialisedAssemblyAdvancedSystemDeflection"],
        "_7377": ["SpiralBevelGearAdvancedSystemDeflection"],
        "_7378": ["SpiralBevelGearMeshAdvancedSystemDeflection"],
        "_7379": ["SpiralBevelGearSetAdvancedSystemDeflection"],
        "_7380": ["SpringDamperAdvancedSystemDeflection"],
        "_7381": ["SpringDamperConnectionAdvancedSystemDeflection"],
        "_7382": ["SpringDamperHalfAdvancedSystemDeflection"],
        "_7383": ["StraightBevelDiffGearAdvancedSystemDeflection"],
        "_7384": ["StraightBevelDiffGearMeshAdvancedSystemDeflection"],
        "_7385": ["StraightBevelDiffGearSetAdvancedSystemDeflection"],
        "_7386": ["StraightBevelGearAdvancedSystemDeflection"],
        "_7387": ["StraightBevelGearMeshAdvancedSystemDeflection"],
        "_7388": ["StraightBevelGearSetAdvancedSystemDeflection"],
        "_7389": ["StraightBevelPlanetGearAdvancedSystemDeflection"],
        "_7390": ["StraightBevelSunGearAdvancedSystemDeflection"],
        "_7391": ["SynchroniserAdvancedSystemDeflection"],
        "_7392": ["SynchroniserHalfAdvancedSystemDeflection"],
        "_7393": ["SynchroniserPartAdvancedSystemDeflection"],
        "_7394": ["SynchroniserSleeveAdvancedSystemDeflection"],
        "_7395": ["TorqueConverterAdvancedSystemDeflection"],
        "_7396": ["TorqueConverterConnectionAdvancedSystemDeflection"],
        "_7397": ["TorqueConverterPumpAdvancedSystemDeflection"],
        "_7398": ["TorqueConverterTurbineAdvancedSystemDeflection"],
        "_7399": ["TransmissionErrorToOtherPowerLoad"],
        "_7400": ["UnbalancedMassAdvancedSystemDeflection"],
        "_7401": ["VirtualComponentAdvancedSystemDeflection"],
        "_7402": ["WormGearAdvancedSystemDeflection"],
        "_7403": ["WormGearMeshAdvancedSystemDeflection"],
        "_7404": ["WormGearSetAdvancedSystemDeflection"],
        "_7405": ["ZerolBevelGearAdvancedSystemDeflection"],
        "_7406": ["ZerolBevelGearMeshAdvancedSystemDeflection"],
        "_7407": ["ZerolBevelGearSetAdvancedSystemDeflection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyAdvancedSystemDeflection",
    "AbstractShaftAdvancedSystemDeflection",
    "AbstractShaftOrHousingAdvancedSystemDeflection",
    "AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection",
    "AdvancedSystemDeflection",
    "AdvancedSystemDeflectionOptions",
    "AdvancedSystemDeflectionSubAnalysis",
    "AGMAGleasonConicalGearAdvancedSystemDeflection",
    "AGMAGleasonConicalGearMeshAdvancedSystemDeflection",
    "AGMAGleasonConicalGearSetAdvancedSystemDeflection",
    "AssemblyAdvancedSystemDeflection",
    "BearingAdvancedSystemDeflection",
    "BeltConnectionAdvancedSystemDeflection",
    "BeltDriveAdvancedSystemDeflection",
    "BevelDifferentialGearAdvancedSystemDeflection",
    "BevelDifferentialGearMeshAdvancedSystemDeflection",
    "BevelDifferentialGearSetAdvancedSystemDeflection",
    "BevelDifferentialPlanetGearAdvancedSystemDeflection",
    "BevelDifferentialSunGearAdvancedSystemDeflection",
    "BevelGearAdvancedSystemDeflection",
    "BevelGearMeshAdvancedSystemDeflection",
    "BevelGearSetAdvancedSystemDeflection",
    "BoltAdvancedSystemDeflection",
    "BoltedJointAdvancedSystemDeflection",
    "ClutchAdvancedSystemDeflection",
    "ClutchConnectionAdvancedSystemDeflection",
    "ClutchHalfAdvancedSystemDeflection",
    "CoaxialConnectionAdvancedSystemDeflection",
    "ComponentAdvancedSystemDeflection",
    "ConceptCouplingAdvancedSystemDeflection",
    "ConceptCouplingConnectionAdvancedSystemDeflection",
    "ConceptCouplingHalfAdvancedSystemDeflection",
    "ConceptGearAdvancedSystemDeflection",
    "ConceptGearMeshAdvancedSystemDeflection",
    "ConceptGearSetAdvancedSystemDeflection",
    "ConicalGearAdvancedSystemDeflection",
    "ConicalGearMeshAdvancedSystemDeflection",
    "ConicalGearSetAdvancedSystemDeflection",
    "ConnectionAdvancedSystemDeflection",
    "ConnectorAdvancedSystemDeflection",
    "ContactChartPerToothPass",
    "CouplingAdvancedSystemDeflection",
    "CouplingConnectionAdvancedSystemDeflection",
    "CouplingHalfAdvancedSystemDeflection",
    "CVTAdvancedSystemDeflection",
    "CVTBeltConnectionAdvancedSystemDeflection",
    "CVTPulleyAdvancedSystemDeflection",
    "CycloidalAssemblyAdvancedSystemDeflection",
    "CycloidalDiscAdvancedSystemDeflection",
    "CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection",
    "CycloidalDiscPlanetaryBearingConnectionAdvancedSystemDeflection",
    "CylindricalGearAdvancedSystemDeflection",
    "CylindricalGearMeshAdvancedSystemDeflection",
    "CylindricalGearSetAdvancedSystemDeflection",
    "CylindricalMeshedGearAdvancedSystemDeflection",
    "CylindricalPlanetGearAdvancedSystemDeflection",
    "DatumAdvancedSystemDeflection",
    "ExternalCADModelAdvancedSystemDeflection",
    "FaceGearAdvancedSystemDeflection",
    "FaceGearMeshAdvancedSystemDeflection",
    "FaceGearSetAdvancedSystemDeflection",
    "FEPartAdvancedSystemDeflection",
    "FlexiblePinAssemblyAdvancedSystemDeflection",
    "GearAdvancedSystemDeflection",
    "GearMeshAdvancedSystemDeflection",
    "GearSetAdvancedSystemDeflection",
    "GuideDxfModelAdvancedSystemDeflection",
    "HypoidGearAdvancedSystemDeflection",
    "HypoidGearMeshAdvancedSystemDeflection",
    "HypoidGearSetAdvancedSystemDeflection",
    "InterMountableComponentConnectionAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection",
    "UseLtcaInAsdOption",
    "MassDiscAdvancedSystemDeflection",
    "MeasurementComponentAdvancedSystemDeflection",
    "MountableComponentAdvancedSystemDeflection",
    "OilSealAdvancedSystemDeflection",
    "PartAdvancedSystemDeflection",
    "PartToPartShearCouplingAdvancedSystemDeflection",
    "PartToPartShearCouplingConnectionAdvancedSystemDeflection",
    "PartToPartShearCouplingHalfAdvancedSystemDeflection",
    "PlanetaryConnectionAdvancedSystemDeflection",
    "PlanetaryGearSetAdvancedSystemDeflection",
    "PlanetCarrierAdvancedSystemDeflection",
    "PointLoadAdvancedSystemDeflection",
    "PowerLoadAdvancedSystemDeflection",
    "PulleyAdvancedSystemDeflection",
    "RingPinsAdvancedSystemDeflection",
    "RingPinsToDiscConnectionAdvancedSystemDeflection",
    "RollingRingAdvancedSystemDeflection",
    "RollingRingAssemblyAdvancedSystemDeflection",
    "RollingRingConnectionAdvancedSystemDeflection",
    "RootAssemblyAdvancedSystemDeflection",
    "ShaftAdvancedSystemDeflection",
    "ShaftHubConnectionAdvancedSystemDeflection",
    "ShaftToMountableComponentConnectionAdvancedSystemDeflection",
    "SpecialisedAssemblyAdvancedSystemDeflection",
    "SpiralBevelGearAdvancedSystemDeflection",
    "SpiralBevelGearMeshAdvancedSystemDeflection",
    "SpiralBevelGearSetAdvancedSystemDeflection",
    "SpringDamperAdvancedSystemDeflection",
    "SpringDamperConnectionAdvancedSystemDeflection",
    "SpringDamperHalfAdvancedSystemDeflection",
    "StraightBevelDiffGearAdvancedSystemDeflection",
    "StraightBevelDiffGearMeshAdvancedSystemDeflection",
    "StraightBevelDiffGearSetAdvancedSystemDeflection",
    "StraightBevelGearAdvancedSystemDeflection",
    "StraightBevelGearMeshAdvancedSystemDeflection",
    "StraightBevelGearSetAdvancedSystemDeflection",
    "StraightBevelPlanetGearAdvancedSystemDeflection",
    "StraightBevelSunGearAdvancedSystemDeflection",
    "SynchroniserAdvancedSystemDeflection",
    "SynchroniserHalfAdvancedSystemDeflection",
    "SynchroniserPartAdvancedSystemDeflection",
    "SynchroniserSleeveAdvancedSystemDeflection",
    "TorqueConverterAdvancedSystemDeflection",
    "TorqueConverterConnectionAdvancedSystemDeflection",
    "TorqueConverterPumpAdvancedSystemDeflection",
    "TorqueConverterTurbineAdvancedSystemDeflection",
    "TransmissionErrorToOtherPowerLoad",
    "UnbalancedMassAdvancedSystemDeflection",
    "VirtualComponentAdvancedSystemDeflection",
    "WormGearAdvancedSystemDeflection",
    "WormGearMeshAdvancedSystemDeflection",
    "WormGearSetAdvancedSystemDeflection",
    "ZerolBevelGearAdvancedSystemDeflection",
    "ZerolBevelGearMeshAdvancedSystemDeflection",
    "ZerolBevelGearSetAdvancedSystemDeflection",
)
