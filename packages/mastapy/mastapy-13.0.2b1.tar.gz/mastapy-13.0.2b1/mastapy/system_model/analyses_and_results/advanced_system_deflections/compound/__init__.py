"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._7408 import AbstractAssemblyCompoundAdvancedSystemDeflection
    from ._7409 import AbstractShaftCompoundAdvancedSystemDeflection
    from ._7410 import AbstractShaftOrHousingCompoundAdvancedSystemDeflection
    from ._7411 import (
        AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection,
    )
    from ._7412 import AGMAGleasonConicalGearCompoundAdvancedSystemDeflection
    from ._7413 import AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection
    from ._7414 import AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection
    from ._7415 import AssemblyCompoundAdvancedSystemDeflection
    from ._7416 import BearingCompoundAdvancedSystemDeflection
    from ._7417 import BeltConnectionCompoundAdvancedSystemDeflection
    from ._7418 import BeltDriveCompoundAdvancedSystemDeflection
    from ._7419 import BevelDifferentialGearCompoundAdvancedSystemDeflection
    from ._7420 import BevelDifferentialGearMeshCompoundAdvancedSystemDeflection
    from ._7421 import BevelDifferentialGearSetCompoundAdvancedSystemDeflection
    from ._7422 import BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection
    from ._7423 import BevelDifferentialSunGearCompoundAdvancedSystemDeflection
    from ._7424 import BevelGearCompoundAdvancedSystemDeflection
    from ._7425 import BevelGearMeshCompoundAdvancedSystemDeflection
    from ._7426 import BevelGearSetCompoundAdvancedSystemDeflection
    from ._7427 import BoltCompoundAdvancedSystemDeflection
    from ._7428 import BoltedJointCompoundAdvancedSystemDeflection
    from ._7429 import ClutchCompoundAdvancedSystemDeflection
    from ._7430 import ClutchConnectionCompoundAdvancedSystemDeflection
    from ._7431 import ClutchHalfCompoundAdvancedSystemDeflection
    from ._7432 import CoaxialConnectionCompoundAdvancedSystemDeflection
    from ._7433 import ComponentCompoundAdvancedSystemDeflection
    from ._7434 import ConceptCouplingCompoundAdvancedSystemDeflection
    from ._7435 import ConceptCouplingConnectionCompoundAdvancedSystemDeflection
    from ._7436 import ConceptCouplingHalfCompoundAdvancedSystemDeflection
    from ._7437 import ConceptGearCompoundAdvancedSystemDeflection
    from ._7438 import ConceptGearMeshCompoundAdvancedSystemDeflection
    from ._7439 import ConceptGearSetCompoundAdvancedSystemDeflection
    from ._7440 import ConicalGearCompoundAdvancedSystemDeflection
    from ._7441 import ConicalGearMeshCompoundAdvancedSystemDeflection
    from ._7442 import ConicalGearSetCompoundAdvancedSystemDeflection
    from ._7443 import ConnectionCompoundAdvancedSystemDeflection
    from ._7444 import ConnectorCompoundAdvancedSystemDeflection
    from ._7445 import CouplingCompoundAdvancedSystemDeflection
    from ._7446 import CouplingConnectionCompoundAdvancedSystemDeflection
    from ._7447 import CouplingHalfCompoundAdvancedSystemDeflection
    from ._7448 import CVTBeltConnectionCompoundAdvancedSystemDeflection
    from ._7449 import CVTCompoundAdvancedSystemDeflection
    from ._7450 import CVTPulleyCompoundAdvancedSystemDeflection
    from ._7451 import CycloidalAssemblyCompoundAdvancedSystemDeflection
    from ._7452 import (
        CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection,
    )
    from ._7453 import CycloidalDiscCompoundAdvancedSystemDeflection
    from ._7454 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection,
    )
    from ._7455 import CylindricalGearCompoundAdvancedSystemDeflection
    from ._7456 import CylindricalGearMeshCompoundAdvancedSystemDeflection
    from ._7457 import CylindricalGearSetCompoundAdvancedSystemDeflection
    from ._7458 import CylindricalPlanetGearCompoundAdvancedSystemDeflection
    from ._7459 import DatumCompoundAdvancedSystemDeflection
    from ._7460 import ExternalCADModelCompoundAdvancedSystemDeflection
    from ._7461 import FaceGearCompoundAdvancedSystemDeflection
    from ._7462 import FaceGearMeshCompoundAdvancedSystemDeflection
    from ._7463 import FaceGearSetCompoundAdvancedSystemDeflection
    from ._7464 import FEPartCompoundAdvancedSystemDeflection
    from ._7465 import FlexiblePinAssemblyCompoundAdvancedSystemDeflection
    from ._7466 import GearCompoundAdvancedSystemDeflection
    from ._7467 import GearMeshCompoundAdvancedSystemDeflection
    from ._7468 import GearSetCompoundAdvancedSystemDeflection
    from ._7469 import GuideDxfModelCompoundAdvancedSystemDeflection
    from ._7470 import HypoidGearCompoundAdvancedSystemDeflection
    from ._7471 import HypoidGearMeshCompoundAdvancedSystemDeflection
    from ._7472 import HypoidGearSetCompoundAdvancedSystemDeflection
    from ._7473 import InterMountableComponentConnectionCompoundAdvancedSystemDeflection
    from ._7474 import (
        KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection,
    )
    from ._7475 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection,
    )
    from ._7476 import (
        KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection,
    )
    from ._7477 import (
        KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection,
    )
    from ._7478 import (
        KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection,
    )
    from ._7479 import (
        KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection,
    )
    from ._7480 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection,
    )
    from ._7481 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection,
    )
    from ._7482 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection,
    )
    from ._7483 import MassDiscCompoundAdvancedSystemDeflection
    from ._7484 import MeasurementComponentCompoundAdvancedSystemDeflection
    from ._7485 import MountableComponentCompoundAdvancedSystemDeflection
    from ._7486 import OilSealCompoundAdvancedSystemDeflection
    from ._7487 import PartCompoundAdvancedSystemDeflection
    from ._7488 import PartToPartShearCouplingCompoundAdvancedSystemDeflection
    from ._7489 import PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection
    from ._7490 import PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection
    from ._7491 import PlanetaryConnectionCompoundAdvancedSystemDeflection
    from ._7492 import PlanetaryGearSetCompoundAdvancedSystemDeflection
    from ._7493 import PlanetCarrierCompoundAdvancedSystemDeflection
    from ._7494 import PointLoadCompoundAdvancedSystemDeflection
    from ._7495 import PowerLoadCompoundAdvancedSystemDeflection
    from ._7496 import PulleyCompoundAdvancedSystemDeflection
    from ._7497 import RingPinsCompoundAdvancedSystemDeflection
    from ._7498 import RingPinsToDiscConnectionCompoundAdvancedSystemDeflection
    from ._7499 import RollingRingAssemblyCompoundAdvancedSystemDeflection
    from ._7500 import RollingRingCompoundAdvancedSystemDeflection
    from ._7501 import RollingRingConnectionCompoundAdvancedSystemDeflection
    from ._7502 import RootAssemblyCompoundAdvancedSystemDeflection
    from ._7503 import ShaftCompoundAdvancedSystemDeflection
    from ._7504 import ShaftHubConnectionCompoundAdvancedSystemDeflection
    from ._7505 import (
        ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection,
    )
    from ._7506 import SpecialisedAssemblyCompoundAdvancedSystemDeflection
    from ._7507 import SpiralBevelGearCompoundAdvancedSystemDeflection
    from ._7508 import SpiralBevelGearMeshCompoundAdvancedSystemDeflection
    from ._7509 import SpiralBevelGearSetCompoundAdvancedSystemDeflection
    from ._7510 import SpringDamperCompoundAdvancedSystemDeflection
    from ._7511 import SpringDamperConnectionCompoundAdvancedSystemDeflection
    from ._7512 import SpringDamperHalfCompoundAdvancedSystemDeflection
    from ._7513 import StraightBevelDiffGearCompoundAdvancedSystemDeflection
    from ._7514 import StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection
    from ._7515 import StraightBevelDiffGearSetCompoundAdvancedSystemDeflection
    from ._7516 import StraightBevelGearCompoundAdvancedSystemDeflection
    from ._7517 import StraightBevelGearMeshCompoundAdvancedSystemDeflection
    from ._7518 import StraightBevelGearSetCompoundAdvancedSystemDeflection
    from ._7519 import StraightBevelPlanetGearCompoundAdvancedSystemDeflection
    from ._7520 import StraightBevelSunGearCompoundAdvancedSystemDeflection
    from ._7521 import SynchroniserCompoundAdvancedSystemDeflection
    from ._7522 import SynchroniserHalfCompoundAdvancedSystemDeflection
    from ._7523 import SynchroniserPartCompoundAdvancedSystemDeflection
    from ._7524 import SynchroniserSleeveCompoundAdvancedSystemDeflection
    from ._7525 import TorqueConverterCompoundAdvancedSystemDeflection
    from ._7526 import TorqueConverterConnectionCompoundAdvancedSystemDeflection
    from ._7527 import TorqueConverterPumpCompoundAdvancedSystemDeflection
    from ._7528 import TorqueConverterTurbineCompoundAdvancedSystemDeflection
    from ._7529 import UnbalancedMassCompoundAdvancedSystemDeflection
    from ._7530 import VirtualComponentCompoundAdvancedSystemDeflection
    from ._7531 import WormGearCompoundAdvancedSystemDeflection
    from ._7532 import WormGearMeshCompoundAdvancedSystemDeflection
    from ._7533 import WormGearSetCompoundAdvancedSystemDeflection
    from ._7534 import ZerolBevelGearCompoundAdvancedSystemDeflection
    from ._7535 import ZerolBevelGearMeshCompoundAdvancedSystemDeflection
    from ._7536 import ZerolBevelGearSetCompoundAdvancedSystemDeflection
