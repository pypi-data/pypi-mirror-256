"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._6677 import AbstractAssemblyCompoundCriticalSpeedAnalysis
    from ._6678 import AbstractShaftCompoundCriticalSpeedAnalysis
    from ._6679 import AbstractShaftOrHousingCompoundCriticalSpeedAnalysis
    from ._6680 import (
        AbstractShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis,
    )
    from ._6681 import AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis
    from ._6682 import AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis
    from ._6683 import AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis
    from ._6684 import AssemblyCompoundCriticalSpeedAnalysis
    from ._6685 import BearingCompoundCriticalSpeedAnalysis
    from ._6686 import BeltConnectionCompoundCriticalSpeedAnalysis
    from ._6687 import BeltDriveCompoundCriticalSpeedAnalysis
    from ._6688 import BevelDifferentialGearCompoundCriticalSpeedAnalysis
    from ._6689 import BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis
    from ._6690 import BevelDifferentialGearSetCompoundCriticalSpeedAnalysis
    from ._6691 import BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis
    from ._6692 import BevelDifferentialSunGearCompoundCriticalSpeedAnalysis
    from ._6693 import BevelGearCompoundCriticalSpeedAnalysis
    from ._6694 import BevelGearMeshCompoundCriticalSpeedAnalysis
    from ._6695 import BevelGearSetCompoundCriticalSpeedAnalysis
    from ._6696 import BoltCompoundCriticalSpeedAnalysis
    from ._6697 import BoltedJointCompoundCriticalSpeedAnalysis
    from ._6698 import ClutchCompoundCriticalSpeedAnalysis
    from ._6699 import ClutchConnectionCompoundCriticalSpeedAnalysis
    from ._6700 import ClutchHalfCompoundCriticalSpeedAnalysis
    from ._6701 import CoaxialConnectionCompoundCriticalSpeedAnalysis
    from ._6702 import ComponentCompoundCriticalSpeedAnalysis
    from ._6703 import ConceptCouplingCompoundCriticalSpeedAnalysis
    from ._6704 import ConceptCouplingConnectionCompoundCriticalSpeedAnalysis
    from ._6705 import ConceptCouplingHalfCompoundCriticalSpeedAnalysis
    from ._6706 import ConceptGearCompoundCriticalSpeedAnalysis
    from ._6707 import ConceptGearMeshCompoundCriticalSpeedAnalysis
    from ._6708 import ConceptGearSetCompoundCriticalSpeedAnalysis
    from ._6709 import ConicalGearCompoundCriticalSpeedAnalysis
    from ._6710 import ConicalGearMeshCompoundCriticalSpeedAnalysis
    from ._6711 import ConicalGearSetCompoundCriticalSpeedAnalysis
    from ._6712 import ConnectionCompoundCriticalSpeedAnalysis
    from ._6713 import ConnectorCompoundCriticalSpeedAnalysis
    from ._6714 import CouplingCompoundCriticalSpeedAnalysis
    from ._6715 import CouplingConnectionCompoundCriticalSpeedAnalysis
    from ._6716 import CouplingHalfCompoundCriticalSpeedAnalysis
    from ._6717 import CVTBeltConnectionCompoundCriticalSpeedAnalysis
    from ._6718 import CVTCompoundCriticalSpeedAnalysis
    from ._6719 import CVTPulleyCompoundCriticalSpeedAnalysis
    from ._6720 import CycloidalAssemblyCompoundCriticalSpeedAnalysis
    from ._6721 import (
        CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis,
    )
    from ._6722 import CycloidalDiscCompoundCriticalSpeedAnalysis
    from ._6723 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundCriticalSpeedAnalysis,
    )
    from ._6724 import CylindricalGearCompoundCriticalSpeedAnalysis
    from ._6725 import CylindricalGearMeshCompoundCriticalSpeedAnalysis
    from ._6726 import CylindricalGearSetCompoundCriticalSpeedAnalysis
    from ._6727 import CylindricalPlanetGearCompoundCriticalSpeedAnalysis
    from ._6728 import DatumCompoundCriticalSpeedAnalysis
    from ._6729 import ExternalCADModelCompoundCriticalSpeedAnalysis
    from ._6730 import FaceGearCompoundCriticalSpeedAnalysis
    from ._6731 import FaceGearMeshCompoundCriticalSpeedAnalysis
    from ._6732 import FaceGearSetCompoundCriticalSpeedAnalysis
    from ._6733 import FEPartCompoundCriticalSpeedAnalysis
    from ._6734 import FlexiblePinAssemblyCompoundCriticalSpeedAnalysis
    from ._6735 import GearCompoundCriticalSpeedAnalysis
    from ._6736 import GearMeshCompoundCriticalSpeedAnalysis
    from ._6737 import GearSetCompoundCriticalSpeedAnalysis
    from ._6738 import GuideDxfModelCompoundCriticalSpeedAnalysis
    from ._6739 import HypoidGearCompoundCriticalSpeedAnalysis
    from ._6740 import HypoidGearMeshCompoundCriticalSpeedAnalysis
    from ._6741 import HypoidGearSetCompoundCriticalSpeedAnalysis
    from ._6742 import InterMountableComponentConnectionCompoundCriticalSpeedAnalysis
    from ._6743 import KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis
    from ._6744 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis,
    )
    from ._6745 import (
        KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis,
    )
    from ._6746 import KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis
    from ._6747 import (
        KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis,
    )
    from ._6748 import (
        KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis,
    )
    from ._6749 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis,
    )
    from ._6750 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis,
    )
    from ._6751 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis,
    )
    from ._6752 import MassDiscCompoundCriticalSpeedAnalysis
    from ._6753 import MeasurementComponentCompoundCriticalSpeedAnalysis
    from ._6754 import MountableComponentCompoundCriticalSpeedAnalysis
    from ._6755 import OilSealCompoundCriticalSpeedAnalysis
    from ._6756 import PartCompoundCriticalSpeedAnalysis
    from ._6757 import PartToPartShearCouplingCompoundCriticalSpeedAnalysis
    from ._6758 import PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis
    from ._6759 import PartToPartShearCouplingHalfCompoundCriticalSpeedAnalysis
    from ._6760 import PlanetaryConnectionCompoundCriticalSpeedAnalysis
    from ._6761 import PlanetaryGearSetCompoundCriticalSpeedAnalysis
    from ._6762 import PlanetCarrierCompoundCriticalSpeedAnalysis
    from ._6763 import PointLoadCompoundCriticalSpeedAnalysis
    from ._6764 import PowerLoadCompoundCriticalSpeedAnalysis
    from ._6765 import PulleyCompoundCriticalSpeedAnalysis
    from ._6766 import RingPinsCompoundCriticalSpeedAnalysis
    from ._6767 import RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis
    from ._6768 import RollingRingAssemblyCompoundCriticalSpeedAnalysis
    from ._6769 import RollingRingCompoundCriticalSpeedAnalysis
    from ._6770 import RollingRingConnectionCompoundCriticalSpeedAnalysis
    from ._6771 import RootAssemblyCompoundCriticalSpeedAnalysis
    from ._6772 import ShaftCompoundCriticalSpeedAnalysis
    from ._6773 import ShaftHubConnectionCompoundCriticalSpeedAnalysis
    from ._6774 import ShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis
    from ._6775 import SpecialisedAssemblyCompoundCriticalSpeedAnalysis
    from ._6776 import SpiralBevelGearCompoundCriticalSpeedAnalysis
    from ._6777 import SpiralBevelGearMeshCompoundCriticalSpeedAnalysis
    from ._6778 import SpiralBevelGearSetCompoundCriticalSpeedAnalysis
    from ._6779 import SpringDamperCompoundCriticalSpeedAnalysis
    from ._6780 import SpringDamperConnectionCompoundCriticalSpeedAnalysis
    from ._6781 import SpringDamperHalfCompoundCriticalSpeedAnalysis
    from ._6782 import StraightBevelDiffGearCompoundCriticalSpeedAnalysis
    from ._6783 import StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis
    from ._6784 import StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis
    from ._6785 import StraightBevelGearCompoundCriticalSpeedAnalysis
    from ._6786 import StraightBevelGearMeshCompoundCriticalSpeedAnalysis
    from ._6787 import StraightBevelGearSetCompoundCriticalSpeedAnalysis
    from ._6788 import StraightBevelPlanetGearCompoundCriticalSpeedAnalysis
    from ._6789 import StraightBevelSunGearCompoundCriticalSpeedAnalysis
    from ._6790 import SynchroniserCompoundCriticalSpeedAnalysis
    from ._6791 import SynchroniserHalfCompoundCriticalSpeedAnalysis
    from ._6792 import SynchroniserPartCompoundCriticalSpeedAnalysis
    from ._6793 import SynchroniserSleeveCompoundCriticalSpeedAnalysis
    from ._6794 import TorqueConverterCompoundCriticalSpeedAnalysis
    from ._6795 import TorqueConverterConnectionCompoundCriticalSpeedAnalysis
    from ._6796 import TorqueConverterPumpCompoundCriticalSpeedAnalysis
    from ._6797 import TorqueConverterTurbineCompoundCriticalSpeedAnalysis
    from ._6798 import UnbalancedMassCompoundCriticalSpeedAnalysis
    from ._6799 import VirtualComponentCompoundCriticalSpeedAnalysis
    from ._6800 import WormGearCompoundCriticalSpeedAnalysis
    from ._6801 import WormGearMeshCompoundCriticalSpeedAnalysis
    from ._6802 import WormGearSetCompoundCriticalSpeedAnalysis
    from ._6803 import ZerolBevelGearCompoundCriticalSpeedAnalysis
    from ._6804 import ZerolBevelGearMeshCompoundCriticalSpeedAnalysis
    from ._6805 import ZerolBevelGearSetCompoundCriticalSpeedAnalysis
