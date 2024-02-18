"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._6545 import AbstractAssemblyCriticalSpeedAnalysis
    from ._6546 import AbstractShaftCriticalSpeedAnalysis
    from ._6547 import AbstractShaftOrHousingCriticalSpeedAnalysis
    from ._6548 import AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis
    from ._6549 import AGMAGleasonConicalGearCriticalSpeedAnalysis
    from ._6550 import AGMAGleasonConicalGearMeshCriticalSpeedAnalysis
    from ._6551 import AGMAGleasonConicalGearSetCriticalSpeedAnalysis
    from ._6552 import AssemblyCriticalSpeedAnalysis
    from ._6553 import BearingCriticalSpeedAnalysis
    from ._6554 import BeltConnectionCriticalSpeedAnalysis
    from ._6555 import BeltDriveCriticalSpeedAnalysis
    from ._6556 import BevelDifferentialGearCriticalSpeedAnalysis
    from ._6557 import BevelDifferentialGearMeshCriticalSpeedAnalysis
    from ._6558 import BevelDifferentialGearSetCriticalSpeedAnalysis
    from ._6559 import BevelDifferentialPlanetGearCriticalSpeedAnalysis
    from ._6560 import BevelDifferentialSunGearCriticalSpeedAnalysis
    from ._6561 import BevelGearCriticalSpeedAnalysis
    from ._6562 import BevelGearMeshCriticalSpeedAnalysis
    from ._6563 import BevelGearSetCriticalSpeedAnalysis
    from ._6564 import BoltCriticalSpeedAnalysis
    from ._6565 import BoltedJointCriticalSpeedAnalysis
    from ._6566 import ClutchConnectionCriticalSpeedAnalysis
    from ._6567 import ClutchCriticalSpeedAnalysis
    from ._6568 import ClutchHalfCriticalSpeedAnalysis
    from ._6569 import CoaxialConnectionCriticalSpeedAnalysis
    from ._6570 import ComponentCriticalSpeedAnalysis
    from ._6571 import ConceptCouplingConnectionCriticalSpeedAnalysis
    from ._6572 import ConceptCouplingCriticalSpeedAnalysis
    from ._6573 import ConceptCouplingHalfCriticalSpeedAnalysis
    from ._6574 import ConceptGearCriticalSpeedAnalysis
    from ._6575 import ConceptGearMeshCriticalSpeedAnalysis
    from ._6576 import ConceptGearSetCriticalSpeedAnalysis
    from ._6577 import ConicalGearCriticalSpeedAnalysis
    from ._6578 import ConicalGearMeshCriticalSpeedAnalysis
    from ._6579 import ConicalGearSetCriticalSpeedAnalysis
    from ._6580 import ConnectionCriticalSpeedAnalysis
    from ._6581 import ConnectorCriticalSpeedAnalysis
    from ._6582 import CouplingConnectionCriticalSpeedAnalysis
    from ._6583 import CouplingCriticalSpeedAnalysis
    from ._6584 import CouplingHalfCriticalSpeedAnalysis
    from ._6585 import CriticalSpeedAnalysis
    from ._6586 import CriticalSpeedAnalysisDrawStyle
    from ._6587 import CriticalSpeedAnalysisOptions
    from ._6588 import CVTBeltConnectionCriticalSpeedAnalysis
    from ._6589 import CVTCriticalSpeedAnalysis
    from ._6590 import CVTPulleyCriticalSpeedAnalysis
    from ._6591 import CycloidalAssemblyCriticalSpeedAnalysis
    from ._6592 import CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis
    from ._6593 import CycloidalDiscCriticalSpeedAnalysis
    from ._6594 import CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis
    from ._6595 import CylindricalGearCriticalSpeedAnalysis
    from ._6596 import CylindricalGearMeshCriticalSpeedAnalysis
    from ._6597 import CylindricalGearSetCriticalSpeedAnalysis
    from ._6598 import CylindricalPlanetGearCriticalSpeedAnalysis
    from ._6599 import DatumCriticalSpeedAnalysis
    from ._6600 import ExternalCADModelCriticalSpeedAnalysis
    from ._6601 import FaceGearCriticalSpeedAnalysis
    from ._6602 import FaceGearMeshCriticalSpeedAnalysis
    from ._6603 import FaceGearSetCriticalSpeedAnalysis
    from ._6604 import FEPartCriticalSpeedAnalysis
    from ._6605 import FlexiblePinAssemblyCriticalSpeedAnalysis
    from ._6606 import GearCriticalSpeedAnalysis
    from ._6607 import GearMeshCriticalSpeedAnalysis
    from ._6608 import GearSetCriticalSpeedAnalysis
    from ._6609 import GuideDxfModelCriticalSpeedAnalysis
    from ._6610 import HypoidGearCriticalSpeedAnalysis
    from ._6611 import HypoidGearMeshCriticalSpeedAnalysis
    from ._6612 import HypoidGearSetCriticalSpeedAnalysis
    from ._6613 import InterMountableComponentConnectionCriticalSpeedAnalysis
    from ._6614 import KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis
    from ._6615 import KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis
    from ._6616 import KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis
    from ._6617 import KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis
    from ._6618 import KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis
    from ._6619 import KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis
    from ._6620 import KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis
    from ._6621 import KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis
    from ._6622 import KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis
    from ._6623 import MassDiscCriticalSpeedAnalysis
    from ._6624 import MeasurementComponentCriticalSpeedAnalysis
    from ._6625 import MountableComponentCriticalSpeedAnalysis
    from ._6626 import OilSealCriticalSpeedAnalysis
    from ._6627 import PartCriticalSpeedAnalysis
    from ._6628 import PartToPartShearCouplingConnectionCriticalSpeedAnalysis
    from ._6629 import PartToPartShearCouplingCriticalSpeedAnalysis
    from ._6630 import PartToPartShearCouplingHalfCriticalSpeedAnalysis
    from ._6631 import PlanetaryConnectionCriticalSpeedAnalysis
    from ._6632 import PlanetaryGearSetCriticalSpeedAnalysis
    from ._6633 import PlanetCarrierCriticalSpeedAnalysis
    from ._6634 import PointLoadCriticalSpeedAnalysis
    from ._6635 import PowerLoadCriticalSpeedAnalysis
    from ._6636 import PulleyCriticalSpeedAnalysis
    from ._6637 import RingPinsCriticalSpeedAnalysis
    from ._6638 import RingPinsToDiscConnectionCriticalSpeedAnalysis
    from ._6639 import RollingRingAssemblyCriticalSpeedAnalysis
    from ._6640 import RollingRingConnectionCriticalSpeedAnalysis
    from ._6641 import RollingRingCriticalSpeedAnalysis
    from ._6642 import RootAssemblyCriticalSpeedAnalysis
    from ._6643 import ShaftCriticalSpeedAnalysis
    from ._6644 import ShaftHubConnectionCriticalSpeedAnalysis
    from ._6645 import ShaftToMountableComponentConnectionCriticalSpeedAnalysis
    from ._6646 import SpecialisedAssemblyCriticalSpeedAnalysis
    from ._6647 import SpiralBevelGearCriticalSpeedAnalysis
    from ._6648 import SpiralBevelGearMeshCriticalSpeedAnalysis
    from ._6649 import SpiralBevelGearSetCriticalSpeedAnalysis
    from ._6650 import SpringDamperConnectionCriticalSpeedAnalysis
    from ._6651 import SpringDamperCriticalSpeedAnalysis
    from ._6652 import SpringDamperHalfCriticalSpeedAnalysis
    from ._6653 import StraightBevelDiffGearCriticalSpeedAnalysis
    from ._6654 import StraightBevelDiffGearMeshCriticalSpeedAnalysis
    from ._6655 import StraightBevelDiffGearSetCriticalSpeedAnalysis
    from ._6656 import StraightBevelGearCriticalSpeedAnalysis
    from ._6657 import StraightBevelGearMeshCriticalSpeedAnalysis
    from ._6658 import StraightBevelGearSetCriticalSpeedAnalysis
    from ._6659 import StraightBevelPlanetGearCriticalSpeedAnalysis
    from ._6660 import StraightBevelSunGearCriticalSpeedAnalysis
    from ._6661 import SynchroniserCriticalSpeedAnalysis
    from ._6662 import SynchroniserHalfCriticalSpeedAnalysis
    from ._6663 import SynchroniserPartCriticalSpeedAnalysis
    from ._6664 import SynchroniserSleeveCriticalSpeedAnalysis
    from ._6665 import TorqueConverterConnectionCriticalSpeedAnalysis
    from ._6666 import TorqueConverterCriticalSpeedAnalysis
    from ._6667 import TorqueConverterPumpCriticalSpeedAnalysis
    from ._6668 import TorqueConverterTurbineCriticalSpeedAnalysis
    from ._6669 import UnbalancedMassCriticalSpeedAnalysis
    from ._6670 import VirtualComponentCriticalSpeedAnalysis
    from ._6671 import WormGearCriticalSpeedAnalysis
    from ._6672 import WormGearMeshCriticalSpeedAnalysis
    from ._6673 import WormGearSetCriticalSpeedAnalysis
    from ._6674 import ZerolBevelGearCriticalSpeedAnalysis
    from ._6675 import ZerolBevelGearMeshCriticalSpeedAnalysis
    from ._6676 import ZerolBevelGearSetCriticalSpeedAnalysis
