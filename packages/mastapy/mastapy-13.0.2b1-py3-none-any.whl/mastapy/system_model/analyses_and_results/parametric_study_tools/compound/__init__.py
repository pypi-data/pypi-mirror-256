"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._4445 import AbstractAssemblyCompoundParametricStudyTool
    from ._4446 import AbstractShaftCompoundParametricStudyTool
    from ._4447 import AbstractShaftOrHousingCompoundParametricStudyTool
    from ._4448 import (
        AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool,
    )
    from ._4449 import AGMAGleasonConicalGearCompoundParametricStudyTool
    from ._4450 import AGMAGleasonConicalGearMeshCompoundParametricStudyTool
    from ._4451 import AGMAGleasonConicalGearSetCompoundParametricStudyTool
    from ._4452 import AssemblyCompoundParametricStudyTool
    from ._4453 import BearingCompoundParametricStudyTool
    from ._4454 import BeltConnectionCompoundParametricStudyTool
    from ._4455 import BeltDriveCompoundParametricStudyTool
    from ._4456 import BevelDifferentialGearCompoundParametricStudyTool
    from ._4457 import BevelDifferentialGearMeshCompoundParametricStudyTool
    from ._4458 import BevelDifferentialGearSetCompoundParametricStudyTool
    from ._4459 import BevelDifferentialPlanetGearCompoundParametricStudyTool
    from ._4460 import BevelDifferentialSunGearCompoundParametricStudyTool
    from ._4461 import BevelGearCompoundParametricStudyTool
    from ._4462 import BevelGearMeshCompoundParametricStudyTool
    from ._4463 import BevelGearSetCompoundParametricStudyTool
    from ._4464 import BoltCompoundParametricStudyTool
    from ._4465 import BoltedJointCompoundParametricStudyTool
    from ._4466 import ClutchCompoundParametricStudyTool
    from ._4467 import ClutchConnectionCompoundParametricStudyTool
    from ._4468 import ClutchHalfCompoundParametricStudyTool
    from ._4469 import CoaxialConnectionCompoundParametricStudyTool
    from ._4470 import ComponentCompoundParametricStudyTool
    from ._4471 import ConceptCouplingCompoundParametricStudyTool
    from ._4472 import ConceptCouplingConnectionCompoundParametricStudyTool
    from ._4473 import ConceptCouplingHalfCompoundParametricStudyTool
    from ._4474 import ConceptGearCompoundParametricStudyTool
    from ._4475 import ConceptGearMeshCompoundParametricStudyTool
    from ._4476 import ConceptGearSetCompoundParametricStudyTool
    from ._4477 import ConicalGearCompoundParametricStudyTool
    from ._4478 import ConicalGearMeshCompoundParametricStudyTool
    from ._4479 import ConicalGearSetCompoundParametricStudyTool
    from ._4480 import ConnectionCompoundParametricStudyTool
    from ._4481 import ConnectorCompoundParametricStudyTool
    from ._4482 import CouplingCompoundParametricStudyTool
    from ._4483 import CouplingConnectionCompoundParametricStudyTool
    from ._4484 import CouplingHalfCompoundParametricStudyTool
    from ._4485 import CVTBeltConnectionCompoundParametricStudyTool
    from ._4486 import CVTCompoundParametricStudyTool
    from ._4487 import CVTPulleyCompoundParametricStudyTool
    from ._4488 import CycloidalAssemblyCompoundParametricStudyTool
    from ._4489 import CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool
    from ._4490 import CycloidalDiscCompoundParametricStudyTool
    from ._4491 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool,
    )
    from ._4492 import CylindricalGearCompoundParametricStudyTool
    from ._4493 import CylindricalGearMeshCompoundParametricStudyTool
    from ._4494 import CylindricalGearSetCompoundParametricStudyTool
    from ._4495 import CylindricalPlanetGearCompoundParametricStudyTool
    from ._4496 import DatumCompoundParametricStudyTool
    from ._4497 import ExternalCADModelCompoundParametricStudyTool
    from ._4498 import FaceGearCompoundParametricStudyTool
    from ._4499 import FaceGearMeshCompoundParametricStudyTool
    from ._4500 import FaceGearSetCompoundParametricStudyTool
    from ._4501 import FEPartCompoundParametricStudyTool
    from ._4502 import FlexiblePinAssemblyCompoundParametricStudyTool
    from ._4503 import GearCompoundParametricStudyTool
    from ._4504 import GearMeshCompoundParametricStudyTool
    from ._4505 import GearSetCompoundParametricStudyTool
    from ._4506 import GuideDxfModelCompoundParametricStudyTool
    from ._4507 import HypoidGearCompoundParametricStudyTool
    from ._4508 import HypoidGearMeshCompoundParametricStudyTool
    from ._4509 import HypoidGearSetCompoundParametricStudyTool
    from ._4510 import InterMountableComponentConnectionCompoundParametricStudyTool
    from ._4511 import KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool
    from ._4512 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool,
    )
    from ._4513 import KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool
    from ._4514 import KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool
    from ._4515 import KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
    from ._4516 import KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool
    from ._4517 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool,
    )
    from ._4518 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool,
    )
    from ._4519 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool,
    )
    from ._4520 import MassDiscCompoundParametricStudyTool
    from ._4521 import MeasurementComponentCompoundParametricStudyTool
    from ._4522 import MountableComponentCompoundParametricStudyTool
    from ._4523 import OilSealCompoundParametricStudyTool
    from ._4524 import PartCompoundParametricStudyTool
    from ._4525 import PartToPartShearCouplingCompoundParametricStudyTool
    from ._4526 import PartToPartShearCouplingConnectionCompoundParametricStudyTool
    from ._4527 import PartToPartShearCouplingHalfCompoundParametricStudyTool
    from ._4528 import PlanetaryConnectionCompoundParametricStudyTool
    from ._4529 import PlanetaryGearSetCompoundParametricStudyTool
    from ._4530 import PlanetCarrierCompoundParametricStudyTool
    from ._4531 import PointLoadCompoundParametricStudyTool
    from ._4532 import PowerLoadCompoundParametricStudyTool
    from ._4533 import PulleyCompoundParametricStudyTool
    from ._4534 import RingPinsCompoundParametricStudyTool
    from ._4535 import RingPinsToDiscConnectionCompoundParametricStudyTool
    from ._4536 import RollingRingAssemblyCompoundParametricStudyTool
    from ._4537 import RollingRingCompoundParametricStudyTool
    from ._4538 import RollingRingConnectionCompoundParametricStudyTool
    from ._4539 import RootAssemblyCompoundParametricStudyTool
    from ._4540 import ShaftCompoundParametricStudyTool
    from ._4541 import ShaftHubConnectionCompoundParametricStudyTool
    from ._4542 import ShaftToMountableComponentConnectionCompoundParametricStudyTool
    from ._4543 import SpecialisedAssemblyCompoundParametricStudyTool
    from ._4544 import SpiralBevelGearCompoundParametricStudyTool
    from ._4545 import SpiralBevelGearMeshCompoundParametricStudyTool
    from ._4546 import SpiralBevelGearSetCompoundParametricStudyTool
    from ._4547 import SpringDamperCompoundParametricStudyTool
    from ._4548 import SpringDamperConnectionCompoundParametricStudyTool
    from ._4549 import SpringDamperHalfCompoundParametricStudyTool
    from ._4550 import StraightBevelDiffGearCompoundParametricStudyTool
    from ._4551 import StraightBevelDiffGearMeshCompoundParametricStudyTool
    from ._4552 import StraightBevelDiffGearSetCompoundParametricStudyTool
    from ._4553 import StraightBevelGearCompoundParametricStudyTool
    from ._4554 import StraightBevelGearMeshCompoundParametricStudyTool
    from ._4555 import StraightBevelGearSetCompoundParametricStudyTool
    from ._4556 import StraightBevelPlanetGearCompoundParametricStudyTool
    from ._4557 import StraightBevelSunGearCompoundParametricStudyTool
    from ._4558 import SynchroniserCompoundParametricStudyTool
    from ._4559 import SynchroniserHalfCompoundParametricStudyTool
    from ._4560 import SynchroniserPartCompoundParametricStudyTool
    from ._4561 import SynchroniserSleeveCompoundParametricStudyTool
    from ._4562 import TorqueConverterCompoundParametricStudyTool
    from ._4563 import TorqueConverterConnectionCompoundParametricStudyTool
    from ._4564 import TorqueConverterPumpCompoundParametricStudyTool
    from ._4565 import TorqueConverterTurbineCompoundParametricStudyTool
    from ._4566 import UnbalancedMassCompoundParametricStudyTool
    from ._4567 import VirtualComponentCompoundParametricStudyTool
    from ._4568 import WormGearCompoundParametricStudyTool
    from ._4569 import WormGearMeshCompoundParametricStudyTool
    from ._4570 import WormGearSetCompoundParametricStudyTool
    from ._4571 import ZerolBevelGearCompoundParametricStudyTool
    from ._4572 import ZerolBevelGearMeshCompoundParametricStudyTool
    from ._4573 import ZerolBevelGearSetCompoundParametricStudyTool
