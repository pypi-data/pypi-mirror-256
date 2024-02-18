"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2687 import AbstractAssemblySystemDeflection
    from ._2688 import AbstractShaftOrHousingSystemDeflection
    from ._2689 import AbstractShaftSystemDeflection
    from ._2690 import AbstractShaftToMountableComponentConnectionSystemDeflection
    from ._2691 import AGMAGleasonConicalGearMeshSystemDeflection
    from ._2692 import AGMAGleasonConicalGearSetSystemDeflection
    from ._2693 import AGMAGleasonConicalGearSystemDeflection
    from ._2694 import AssemblySystemDeflection
    from ._2695 import BearingDynamicElementContactPropertyWrapper
    from ._2696 import BearingDynamicElementPropertyWrapper
    from ._2697 import BearingDynamicPostAnalysisResultWrapper
    from ._2698 import BearingDynamicResultsPropertyWrapper
    from ._2699 import BearingDynamicResultsUIWrapper
    from ._2700 import BearingSystemDeflection
    from ._2701 import BeltConnectionSystemDeflection
    from ._2702 import BeltDriveSystemDeflection
    from ._2703 import BevelDifferentialGearMeshSystemDeflection
    from ._2704 import BevelDifferentialGearSetSystemDeflection
    from ._2705 import BevelDifferentialGearSystemDeflection
    from ._2706 import BevelDifferentialPlanetGearSystemDeflection
    from ._2707 import BevelDifferentialSunGearSystemDeflection
    from ._2708 import BevelGearMeshSystemDeflection
    from ._2709 import BevelGearSetSystemDeflection
    from ._2710 import BevelGearSystemDeflection
    from ._2711 import BoltedJointSystemDeflection
    from ._2712 import BoltSystemDeflection
    from ._2713 import ClutchConnectionSystemDeflection
    from ._2714 import ClutchHalfSystemDeflection
    from ._2715 import ClutchSystemDeflection
    from ._2716 import CoaxialConnectionSystemDeflection
    from ._2717 import ComponentSystemDeflection
    from ._2718 import ConcentricPartGroupCombinationSystemDeflectionResults
    from ._2719 import ConceptCouplingConnectionSystemDeflection
    from ._2720 import ConceptCouplingHalfSystemDeflection
    from ._2721 import ConceptCouplingSystemDeflection
    from ._2722 import ConceptGearMeshSystemDeflection
    from ._2723 import ConceptGearSetSystemDeflection
    from ._2724 import ConceptGearSystemDeflection
    from ._2725 import ConicalGearMeshMisalignmentsWithRespectToCrossPointCalculator
    from ._2726 import ConicalGearMeshSystemDeflection
    from ._2727 import ConicalGearSetSystemDeflection
    from ._2728 import ConicalGearSystemDeflection
    from ._2729 import ConnectionSystemDeflection
    from ._2730 import ConnectorSystemDeflection
    from ._2731 import CouplingConnectionSystemDeflection
    from ._2732 import CouplingHalfSystemDeflection
    from ._2733 import CouplingSystemDeflection
    from ._2734 import CVTBeltConnectionSystemDeflection
    from ._2735 import CVTPulleySystemDeflection
    from ._2736 import CVTSystemDeflection
    from ._2737 import CycloidalAssemblySystemDeflection
    from ._2738 import CycloidalDiscCentralBearingConnectionSystemDeflection
    from ._2739 import CycloidalDiscPlanetaryBearingConnectionSystemDeflection
    from ._2740 import CycloidalDiscSystemDeflection
    from ._2741 import CylindricalGearMeshSystemDeflection
    from ._2742 import CylindricalGearMeshSystemDeflectionTimestep
    from ._2743 import CylindricalGearMeshSystemDeflectionWithLTCAResults
    from ._2744 import CylindricalGearSetSystemDeflection
    from ._2745 import CylindricalGearSetSystemDeflectionTimestep
    from ._2746 import CylindricalGearSetSystemDeflectionWithLTCAResults
    from ._2747 import CylindricalGearSystemDeflection
    from ._2748 import CylindricalGearSystemDeflectionTimestep
    from ._2749 import CylindricalGearSystemDeflectionWithLTCAResults
    from ._2750 import CylindricalMeshedGearFlankSystemDeflection
    from ._2751 import CylindricalMeshedGearSystemDeflection
    from ._2752 import CylindricalPlanetGearSystemDeflection
    from ._2753 import DatumSystemDeflection
    from ._2754 import ExternalCADModelSystemDeflection
    from ._2755 import FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator
    from ._2756 import FaceGearMeshSystemDeflection
    from ._2757 import FaceGearSetSystemDeflection
    from ._2758 import FaceGearSystemDeflection
    from ._2759 import FEPartSystemDeflection
    from ._2760 import FlexiblePinAssemblySystemDeflection
    from ._2761 import GearMeshSystemDeflection
    from ._2762 import GearSetSystemDeflection
    from ._2763 import GearSystemDeflection
    from ._2764 import GuideDxfModelSystemDeflection
    from ._2765 import HypoidGearMeshSystemDeflection
    from ._2766 import HypoidGearSetSystemDeflection
    from ._2767 import HypoidGearSystemDeflection
    from ._2768 import InformationForContactAtPointAlongFaceWidth
    from ._2769 import InterMountableComponentConnectionSystemDeflection
    from ._2770 import KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
    from ._2771 import KlingelnbergCycloPalloidConicalGearSetSystemDeflection
    from ._2772 import KlingelnbergCycloPalloidConicalGearSystemDeflection
    from ._2773 import KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
    from ._2774 import KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
    from ._2775 import KlingelnbergCycloPalloidHypoidGearSystemDeflection
    from ._2776 import KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
    from ._2777 import KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
    from ._2778 import KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
    from ._2779 import LoadCaseOverallEfficiencyResult
    from ._2780 import LoadSharingFactorReporter
    from ._2781 import MassDiscSystemDeflection
    from ._2782 import MeasurementComponentSystemDeflection
    from ._2783 import MeshSeparationsAtFaceWidth
    from ._2784 import MountableComponentSystemDeflection
    from ._2785 import ObservedPinStiffnessReporter
    from ._2786 import OilSealSystemDeflection
    from ._2787 import PartSystemDeflection
    from ._2788 import PartToPartShearCouplingConnectionSystemDeflection
    from ._2789 import PartToPartShearCouplingHalfSystemDeflection
    from ._2790 import PartToPartShearCouplingSystemDeflection
    from ._2791 import PlanetaryConnectionSystemDeflection
    from ._2792 import PlanetCarrierSystemDeflection
    from ._2793 import PointLoadSystemDeflection
    from ._2794 import PowerLoadSystemDeflection
    from ._2795 import PulleySystemDeflection
    from ._2796 import RingPinsSystemDeflection
    from ._2797 import RingPinsToDiscConnectionSystemDeflection
    from ._2798 import RingPinToDiscContactReporting
    from ._2799 import RollingRingAssemblySystemDeflection
    from ._2800 import RollingRingConnectionSystemDeflection
    from ._2801 import RollingRingSystemDeflection
    from ._2802 import RootAssemblySystemDeflection
    from ._2803 import ShaftHubConnectionSystemDeflection
    from ._2804 import ShaftSectionEndResultsSystemDeflection
    from ._2805 import ShaftSectionSystemDeflection
    from ._2806 import ShaftSystemDeflection
    from ._2807 import ShaftToMountableComponentConnectionSystemDeflection
    from ._2808 import SpecialisedAssemblySystemDeflection
    from ._2809 import SpiralBevelGearMeshSystemDeflection
    from ._2810 import SpiralBevelGearSetSystemDeflection
    from ._2811 import SpiralBevelGearSystemDeflection
    from ._2812 import SpringDamperConnectionSystemDeflection
    from ._2813 import SpringDamperHalfSystemDeflection
    from ._2814 import SpringDamperSystemDeflection
    from ._2815 import StraightBevelDiffGearMeshSystemDeflection
    from ._2816 import StraightBevelDiffGearSetSystemDeflection
    from ._2817 import StraightBevelDiffGearSystemDeflection
    from ._2818 import StraightBevelGearMeshSystemDeflection
    from ._2819 import StraightBevelGearSetSystemDeflection
    from ._2820 import StraightBevelGearSystemDeflection
    from ._2821 import StraightBevelPlanetGearSystemDeflection
    from ._2822 import StraightBevelSunGearSystemDeflection
    from ._2823 import SynchroniserHalfSystemDeflection
    from ._2824 import SynchroniserPartSystemDeflection
    from ._2825 import SynchroniserSleeveSystemDeflection
    from ._2826 import SynchroniserSystemDeflection
    from ._2827 import SystemDeflection
    from ._2828 import SystemDeflectionDrawStyle
    from ._2829 import SystemDeflectionOptions
    from ._2830 import TorqueConverterConnectionSystemDeflection
    from ._2831 import TorqueConverterPumpSystemDeflection
    from ._2832 import TorqueConverterSystemDeflection
    from ._2833 import TorqueConverterTurbineSystemDeflection
    from ._2834 import TorsionalSystemDeflection
    from ._2835 import TransmissionErrorResult
    from ._2836 import UnbalancedMassSystemDeflection
    from ._2837 import VirtualComponentSystemDeflection
    from ._2838 import WormGearMeshSystemDeflection
    from ._2839 import WormGearSetSystemDeflection
    from ._2840 import WormGearSystemDeflection
    from ._2841 import ZerolBevelGearMeshSystemDeflection
    from ._2842 import ZerolBevelGearSetSystemDeflection
    from ._2843 import ZerolBevelGearSystemDeflection