else:
    import_structure = {
        "_6545": ["AbstractAssemblyCriticalSpeedAnalysis"],
        "_6546": ["AbstractShaftCriticalSpeedAnalysis"],
        "_6547": ["AbstractShaftOrHousingCriticalSpeedAnalysis"],
        "_6548": ["AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis"],
        "_6549": ["AGMAGleasonConicalGearCriticalSpeedAnalysis"],
        "_6550": ["AGMAGleasonConicalGearMeshCriticalSpeedAnalysis"],
        "_6551": ["AGMAGleasonConicalGearSetCriticalSpeedAnalysis"],
        "_6552": ["AssemblyCriticalSpeedAnalysis"],
        "_6553": ["BearingCriticalSpeedAnalysis"],
        "_6554": ["BeltConnectionCriticalSpeedAnalysis"],
        "_6555": ["BeltDriveCriticalSpeedAnalysis"],
        "_6556": ["BevelDifferentialGearCriticalSpeedAnalysis"],
        "_6557": ["BevelDifferentialGearMeshCriticalSpeedAnalysis"],
        "_6558": ["BevelDifferentialGearSetCriticalSpeedAnalysis"],
        "_6559": ["BevelDifferentialPlanetGearCriticalSpeedAnalysis"],
        "_6560": ["BevelDifferentialSunGearCriticalSpeedAnalysis"],
        "_6561": ["BevelGearCriticalSpeedAnalysis"],
        "_6562": ["BevelGearMeshCriticalSpeedAnalysis"],
        "_6563": ["BevelGearSetCriticalSpeedAnalysis"],
        "_6564": ["BoltCriticalSpeedAnalysis"],
        "_6565": ["BoltedJointCriticalSpeedAnalysis"],
        "_6566": ["ClutchConnectionCriticalSpeedAnalysis"],
        "_6567": ["ClutchCriticalSpeedAnalysis"],
        "_6568": ["ClutchHalfCriticalSpeedAnalysis"],
        "_6569": ["CoaxialConnectionCriticalSpeedAnalysis"],
        "_6570": ["ComponentCriticalSpeedAnalysis"],
        "_6571": ["ConceptCouplingConnectionCriticalSpeedAnalysis"],
        "_6572": ["ConceptCouplingCriticalSpeedAnalysis"],
        "_6573": ["ConceptCouplingHalfCriticalSpeedAnalysis"],
        "_6574": ["ConceptGearCriticalSpeedAnalysis"],
        "_6575": ["ConceptGearMeshCriticalSpeedAnalysis"],
        "_6576": ["ConceptGearSetCriticalSpeedAnalysis"],
        "_6577": ["ConicalGearCriticalSpeedAnalysis"],
        "_6578": ["ConicalGearMeshCriticalSpeedAnalysis"],
        "_6579": ["ConicalGearSetCriticalSpeedAnalysis"],
        "_6580": ["ConnectionCriticalSpeedAnalysis"],
        "_6581": ["ConnectorCriticalSpeedAnalysis"],
        "_6582": ["CouplingConnectionCriticalSpeedAnalysis"],
        "_6583": ["CouplingCriticalSpeedAnalysis"],
        "_6584": ["CouplingHalfCriticalSpeedAnalysis"],
        "_6585": ["CriticalSpeedAnalysis"],
        "_6586": ["CriticalSpeedAnalysisDrawStyle"],
        "_6587": ["CriticalSpeedAnalysisOptions"],
        "_6588": ["CVTBeltConnectionCriticalSpeedAnalysis"],
        "_6589": ["CVTCriticalSpeedAnalysis"],
        "_6590": ["CVTPulleyCriticalSpeedAnalysis"],
        "_6591": ["CycloidalAssemblyCriticalSpeedAnalysis"],
        "_6592": ["CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis"],
        "_6593": ["CycloidalDiscCriticalSpeedAnalysis"],
        "_6594": ["CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis"],
        "_6595": ["CylindricalGearCriticalSpeedAnalysis"],
        "_6596": ["CylindricalGearMeshCriticalSpeedAnalysis"],
        "_6597": ["CylindricalGearSetCriticalSpeedAnalysis"],
        "_6598": ["CylindricalPlanetGearCriticalSpeedAnalysis"],
        "_6599": ["DatumCriticalSpeedAnalysis"],
        "_6600": ["ExternalCADModelCriticalSpeedAnalysis"],
        "_6601": ["FaceGearCriticalSpeedAnalysis"],
        "_6602": ["FaceGearMeshCriticalSpeedAnalysis"],
        "_6603": ["FaceGearSetCriticalSpeedAnalysis"],
        "_6604": ["FEPartCriticalSpeedAnalysis"],
        "_6605": ["FlexiblePinAssemblyCriticalSpeedAnalysis"],
        "_6606": ["GearCriticalSpeedAnalysis"],
        "_6607": ["GearMeshCriticalSpeedAnalysis"],
        "_6608": ["GearSetCriticalSpeedAnalysis"],
        "_6609": ["GuideDxfModelCriticalSpeedAnalysis"],
        "_6610": ["HypoidGearCriticalSpeedAnalysis"],
        "_6611": ["HypoidGearMeshCriticalSpeedAnalysis"],
        "_6612": ["HypoidGearSetCriticalSpeedAnalysis"],
        "_6613": ["InterMountableComponentConnectionCriticalSpeedAnalysis"],
        "_6614": ["KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis"],
        "_6615": ["KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis"],
        "_6616": ["KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis"],
        "_6617": ["KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis"],
        "_6618": ["KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis"],
        "_6619": ["KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis"],
        "_6620": ["KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis"],
        "_6621": ["KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis"],
        "_6622": ["KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis"],
        "_6623": ["MassDiscCriticalSpeedAnalysis"],
        "_6624": ["MeasurementComponentCriticalSpeedAnalysis"],
        "_6625": ["MountableComponentCriticalSpeedAnalysis"],
        "_6626": ["OilSealCriticalSpeedAnalysis"],
        "_6627": ["PartCriticalSpeedAnalysis"],
        "_6628": ["PartToPartShearCouplingConnectionCriticalSpeedAnalysis"],
        "_6629": ["PartToPartShearCouplingCriticalSpeedAnalysis"],
        "_6630": ["PartToPartShearCouplingHalfCriticalSpeedAnalysis"],
        "_6631": ["PlanetaryConnectionCriticalSpeedAnalysis"],
        "_6632": ["PlanetaryGearSetCriticalSpeedAnalysis"],
        "_6633": ["PlanetCarrierCriticalSpeedAnalysis"],
        "_6634": ["PointLoadCriticalSpeedAnalysis"],
        "_6635": ["PowerLoadCriticalSpeedAnalysis"],
        "_6636": ["PulleyCriticalSpeedAnalysis"],
        "_6637": ["RingPinsCriticalSpeedAnalysis"],
        "_6638": ["RingPinsToDiscConnectionCriticalSpeedAnalysis"],
        "_6639": ["RollingRingAssemblyCriticalSpeedAnalysis"],
        "_6640": ["RollingRingConnectionCriticalSpeedAnalysis"],
        "_6641": ["RollingRingCriticalSpeedAnalysis"],
        "_6642": ["RootAssemblyCriticalSpeedAnalysis"],
        "_6643": ["ShaftCriticalSpeedAnalysis"],
        "_6644": ["ShaftHubConnectionCriticalSpeedAnalysis"],
        "_6645": ["ShaftToMountableComponentConnectionCriticalSpeedAnalysis"],
        "_6646": ["SpecialisedAssemblyCriticalSpeedAnalysis"],
        "_6647": ["SpiralBevelGearCriticalSpeedAnalysis"],
        "_6648": ["SpiralBevelGearMeshCriticalSpeedAnalysis"],
        "_6649": ["SpiralBevelGearSetCriticalSpeedAnalysis"],
        "_6650": ["SpringDamperConnectionCriticalSpeedAnalysis"],
        "_6651": ["SpringDamperCriticalSpeedAnalysis"],
        "_6652": ["SpringDamperHalfCriticalSpeedAnalysis"],
        "_6653": ["StraightBevelDiffGearCriticalSpeedAnalysis"],
        "_6654": ["StraightBevelDiffGearMeshCriticalSpeedAnalysis"],
        "_6655": ["StraightBevelDiffGearSetCriticalSpeedAnalysis"],
        "_6656": ["StraightBevelGearCriticalSpeedAnalysis"],
        "_6657": ["StraightBevelGearMeshCriticalSpeedAnalysis"],
        "_6658": ["StraightBevelGearSetCriticalSpeedAnalysis"],
        "_6659": ["StraightBevelPlanetGearCriticalSpeedAnalysis"],
        "_6660": ["StraightBevelSunGearCriticalSpeedAnalysis"],
        "_6661": ["SynchroniserCriticalSpeedAnalysis"],
        "_6662": ["SynchroniserHalfCriticalSpeedAnalysis"],
        "_6663": ["SynchroniserPartCriticalSpeedAnalysis"],
        "_6664": ["SynchroniserSleeveCriticalSpeedAnalysis"],
        "_6665": ["TorqueConverterConnectionCriticalSpeedAnalysis"],
        "_6666": ["TorqueConverterCriticalSpeedAnalysis"],
        "_6667": ["TorqueConverterPumpCriticalSpeedAnalysis"],
        "_6668": ["TorqueConverterTurbineCriticalSpeedAnalysis"],
        "_6669": ["UnbalancedMassCriticalSpeedAnalysis"],
        "_6670": ["VirtualComponentCriticalSpeedAnalysis"],
        "_6671": ["WormGearCriticalSpeedAnalysis"],
        "_6672": ["WormGearMeshCriticalSpeedAnalysis"],
        "_6673": ["WormGearSetCriticalSpeedAnalysis"],
        "_6674": ["ZerolBevelGearCriticalSpeedAnalysis"],
        "_6675": ["ZerolBevelGearMeshCriticalSpeedAnalysis"],
        "_6676": ["ZerolBevelGearSetCriticalSpeedAnalysis"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCriticalSpeedAnalysis",
    "AbstractShaftCriticalSpeedAnalysis",
    "AbstractShaftOrHousingCriticalSpeedAnalysis",
    "AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis",
    "AGMAGleasonConicalGearCriticalSpeedAnalysis",
    "AGMAGleasonConicalGearMeshCriticalSpeedAnalysis",
    "AGMAGleasonConicalGearSetCriticalSpeedAnalysis",
    "AssemblyCriticalSpeedAnalysis",
    "BearingCriticalSpeedAnalysis",
    "BeltConnectionCriticalSpeedAnalysis",
    "BeltDriveCriticalSpeedAnalysis",
    "BevelDifferentialGearCriticalSpeedAnalysis",
    "BevelDifferentialGearMeshCriticalSpeedAnalysis",
    "BevelDifferentialGearSetCriticalSpeedAnalysis",
    "BevelDifferentialPlanetGearCriticalSpeedAnalysis",
    "BevelDifferentialSunGearCriticalSpeedAnalysis",
    "BevelGearCriticalSpeedAnalysis",
    "BevelGearMeshCriticalSpeedAnalysis",
    "BevelGearSetCriticalSpeedAnalysis",
    "BoltCriticalSpeedAnalysis",
    "BoltedJointCriticalSpeedAnalysis",
    "ClutchConnectionCriticalSpeedAnalysis",
    "ClutchCriticalSpeedAnalysis",
    "ClutchHalfCriticalSpeedAnalysis",
    "CoaxialConnectionCriticalSpeedAnalysis",
    "ComponentCriticalSpeedAnalysis",
    "ConceptCouplingConnectionCriticalSpeedAnalysis",
    "ConceptCouplingCriticalSpeedAnalysis",
    "ConceptCouplingHalfCriticalSpeedAnalysis",
    "ConceptGearCriticalSpeedAnalysis",
    "ConceptGearMeshCriticalSpeedAnalysis",
    "ConceptGearSetCriticalSpeedAnalysis",
    "ConicalGearCriticalSpeedAnalysis",
    "ConicalGearMeshCriticalSpeedAnalysis",
    "ConicalGearSetCriticalSpeedAnalysis",
    "ConnectionCriticalSpeedAnalysis",
    "ConnectorCriticalSpeedAnalysis",
    "CouplingConnectionCriticalSpeedAnalysis",
    "CouplingCriticalSpeedAnalysis",
    "CouplingHalfCriticalSpeedAnalysis",
    "CriticalSpeedAnalysis",
    "CriticalSpeedAnalysisDrawStyle",
    "CriticalSpeedAnalysisOptions",
    "CVTBeltConnectionCriticalSpeedAnalysis",
    "CVTCriticalSpeedAnalysis",
    "CVTPulleyCriticalSpeedAnalysis",
    "CycloidalAssemblyCriticalSpeedAnalysis",
    "CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis",
    "CycloidalDiscCriticalSpeedAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionCriticalSpeedAnalysis",
    "CylindricalGearCriticalSpeedAnalysis",
    "CylindricalGearMeshCriticalSpeedAnalysis",
    "CylindricalGearSetCriticalSpeedAnalysis",
    "CylindricalPlanetGearCriticalSpeedAnalysis",
    "DatumCriticalSpeedAnalysis",
    "ExternalCADModelCriticalSpeedAnalysis",
    "FaceGearCriticalSpeedAnalysis",
    "FaceGearMeshCriticalSpeedAnalysis",
    "FaceGearSetCriticalSpeedAnalysis",
    "FEPartCriticalSpeedAnalysis",
    "FlexiblePinAssemblyCriticalSpeedAnalysis",
    "GearCriticalSpeedAnalysis",
    "GearMeshCriticalSpeedAnalysis",
    "GearSetCriticalSpeedAnalysis",
    "GuideDxfModelCriticalSpeedAnalysis",
    "HypoidGearCriticalSpeedAnalysis",
    "HypoidGearMeshCriticalSpeedAnalysis",
    "HypoidGearSetCriticalSpeedAnalysis",
    "InterMountableComponentConnectionCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis",
    "MassDiscCriticalSpeedAnalysis",
    "MeasurementComponentCriticalSpeedAnalysis",
    "MountableComponentCriticalSpeedAnalysis",
    "OilSealCriticalSpeedAnalysis",
    "PartCriticalSpeedAnalysis",
    "PartToPartShearCouplingConnectionCriticalSpeedAnalysis",
    "PartToPartShearCouplingCriticalSpeedAnalysis",
    "PartToPartShearCouplingHalfCriticalSpeedAnalysis",
    "PlanetaryConnectionCriticalSpeedAnalysis",
    "PlanetaryGearSetCriticalSpeedAnalysis",
    "PlanetCarrierCriticalSpeedAnalysis",
    "PointLoadCriticalSpeedAnalysis",
    "PowerLoadCriticalSpeedAnalysis",
    "PulleyCriticalSpeedAnalysis",
    "RingPinsCriticalSpeedAnalysis",
    "RingPinsToDiscConnectionCriticalSpeedAnalysis",
    "RollingRingAssemblyCriticalSpeedAnalysis",
    "RollingRingConnectionCriticalSpeedAnalysis",
    "RollingRingCriticalSpeedAnalysis",
    "RootAssemblyCriticalSpeedAnalysis",
    "ShaftCriticalSpeedAnalysis",
    "ShaftHubConnectionCriticalSpeedAnalysis",
    "ShaftToMountableComponentConnectionCriticalSpeedAnalysis",
    "SpecialisedAssemblyCriticalSpeedAnalysis",
    "SpiralBevelGearCriticalSpeedAnalysis",
    "SpiralBevelGearMeshCriticalSpeedAnalysis",
    "SpiralBevelGearSetCriticalSpeedAnalysis",
    "SpringDamperConnectionCriticalSpeedAnalysis",
    "SpringDamperCriticalSpeedAnalysis",
    "SpringDamperHalfCriticalSpeedAnalysis",
    "StraightBevelDiffGearCriticalSpeedAnalysis",
    "StraightBevelDiffGearMeshCriticalSpeedAnalysis",
    "StraightBevelDiffGearSetCriticalSpeedAnalysis",
    "StraightBevelGearCriticalSpeedAnalysis",
    "StraightBevelGearMeshCriticalSpeedAnalysis",
    "StraightBevelGearSetCriticalSpeedAnalysis",
    "StraightBevelPlanetGearCriticalSpeedAnalysis",
    "StraightBevelSunGearCriticalSpeedAnalysis",
    "SynchroniserCriticalSpeedAnalysis",
    "SynchroniserHalfCriticalSpeedAnalysis",
    "SynchroniserPartCriticalSpeedAnalysis",
    "SynchroniserSleeveCriticalSpeedAnalysis",
    "TorqueConverterConnectionCriticalSpeedAnalysis",
    "TorqueConverterCriticalSpeedAnalysis",
    "TorqueConverterPumpCriticalSpeedAnalysis",
    "TorqueConverterTurbineCriticalSpeedAnalysis",
    "UnbalancedMassCriticalSpeedAnalysis",
    "VirtualComponentCriticalSpeedAnalysis",
    "WormGearCriticalSpeedAnalysis",
    "WormGearMeshCriticalSpeedAnalysis",
    "WormGearSetCriticalSpeedAnalysis",
    "ZerolBevelGearCriticalSpeedAnalysis",
    "ZerolBevelGearMeshCriticalSpeedAnalysis",
    "ZerolBevelGearSetCriticalSpeedAnalysis",
)