else:
    import_structure = {
        "_4445": ["AbstractAssemblyCompoundParametricStudyTool"],
        "_4446": ["AbstractShaftCompoundParametricStudyTool"],
        "_4447": ["AbstractShaftOrHousingCompoundParametricStudyTool"],
        "_4448": [
            "AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool"
        ],
        "_4449": ["AGMAGleasonConicalGearCompoundParametricStudyTool"],
        "_4450": ["AGMAGleasonConicalGearMeshCompoundParametricStudyTool"],
        "_4451": ["AGMAGleasonConicalGearSetCompoundParametricStudyTool"],
        "_4452": ["AssemblyCompoundParametricStudyTool"],
        "_4453": ["BearingCompoundParametricStudyTool"],
        "_4454": ["BeltConnectionCompoundParametricStudyTool"],
        "_4455": ["BeltDriveCompoundParametricStudyTool"],
        "_4456": ["BevelDifferentialGearCompoundParametricStudyTool"],
        "_4457": ["BevelDifferentialGearMeshCompoundParametricStudyTool"],
        "_4458": ["BevelDifferentialGearSetCompoundParametricStudyTool"],
        "_4459": ["BevelDifferentialPlanetGearCompoundParametricStudyTool"],
        "_4460": ["BevelDifferentialSunGearCompoundParametricStudyTool"],
        "_4461": ["BevelGearCompoundParametricStudyTool"],
        "_4462": ["BevelGearMeshCompoundParametricStudyTool"],
        "_4463": ["BevelGearSetCompoundParametricStudyTool"],
        "_4464": ["BoltCompoundParametricStudyTool"],
        "_4465": ["BoltedJointCompoundParametricStudyTool"],
        "_4466": ["ClutchCompoundParametricStudyTool"],
        "_4467": ["ClutchConnectionCompoundParametricStudyTool"],
        "_4468": ["ClutchHalfCompoundParametricStudyTool"],
        "_4469": ["CoaxialConnectionCompoundParametricStudyTool"],
        "_4470": ["ComponentCompoundParametricStudyTool"],
        "_4471": ["ConceptCouplingCompoundParametricStudyTool"],
        "_4472": ["ConceptCouplingConnectionCompoundParametricStudyTool"],
        "_4473": ["ConceptCouplingHalfCompoundParametricStudyTool"],
        "_4474": ["ConceptGearCompoundParametricStudyTool"],
        "_4475": ["ConceptGearMeshCompoundParametricStudyTool"],
        "_4476": ["ConceptGearSetCompoundParametricStudyTool"],
        "_4477": ["ConicalGearCompoundParametricStudyTool"],
        "_4478": ["ConicalGearMeshCompoundParametricStudyTool"],
        "_4479": ["ConicalGearSetCompoundParametricStudyTool"],
        "_4480": ["ConnectionCompoundParametricStudyTool"],
        "_4481": ["ConnectorCompoundParametricStudyTool"],
        "_4482": ["CouplingCompoundParametricStudyTool"],
        "_4483": ["CouplingConnectionCompoundParametricStudyTool"],
        "_4484": ["CouplingHalfCompoundParametricStudyTool"],
        "_4485": ["CVTBeltConnectionCompoundParametricStudyTool"],
        "_4486": ["CVTCompoundParametricStudyTool"],
        "_4487": ["CVTPulleyCompoundParametricStudyTool"],
        "_4488": ["CycloidalAssemblyCompoundParametricStudyTool"],
        "_4489": ["CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool"],
        "_4490": ["CycloidalDiscCompoundParametricStudyTool"],
        "_4491": ["CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool"],
        "_4492": ["CylindricalGearCompoundParametricStudyTool"],
        "_4493": ["CylindricalGearMeshCompoundParametricStudyTool"],
        "_4494": ["CylindricalGearSetCompoundParametricStudyTool"],
        "_4495": ["CylindricalPlanetGearCompoundParametricStudyTool"],
        "_4496": ["DatumCompoundParametricStudyTool"],
        "_4497": ["ExternalCADModelCompoundParametricStudyTool"],
        "_4498": ["FaceGearCompoundParametricStudyTool"],
        "_4499": ["FaceGearMeshCompoundParametricStudyTool"],
        "_4500": ["FaceGearSetCompoundParametricStudyTool"],
        "_4501": ["FEPartCompoundParametricStudyTool"],
        "_4502": ["FlexiblePinAssemblyCompoundParametricStudyTool"],
        "_4503": ["GearCompoundParametricStudyTool"],
        "_4504": ["GearMeshCompoundParametricStudyTool"],
        "_4505": ["GearSetCompoundParametricStudyTool"],
        "_4506": ["GuideDxfModelCompoundParametricStudyTool"],
        "_4507": ["HypoidGearCompoundParametricStudyTool"],
        "_4508": ["HypoidGearMeshCompoundParametricStudyTool"],
        "_4509": ["HypoidGearSetCompoundParametricStudyTool"],
        "_4510": ["InterMountableComponentConnectionCompoundParametricStudyTool"],
        "_4511": ["KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool"],
        "_4512": ["KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool"],
        "_4513": ["KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool"],
        "_4514": ["KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool"],
        "_4515": ["KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool"],
        "_4516": ["KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool"],
        "_4517": ["KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool"],
        "_4518": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool"
        ],
        "_4519": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool"
        ],
        "_4520": ["MassDiscCompoundParametricStudyTool"],
        "_4521": ["MeasurementComponentCompoundParametricStudyTool"],
        "_4522": ["MountableComponentCompoundParametricStudyTool"],
        "_4523": ["OilSealCompoundParametricStudyTool"],
        "_4524": ["PartCompoundParametricStudyTool"],
        "_4525": ["PartToPartShearCouplingCompoundParametricStudyTool"],
        "_4526": ["PartToPartShearCouplingConnectionCompoundParametricStudyTool"],
        "_4527": ["PartToPartShearCouplingHalfCompoundParametricStudyTool"],
        "_4528": ["PlanetaryConnectionCompoundParametricStudyTool"],
        "_4529": ["PlanetaryGearSetCompoundParametricStudyTool"],
        "_4530": ["PlanetCarrierCompoundParametricStudyTool"],
        "_4531": ["PointLoadCompoundParametricStudyTool"],
        "_4532": ["PowerLoadCompoundParametricStudyTool"],
        "_4533": ["PulleyCompoundParametricStudyTool"],
        "_4534": ["RingPinsCompoundParametricStudyTool"],
        "_4535": ["RingPinsToDiscConnectionCompoundParametricStudyTool"],
        "_4536": ["RollingRingAssemblyCompoundParametricStudyTool"],
        "_4537": ["RollingRingCompoundParametricStudyTool"],
        "_4538": ["RollingRingConnectionCompoundParametricStudyTool"],
        "_4539": ["RootAssemblyCompoundParametricStudyTool"],
        "_4540": ["ShaftCompoundParametricStudyTool"],
        "_4541": ["ShaftHubConnectionCompoundParametricStudyTool"],
        "_4542": ["ShaftToMountableComponentConnectionCompoundParametricStudyTool"],
        "_4543": ["SpecialisedAssemblyCompoundParametricStudyTool"],
        "_4544": ["SpiralBevelGearCompoundParametricStudyTool"],
        "_4545": ["SpiralBevelGearMeshCompoundParametricStudyTool"],
        "_4546": ["SpiralBevelGearSetCompoundParametricStudyTool"],
        "_4547": ["SpringDamperCompoundParametricStudyTool"],
        "_4548": ["SpringDamperConnectionCompoundParametricStudyTool"],
        "_4549": ["SpringDamperHalfCompoundParametricStudyTool"],
        "_4550": ["StraightBevelDiffGearCompoundParametricStudyTool"],
        "_4551": ["StraightBevelDiffGearMeshCompoundParametricStudyTool"],
        "_4552": ["StraightBevelDiffGearSetCompoundParametricStudyTool"],
        "_4553": ["StraightBevelGearCompoundParametricStudyTool"],
        "_4554": ["StraightBevelGearMeshCompoundParametricStudyTool"],
        "_4555": ["StraightBevelGearSetCompoundParametricStudyTool"],
        "_4556": ["StraightBevelPlanetGearCompoundParametricStudyTool"],
        "_4557": ["StraightBevelSunGearCompoundParametricStudyTool"],
        "_4558": ["SynchroniserCompoundParametricStudyTool"],
        "_4559": ["SynchroniserHalfCompoundParametricStudyTool"],
        "_4560": ["SynchroniserPartCompoundParametricStudyTool"],
        "_4561": ["SynchroniserSleeveCompoundParametricStudyTool"],
        "_4562": ["TorqueConverterCompoundParametricStudyTool"],
        "_4563": ["TorqueConverterConnectionCompoundParametricStudyTool"],
        "_4564": ["TorqueConverterPumpCompoundParametricStudyTool"],
        "_4565": ["TorqueConverterTurbineCompoundParametricStudyTool"],
        "_4566": ["UnbalancedMassCompoundParametricStudyTool"],
        "_4567": ["VirtualComponentCompoundParametricStudyTool"],
        "_4568": ["WormGearCompoundParametricStudyTool"],
        "_4569": ["WormGearMeshCompoundParametricStudyTool"],
        "_4570": ["WormGearSetCompoundParametricStudyTool"],
        "_4571": ["ZerolBevelGearCompoundParametricStudyTool"],
        "_4572": ["ZerolBevelGearMeshCompoundParametricStudyTool"],
        "_4573": ["ZerolBevelGearSetCompoundParametricStudyTool"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundParametricStudyTool",
    "AbstractShaftCompoundParametricStudyTool",
    "AbstractShaftOrHousingCompoundParametricStudyTool",
    "AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool",
    "AGMAGleasonConicalGearCompoundParametricStudyTool",
    "AGMAGleasonConicalGearMeshCompoundParametricStudyTool",
    "AGMAGleasonConicalGearSetCompoundParametricStudyTool",
    "AssemblyCompoundParametricStudyTool",
    "BearingCompoundParametricStudyTool",
    "BeltConnectionCompoundParametricStudyTool",
    "BeltDriveCompoundParametricStudyTool",
    "BevelDifferentialGearCompoundParametricStudyTool",
    "BevelDifferentialGearMeshCompoundParametricStudyTool",
    "BevelDifferentialGearSetCompoundParametricStudyTool",
    "BevelDifferentialPlanetGearCompoundParametricStudyTool",
    "BevelDifferentialSunGearCompoundParametricStudyTool",
    "BevelGearCompoundParametricStudyTool",
    "BevelGearMeshCompoundParametricStudyTool",
    "BevelGearSetCompoundParametricStudyTool",
    "BoltCompoundParametricStudyTool",
    "BoltedJointCompoundParametricStudyTool",
    "ClutchCompoundParametricStudyTool",
    "ClutchConnectionCompoundParametricStudyTool",
    "ClutchHalfCompoundParametricStudyTool",
    "CoaxialConnectionCompoundParametricStudyTool",
    "ComponentCompoundParametricStudyTool",
    "ConceptCouplingCompoundParametricStudyTool",
    "ConceptCouplingConnectionCompoundParametricStudyTool",
    "ConceptCouplingHalfCompoundParametricStudyTool",
    "ConceptGearCompoundParametricStudyTool",
    "ConceptGearMeshCompoundParametricStudyTool",
    "ConceptGearSetCompoundParametricStudyTool",
    "ConicalGearCompoundParametricStudyTool",
    "ConicalGearMeshCompoundParametricStudyTool",
    "ConicalGearSetCompoundParametricStudyTool",
    "ConnectionCompoundParametricStudyTool",
    "ConnectorCompoundParametricStudyTool",
    "CouplingCompoundParametricStudyTool",
    "CouplingConnectionCompoundParametricStudyTool",
    "CouplingHalfCompoundParametricStudyTool",
    "CVTBeltConnectionCompoundParametricStudyTool",
    "CVTCompoundParametricStudyTool",
    "CVTPulleyCompoundParametricStudyTool",
    "CycloidalAssemblyCompoundParametricStudyTool",
    "CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool",
    "CycloidalDiscCompoundParametricStudyTool",
    "CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool",
    "CylindricalGearCompoundParametricStudyTool",
    "CylindricalGearMeshCompoundParametricStudyTool",
    "CylindricalGearSetCompoundParametricStudyTool",
    "CylindricalPlanetGearCompoundParametricStudyTool",
    "DatumCompoundParametricStudyTool",
    "ExternalCADModelCompoundParametricStudyTool",
    "FaceGearCompoundParametricStudyTool",
    "FaceGearMeshCompoundParametricStudyTool",
    "FaceGearSetCompoundParametricStudyTool",
    "FEPartCompoundParametricStudyTool",
    "FlexiblePinAssemblyCompoundParametricStudyTool",
    "GearCompoundParametricStudyTool",
    "GearMeshCompoundParametricStudyTool",
    "GearSetCompoundParametricStudyTool",
    "GuideDxfModelCompoundParametricStudyTool",
    "HypoidGearCompoundParametricStudyTool",
    "HypoidGearMeshCompoundParametricStudyTool",
    "HypoidGearSetCompoundParametricStudyTool",
    "InterMountableComponentConnectionCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool",
    "MassDiscCompoundParametricStudyTool",
    "MeasurementComponentCompoundParametricStudyTool",
    "MountableComponentCompoundParametricStudyTool",
    "OilSealCompoundParametricStudyTool",
    "PartCompoundParametricStudyTool",
    "PartToPartShearCouplingCompoundParametricStudyTool",
    "PartToPartShearCouplingConnectionCompoundParametricStudyTool",
    "PartToPartShearCouplingHalfCompoundParametricStudyTool",
    "PlanetaryConnectionCompoundParametricStudyTool",
    "PlanetaryGearSetCompoundParametricStudyTool",
    "PlanetCarrierCompoundParametricStudyTool",
    "PointLoadCompoundParametricStudyTool",
    "PowerLoadCompoundParametricStudyTool",
    "PulleyCompoundParametricStudyTool",
    "RingPinsCompoundParametricStudyTool",
    "RingPinsToDiscConnectionCompoundParametricStudyTool",
    "RollingRingAssemblyCompoundParametricStudyTool",
    "RollingRingCompoundParametricStudyTool",
    "RollingRingConnectionCompoundParametricStudyTool",
    "RootAssemblyCompoundParametricStudyTool",
    "ShaftCompoundParametricStudyTool",
    "ShaftHubConnectionCompoundParametricStudyTool",
    "ShaftToMountableComponentConnectionCompoundParametricStudyTool",
    "SpecialisedAssemblyCompoundParametricStudyTool",
    "SpiralBevelGearCompoundParametricStudyTool",
    "SpiralBevelGearMeshCompoundParametricStudyTool",
    "SpiralBevelGearSetCompoundParametricStudyTool",
    "SpringDamperCompoundParametricStudyTool",
    "SpringDamperConnectionCompoundParametricStudyTool",
    "SpringDamperHalfCompoundParametricStudyTool",
    "StraightBevelDiffGearCompoundParametricStudyTool",
    "StraightBevelDiffGearMeshCompoundParametricStudyTool",
    "StraightBevelDiffGearSetCompoundParametricStudyTool",
    "StraightBevelGearCompoundParametricStudyTool",
    "StraightBevelGearMeshCompoundParametricStudyTool",
    "StraightBevelGearSetCompoundParametricStudyTool",
    "StraightBevelPlanetGearCompoundParametricStudyTool",
    "StraightBevelSunGearCompoundParametricStudyTool",
    "SynchroniserCompoundParametricStudyTool",
    "SynchroniserHalfCompoundParametricStudyTool",
    "SynchroniserPartCompoundParametricStudyTool",
    "SynchroniserSleeveCompoundParametricStudyTool",
    "TorqueConverterCompoundParametricStudyTool",
    "TorqueConverterConnectionCompoundParametricStudyTool",
    "TorqueConverterPumpCompoundParametricStudyTool",
    "TorqueConverterTurbineCompoundParametricStudyTool",
    "UnbalancedMassCompoundParametricStudyTool",
    "VirtualComponentCompoundParametricStudyTool",
    "WormGearCompoundParametricStudyTool",
    "WormGearMeshCompoundParametricStudyTool",
    "WormGearSetCompoundParametricStudyTool",
    "ZerolBevelGearCompoundParametricStudyTool",
    "ZerolBevelGearMeshCompoundParametricStudyTool",
    "ZerolBevelGearSetCompoundParametricStudyTool",
)