else:
    import_structure = {
        "_2687": ["AbstractAssemblySystemDeflection"],
        "_2688": ["AbstractShaftOrHousingSystemDeflection"],
        "_2689": ["AbstractShaftSystemDeflection"],
        "_2690": ["AbstractShaftToMountableComponentConnectionSystemDeflection"],
        "_2691": ["AGMAGleasonConicalGearMeshSystemDeflection"],
        "_2692": ["AGMAGleasonConicalGearSetSystemDeflection"],
        "_2693": ["AGMAGleasonConicalGearSystemDeflection"],
        "_2694": ["AssemblySystemDeflection"],
        "_2695": ["BearingDynamicElementContactPropertyWrapper"],
        "_2696": ["BearingDynamicElementPropertyWrapper"],
        "_2697": ["BearingDynamicPostAnalysisResultWrapper"],
        "_2698": ["BearingDynamicResultsPropertyWrapper"],
        "_2699": ["BearingDynamicResultsUIWrapper"],
        "_2700": ["BearingSystemDeflection"],
        "_2701": ["BeltConnectionSystemDeflection"],
        "_2702": ["BeltDriveSystemDeflection"],
        "_2703": ["BevelDifferentialGearMeshSystemDeflection"],
        "_2704": ["BevelDifferentialGearSetSystemDeflection"],
        "_2705": ["BevelDifferentialGearSystemDeflection"],
        "_2706": ["BevelDifferentialPlanetGearSystemDeflection"],
        "_2707": ["BevelDifferentialSunGearSystemDeflection"],
        "_2708": ["BevelGearMeshSystemDeflection"],
        "_2709": ["BevelGearSetSystemDeflection"],
        "_2710": ["BevelGearSystemDeflection"],
        "_2711": ["BoltedJointSystemDeflection"],
        "_2712": ["BoltSystemDeflection"],
        "_2713": ["ClutchConnectionSystemDeflection"],
        "_2714": ["ClutchHalfSystemDeflection"],
        "_2715": ["ClutchSystemDeflection"],
        "_2716": ["CoaxialConnectionSystemDeflection"],
        "_2717": ["ComponentSystemDeflection"],
        "_2718": ["ConcentricPartGroupCombinationSystemDeflectionResults"],
        "_2719": ["ConceptCouplingConnectionSystemDeflection"],
        "_2720": ["ConceptCouplingHalfSystemDeflection"],
        "_2721": ["ConceptCouplingSystemDeflection"],
        "_2722": ["ConceptGearMeshSystemDeflection"],
        "_2723": ["ConceptGearSetSystemDeflection"],
        "_2724": ["ConceptGearSystemDeflection"],
        "_2725": ["ConicalGearMeshMisalignmentsWithRespectToCrossPointCalculator"],
        "_2726": ["ConicalGearMeshSystemDeflection"],
        "_2727": ["ConicalGearSetSystemDeflection"],
        "_2728": ["ConicalGearSystemDeflection"],
        "_2729": ["ConnectionSystemDeflection"],
        "_2730": ["ConnectorSystemDeflection"],
        "_2731": ["CouplingConnectionSystemDeflection"],
        "_2732": ["CouplingHalfSystemDeflection"],
        "_2733": ["CouplingSystemDeflection"],
        "_2734": ["CVTBeltConnectionSystemDeflection"],
        "_2735": ["CVTPulleySystemDeflection"],
        "_2736": ["CVTSystemDeflection"],
        "_2737": ["CycloidalAssemblySystemDeflection"],
        "_2738": ["CycloidalDiscCentralBearingConnectionSystemDeflection"],
        "_2739": ["CycloidalDiscPlanetaryBearingConnectionSystemDeflection"],
        "_2740": ["CycloidalDiscSystemDeflection"],
        "_2741": ["CylindricalGearMeshSystemDeflection"],
        "_2742": ["CylindricalGearMeshSystemDeflectionTimestep"],
        "_2743": ["CylindricalGearMeshSystemDeflectionWithLTCAResults"],
        "_2744": ["CylindricalGearSetSystemDeflection"],
        "_2745": ["CylindricalGearSetSystemDeflectionTimestep"],
        "_2746": ["CylindricalGearSetSystemDeflectionWithLTCAResults"],
        "_2747": ["CylindricalGearSystemDeflection"],
        "_2748": ["CylindricalGearSystemDeflectionTimestep"],
        "_2749": ["CylindricalGearSystemDeflectionWithLTCAResults"],
        "_2750": ["CylindricalMeshedGearFlankSystemDeflection"],
        "_2751": ["CylindricalMeshedGearSystemDeflection"],
        "_2752": ["CylindricalPlanetGearSystemDeflection"],
        "_2753": ["DatumSystemDeflection"],
        "_2754": ["ExternalCADModelSystemDeflection"],
        "_2755": ["FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator"],
        "_2756": ["FaceGearMeshSystemDeflection"],
        "_2757": ["FaceGearSetSystemDeflection"],
        "_2758": ["FaceGearSystemDeflection"],
        "_2759": ["FEPartSystemDeflection"],
        "_2760": ["FlexiblePinAssemblySystemDeflection"],
        "_2761": ["GearMeshSystemDeflection"],
        "_2762": ["GearSetSystemDeflection"],
        "_2763": ["GearSystemDeflection"],
        "_2764": ["GuideDxfModelSystemDeflection"],
        "_2765": ["HypoidGearMeshSystemDeflection"],
        "_2766": ["HypoidGearSetSystemDeflection"],
        "_2767": ["HypoidGearSystemDeflection"],
        "_2768": ["InformationForContactAtPointAlongFaceWidth"],
        "_2769": ["InterMountableComponentConnectionSystemDeflection"],
        "_2770": ["KlingelnbergCycloPalloidConicalGearMeshSystemDeflection"],
        "_2771": ["KlingelnbergCycloPalloidConicalGearSetSystemDeflection"],
        "_2772": ["KlingelnbergCycloPalloidConicalGearSystemDeflection"],
        "_2773": ["KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection"],
        "_2774": ["KlingelnbergCycloPalloidHypoidGearSetSystemDeflection"],
        "_2775": ["KlingelnbergCycloPalloidHypoidGearSystemDeflection"],
        "_2776": ["KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection"],
        "_2777": ["KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection"],
        "_2778": ["KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection"],
        "_2779": ["LoadCaseOverallEfficiencyResult"],
        "_2780": ["LoadSharingFactorReporter"],
        "_2781": ["MassDiscSystemDeflection"],
        "_2782": ["MeasurementComponentSystemDeflection"],
        "_2783": ["MeshSeparationsAtFaceWidth"],
        "_2784": ["MountableComponentSystemDeflection"],
        "_2785": ["ObservedPinStiffnessReporter"],
        "_2786": ["OilSealSystemDeflection"],
        "_2787": ["PartSystemDeflection"],
        "_2788": ["PartToPartShearCouplingConnectionSystemDeflection"],
        "_2789": ["PartToPartShearCouplingHalfSystemDeflection"],
        "_2790": ["PartToPartShearCouplingSystemDeflection"],
        "_2791": ["PlanetaryConnectionSystemDeflection"],
        "_2792": ["PlanetCarrierSystemDeflection"],
        "_2793": ["PointLoadSystemDeflection"],
        "_2794": ["PowerLoadSystemDeflection"],
        "_2795": ["PulleySystemDeflection"],
        "_2796": ["RingPinsSystemDeflection"],
        "_2797": ["RingPinsToDiscConnectionSystemDeflection"],
        "_2798": ["RingPinToDiscContactReporting"],
        "_2799": ["RollingRingAssemblySystemDeflection"],
        "_2800": ["RollingRingConnectionSystemDeflection"],
        "_2801": ["RollingRingSystemDeflection"],
        "_2802": ["RootAssemblySystemDeflection"],
        "_2803": ["ShaftHubConnectionSystemDeflection"],
        "_2804": ["ShaftSectionEndResultsSystemDeflection"],
        "_2805": ["ShaftSectionSystemDeflection"],
        "_2806": ["ShaftSystemDeflection"],
        "_2807": ["ShaftToMountableComponentConnectionSystemDeflection"],
        "_2808": ["SpecialisedAssemblySystemDeflection"],
        "_2809": ["SpiralBevelGearMeshSystemDeflection"],
        "_2810": ["SpiralBevelGearSetSystemDeflection"],
        "_2811": ["SpiralBevelGearSystemDeflection"],
        "_2812": ["SpringDamperConnectionSystemDeflection"],
        "_2813": ["SpringDamperHalfSystemDeflection"],
        "_2814": ["SpringDamperSystemDeflection"],
        "_2815": ["StraightBevelDiffGearMeshSystemDeflection"],
        "_2816": ["StraightBevelDiffGearSetSystemDeflection"],
        "_2817": ["StraightBevelDiffGearSystemDeflection"],
        "_2818": ["StraightBevelGearMeshSystemDeflection"],
        "_2819": ["StraightBevelGearSetSystemDeflection"],
        "_2820": ["StraightBevelGearSystemDeflection"],
        "_2821": ["StraightBevelPlanetGearSystemDeflection"],
        "_2822": ["StraightBevelSunGearSystemDeflection"],
        "_2823": ["SynchroniserHalfSystemDeflection"],
        "_2824": ["SynchroniserPartSystemDeflection"],
        "_2825": ["SynchroniserSleeveSystemDeflection"],
        "_2826": ["SynchroniserSystemDeflection"],
        "_2827": ["SystemDeflection"],
        "_2828": ["SystemDeflectionDrawStyle"],
        "_2829": ["SystemDeflectionOptions"],
        "_2830": ["TorqueConverterConnectionSystemDeflection"],
        "_2831": ["TorqueConverterPumpSystemDeflection"],
        "_2832": ["TorqueConverterSystemDeflection"],
        "_2833": ["TorqueConverterTurbineSystemDeflection"],
        "_2834": ["TorsionalSystemDeflection"],
        "_2835": ["TransmissionErrorResult"],
        "_2836": ["UnbalancedMassSystemDeflection"],
        "_2837": ["VirtualComponentSystemDeflection"],
        "_2838": ["WormGearMeshSystemDeflection"],
        "_2839": ["WormGearSetSystemDeflection"],
        "_2840": ["WormGearSystemDeflection"],
        "_2841": ["ZerolBevelGearMeshSystemDeflection"],
        "_2842": ["ZerolBevelGearSetSystemDeflection"],
        "_2843": ["ZerolBevelGearSystemDeflection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblySystemDeflection",
    "AbstractShaftOrHousingSystemDeflection",
    "AbstractShaftSystemDeflection",
    "AbstractShaftToMountableComponentConnectionSystemDeflection",
    "AGMAGleasonConicalGearMeshSystemDeflection",
    "AGMAGleasonConicalGearSetSystemDeflection",
    "AGMAGleasonConicalGearSystemDeflection",
    "AssemblySystemDeflection",
    "BearingDynamicElementContactPropertyWrapper",
    "BearingDynamicElementPropertyWrapper",
    "BearingDynamicPostAnalysisResultWrapper",
    "BearingDynamicResultsPropertyWrapper",
    "BearingDynamicResultsUIWrapper",
    "BearingSystemDeflection",
    "BeltConnectionSystemDeflection",
    "BeltDriveSystemDeflection",
    "BevelDifferentialGearMeshSystemDeflection",
    "BevelDifferentialGearSetSystemDeflection",
    "BevelDifferentialGearSystemDeflection",
    "BevelDifferentialPlanetGearSystemDeflection",
    "BevelDifferentialSunGearSystemDeflection",
    "BevelGearMeshSystemDeflection",
    "BevelGearSetSystemDeflection",
    "BevelGearSystemDeflection",
    "BoltedJointSystemDeflection",
    "BoltSystemDeflection",
    "ClutchConnectionSystemDeflection",
    "ClutchHalfSystemDeflection",
    "ClutchSystemDeflection",
    "CoaxialConnectionSystemDeflection",
    "ComponentSystemDeflection",
    "ConcentricPartGroupCombinationSystemDeflectionResults",
    "ConceptCouplingConnectionSystemDeflection",
    "ConceptCouplingHalfSystemDeflection",
    "ConceptCouplingSystemDeflection",
    "ConceptGearMeshSystemDeflection",
    "ConceptGearSetSystemDeflection",
    "ConceptGearSystemDeflection",
    "ConicalGearMeshMisalignmentsWithRespectToCrossPointCalculator",
    "ConicalGearMeshSystemDeflection",
    "ConicalGearSetSystemDeflection",
    "ConicalGearSystemDeflection",
    "ConnectionSystemDeflection",
    "ConnectorSystemDeflection",
    "CouplingConnectionSystemDeflection",
    "CouplingHalfSystemDeflection",
    "CouplingSystemDeflection",
    "CVTBeltConnectionSystemDeflection",
    "CVTPulleySystemDeflection",
    "CVTSystemDeflection",
    "CycloidalAssemblySystemDeflection",
    "CycloidalDiscCentralBearingConnectionSystemDeflection",
    "CycloidalDiscPlanetaryBearingConnectionSystemDeflection",
    "CycloidalDiscSystemDeflection",
    "CylindricalGearMeshSystemDeflection",
    "CylindricalGearMeshSystemDeflectionTimestep",
    "CylindricalGearMeshSystemDeflectionWithLTCAResults",
    "CylindricalGearSetSystemDeflection",
    "CylindricalGearSetSystemDeflectionTimestep",
    "CylindricalGearSetSystemDeflectionWithLTCAResults",
    "CylindricalGearSystemDeflection",
    "CylindricalGearSystemDeflectionTimestep",
    "CylindricalGearSystemDeflectionWithLTCAResults",
    "CylindricalMeshedGearFlankSystemDeflection",
    "CylindricalMeshedGearSystemDeflection",
    "CylindricalPlanetGearSystemDeflection",
    "DatumSystemDeflection",
    "ExternalCADModelSystemDeflection",
    "FaceGearMeshMisalignmentsWithRespectToCrossPointCalculator",
    "FaceGearMeshSystemDeflection",
    "FaceGearSetSystemDeflection",
    "FaceGearSystemDeflection",
    "FEPartSystemDeflection",
    "FlexiblePinAssemblySystemDeflection",
    "GearMeshSystemDeflection",
    "GearSetSystemDeflection",
    "GearSystemDeflection",
    "GuideDxfModelSystemDeflection",
    "HypoidGearMeshSystemDeflection",
    "HypoidGearSetSystemDeflection",
    "HypoidGearSystemDeflection",
    "InformationForContactAtPointAlongFaceWidth",
    "InterMountableComponentConnectionSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearMeshSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearSetSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearSetSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection",
    "LoadCaseOverallEfficiencyResult",
    "LoadSharingFactorReporter",
    "MassDiscSystemDeflection",
    "MeasurementComponentSystemDeflection",
    "MeshSeparationsAtFaceWidth",
    "MountableComponentSystemDeflection",
    "ObservedPinStiffnessReporter",
    "OilSealSystemDeflection",
    "PartSystemDeflection",
    "PartToPartShearCouplingConnectionSystemDeflection",
    "PartToPartShearCouplingHalfSystemDeflection",
    "PartToPartShearCouplingSystemDeflection",
    "PlanetaryConnectionSystemDeflection",
    "PlanetCarrierSystemDeflection",
    "PointLoadSystemDeflection",
    "PowerLoadSystemDeflection",
    "PulleySystemDeflection",
    "RingPinsSystemDeflection",
    "RingPinsToDiscConnectionSystemDeflection",
    "RingPinToDiscContactReporting",
    "RollingRingAssemblySystemDeflection",
    "RollingRingConnectionSystemDeflection",
    "RollingRingSystemDeflection",
    "RootAssemblySystemDeflection",
    "ShaftHubConnectionSystemDeflection",
    "ShaftSectionEndResultsSystemDeflection",
    "ShaftSectionSystemDeflection",
    "ShaftSystemDeflection",
    "ShaftToMountableComponentConnectionSystemDeflection",
    "SpecialisedAssemblySystemDeflection",
    "SpiralBevelGearMeshSystemDeflection",
    "SpiralBevelGearSetSystemDeflection",
    "SpiralBevelGearSystemDeflection",
    "SpringDamperConnectionSystemDeflection",
    "SpringDamperHalfSystemDeflection",
    "SpringDamperSystemDeflection",
    "StraightBevelDiffGearMeshSystemDeflection",
    "StraightBevelDiffGearSetSystemDeflection",
    "StraightBevelDiffGearSystemDeflection",
    "StraightBevelGearMeshSystemDeflection",
    "StraightBevelGearSetSystemDeflection",
    "StraightBevelGearSystemDeflection",
    "StraightBevelPlanetGearSystemDeflection",
    "StraightBevelSunGearSystemDeflection",
    "SynchroniserHalfSystemDeflection",
    "SynchroniserPartSystemDeflection",
    "SynchroniserSleeveSystemDeflection",
    "SynchroniserSystemDeflection",
    "SystemDeflection",
    "SystemDeflectionDrawStyle",
    "SystemDeflectionOptions",
    "TorqueConverterConnectionSystemDeflection",
    "TorqueConverterPumpSystemDeflection",
    "TorqueConverterSystemDeflection",
    "TorqueConverterTurbineSystemDeflection",
    "TorsionalSystemDeflection",
    "TransmissionErrorResult",
    "UnbalancedMassSystemDeflection",
    "VirtualComponentSystemDeflection",
    "WormGearMeshSystemDeflection",
    "WormGearSetSystemDeflection",
    "WormGearSystemDeflection",
    "ZerolBevelGearMeshSystemDeflection",
    "ZerolBevelGearSetSystemDeflection",
    "ZerolBevelGearSystemDeflection",
)
