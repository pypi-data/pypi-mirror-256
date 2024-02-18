"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5680 import AbstractAssemblyHarmonicAnalysis
    from ._5681 import AbstractPeriodicExcitationDetail
    from ._5682 import AbstractShaftHarmonicAnalysis
    from ._5683 import AbstractShaftOrHousingHarmonicAnalysis
    from ._5684 import AbstractShaftToMountableComponentConnectionHarmonicAnalysis
    from ._5685 import AGMAGleasonConicalGearHarmonicAnalysis
    from ._5686 import AGMAGleasonConicalGearMeshHarmonicAnalysis
    from ._5687 import AGMAGleasonConicalGearSetHarmonicAnalysis
    from ._5688 import AssemblyHarmonicAnalysis
    from ._5689 import BearingHarmonicAnalysis
    from ._5690 import BeltConnectionHarmonicAnalysis
    from ._5691 import BeltDriveHarmonicAnalysis
    from ._5692 import BevelDifferentialGearHarmonicAnalysis
    from ._5693 import BevelDifferentialGearMeshHarmonicAnalysis
    from ._5694 import BevelDifferentialGearSetHarmonicAnalysis
    from ._5695 import BevelDifferentialPlanetGearHarmonicAnalysis
    from ._5696 import BevelDifferentialSunGearHarmonicAnalysis
    from ._5697 import BevelGearHarmonicAnalysis
    from ._5698 import BevelGearMeshHarmonicAnalysis
    from ._5699 import BevelGearSetHarmonicAnalysis
    from ._5700 import BoltedJointHarmonicAnalysis
    from ._5701 import BoltHarmonicAnalysis
    from ._5702 import ClutchConnectionHarmonicAnalysis
    from ._5703 import ClutchHalfHarmonicAnalysis
    from ._5704 import ClutchHarmonicAnalysis
    from ._5705 import CoaxialConnectionHarmonicAnalysis
    from ._5706 import ComplianceAndForceData
    from ._5707 import ComponentHarmonicAnalysis
    from ._5708 import ConceptCouplingConnectionHarmonicAnalysis
    from ._5709 import ConceptCouplingHalfHarmonicAnalysis
    from ._5710 import ConceptCouplingHarmonicAnalysis
    from ._5711 import ConceptGearHarmonicAnalysis
    from ._5712 import ConceptGearMeshHarmonicAnalysis
    from ._5713 import ConceptGearSetHarmonicAnalysis
    from ._5714 import ConicalGearHarmonicAnalysis
    from ._5715 import ConicalGearMeshHarmonicAnalysis
    from ._5716 import ConicalGearSetHarmonicAnalysis
    from ._5717 import ConnectionHarmonicAnalysis
    from ._5718 import ConnectorHarmonicAnalysis
    from ._5719 import CouplingConnectionHarmonicAnalysis
    from ._5720 import CouplingHalfHarmonicAnalysis
    from ._5721 import CouplingHarmonicAnalysis
    from ._5722 import CVTBeltConnectionHarmonicAnalysis
    from ._5723 import CVTHarmonicAnalysis
    from ._5724 import CVTPulleyHarmonicAnalysis
    from ._5725 import CycloidalAssemblyHarmonicAnalysis
    from ._5726 import CycloidalDiscCentralBearingConnectionHarmonicAnalysis
    from ._5727 import CycloidalDiscHarmonicAnalysis
    from ._5728 import CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis
    from ._5729 import CylindricalGearHarmonicAnalysis
    from ._5730 import CylindricalGearMeshHarmonicAnalysis
    from ._5731 import CylindricalGearSetHarmonicAnalysis
    from ._5732 import CylindricalPlanetGearHarmonicAnalysis
    from ._5733 import DatumHarmonicAnalysis
    from ._5734 import DynamicModelForHarmonicAnalysis
    from ._5735 import ElectricMachinePeriodicExcitationDetail
    from ._5736 import ElectricMachineRotorXForcePeriodicExcitationDetail
    from ._5737 import ElectricMachineRotorXMomentPeriodicExcitationDetail
    from ._5738 import ElectricMachineRotorYForcePeriodicExcitationDetail
    from ._5739 import ElectricMachineRotorYMomentPeriodicExcitationDetail
    from ._5740 import ElectricMachineRotorZForcePeriodicExcitationDetail
    from ._5741 import ElectricMachineStatorToothAxialLoadsExcitationDetail
    from ._5742 import ElectricMachineStatorToothLoadsExcitationDetail
    from ._5743 import ElectricMachineStatorToothMomentsExcitationDetail
    from ._5744 import ElectricMachineStatorToothRadialLoadsExcitationDetail
    from ._5745 import ElectricMachineStatorToothTangentialLoadsExcitationDetail
    from ._5746 import ElectricMachineTorqueRipplePeriodicExcitationDetail
    from ._5747 import ExportOutputType
    from ._5748 import ExternalCADModelHarmonicAnalysis
    from ._5749 import FaceGearHarmonicAnalysis
    from ._5750 import FaceGearMeshHarmonicAnalysis
    from ._5751 import FaceGearSetHarmonicAnalysis
    from ._5752 import FEPartHarmonicAnalysis
    from ._5753 import FlexiblePinAssemblyHarmonicAnalysis
    from ._5754 import FrequencyOptionsForHarmonicAnalysisResults
    from ._5755 import GearHarmonicAnalysis
    from ._5756 import GearMeshExcitationDetail
    from ._5757 import GearMeshHarmonicAnalysis
    from ._5758 import GearMeshMisalignmentExcitationDetail
    from ._5759 import GearMeshTEExcitationDetail
    from ._5760 import GearSetHarmonicAnalysis
    from ._5761 import GeneralPeriodicExcitationDetail
    from ._5762 import GuideDxfModelHarmonicAnalysis
    from ._5763 import HarmonicAnalysis
    from ._5764 import HarmonicAnalysisDrawStyle
    from ._5765 import HarmonicAnalysisExportOptions
    from ._5766 import HarmonicAnalysisFEExportOptions
    from ._5767 import HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
    from ._5768 import HarmonicAnalysisOptions
    from ._5769 import HarmonicAnalysisRootAssemblyExportOptions
    from ._5770 import HarmonicAnalysisShaftExportOptions
    from ._5771 import HarmonicAnalysisTorqueInputType
    from ._5772 import HarmonicAnalysisWithVaryingStiffnessStaticLoadCase
    from ._5773 import HypoidGearHarmonicAnalysis
    from ._5774 import HypoidGearMeshHarmonicAnalysis
    from ._5775 import HypoidGearSetHarmonicAnalysis
    from ._5776 import InterMountableComponentConnectionHarmonicAnalysis
    from ._5777 import KlingelnbergCycloPalloidConicalGearHarmonicAnalysis
    from ._5778 import KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis
    from ._5779 import KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis
    from ._5780 import KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis
    from ._5781 import KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis
    from ._5782 import KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis
    from ._5783 import KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis
    from ._5784 import KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis
    from ._5785 import KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis
    from ._5786 import MassDiscHarmonicAnalysis
    from ._5787 import MeasurementComponentHarmonicAnalysis
    from ._5788 import MountableComponentHarmonicAnalysis
    from ._5789 import OilSealHarmonicAnalysis
    from ._5790 import PartHarmonicAnalysis
    from ._5791 import PartToPartShearCouplingConnectionHarmonicAnalysis
    from ._5792 import PartToPartShearCouplingHalfHarmonicAnalysis
    from ._5793 import PartToPartShearCouplingHarmonicAnalysis
    from ._5794 import PeriodicExcitationWithReferenceShaft
    from ._5795 import PlanetaryConnectionHarmonicAnalysis
    from ._5796 import PlanetaryGearSetHarmonicAnalysis
    from ._5797 import PlanetCarrierHarmonicAnalysis
    from ._5798 import PointLoadHarmonicAnalysis
    from ._5799 import PowerLoadHarmonicAnalysis
    from ._5800 import PulleyHarmonicAnalysis
    from ._5801 import ResponseCacheLevel
    from ._5802 import RingPinsHarmonicAnalysis
    from ._5803 import RingPinsToDiscConnectionHarmonicAnalysis
    from ._5804 import RollingRingAssemblyHarmonicAnalysis
    from ._5805 import RollingRingConnectionHarmonicAnalysis
    from ._5806 import RollingRingHarmonicAnalysis
    from ._5807 import RootAssemblyHarmonicAnalysis
    from ._5808 import ShaftHarmonicAnalysis
    from ._5809 import ShaftHubConnectionHarmonicAnalysis
    from ._5810 import ShaftToMountableComponentConnectionHarmonicAnalysis
    from ._5811 import SingleNodePeriodicExcitationWithReferenceShaft
    from ._5812 import SpecialisedAssemblyHarmonicAnalysis
    from ._5813 import SpeedOptionsForHarmonicAnalysisResults
    from ._5814 import SpiralBevelGearHarmonicAnalysis
    from ._5815 import SpiralBevelGearMeshHarmonicAnalysis
    from ._5816 import SpiralBevelGearSetHarmonicAnalysis
    from ._5817 import SpringDamperConnectionHarmonicAnalysis
    from ._5818 import SpringDamperHalfHarmonicAnalysis
    from ._5819 import SpringDamperHarmonicAnalysis
    from ._5820 import StiffnessOptionsForHarmonicAnalysis
    from ._5821 import StraightBevelDiffGearHarmonicAnalysis
    from ._5822 import StraightBevelDiffGearMeshHarmonicAnalysis
    from ._5823 import StraightBevelDiffGearSetHarmonicAnalysis
    from ._5824 import StraightBevelGearHarmonicAnalysis
    from ._5825 import StraightBevelGearMeshHarmonicAnalysis
    from ._5826 import StraightBevelGearSetHarmonicAnalysis
    from ._5827 import StraightBevelPlanetGearHarmonicAnalysis
    from ._5828 import StraightBevelSunGearHarmonicAnalysis
    from ._5829 import SynchroniserHalfHarmonicAnalysis
    from ._5830 import SynchroniserHarmonicAnalysis
    from ._5831 import SynchroniserPartHarmonicAnalysis
    from ._5832 import SynchroniserSleeveHarmonicAnalysis
    from ._5833 import TorqueConverterConnectionHarmonicAnalysis
    from ._5834 import TorqueConverterHarmonicAnalysis
    from ._5835 import TorqueConverterPumpHarmonicAnalysis
    from ._5836 import TorqueConverterTurbineHarmonicAnalysis
    from ._5837 import UnbalancedMassExcitationDetail
    from ._5838 import UnbalancedMassHarmonicAnalysis
    from ._5839 import VirtualComponentHarmonicAnalysis
    from ._5840 import WormGearHarmonicAnalysis
    from ._5841 import WormGearMeshHarmonicAnalysis
    from ._5842 import WormGearSetHarmonicAnalysis
    from ._5843 import ZerolBevelGearHarmonicAnalysis
    from ._5844 import ZerolBevelGearMeshHarmonicAnalysis
    from ._5845 import ZerolBevelGearSetHarmonicAnalysis