else:
    import_structure = {
        "_6677": ["AbstractAssemblyCompoundCriticalSpeedAnalysis"],
        "_6678": ["AbstractShaftCompoundCriticalSpeedAnalysis"],
        "_6679": ["AbstractShaftOrHousingCompoundCriticalSpeedAnalysis"],
        "_6680": [
            "AbstractShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis"
        ],
        "_6681": ["AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis"],
        "_6682": ["AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis"],
        "_6683": ["AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis"],
        "_6684": ["AssemblyCompoundCriticalSpeedAnalysis"],
        "_6685": ["BearingCompoundCriticalSpeedAnalysis"],
        "_6686": ["BeltConnectionCompoundCriticalSpeedAnalysis"],
        "_6687": ["BeltDriveCompoundCriticalSpeedAnalysis"],
        "_6688": ["BevelDifferentialGearCompoundCriticalSpeedAnalysis"],
        "_6689": ["BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis"],
        "_6690": ["BevelDifferentialGearSetCompoundCriticalSpeedAnalysis"],
        "_6691": ["BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis"],
        "_6692": ["BevelDifferentialSunGearCompoundCriticalSpeedAnalysis"],
        "_6693": ["BevelGearCompoundCriticalSpeedAnalysis"],
        "_6694": ["BevelGearMeshCompoundCriticalSpeedAnalysis"],
        "_6695": ["BevelGearSetCompoundCriticalSpeedAnalysis"],
        "_6696": ["BoltCompoundCriticalSpeedAnalysis"],
        "_6697": ["BoltedJointCompoundCriticalSpeedAnalysis"],
        "_6698": ["ClutchCompoundCriticalSpeedAnalysis"],
        "_6699": ["ClutchConnectionCompoundCriticalSpeedAnalysis"],
        "_6700": ["ClutchHalfCompoundCriticalSpeedAnalysis"],
        "_6701": ["CoaxialConnectionCompoundCriticalSpeedAnalysis"],
        "_6702": ["ComponentCompoundCriticalSpeedAnalysis"],
        "_6703": ["ConceptCouplingCompoundCriticalSpeedAnalysis"],
        "_6704": ["ConceptCouplingConnectionCompoundCriticalSpeedAnalysis"],
        "_6705": ["ConceptCouplingHalfCompoundCriticalSpeedAnalysis"],
        "_6706": ["ConceptGearCompoundCriticalSpeedAnalysis"],
        "_6707": ["ConceptGearMeshCompoundCriticalSpeedAnalysis"],
        "_6708": ["ConceptGearSetCompoundCriticalSpeedAnalysis"],
        "_6709": ["ConicalGearCompoundCriticalSpeedAnalysis"],
        "_6710": ["ConicalGearMeshCompoundCriticalSpeedAnalysis"],
        "_6711": ["ConicalGearSetCompoundCriticalSpeedAnalysis"],
        "_6712": ["ConnectionCompoundCriticalSpeedAnalysis"],
        "_6713": ["ConnectorCompoundCriticalSpeedAnalysis"],
        "_6714": ["CouplingCompoundCriticalSpeedAnalysis"],
        "_6715": ["CouplingConnectionCompoundCriticalSpeedAnalysis"],
        "_6716": ["CouplingHalfCompoundCriticalSpeedAnalysis"],
        "_6717": ["CVTBeltConnectionCompoundCriticalSpeedAnalysis"],
        "_6718": ["CVTCompoundCriticalSpeedAnalysis"],
        "_6719": ["CVTPulleyCompoundCriticalSpeedAnalysis"],
        "_6720": ["CycloidalAssemblyCompoundCriticalSpeedAnalysis"],
        "_6721": ["CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis"],
        "_6722": ["CycloidalDiscCompoundCriticalSpeedAnalysis"],
        "_6723": [
            "CycloidalDiscPlanetaryBearingConnectionCompoundCriticalSpeedAnalysis"
        ],
        "_6724": ["CylindricalGearCompoundCriticalSpeedAnalysis"],
        "_6725": ["CylindricalGearMeshCompoundCriticalSpeedAnalysis"],
        "_6726": ["CylindricalGearSetCompoundCriticalSpeedAnalysis"],
        "_6727": ["CylindricalPlanetGearCompoundCriticalSpeedAnalysis"],
        "_6728": ["DatumCompoundCriticalSpeedAnalysis"],
        "_6729": ["ExternalCADModelCompoundCriticalSpeedAnalysis"],
        "_6730": ["FaceGearCompoundCriticalSpeedAnalysis"],
        "_6731": ["FaceGearMeshCompoundCriticalSpeedAnalysis"],
        "_6732": ["FaceGearSetCompoundCriticalSpeedAnalysis"],
        "_6733": ["FEPartCompoundCriticalSpeedAnalysis"],
        "_6734": ["FlexiblePinAssemblyCompoundCriticalSpeedAnalysis"],
        "_6735": ["GearCompoundCriticalSpeedAnalysis"],
        "_6736": ["GearMeshCompoundCriticalSpeedAnalysis"],
        "_6737": ["GearSetCompoundCriticalSpeedAnalysis"],
        "_6738": ["GuideDxfModelCompoundCriticalSpeedAnalysis"],
        "_6739": ["HypoidGearCompoundCriticalSpeedAnalysis"],
        "_6740": ["HypoidGearMeshCompoundCriticalSpeedAnalysis"],
        "_6741": ["HypoidGearSetCompoundCriticalSpeedAnalysis"],
        "_6742": ["InterMountableComponentConnectionCompoundCriticalSpeedAnalysis"],
        "_6743": ["KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis"],
        "_6744": [
            "KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis"
        ],
        "_6745": [
            "KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis"
        ],
        "_6746": ["KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis"],
        "_6747": [
            "KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis"
        ],
        "_6748": ["KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis"],
        "_6749": [
            "KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis"
        ],
        "_6750": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis"
        ],
        "_6751": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis"
        ],
        "_6752": ["MassDiscCompoundCriticalSpeedAnalysis"],
        "_6753": ["MeasurementComponentCompoundCriticalSpeedAnalysis"],
        "_6754": ["MountableComponentCompoundCriticalSpeedAnalysis"],
        "_6755": ["OilSealCompoundCriticalSpeedAnalysis"],
        "_6756": ["PartCompoundCriticalSpeedAnalysis"],
        "_6757": ["PartToPartShearCouplingCompoundCriticalSpeedAnalysis"],
        "_6758": ["PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis"],
        "_6759": ["PartToPartShearCouplingHalfCompoundCriticalSpeedAnalysis"],
        "_6760": ["PlanetaryConnectionCompoundCriticalSpeedAnalysis"],
        "_6761": ["PlanetaryGearSetCompoundCriticalSpeedAnalysis"],
        "_6762": ["PlanetCarrierCompoundCriticalSpeedAnalysis"],
        "_6763": ["PointLoadCompoundCriticalSpeedAnalysis"],
        "_6764": ["PowerLoadCompoundCriticalSpeedAnalysis"],
        "_6765": ["PulleyCompoundCriticalSpeedAnalysis"],
        "_6766": ["RingPinsCompoundCriticalSpeedAnalysis"],
        "_6767": ["RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis"],
        "_6768": ["RollingRingAssemblyCompoundCriticalSpeedAnalysis"],
        "_6769": ["RollingRingCompoundCriticalSpeedAnalysis"],
        "_6770": ["RollingRingConnectionCompoundCriticalSpeedAnalysis"],
        "_6771": ["RootAssemblyCompoundCriticalSpeedAnalysis"],
        "_6772": ["ShaftCompoundCriticalSpeedAnalysis"],
        "_6773": ["ShaftHubConnectionCompoundCriticalSpeedAnalysis"],
        "_6774": ["ShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis"],
        "_6775": ["SpecialisedAssemblyCompoundCriticalSpeedAnalysis"],
        "_6776": ["SpiralBevelGearCompoundCriticalSpeedAnalysis"],
        "_6777": ["SpiralBevelGearMeshCompoundCriticalSpeedAnalysis"],
        "_6778": ["SpiralBevelGearSetCompoundCriticalSpeedAnalysis"],
        "_6779": ["SpringDamperCompoundCriticalSpeedAnalysis"],
        "_6780": ["SpringDamperConnectionCompoundCriticalSpeedAnalysis"],
        "_6781": ["SpringDamperHalfCompoundCriticalSpeedAnalysis"],
        "_6782": ["StraightBevelDiffGearCompoundCriticalSpeedAnalysis"],
        "_6783": ["StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis"],
        "_6784": ["StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis"],
        "_6785": ["StraightBevelGearCompoundCriticalSpeedAnalysis"],
        "_6786": ["StraightBevelGearMeshCompoundCriticalSpeedAnalysis"],
        "_6787": ["StraightBevelGearSetCompoundCriticalSpeedAnalysis"],
        "_6788": ["StraightBevelPlanetGearCompoundCriticalSpeedAnalysis"],
        "_6789": ["StraightBevelSunGearCompoundCriticalSpeedAnalysis"],
        "_6790": ["SynchroniserCompoundCriticalSpeedAnalysis"],
        "_6791": ["SynchroniserHalfCompoundCriticalSpeedAnalysis"],
        "_6792": ["SynchroniserPartCompoundCriticalSpeedAnalysis"],
        "_6793": ["SynchroniserSleeveCompoundCriticalSpeedAnalysis"],
        "_6794": ["TorqueConverterCompoundCriticalSpeedAnalysis"],
        "_6795": ["TorqueConverterConnectionCompoundCriticalSpeedAnalysis"],
        "_6796": ["TorqueConverterPumpCompoundCriticalSpeedAnalysis"],
        "_6797": ["TorqueConverterTurbineCompoundCriticalSpeedAnalysis"],
        "_6798": ["UnbalancedMassCompoundCriticalSpeedAnalysis"],
        "_6799": ["VirtualComponentCompoundCriticalSpeedAnalysis"],
        "_6800": ["WormGearCompoundCriticalSpeedAnalysis"],
        "_6801": ["WormGearMeshCompoundCriticalSpeedAnalysis"],
        "_6802": ["WormGearSetCompoundCriticalSpeedAnalysis"],
        "_6803": ["ZerolBevelGearCompoundCriticalSpeedAnalysis"],
        "_6804": ["ZerolBevelGearMeshCompoundCriticalSpeedAnalysis"],
        "_6805": ["ZerolBevelGearSetCompoundCriticalSpeedAnalysis"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundCriticalSpeedAnalysis",
    "AbstractShaftCompoundCriticalSpeedAnalysis",
    "AbstractShaftOrHousingCompoundCriticalSpeedAnalysis",
    "AbstractShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis",
    "AGMAGleasonConicalGearCompoundCriticalSpeedAnalysis",
    "AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis",
    "AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis",
    "AssemblyCompoundCriticalSpeedAnalysis",
    "BearingCompoundCriticalSpeedAnalysis",
    "BeltConnectionCompoundCriticalSpeedAnalysis",
    "BeltDriveCompoundCriticalSpeedAnalysis",
    "BevelDifferentialGearCompoundCriticalSpeedAnalysis",
    "BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis",
    "BevelDifferentialGearSetCompoundCriticalSpeedAnalysis",
    "BevelDifferentialPlanetGearCompoundCriticalSpeedAnalysis",
    "BevelDifferentialSunGearCompoundCriticalSpeedAnalysis",
    "BevelGearCompoundCriticalSpeedAnalysis",
    "BevelGearMeshCompoundCriticalSpeedAnalysis",
    "BevelGearSetCompoundCriticalSpeedAnalysis",
    "BoltCompoundCriticalSpeedAnalysis",
    "BoltedJointCompoundCriticalSpeedAnalysis",
    "ClutchCompoundCriticalSpeedAnalysis",
    "ClutchConnectionCompoundCriticalSpeedAnalysis",
    "ClutchHalfCompoundCriticalSpeedAnalysis",
    "CoaxialConnectionCompoundCriticalSpeedAnalysis",
    "ComponentCompoundCriticalSpeedAnalysis",
    "ConceptCouplingCompoundCriticalSpeedAnalysis",
    "ConceptCouplingConnectionCompoundCriticalSpeedAnalysis",
    "ConceptCouplingHalfCompoundCriticalSpeedAnalysis",
    "ConceptGearCompoundCriticalSpeedAnalysis",
    "ConceptGearMeshCompoundCriticalSpeedAnalysis",
    "ConceptGearSetCompoundCriticalSpeedAnalysis",
    "ConicalGearCompoundCriticalSpeedAnalysis",
    "ConicalGearMeshCompoundCriticalSpeedAnalysis",
    "ConicalGearSetCompoundCriticalSpeedAnalysis",
    "ConnectionCompoundCriticalSpeedAnalysis",
    "ConnectorCompoundCriticalSpeedAnalysis",
    "CouplingCompoundCriticalSpeedAnalysis",
    "CouplingConnectionCompoundCriticalSpeedAnalysis",
    "CouplingHalfCompoundCriticalSpeedAnalysis",
    "CVTBeltConnectionCompoundCriticalSpeedAnalysis",
    "CVTCompoundCriticalSpeedAnalysis",
    "CVTPulleyCompoundCriticalSpeedAnalysis",
    "CycloidalAssemblyCompoundCriticalSpeedAnalysis",
    "CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis",
    "CycloidalDiscCompoundCriticalSpeedAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionCompoundCriticalSpeedAnalysis",
    "CylindricalGearCompoundCriticalSpeedAnalysis",
    "CylindricalGearMeshCompoundCriticalSpeedAnalysis",
    "CylindricalGearSetCompoundCriticalSpeedAnalysis",
    "CylindricalPlanetGearCompoundCriticalSpeedAnalysis",
    "DatumCompoundCriticalSpeedAnalysis",
    "ExternalCADModelCompoundCriticalSpeedAnalysis",
    "FaceGearCompoundCriticalSpeedAnalysis",
    "FaceGearMeshCompoundCriticalSpeedAnalysis",
    "FaceGearSetCompoundCriticalSpeedAnalysis",
    "FEPartCompoundCriticalSpeedAnalysis",
    "FlexiblePinAssemblyCompoundCriticalSpeedAnalysis",
    "GearCompoundCriticalSpeedAnalysis",
    "GearMeshCompoundCriticalSpeedAnalysis",
    "GearSetCompoundCriticalSpeedAnalysis",
    "GuideDxfModelCompoundCriticalSpeedAnalysis",
    "HypoidGearCompoundCriticalSpeedAnalysis",
    "HypoidGearMeshCompoundCriticalSpeedAnalysis",
    "HypoidGearSetCompoundCriticalSpeedAnalysis",
    "InterMountableComponentConnectionCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis",
    "MassDiscCompoundCriticalSpeedAnalysis",
    "MeasurementComponentCompoundCriticalSpeedAnalysis",
    "MountableComponentCompoundCriticalSpeedAnalysis",
    "OilSealCompoundCriticalSpeedAnalysis",
    "PartCompoundCriticalSpeedAnalysis",
    "PartToPartShearCouplingCompoundCriticalSpeedAnalysis",
    "PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis",
    "PartToPartShearCouplingHalfCompoundCriticalSpeedAnalysis",
    "PlanetaryConnectionCompoundCriticalSpeedAnalysis",
    "PlanetaryGearSetCompoundCriticalSpeedAnalysis",
    "PlanetCarrierCompoundCriticalSpeedAnalysis",
    "PointLoadCompoundCriticalSpeedAnalysis",
    "PowerLoadCompoundCriticalSpeedAnalysis",
    "PulleyCompoundCriticalSpeedAnalysis",
    "RingPinsCompoundCriticalSpeedAnalysis",
    "RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis",
    "RollingRingAssemblyCompoundCriticalSpeedAnalysis",
    "RollingRingCompoundCriticalSpeedAnalysis",
    "RollingRingConnectionCompoundCriticalSpeedAnalysis",
    "RootAssemblyCompoundCriticalSpeedAnalysis",
    "ShaftCompoundCriticalSpeedAnalysis",
    "ShaftHubConnectionCompoundCriticalSpeedAnalysis",
    "ShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis",
    "SpecialisedAssemblyCompoundCriticalSpeedAnalysis",
    "SpiralBevelGearCompoundCriticalSpeedAnalysis",
    "SpiralBevelGearMeshCompoundCriticalSpeedAnalysis",
    "SpiralBevelGearSetCompoundCriticalSpeedAnalysis",
    "SpringDamperCompoundCriticalSpeedAnalysis",
    "SpringDamperConnectionCompoundCriticalSpeedAnalysis",
    "SpringDamperHalfCompoundCriticalSpeedAnalysis",
    "StraightBevelDiffGearCompoundCriticalSpeedAnalysis",
    "StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis",
    "StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis",
    "StraightBevelGearCompoundCriticalSpeedAnalysis",
    "StraightBevelGearMeshCompoundCriticalSpeedAnalysis",
    "StraightBevelGearSetCompoundCriticalSpeedAnalysis",
    "StraightBevelPlanetGearCompoundCriticalSpeedAnalysis",
    "StraightBevelSunGearCompoundCriticalSpeedAnalysis",
    "SynchroniserCompoundCriticalSpeedAnalysis",
    "SynchroniserHalfCompoundCriticalSpeedAnalysis",
    "SynchroniserPartCompoundCriticalSpeedAnalysis",
    "SynchroniserSleeveCompoundCriticalSpeedAnalysis",
    "TorqueConverterCompoundCriticalSpeedAnalysis",
    "TorqueConverterConnectionCompoundCriticalSpeedAnalysis",
    "TorqueConverterPumpCompoundCriticalSpeedAnalysis",
    "TorqueConverterTurbineCompoundCriticalSpeedAnalysis",
    "UnbalancedMassCompoundCriticalSpeedAnalysis",
    "VirtualComponentCompoundCriticalSpeedAnalysis",
    "WormGearCompoundCriticalSpeedAnalysis",
    "WormGearMeshCompoundCriticalSpeedAnalysis",
    "WormGearSetCompoundCriticalSpeedAnalysis",
    "ZerolBevelGearCompoundCriticalSpeedAnalysis",
    "ZerolBevelGearMeshCompoundCriticalSpeedAnalysis",
    "ZerolBevelGearSetCompoundCriticalSpeedAnalysis",
)