else:
    import_structure = {
        "_7408": ["AbstractAssemblyCompoundAdvancedSystemDeflection"],
        "_7409": ["AbstractShaftCompoundAdvancedSystemDeflection"],
        "_7410": ["AbstractShaftOrHousingCompoundAdvancedSystemDeflection"],
        "_7411": [
            "AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection"
        ],
        "_7412": ["AGMAGleasonConicalGearCompoundAdvancedSystemDeflection"],
        "_7413": ["AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection"],
        "_7414": ["AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection"],
        "_7415": ["AssemblyCompoundAdvancedSystemDeflection"],
        "_7416": ["BearingCompoundAdvancedSystemDeflection"],
        "_7417": ["BeltConnectionCompoundAdvancedSystemDeflection"],
        "_7418": ["BeltDriveCompoundAdvancedSystemDeflection"],
        "_7419": ["BevelDifferentialGearCompoundAdvancedSystemDeflection"],
        "_7420": ["BevelDifferentialGearMeshCompoundAdvancedSystemDeflection"],
        "_7421": ["BevelDifferentialGearSetCompoundAdvancedSystemDeflection"],
        "_7422": ["BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection"],
        "_7423": ["BevelDifferentialSunGearCompoundAdvancedSystemDeflection"],
        "_7424": ["BevelGearCompoundAdvancedSystemDeflection"],
        "_7425": ["BevelGearMeshCompoundAdvancedSystemDeflection"],
        "_7426": ["BevelGearSetCompoundAdvancedSystemDeflection"],
        "_7427": ["BoltCompoundAdvancedSystemDeflection"],
        "_7428": ["BoltedJointCompoundAdvancedSystemDeflection"],
        "_7429": ["ClutchCompoundAdvancedSystemDeflection"],
        "_7430": ["ClutchConnectionCompoundAdvancedSystemDeflection"],
        "_7431": ["ClutchHalfCompoundAdvancedSystemDeflection"],
        "_7432": ["CoaxialConnectionCompoundAdvancedSystemDeflection"],
        "_7433": ["ComponentCompoundAdvancedSystemDeflection"],
        "_7434": ["ConceptCouplingCompoundAdvancedSystemDeflection"],
        "_7435": ["ConceptCouplingConnectionCompoundAdvancedSystemDeflection"],
        "_7436": ["ConceptCouplingHalfCompoundAdvancedSystemDeflection"],
        "_7437": ["ConceptGearCompoundAdvancedSystemDeflection"],
        "_7438": ["ConceptGearMeshCompoundAdvancedSystemDeflection"],
        "_7439": ["ConceptGearSetCompoundAdvancedSystemDeflection"],
        "_7440": ["ConicalGearCompoundAdvancedSystemDeflection"],
        "_7441": ["ConicalGearMeshCompoundAdvancedSystemDeflection"],
        "_7442": ["ConicalGearSetCompoundAdvancedSystemDeflection"],
        "_7443": ["ConnectionCompoundAdvancedSystemDeflection"],
        "_7444": ["ConnectorCompoundAdvancedSystemDeflection"],
        "_7445": ["CouplingCompoundAdvancedSystemDeflection"],
        "_7446": ["CouplingConnectionCompoundAdvancedSystemDeflection"],
        "_7447": ["CouplingHalfCompoundAdvancedSystemDeflection"],
        "_7448": ["CVTBeltConnectionCompoundAdvancedSystemDeflection"],
        "_7449": ["CVTCompoundAdvancedSystemDeflection"],
        "_7450": ["CVTPulleyCompoundAdvancedSystemDeflection"],
        "_7451": ["CycloidalAssemblyCompoundAdvancedSystemDeflection"],
        "_7452": [
            "CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection"
        ],
        "_7453": ["CycloidalDiscCompoundAdvancedSystemDeflection"],
        "_7454": [
            "CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection"
        ],
        "_7455": ["CylindricalGearCompoundAdvancedSystemDeflection"],
        "_7456": ["CylindricalGearMeshCompoundAdvancedSystemDeflection"],
        "_7457": ["CylindricalGearSetCompoundAdvancedSystemDeflection"],
        "_7458": ["CylindricalPlanetGearCompoundAdvancedSystemDeflection"],
        "_7459": ["DatumCompoundAdvancedSystemDeflection"],
        "_7460": ["ExternalCADModelCompoundAdvancedSystemDeflection"],
        "_7461": ["FaceGearCompoundAdvancedSystemDeflection"],
        "_7462": ["FaceGearMeshCompoundAdvancedSystemDeflection"],
        "_7463": ["FaceGearSetCompoundAdvancedSystemDeflection"],
        "_7464": ["FEPartCompoundAdvancedSystemDeflection"],
        "_7465": ["FlexiblePinAssemblyCompoundAdvancedSystemDeflection"],
        "_7466": ["GearCompoundAdvancedSystemDeflection"],
        "_7467": ["GearMeshCompoundAdvancedSystemDeflection"],
        "_7468": ["GearSetCompoundAdvancedSystemDeflection"],
        "_7469": ["GuideDxfModelCompoundAdvancedSystemDeflection"],
        "_7470": ["HypoidGearCompoundAdvancedSystemDeflection"],
        "_7471": ["HypoidGearMeshCompoundAdvancedSystemDeflection"],
        "_7472": ["HypoidGearSetCompoundAdvancedSystemDeflection"],
        "_7473": ["InterMountableComponentConnectionCompoundAdvancedSystemDeflection"],
        "_7474": [
            "KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection"
        ],
        "_7475": [
            "KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection"
        ],
        "_7476": [
            "KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection"
        ],
        "_7477": ["KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection"],
        "_7478": [
            "KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection"
        ],
        "_7479": [
            "KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection"
        ],
        "_7480": [
            "KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection"
        ],
        "_7481": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection"
        ],
        "_7482": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection"
        ],
        "_7483": ["MassDiscCompoundAdvancedSystemDeflection"],
        "_7484": ["MeasurementComponentCompoundAdvancedSystemDeflection"],
        "_7485": ["MountableComponentCompoundAdvancedSystemDeflection"],
        "_7486": ["OilSealCompoundAdvancedSystemDeflection"],
        "_7487": ["PartCompoundAdvancedSystemDeflection"],
        "_7488": ["PartToPartShearCouplingCompoundAdvancedSystemDeflection"],
        "_7489": ["PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection"],
        "_7490": ["PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection"],
        "_7491": ["PlanetaryConnectionCompoundAdvancedSystemDeflection"],
        "_7492": ["PlanetaryGearSetCompoundAdvancedSystemDeflection"],
        "_7493": ["PlanetCarrierCompoundAdvancedSystemDeflection"],
        "_7494": ["PointLoadCompoundAdvancedSystemDeflection"],
        "_7495": ["PowerLoadCompoundAdvancedSystemDeflection"],
        "_7496": ["PulleyCompoundAdvancedSystemDeflection"],
        "_7497": ["RingPinsCompoundAdvancedSystemDeflection"],
        "_7498": ["RingPinsToDiscConnectionCompoundAdvancedSystemDeflection"],
        "_7499": ["RollingRingAssemblyCompoundAdvancedSystemDeflection"],
        "_7500": ["RollingRingCompoundAdvancedSystemDeflection"],
        "_7501": ["RollingRingConnectionCompoundAdvancedSystemDeflection"],
        "_7502": ["RootAssemblyCompoundAdvancedSystemDeflection"],
        "_7503": ["ShaftCompoundAdvancedSystemDeflection"],
        "_7504": ["ShaftHubConnectionCompoundAdvancedSystemDeflection"],
        "_7505": [
            "ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection"
        ],
        "_7506": ["SpecialisedAssemblyCompoundAdvancedSystemDeflection"],
        "_7507": ["SpiralBevelGearCompoundAdvancedSystemDeflection"],
        "_7508": ["SpiralBevelGearMeshCompoundAdvancedSystemDeflection"],
        "_7509": ["SpiralBevelGearSetCompoundAdvancedSystemDeflection"],
        "_7510": ["SpringDamperCompoundAdvancedSystemDeflection"],
        "_7511": ["SpringDamperConnectionCompoundAdvancedSystemDeflection"],
        "_7512": ["SpringDamperHalfCompoundAdvancedSystemDeflection"],
        "_7513": ["StraightBevelDiffGearCompoundAdvancedSystemDeflection"],
        "_7514": ["StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection"],
        "_7515": ["StraightBevelDiffGearSetCompoundAdvancedSystemDeflection"],
        "_7516": ["StraightBevelGearCompoundAdvancedSystemDeflection"],
        "_7517": ["StraightBevelGearMeshCompoundAdvancedSystemDeflection"],
        "_7518": ["StraightBevelGearSetCompoundAdvancedSystemDeflection"],
        "_7519": ["StraightBevelPlanetGearCompoundAdvancedSystemDeflection"],
        "_7520": ["StraightBevelSunGearCompoundAdvancedSystemDeflection"],
        "_7521": ["SynchroniserCompoundAdvancedSystemDeflection"],
        "_7522": ["SynchroniserHalfCompoundAdvancedSystemDeflection"],
        "_7523": ["SynchroniserPartCompoundAdvancedSystemDeflection"],
        "_7524": ["SynchroniserSleeveCompoundAdvancedSystemDeflection"],
        "_7525": ["TorqueConverterCompoundAdvancedSystemDeflection"],
        "_7526": ["TorqueConverterConnectionCompoundAdvancedSystemDeflection"],
        "_7527": ["TorqueConverterPumpCompoundAdvancedSystemDeflection"],
        "_7528": ["TorqueConverterTurbineCompoundAdvancedSystemDeflection"],
        "_7529": ["UnbalancedMassCompoundAdvancedSystemDeflection"],
        "_7530": ["VirtualComponentCompoundAdvancedSystemDeflection"],
        "_7531": ["WormGearCompoundAdvancedSystemDeflection"],
        "_7532": ["WormGearMeshCompoundAdvancedSystemDeflection"],
        "_7533": ["WormGearSetCompoundAdvancedSystemDeflection"],
        "_7534": ["ZerolBevelGearCompoundAdvancedSystemDeflection"],
        "_7535": ["ZerolBevelGearMeshCompoundAdvancedSystemDeflection"],
        "_7536": ["ZerolBevelGearSetCompoundAdvancedSystemDeflection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundAdvancedSystemDeflection",
    "AbstractShaftCompoundAdvancedSystemDeflection",
    "AbstractShaftOrHousingCompoundAdvancedSystemDeflection",
    "AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection",
    "AGMAGleasonConicalGearCompoundAdvancedSystemDeflection",
    "AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection",
    "AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection",
    "AssemblyCompoundAdvancedSystemDeflection",
    "BearingCompoundAdvancedSystemDeflection",
    "BeltConnectionCompoundAdvancedSystemDeflection",
    "BeltDriveCompoundAdvancedSystemDeflection",
    "BevelDifferentialGearCompoundAdvancedSystemDeflection",
    "BevelDifferentialGearMeshCompoundAdvancedSystemDeflection",
    "BevelDifferentialGearSetCompoundAdvancedSystemDeflection",
    "BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection",
    "BevelDifferentialSunGearCompoundAdvancedSystemDeflection",
    "BevelGearCompoundAdvancedSystemDeflection",
    "BevelGearMeshCompoundAdvancedSystemDeflection",
    "BevelGearSetCompoundAdvancedSystemDeflection",
    "BoltCompoundAdvancedSystemDeflection",
    "BoltedJointCompoundAdvancedSystemDeflection",
    "ClutchCompoundAdvancedSystemDeflection",
    "ClutchConnectionCompoundAdvancedSystemDeflection",
    "ClutchHalfCompoundAdvancedSystemDeflection",
    "CoaxialConnectionCompoundAdvancedSystemDeflection",
    "ComponentCompoundAdvancedSystemDeflection",
    "ConceptCouplingCompoundAdvancedSystemDeflection",
    "ConceptCouplingConnectionCompoundAdvancedSystemDeflection",
    "ConceptCouplingHalfCompoundAdvancedSystemDeflection",
    "ConceptGearCompoundAdvancedSystemDeflection",
    "ConceptGearMeshCompoundAdvancedSystemDeflection",
    "ConceptGearSetCompoundAdvancedSystemDeflection",
    "ConicalGearCompoundAdvancedSystemDeflection",
    "ConicalGearMeshCompoundAdvancedSystemDeflection",
    "ConicalGearSetCompoundAdvancedSystemDeflection",
    "ConnectionCompoundAdvancedSystemDeflection",
    "ConnectorCompoundAdvancedSystemDeflection",
    "CouplingCompoundAdvancedSystemDeflection",
    "CouplingConnectionCompoundAdvancedSystemDeflection",
    "CouplingHalfCompoundAdvancedSystemDeflection",
    "CVTBeltConnectionCompoundAdvancedSystemDeflection",
    "CVTCompoundAdvancedSystemDeflection",
    "CVTPulleyCompoundAdvancedSystemDeflection",
    "CycloidalAssemblyCompoundAdvancedSystemDeflection",
    "CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection",
    "CycloidalDiscCompoundAdvancedSystemDeflection",
    "CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection",
    "CylindricalGearCompoundAdvancedSystemDeflection",
    "CylindricalGearMeshCompoundAdvancedSystemDeflection",
    "CylindricalGearSetCompoundAdvancedSystemDeflection",
    "CylindricalPlanetGearCompoundAdvancedSystemDeflection",
    "DatumCompoundAdvancedSystemDeflection",
    "ExternalCADModelCompoundAdvancedSystemDeflection",
    "FaceGearCompoundAdvancedSystemDeflection",
    "FaceGearMeshCompoundAdvancedSystemDeflection",
    "FaceGearSetCompoundAdvancedSystemDeflection",
    "FEPartCompoundAdvancedSystemDeflection",
    "FlexiblePinAssemblyCompoundAdvancedSystemDeflection",
    "GearCompoundAdvancedSystemDeflection",
    "GearMeshCompoundAdvancedSystemDeflection",
    "GearSetCompoundAdvancedSystemDeflection",
    "GuideDxfModelCompoundAdvancedSystemDeflection",
    "HypoidGearCompoundAdvancedSystemDeflection",
    "HypoidGearMeshCompoundAdvancedSystemDeflection",
    "HypoidGearSetCompoundAdvancedSystemDeflection",
    "InterMountableComponentConnectionCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection",
    "MassDiscCompoundAdvancedSystemDeflection",
    "MeasurementComponentCompoundAdvancedSystemDeflection",
    "MountableComponentCompoundAdvancedSystemDeflection",
    "OilSealCompoundAdvancedSystemDeflection",
    "PartCompoundAdvancedSystemDeflection",
    "PartToPartShearCouplingCompoundAdvancedSystemDeflection",
    "PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection",
    "PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection",
    "PlanetaryConnectionCompoundAdvancedSystemDeflection",
    "PlanetaryGearSetCompoundAdvancedSystemDeflection",
    "PlanetCarrierCompoundAdvancedSystemDeflection",
    "PointLoadCompoundAdvancedSystemDeflection",
    "PowerLoadCompoundAdvancedSystemDeflection",
    "PulleyCompoundAdvancedSystemDeflection",
    "RingPinsCompoundAdvancedSystemDeflection",
    "RingPinsToDiscConnectionCompoundAdvancedSystemDeflection",
    "RollingRingAssemblyCompoundAdvancedSystemDeflection",
    "RollingRingCompoundAdvancedSystemDeflection",
    "RollingRingConnectionCompoundAdvancedSystemDeflection",
    "RootAssemblyCompoundAdvancedSystemDeflection",
    "ShaftCompoundAdvancedSystemDeflection",
    "ShaftHubConnectionCompoundAdvancedSystemDeflection",
    "ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection",
    "SpecialisedAssemblyCompoundAdvancedSystemDeflection",
    "SpiralBevelGearCompoundAdvancedSystemDeflection",
    "SpiralBevelGearMeshCompoundAdvancedSystemDeflection",
    "SpiralBevelGearSetCompoundAdvancedSystemDeflection",
    "SpringDamperCompoundAdvancedSystemDeflection",
    "SpringDamperConnectionCompoundAdvancedSystemDeflection",
    "SpringDamperHalfCompoundAdvancedSystemDeflection",
    "StraightBevelDiffGearCompoundAdvancedSystemDeflection",
    "StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection",
    "StraightBevelDiffGearSetCompoundAdvancedSystemDeflection",
    "StraightBevelGearCompoundAdvancedSystemDeflection",
    "StraightBevelGearMeshCompoundAdvancedSystemDeflection",
    "StraightBevelGearSetCompoundAdvancedSystemDeflection",
    "StraightBevelPlanetGearCompoundAdvancedSystemDeflection",
    "StraightBevelSunGearCompoundAdvancedSystemDeflection",
    "SynchroniserCompoundAdvancedSystemDeflection",
    "SynchroniserHalfCompoundAdvancedSystemDeflection",
    "SynchroniserPartCompoundAdvancedSystemDeflection",
    "SynchroniserSleeveCompoundAdvancedSystemDeflection",
    "TorqueConverterCompoundAdvancedSystemDeflection",
    "TorqueConverterConnectionCompoundAdvancedSystemDeflection",
    "TorqueConverterPumpCompoundAdvancedSystemDeflection",
    "TorqueConverterTurbineCompoundAdvancedSystemDeflection",
    "UnbalancedMassCompoundAdvancedSystemDeflection",
    "VirtualComponentCompoundAdvancedSystemDeflection",
    "WormGearCompoundAdvancedSystemDeflection",
    "WormGearMeshCompoundAdvancedSystemDeflection",
    "WormGearSetCompoundAdvancedSystemDeflection",
    "ZerolBevelGearCompoundAdvancedSystemDeflection",
    "ZerolBevelGearMeshCompoundAdvancedSystemDeflection",
    "ZerolBevelGearSetCompoundAdvancedSystemDeflection",
)