else:
    import_structure = {
        "_5680": ["AbstractAssemblyHarmonicAnalysis"],
        "_5681": ["AbstractPeriodicExcitationDetail"],
        "_5682": ["AbstractShaftHarmonicAnalysis"],
        "_5683": ["AbstractShaftOrHousingHarmonicAnalysis"],
        "_5684": ["AbstractShaftToMountableComponentConnectionHarmonicAnalysis"],
        "_5685": ["AGMAGleasonConicalGearHarmonicAnalysis"],
        "_5686": ["AGMAGleasonConicalGearMeshHarmonicAnalysis"],
        "_5687": ["AGMAGleasonConicalGearSetHarmonicAnalysis"],
        "_5688": ["AssemblyHarmonicAnalysis"],
        "_5689": ["BearingHarmonicAnalysis"],
        "_5690": ["BeltConnectionHarmonicAnalysis"],
        "_5691": ["BeltDriveHarmonicAnalysis"],
        "_5692": ["BevelDifferentialGearHarmonicAnalysis"],
        "_5693": ["BevelDifferentialGearMeshHarmonicAnalysis"],
        "_5694": ["BevelDifferentialGearSetHarmonicAnalysis"],
        "_5695": ["BevelDifferentialPlanetGearHarmonicAnalysis"],
        "_5696": ["BevelDifferentialSunGearHarmonicAnalysis"],
        "_5697": ["BevelGearHarmonicAnalysis"],
        "_5698": ["BevelGearMeshHarmonicAnalysis"],
        "_5699": ["BevelGearSetHarmonicAnalysis"],
        "_5700": ["BoltedJointHarmonicAnalysis"],
        "_5701": ["BoltHarmonicAnalysis"],
        "_5702": ["ClutchConnectionHarmonicAnalysis"],
        "_5703": ["ClutchHalfHarmonicAnalysis"],
        "_5704": ["ClutchHarmonicAnalysis"],
        "_5705": ["CoaxialConnectionHarmonicAnalysis"],
        "_5706": ["ComplianceAndForceData"],
        "_5707": ["ComponentHarmonicAnalysis"],
        "_5708": ["ConceptCouplingConnectionHarmonicAnalysis"],
        "_5709": ["ConceptCouplingHalfHarmonicAnalysis"],
        "_5710": ["ConceptCouplingHarmonicAnalysis"],
        "_5711": ["ConceptGearHarmonicAnalysis"],
        "_5712": ["ConceptGearMeshHarmonicAnalysis"],
        "_5713": ["ConceptGearSetHarmonicAnalysis"],
        "_5714": ["ConicalGearHarmonicAnalysis"],
        "_5715": ["ConicalGearMeshHarmonicAnalysis"],
        "_5716": ["ConicalGearSetHarmonicAnalysis"],
        "_5717": ["ConnectionHarmonicAnalysis"],
        "_5718": ["ConnectorHarmonicAnalysis"],
        "_5719": ["CouplingConnectionHarmonicAnalysis"],
        "_5720": ["CouplingHalfHarmonicAnalysis"],
        "_5721": ["CouplingHarmonicAnalysis"],
        "_5722": ["CVTBeltConnectionHarmonicAnalysis"],
        "_5723": ["CVTHarmonicAnalysis"],
        "_5724": ["CVTPulleyHarmonicAnalysis"],
        "_5725": ["CycloidalAssemblyHarmonicAnalysis"],
        "_5726": ["CycloidalDiscCentralBearingConnectionHarmonicAnalysis"],
        "_5727": ["CycloidalDiscHarmonicAnalysis"],
        "_5728": ["CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis"],
        "_5729": ["CylindricalGearHarmonicAnalysis"],
        "_5730": ["CylindricalGearMeshHarmonicAnalysis"],
        "_5731": ["CylindricalGearSetHarmonicAnalysis"],
        "_5732": ["CylindricalPlanetGearHarmonicAnalysis"],
        "_5733": ["DatumHarmonicAnalysis"],
        "_5734": ["DynamicModelForHarmonicAnalysis"],
        "_5735": ["ElectricMachinePeriodicExcitationDetail"],
        "_5736": ["ElectricMachineRotorXForcePeriodicExcitationDetail"],
        "_5737": ["ElectricMachineRotorXMomentPeriodicExcitationDetail"],
        "_5738": ["ElectricMachineRotorYForcePeriodicExcitationDetail"],
        "_5739": ["ElectricMachineRotorYMomentPeriodicExcitationDetail"],
        "_5740": ["ElectricMachineRotorZForcePeriodicExcitationDetail"],
        "_5741": ["ElectricMachineStatorToothAxialLoadsExcitationDetail"],
        "_5742": ["ElectricMachineStatorToothLoadsExcitationDetail"],
        "_5743": ["ElectricMachineStatorToothMomentsExcitationDetail"],
        "_5744": ["ElectricMachineStatorToothRadialLoadsExcitationDetail"],
        "_5745": ["ElectricMachineStatorToothTangentialLoadsExcitationDetail"],
        "_5746": ["ElectricMachineTorqueRipplePeriodicExcitationDetail"],
        "_5747": ["ExportOutputType"],
        "_5748": ["ExternalCADModelHarmonicAnalysis"],
        "_5749": ["FaceGearHarmonicAnalysis"],
        "_5750": ["FaceGearMeshHarmonicAnalysis"],
        "_5751": ["FaceGearSetHarmonicAnalysis"],
        "_5752": ["FEPartHarmonicAnalysis"],
        "_5753": ["FlexiblePinAssemblyHarmonicAnalysis"],
        "_5754": ["FrequencyOptionsForHarmonicAnalysisResults"],
        "_5755": ["GearHarmonicAnalysis"],
        "_5756": ["GearMeshExcitationDetail"],
        "_5757": ["GearMeshHarmonicAnalysis"],
        "_5758": ["GearMeshMisalignmentExcitationDetail"],
        "_5759": ["GearMeshTEExcitationDetail"],
        "_5760": ["GearSetHarmonicAnalysis"],
        "_5761": ["GeneralPeriodicExcitationDetail"],
        "_5762": ["GuideDxfModelHarmonicAnalysis"],
        "_5763": ["HarmonicAnalysis"],
        "_5764": ["HarmonicAnalysisDrawStyle"],
        "_5765": ["HarmonicAnalysisExportOptions"],
        "_5766": ["HarmonicAnalysisFEExportOptions"],
        "_5767": ["HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"],
        "_5768": ["HarmonicAnalysisOptions"],
        "_5769": ["HarmonicAnalysisRootAssemblyExportOptions"],
        "_5770": ["HarmonicAnalysisShaftExportOptions"],
        "_5771": ["HarmonicAnalysisTorqueInputType"],
        "_5772": ["HarmonicAnalysisWithVaryingStiffnessStaticLoadCase"],
        "_5773": ["HypoidGearHarmonicAnalysis"],
        "_5774": ["HypoidGearMeshHarmonicAnalysis"],
        "_5775": ["HypoidGearSetHarmonicAnalysis"],
        "_5776": ["InterMountableComponentConnectionHarmonicAnalysis"],
        "_5777": ["KlingelnbergCycloPalloidConicalGearHarmonicAnalysis"],
        "_5778": ["KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis"],
        "_5779": ["KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis"],
        "_5780": ["KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis"],
        "_5781": ["KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis"],
        "_5782": ["KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis"],
        "_5783": ["KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis"],
        "_5784": ["KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis"],
        "_5785": ["KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis"],
        "_5786": ["MassDiscHarmonicAnalysis"],
        "_5787": ["MeasurementComponentHarmonicAnalysis"],
        "_5788": ["MountableComponentHarmonicAnalysis"],
        "_5789": ["OilSealHarmonicAnalysis"],
        "_5790": ["PartHarmonicAnalysis"],
        "_5791": ["PartToPartShearCouplingConnectionHarmonicAnalysis"],
        "_5792": ["PartToPartShearCouplingHalfHarmonicAnalysis"],
        "_5793": ["PartToPartShearCouplingHarmonicAnalysis"],
        "_5794": ["PeriodicExcitationWithReferenceShaft"],
        "_5795": ["PlanetaryConnectionHarmonicAnalysis"],
        "_5796": ["PlanetaryGearSetHarmonicAnalysis"],
        "_5797": ["PlanetCarrierHarmonicAnalysis"],
        "_5798": ["PointLoadHarmonicAnalysis"],
        "_5799": ["PowerLoadHarmonicAnalysis"],
        "_5800": ["PulleyHarmonicAnalysis"],
        "_5801": ["ResponseCacheLevel"],
        "_5802": ["RingPinsHarmonicAnalysis"],
        "_5803": ["RingPinsToDiscConnectionHarmonicAnalysis"],
        "_5804": ["RollingRingAssemblyHarmonicAnalysis"],
        "_5805": ["RollingRingConnectionHarmonicAnalysis"],
        "_5806": ["RollingRingHarmonicAnalysis"],
        "_5807": ["RootAssemblyHarmonicAnalysis"],
        "_5808": ["ShaftHarmonicAnalysis"],
        "_5809": ["ShaftHubConnectionHarmonicAnalysis"],
        "_5810": ["ShaftToMountableComponentConnectionHarmonicAnalysis"],
        "_5811": ["SingleNodePeriodicExcitationWithReferenceShaft"],
        "_5812": ["SpecialisedAssemblyHarmonicAnalysis"],
        "_5813": ["SpeedOptionsForHarmonicAnalysisResults"],
        "_5814": ["SpiralBevelGearHarmonicAnalysis"],
        "_5815": ["SpiralBevelGearMeshHarmonicAnalysis"],
        "_5816": ["SpiralBevelGearSetHarmonicAnalysis"],
        "_5817": ["SpringDamperConnectionHarmonicAnalysis"],
        "_5818": ["SpringDamperHalfHarmonicAnalysis"],
        "_5819": ["SpringDamperHarmonicAnalysis"],
        "_5820": ["StiffnessOptionsForHarmonicAnalysis"],
        "_5821": ["StraightBevelDiffGearHarmonicAnalysis"],
        "_5822": ["StraightBevelDiffGearMeshHarmonicAnalysis"],
        "_5823": ["StraightBevelDiffGearSetHarmonicAnalysis"],
        "_5824": ["StraightBevelGearHarmonicAnalysis"],
        "_5825": ["StraightBevelGearMeshHarmonicAnalysis"],
        "_5826": ["StraightBevelGearSetHarmonicAnalysis"],
        "_5827": ["StraightBevelPlanetGearHarmonicAnalysis"],
        "_5828": ["StraightBevelSunGearHarmonicAnalysis"],
        "_5829": ["SynchroniserHalfHarmonicAnalysis"],
        "_5830": ["SynchroniserHarmonicAnalysis"],
        "_5831": ["SynchroniserPartHarmonicAnalysis"],
        "_5832": ["SynchroniserSleeveHarmonicAnalysis"],
        "_5833": ["TorqueConverterConnectionHarmonicAnalysis"],
        "_5834": ["TorqueConverterHarmonicAnalysis"],
        "_5835": ["TorqueConverterPumpHarmonicAnalysis"],
        "_5836": ["TorqueConverterTurbineHarmonicAnalysis"],
        "_5837": ["UnbalancedMassExcitationDetail"],
        "_5838": ["UnbalancedMassHarmonicAnalysis"],
        "_5839": ["VirtualComponentHarmonicAnalysis"],
        "_5840": ["WormGearHarmonicAnalysis"],
        "_5841": ["WormGearMeshHarmonicAnalysis"],
        "_5842": ["WormGearSetHarmonicAnalysis"],
        "_5843": ["ZerolBevelGearHarmonicAnalysis"],
        "_5844": ["ZerolBevelGearMeshHarmonicAnalysis"],
        "_5845": ["ZerolBevelGearSetHarmonicAnalysis"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyHarmonicAnalysis",
    "AbstractPeriodicExcitationDetail",
    "AbstractShaftHarmonicAnalysis",
    "AbstractShaftOrHousingHarmonicAnalysis",
    "AbstractShaftToMountableComponentConnectionHarmonicAnalysis",
    "AGMAGleasonConicalGearHarmonicAnalysis",
    "AGMAGleasonConicalGearMeshHarmonicAnalysis",
    "AGMAGleasonConicalGearSetHarmonicAnalysis",
    "AssemblyHarmonicAnalysis",
    "BearingHarmonicAnalysis",
    "BeltConnectionHarmonicAnalysis",
    "BeltDriveHarmonicAnalysis",
    "BevelDifferentialGearHarmonicAnalysis",
    "BevelDifferentialGearMeshHarmonicAnalysis",
    "BevelDifferentialGearSetHarmonicAnalysis",
    "BevelDifferentialPlanetGearHarmonicAnalysis",
    "BevelDifferentialSunGearHarmonicAnalysis",
    "BevelGearHarmonicAnalysis",
    "BevelGearMeshHarmonicAnalysis",
    "BevelGearSetHarmonicAnalysis",
    "BoltedJointHarmonicAnalysis",
    "BoltHarmonicAnalysis",
    "ClutchConnectionHarmonicAnalysis",
    "ClutchHalfHarmonicAnalysis",
    "ClutchHarmonicAnalysis",
    "CoaxialConnectionHarmonicAnalysis",
    "ComplianceAndForceData",
    "ComponentHarmonicAnalysis",
    "ConceptCouplingConnectionHarmonicAnalysis",
    "ConceptCouplingHalfHarmonicAnalysis",
    "ConceptCouplingHarmonicAnalysis",
    "ConceptGearHarmonicAnalysis",
    "ConceptGearMeshHarmonicAnalysis",
    "ConceptGearSetHarmonicAnalysis",
    "ConicalGearHarmonicAnalysis",
    "ConicalGearMeshHarmonicAnalysis",
    "ConicalGearSetHarmonicAnalysis",
    "ConnectionHarmonicAnalysis",
    "ConnectorHarmonicAnalysis",
    "CouplingConnectionHarmonicAnalysis",
    "CouplingHalfHarmonicAnalysis",
    "CouplingHarmonicAnalysis",
    "CVTBeltConnectionHarmonicAnalysis",
    "CVTHarmonicAnalysis",
    "CVTPulleyHarmonicAnalysis",
    "CycloidalAssemblyHarmonicAnalysis",
    "CycloidalDiscCentralBearingConnectionHarmonicAnalysis",
    "CycloidalDiscHarmonicAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis",
    "CylindricalGearHarmonicAnalysis",
    "CylindricalGearMeshHarmonicAnalysis",
    "CylindricalGearSetHarmonicAnalysis",
    "CylindricalPlanetGearHarmonicAnalysis",
    "DatumHarmonicAnalysis",
    "DynamicModelForHarmonicAnalysis",
    "ElectricMachinePeriodicExcitationDetail",
    "ElectricMachineRotorXForcePeriodicExcitationDetail",
    "ElectricMachineRotorXMomentPeriodicExcitationDetail",
    "ElectricMachineRotorYForcePeriodicExcitationDetail",
    "ElectricMachineRotorYMomentPeriodicExcitationDetail",
    "ElectricMachineRotorZForcePeriodicExcitationDetail",
    "ElectricMachineStatorToothAxialLoadsExcitationDetail",
    "ElectricMachineStatorToothLoadsExcitationDetail",
    "ElectricMachineStatorToothMomentsExcitationDetail",
    "ElectricMachineStatorToothRadialLoadsExcitationDetail",
    "ElectricMachineStatorToothTangentialLoadsExcitationDetail",
    "ElectricMachineTorqueRipplePeriodicExcitationDetail",
    "ExportOutputType",
    "ExternalCADModelHarmonicAnalysis",
    "FaceGearHarmonicAnalysis",
    "FaceGearMeshHarmonicAnalysis",
    "FaceGearSetHarmonicAnalysis",
    "FEPartHarmonicAnalysis",
    "FlexiblePinAssemblyHarmonicAnalysis",
    "FrequencyOptionsForHarmonicAnalysisResults",
    "GearHarmonicAnalysis",
    "GearMeshExcitationDetail",
    "GearMeshHarmonicAnalysis",
    "GearMeshMisalignmentExcitationDetail",
    "GearMeshTEExcitationDetail",
    "GearSetHarmonicAnalysis",
    "GeneralPeriodicExcitationDetail",
    "GuideDxfModelHarmonicAnalysis",
    "HarmonicAnalysis",
    "HarmonicAnalysisDrawStyle",
    "HarmonicAnalysisExportOptions",
    "HarmonicAnalysisFEExportOptions",
    "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "HarmonicAnalysisOptions",
    "HarmonicAnalysisRootAssemblyExportOptions",
    "HarmonicAnalysisShaftExportOptions",
    "HarmonicAnalysisTorqueInputType",
    "HarmonicAnalysisWithVaryingStiffnessStaticLoadCase",
    "HypoidGearHarmonicAnalysis",
    "HypoidGearMeshHarmonicAnalysis",
    "HypoidGearSetHarmonicAnalysis",
    "InterMountableComponentConnectionHarmonicAnalysis",
    "KlingelnbergCycloPalloidConicalGearHarmonicAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis",
    "KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis",
    "MassDiscHarmonicAnalysis",
    "MeasurementComponentHarmonicAnalysis",
    "MountableComponentHarmonicAnalysis",
    "OilSealHarmonicAnalysis",
    "PartHarmonicAnalysis",
    "PartToPartShearCouplingConnectionHarmonicAnalysis",
    "PartToPartShearCouplingHalfHarmonicAnalysis",
    "PartToPartShearCouplingHarmonicAnalysis",
    "PeriodicExcitationWithReferenceShaft",
    "PlanetaryConnectionHarmonicAnalysis",
    "PlanetaryGearSetHarmonicAnalysis",
    "PlanetCarrierHarmonicAnalysis",
    "PointLoadHarmonicAnalysis",
    "PowerLoadHarmonicAnalysis",
    "PulleyHarmonicAnalysis",
    "ResponseCacheLevel",
    "RingPinsHarmonicAnalysis",
    "RingPinsToDiscConnectionHarmonicAnalysis",
    "RollingRingAssemblyHarmonicAnalysis",
    "RollingRingConnectionHarmonicAnalysis",
    "RollingRingHarmonicAnalysis",
    "RootAssemblyHarmonicAnalysis",
    "ShaftHarmonicAnalysis",
    "ShaftHubConnectionHarmonicAnalysis",
    "ShaftToMountableComponentConnectionHarmonicAnalysis",
    "SingleNodePeriodicExcitationWithReferenceShaft",
    "SpecialisedAssemblyHarmonicAnalysis",
    "SpeedOptionsForHarmonicAnalysisResults",
    "SpiralBevelGearHarmonicAnalysis",
    "SpiralBevelGearMeshHarmonicAnalysis",
    "SpiralBevelGearSetHarmonicAnalysis",
    "SpringDamperConnectionHarmonicAnalysis",
    "SpringDamperHalfHarmonicAnalysis",
    "SpringDamperHarmonicAnalysis",
    "StiffnessOptionsForHarmonicAnalysis",
    "StraightBevelDiffGearHarmonicAnalysis",
    "StraightBevelDiffGearMeshHarmonicAnalysis",
    "StraightBevelDiffGearSetHarmonicAnalysis",
    "StraightBevelGearHarmonicAnalysis",
    "StraightBevelGearMeshHarmonicAnalysis",
    "StraightBevelGearSetHarmonicAnalysis",
    "StraightBevelPlanetGearHarmonicAnalysis",
    "StraightBevelSunGearHarmonicAnalysis",
    "SynchroniserHalfHarmonicAnalysis",
    "SynchroniserHarmonicAnalysis",
    "SynchroniserPartHarmonicAnalysis",
    "SynchroniserSleeveHarmonicAnalysis",
    "TorqueConverterConnectionHarmonicAnalysis",
    "TorqueConverterHarmonicAnalysis",
    "TorqueConverterPumpHarmonicAnalysis",
    "TorqueConverterTurbineHarmonicAnalysis",
    "UnbalancedMassExcitationDetail",
    "UnbalancedMassHarmonicAnalysis",
    "VirtualComponentHarmonicAnalysis",
    "WormGearHarmonicAnalysis",
    "WormGearMeshHarmonicAnalysis",
    "WormGearSetHarmonicAnalysis",
    "ZerolBevelGearHarmonicAnalysis",
    "ZerolBevelGearMeshHarmonicAnalysis",
    "ZerolBevelGearSetHarmonicAnalysis",
)
