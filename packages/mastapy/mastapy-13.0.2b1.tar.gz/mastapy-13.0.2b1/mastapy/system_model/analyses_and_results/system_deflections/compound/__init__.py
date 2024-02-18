"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2853 import AbstractAssemblyCompoundSystemDeflection
    from ._2854 import AbstractShaftCompoundSystemDeflection
    from ._2855 import AbstractShaftOrHousingCompoundSystemDeflection
    from ._2856 import (
        AbstractShaftToMountableComponentConnectionCompoundSystemDeflection,
    )
    from ._2857 import AGMAGleasonConicalGearCompoundSystemDeflection
    from ._2858 import AGMAGleasonConicalGearMeshCompoundSystemDeflection
    from ._2859 import AGMAGleasonConicalGearSetCompoundSystemDeflection
    from ._2860 import AssemblyCompoundSystemDeflection
    from ._2861 import BearingCompoundSystemDeflection
    from ._2862 import BeltConnectionCompoundSystemDeflection
    from ._2863 import BeltDriveCompoundSystemDeflection
    from ._2864 import BevelDifferentialGearCompoundSystemDeflection
    from ._2865 import BevelDifferentialGearMeshCompoundSystemDeflection
    from ._2866 import BevelDifferentialGearSetCompoundSystemDeflection
    from ._2867 import BevelDifferentialPlanetGearCompoundSystemDeflection
    from ._2868 import BevelDifferentialSunGearCompoundSystemDeflection
    from ._2869 import BevelGearCompoundSystemDeflection
    from ._2870 import BevelGearMeshCompoundSystemDeflection
    from ._2871 import BevelGearSetCompoundSystemDeflection
    from ._2872 import BoltCompoundSystemDeflection
    from ._2873 import BoltedJointCompoundSystemDeflection
    from ._2874 import ClutchCompoundSystemDeflection
    from ._2875 import ClutchConnectionCompoundSystemDeflection
    from ._2876 import ClutchHalfCompoundSystemDeflection
    from ._2877 import CoaxialConnectionCompoundSystemDeflection
    from ._2878 import ComponentCompoundSystemDeflection
    from ._2879 import ConceptCouplingCompoundSystemDeflection
    from ._2880 import ConceptCouplingConnectionCompoundSystemDeflection
    from ._2881 import ConceptCouplingHalfCompoundSystemDeflection
    from ._2882 import ConceptGearCompoundSystemDeflection
    from ._2883 import ConceptGearMeshCompoundSystemDeflection
    from ._2884 import ConceptGearSetCompoundSystemDeflection
    from ._2885 import ConicalGearCompoundSystemDeflection
    from ._2886 import ConicalGearMeshCompoundSystemDeflection
    from ._2887 import ConicalGearSetCompoundSystemDeflection
    from ._2888 import ConnectionCompoundSystemDeflection
    from ._2889 import ConnectorCompoundSystemDeflection
    from ._2890 import CouplingCompoundSystemDeflection
    from ._2891 import CouplingConnectionCompoundSystemDeflection
    from ._2892 import CouplingHalfCompoundSystemDeflection
    from ._2893 import CVTBeltConnectionCompoundSystemDeflection
    from ._2894 import CVTCompoundSystemDeflection
    from ._2895 import CVTPulleyCompoundSystemDeflection
    from ._2896 import CycloidalAssemblyCompoundSystemDeflection
    from ._2897 import CycloidalDiscCentralBearingConnectionCompoundSystemDeflection
    from ._2898 import CycloidalDiscCompoundSystemDeflection
    from ._2899 import CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection
    from ._2900 import CylindricalGearCompoundSystemDeflection
    from ._2901 import CylindricalGearMeshCompoundSystemDeflection
    from ._2902 import CylindricalGearSetCompoundSystemDeflection
    from ._2903 import CylindricalPlanetGearCompoundSystemDeflection
    from ._2904 import DatumCompoundSystemDeflection
    from ._2905 import DutyCycleEfficiencyResults
    from ._2906 import ExternalCADModelCompoundSystemDeflection
    from ._2907 import FaceGearCompoundSystemDeflection
    from ._2908 import FaceGearMeshCompoundSystemDeflection
    from ._2909 import FaceGearSetCompoundSystemDeflection
    from ._2910 import FEPartCompoundSystemDeflection
    from ._2911 import FlexiblePinAssemblyCompoundSystemDeflection
    from ._2912 import GearCompoundSystemDeflection
    from ._2913 import GearMeshCompoundSystemDeflection
    from ._2914 import GearSetCompoundSystemDeflection
    from ._2915 import GuideDxfModelCompoundSystemDeflection
    from ._2916 import HypoidGearCompoundSystemDeflection
    from ._2917 import HypoidGearMeshCompoundSystemDeflection
    from ._2918 import HypoidGearSetCompoundSystemDeflection
    from ._2919 import InterMountableComponentConnectionCompoundSystemDeflection
    from ._2920 import KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection
    from ._2921 import KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection
    from ._2922 import KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection
    from ._2923 import KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection
    from ._2924 import KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection
    from ._2925 import KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection
    from ._2926 import KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection
    from ._2927 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection,
    )
    from ._2928 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection,
    )
    from ._2929 import MassDiscCompoundSystemDeflection
    from ._2930 import MeasurementComponentCompoundSystemDeflection
    from ._2931 import MountableComponentCompoundSystemDeflection
    from ._2932 import OilSealCompoundSystemDeflection
    from ._2933 import PartCompoundSystemDeflection
    from ._2934 import PartToPartShearCouplingCompoundSystemDeflection
    from ._2935 import PartToPartShearCouplingConnectionCompoundSystemDeflection
    from ._2936 import PartToPartShearCouplingHalfCompoundSystemDeflection
    from ._2937 import PlanetaryConnectionCompoundSystemDeflection
    from ._2938 import PlanetaryGearSetCompoundSystemDeflection
    from ._2939 import PlanetCarrierCompoundSystemDeflection
    from ._2940 import PointLoadCompoundSystemDeflection
    from ._2941 import PowerLoadCompoundSystemDeflection
    from ._2942 import PulleyCompoundSystemDeflection
    from ._2943 import RingPinsCompoundSystemDeflection
    from ._2944 import RingPinsToDiscConnectionCompoundSystemDeflection
    from ._2945 import RollingRingAssemblyCompoundSystemDeflection
    from ._2946 import RollingRingCompoundSystemDeflection
    from ._2947 import RollingRingConnectionCompoundSystemDeflection
    from ._2948 import RootAssemblyCompoundSystemDeflection
    from ._2949 import ShaftCompoundSystemDeflection
    from ._2950 import ShaftDutyCycleSystemDeflection
    from ._2951 import ShaftHubConnectionCompoundSystemDeflection
    from ._2952 import ShaftToMountableComponentConnectionCompoundSystemDeflection
    from ._2953 import SpecialisedAssemblyCompoundSystemDeflection
    from ._2954 import SpiralBevelGearCompoundSystemDeflection
    from ._2955 import SpiralBevelGearMeshCompoundSystemDeflection
    from ._2956 import SpiralBevelGearSetCompoundSystemDeflection
    from ._2957 import SpringDamperCompoundSystemDeflection
    from ._2958 import SpringDamperConnectionCompoundSystemDeflection
    from ._2959 import SpringDamperHalfCompoundSystemDeflection
    from ._2960 import StraightBevelDiffGearCompoundSystemDeflection
    from ._2961 import StraightBevelDiffGearMeshCompoundSystemDeflection
    from ._2962 import StraightBevelDiffGearSetCompoundSystemDeflection
    from ._2963 import StraightBevelGearCompoundSystemDeflection
    from ._2964 import StraightBevelGearMeshCompoundSystemDeflection
    from ._2965 import StraightBevelGearSetCompoundSystemDeflection
    from ._2966 import StraightBevelPlanetGearCompoundSystemDeflection
    from ._2967 import StraightBevelSunGearCompoundSystemDeflection
    from ._2968 import SynchroniserCompoundSystemDeflection
    from ._2969 import SynchroniserHalfCompoundSystemDeflection
    from ._2970 import SynchroniserPartCompoundSystemDeflection
    from ._2971 import SynchroniserSleeveCompoundSystemDeflection
    from ._2972 import TorqueConverterCompoundSystemDeflection
    from ._2973 import TorqueConverterConnectionCompoundSystemDeflection
    from ._2974 import TorqueConverterPumpCompoundSystemDeflection
    from ._2975 import TorqueConverterTurbineCompoundSystemDeflection
    from ._2976 import UnbalancedMassCompoundSystemDeflection
    from ._2977 import VirtualComponentCompoundSystemDeflection
    from ._2978 import WormGearCompoundSystemDeflection
    from ._2979 import WormGearMeshCompoundSystemDeflection
    from ._2980 import WormGearSetCompoundSystemDeflection
    from ._2981 import ZerolBevelGearCompoundSystemDeflection
    from ._2982 import ZerolBevelGearMeshCompoundSystemDeflection
    from ._2983 import ZerolBevelGearSetCompoundSystemDeflection
else:
    import_structure = {
        "_2853": ["AbstractAssemblyCompoundSystemDeflection"],
        "_2854": ["AbstractShaftCompoundSystemDeflection"],
        "_2855": ["AbstractShaftOrHousingCompoundSystemDeflection"],
        "_2856": [
            "AbstractShaftToMountableComponentConnectionCompoundSystemDeflection"
        ],
        "_2857": ["AGMAGleasonConicalGearCompoundSystemDeflection"],
        "_2858": ["AGMAGleasonConicalGearMeshCompoundSystemDeflection"],
        "_2859": ["AGMAGleasonConicalGearSetCompoundSystemDeflection"],
        "_2860": ["AssemblyCompoundSystemDeflection"],
        "_2861": ["BearingCompoundSystemDeflection"],
        "_2862": ["BeltConnectionCompoundSystemDeflection"],
        "_2863": ["BeltDriveCompoundSystemDeflection"],
        "_2864": ["BevelDifferentialGearCompoundSystemDeflection"],
        "_2865": ["BevelDifferentialGearMeshCompoundSystemDeflection"],
        "_2866": ["BevelDifferentialGearSetCompoundSystemDeflection"],
        "_2867": ["BevelDifferentialPlanetGearCompoundSystemDeflection"],
        "_2868": ["BevelDifferentialSunGearCompoundSystemDeflection"],
        "_2869": ["BevelGearCompoundSystemDeflection"],
        "_2870": ["BevelGearMeshCompoundSystemDeflection"],
        "_2871": ["BevelGearSetCompoundSystemDeflection"],
        "_2872": ["BoltCompoundSystemDeflection"],
        "_2873": ["BoltedJointCompoundSystemDeflection"],
        "_2874": ["ClutchCompoundSystemDeflection"],
        "_2875": ["ClutchConnectionCompoundSystemDeflection"],
        "_2876": ["ClutchHalfCompoundSystemDeflection"],
        "_2877": ["CoaxialConnectionCompoundSystemDeflection"],
        "_2878": ["ComponentCompoundSystemDeflection"],
        "_2879": ["ConceptCouplingCompoundSystemDeflection"],
        "_2880": ["ConceptCouplingConnectionCompoundSystemDeflection"],
        "_2881": ["ConceptCouplingHalfCompoundSystemDeflection"],
        "_2882": ["ConceptGearCompoundSystemDeflection"],
        "_2883": ["ConceptGearMeshCompoundSystemDeflection"],
        "_2884": ["ConceptGearSetCompoundSystemDeflection"],
        "_2885": ["ConicalGearCompoundSystemDeflection"],
        "_2886": ["ConicalGearMeshCompoundSystemDeflection"],
        "_2887": ["ConicalGearSetCompoundSystemDeflection"],
        "_2888": ["ConnectionCompoundSystemDeflection"],
        "_2889": ["ConnectorCompoundSystemDeflection"],
        "_2890": ["CouplingCompoundSystemDeflection"],
        "_2891": ["CouplingConnectionCompoundSystemDeflection"],
        "_2892": ["CouplingHalfCompoundSystemDeflection"],
        "_2893": ["CVTBeltConnectionCompoundSystemDeflection"],
        "_2894": ["CVTCompoundSystemDeflection"],
        "_2895": ["CVTPulleyCompoundSystemDeflection"],
        "_2896": ["CycloidalAssemblyCompoundSystemDeflection"],
        "_2897": ["CycloidalDiscCentralBearingConnectionCompoundSystemDeflection"],
        "_2898": ["CycloidalDiscCompoundSystemDeflection"],
        "_2899": ["CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection"],
        "_2900": ["CylindricalGearCompoundSystemDeflection"],
        "_2901": ["CylindricalGearMeshCompoundSystemDeflection"],
        "_2902": ["CylindricalGearSetCompoundSystemDeflection"],
        "_2903": ["CylindricalPlanetGearCompoundSystemDeflection"],
        "_2904": ["DatumCompoundSystemDeflection"],
        "_2905": ["DutyCycleEfficiencyResults"],
        "_2906": ["ExternalCADModelCompoundSystemDeflection"],
        "_2907": ["FaceGearCompoundSystemDeflection"],
        "_2908": ["FaceGearMeshCompoundSystemDeflection"],
        "_2909": ["FaceGearSetCompoundSystemDeflection"],
        "_2910": ["FEPartCompoundSystemDeflection"],
        "_2911": ["FlexiblePinAssemblyCompoundSystemDeflection"],
        "_2912": ["GearCompoundSystemDeflection"],
        "_2913": ["GearMeshCompoundSystemDeflection"],
        "_2914": ["GearSetCompoundSystemDeflection"],
        "_2915": ["GuideDxfModelCompoundSystemDeflection"],
        "_2916": ["HypoidGearCompoundSystemDeflection"],
        "_2917": ["HypoidGearMeshCompoundSystemDeflection"],
        "_2918": ["HypoidGearSetCompoundSystemDeflection"],
        "_2919": ["InterMountableComponentConnectionCompoundSystemDeflection"],
        "_2920": ["KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection"],
        "_2921": ["KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection"],
        "_2922": ["KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection"],
        "_2923": ["KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection"],
        "_2924": ["KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection"],
        "_2925": ["KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection"],
        "_2926": ["KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection"],
        "_2927": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection"
        ],
        "_2928": ["KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection"],
        "_2929": ["MassDiscCompoundSystemDeflection"],
        "_2930": ["MeasurementComponentCompoundSystemDeflection"],
        "_2931": ["MountableComponentCompoundSystemDeflection"],
        "_2932": ["OilSealCompoundSystemDeflection"],
        "_2933": ["PartCompoundSystemDeflection"],
        "_2934": ["PartToPartShearCouplingCompoundSystemDeflection"],
        "_2935": ["PartToPartShearCouplingConnectionCompoundSystemDeflection"],
        "_2936": ["PartToPartShearCouplingHalfCompoundSystemDeflection"],
        "_2937": ["PlanetaryConnectionCompoundSystemDeflection"],
        "_2938": ["PlanetaryGearSetCompoundSystemDeflection"],
        "_2939": ["PlanetCarrierCompoundSystemDeflection"],
        "_2940": ["PointLoadCompoundSystemDeflection"],
        "_2941": ["PowerLoadCompoundSystemDeflection"],
        "_2942": ["PulleyCompoundSystemDeflection"],
        "_2943": ["RingPinsCompoundSystemDeflection"],
        "_2944": ["RingPinsToDiscConnectionCompoundSystemDeflection"],
        "_2945": ["RollingRingAssemblyCompoundSystemDeflection"],
        "_2946": ["RollingRingCompoundSystemDeflection"],
        "_2947": ["RollingRingConnectionCompoundSystemDeflection"],
        "_2948": ["RootAssemblyCompoundSystemDeflection"],
        "_2949": ["ShaftCompoundSystemDeflection"],
        "_2950": ["ShaftDutyCycleSystemDeflection"],
        "_2951": ["ShaftHubConnectionCompoundSystemDeflection"],
        "_2952": ["ShaftToMountableComponentConnectionCompoundSystemDeflection"],
        "_2953": ["SpecialisedAssemblyCompoundSystemDeflection"],
        "_2954": ["SpiralBevelGearCompoundSystemDeflection"],
        "_2955": ["SpiralBevelGearMeshCompoundSystemDeflection"],
        "_2956": ["SpiralBevelGearSetCompoundSystemDeflection"],
        "_2957": ["SpringDamperCompoundSystemDeflection"],
        "_2958": ["SpringDamperConnectionCompoundSystemDeflection"],
        "_2959": ["SpringDamperHalfCompoundSystemDeflection"],
        "_2960": ["StraightBevelDiffGearCompoundSystemDeflection"],
        "_2961": ["StraightBevelDiffGearMeshCompoundSystemDeflection"],
        "_2962": ["StraightBevelDiffGearSetCompoundSystemDeflection"],
        "_2963": ["StraightBevelGearCompoundSystemDeflection"],
        "_2964": ["StraightBevelGearMeshCompoundSystemDeflection"],
        "_2965": ["StraightBevelGearSetCompoundSystemDeflection"],
        "_2966": ["StraightBevelPlanetGearCompoundSystemDeflection"],
        "_2967": ["StraightBevelSunGearCompoundSystemDeflection"],
        "_2968": ["SynchroniserCompoundSystemDeflection"],
        "_2969": ["SynchroniserHalfCompoundSystemDeflection"],
        "_2970": ["SynchroniserPartCompoundSystemDeflection"],
        "_2971": ["SynchroniserSleeveCompoundSystemDeflection"],
        "_2972": ["TorqueConverterCompoundSystemDeflection"],
        "_2973": ["TorqueConverterConnectionCompoundSystemDeflection"],
        "_2974": ["TorqueConverterPumpCompoundSystemDeflection"],
        "_2975": ["TorqueConverterTurbineCompoundSystemDeflection"],
        "_2976": ["UnbalancedMassCompoundSystemDeflection"],
        "_2977": ["VirtualComponentCompoundSystemDeflection"],
        "_2978": ["WormGearCompoundSystemDeflection"],
        "_2979": ["WormGearMeshCompoundSystemDeflection"],
        "_2980": ["WormGearSetCompoundSystemDeflection"],
        "_2981": ["ZerolBevelGearCompoundSystemDeflection"],
        "_2982": ["ZerolBevelGearMeshCompoundSystemDeflection"],
        "_2983": ["ZerolBevelGearSetCompoundSystemDeflection"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundSystemDeflection",
    "AbstractShaftCompoundSystemDeflection",
    "AbstractShaftOrHousingCompoundSystemDeflection",
    "AbstractShaftToMountableComponentConnectionCompoundSystemDeflection",
    "AGMAGleasonConicalGearCompoundSystemDeflection",
    "AGMAGleasonConicalGearMeshCompoundSystemDeflection",
    "AGMAGleasonConicalGearSetCompoundSystemDeflection",
    "AssemblyCompoundSystemDeflection",
    "BearingCompoundSystemDeflection",
    "BeltConnectionCompoundSystemDeflection",
    "BeltDriveCompoundSystemDeflection",
    "BevelDifferentialGearCompoundSystemDeflection",
    "BevelDifferentialGearMeshCompoundSystemDeflection",
    "BevelDifferentialGearSetCompoundSystemDeflection",
    "BevelDifferentialPlanetGearCompoundSystemDeflection",
    "BevelDifferentialSunGearCompoundSystemDeflection",
    "BevelGearCompoundSystemDeflection",
    "BevelGearMeshCompoundSystemDeflection",
    "BevelGearSetCompoundSystemDeflection",
    "BoltCompoundSystemDeflection",
    "BoltedJointCompoundSystemDeflection",
    "ClutchCompoundSystemDeflection",
    "ClutchConnectionCompoundSystemDeflection",
    "ClutchHalfCompoundSystemDeflection",
    "CoaxialConnectionCompoundSystemDeflection",
    "ComponentCompoundSystemDeflection",
    "ConceptCouplingCompoundSystemDeflection",
    "ConceptCouplingConnectionCompoundSystemDeflection",
    "ConceptCouplingHalfCompoundSystemDeflection",
    "ConceptGearCompoundSystemDeflection",
    "ConceptGearMeshCompoundSystemDeflection",
    "ConceptGearSetCompoundSystemDeflection",
    "ConicalGearCompoundSystemDeflection",
    "ConicalGearMeshCompoundSystemDeflection",
    "ConicalGearSetCompoundSystemDeflection",
    "ConnectionCompoundSystemDeflection",
    "ConnectorCompoundSystemDeflection",
    "CouplingCompoundSystemDeflection",
    "CouplingConnectionCompoundSystemDeflection",
    "CouplingHalfCompoundSystemDeflection",
    "CVTBeltConnectionCompoundSystemDeflection",
    "CVTCompoundSystemDeflection",
    "CVTPulleyCompoundSystemDeflection",
    "CycloidalAssemblyCompoundSystemDeflection",
    "CycloidalDiscCentralBearingConnectionCompoundSystemDeflection",
    "CycloidalDiscCompoundSystemDeflection",
    "CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection",
    "CylindricalGearCompoundSystemDeflection",
    "CylindricalGearMeshCompoundSystemDeflection",
    "CylindricalGearSetCompoundSystemDeflection",
    "CylindricalPlanetGearCompoundSystemDeflection",
    "DatumCompoundSystemDeflection",
    "DutyCycleEfficiencyResults",
    "ExternalCADModelCompoundSystemDeflection",
    "FaceGearCompoundSystemDeflection",
    "FaceGearMeshCompoundSystemDeflection",
    "FaceGearSetCompoundSystemDeflection",
    "FEPartCompoundSystemDeflection",
    "FlexiblePinAssemblyCompoundSystemDeflection",
    "GearCompoundSystemDeflection",
    "GearMeshCompoundSystemDeflection",
    "GearSetCompoundSystemDeflection",
    "GuideDxfModelCompoundSystemDeflection",
    "HypoidGearCompoundSystemDeflection",
    "HypoidGearMeshCompoundSystemDeflection",
    "HypoidGearSetCompoundSystemDeflection",
    "InterMountableComponentConnectionCompoundSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection",
    "KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection",
    "MassDiscCompoundSystemDeflection",
    "MeasurementComponentCompoundSystemDeflection",
    "MountableComponentCompoundSystemDeflection",
    "OilSealCompoundSystemDeflection",
    "PartCompoundSystemDeflection",
    "PartToPartShearCouplingCompoundSystemDeflection",
    "PartToPartShearCouplingConnectionCompoundSystemDeflection",
    "PartToPartShearCouplingHalfCompoundSystemDeflection",
    "PlanetaryConnectionCompoundSystemDeflection",
    "PlanetaryGearSetCompoundSystemDeflection",
    "PlanetCarrierCompoundSystemDeflection",
    "PointLoadCompoundSystemDeflection",
    "PowerLoadCompoundSystemDeflection",
    "PulleyCompoundSystemDeflection",
    "RingPinsCompoundSystemDeflection",
    "RingPinsToDiscConnectionCompoundSystemDeflection",
    "RollingRingAssemblyCompoundSystemDeflection",
    "RollingRingCompoundSystemDeflection",
    "RollingRingConnectionCompoundSystemDeflection",
    "RootAssemblyCompoundSystemDeflection",
    "ShaftCompoundSystemDeflection",
    "ShaftDutyCycleSystemDeflection",
    "ShaftHubConnectionCompoundSystemDeflection",
    "ShaftToMountableComponentConnectionCompoundSystemDeflection",
    "SpecialisedAssemblyCompoundSystemDeflection",
    "SpiralBevelGearCompoundSystemDeflection",
    "SpiralBevelGearMeshCompoundSystemDeflection",
    "SpiralBevelGearSetCompoundSystemDeflection",
    "SpringDamperCompoundSystemDeflection",
    "SpringDamperConnectionCompoundSystemDeflection",
    "SpringDamperHalfCompoundSystemDeflection",
    "StraightBevelDiffGearCompoundSystemDeflection",
    "StraightBevelDiffGearMeshCompoundSystemDeflection",
    "StraightBevelDiffGearSetCompoundSystemDeflection",
    "StraightBevelGearCompoundSystemDeflection",
    "StraightBevelGearMeshCompoundSystemDeflection",
    "StraightBevelGearSetCompoundSystemDeflection",
    "StraightBevelPlanetGearCompoundSystemDeflection",
    "StraightBevelSunGearCompoundSystemDeflection",
    "SynchroniserCompoundSystemDeflection",
    "SynchroniserHalfCompoundSystemDeflection",
    "SynchroniserPartCompoundSystemDeflection",
    "SynchroniserSleeveCompoundSystemDeflection",
    "TorqueConverterCompoundSystemDeflection",
    "TorqueConverterConnectionCompoundSystemDeflection",
    "TorqueConverterPumpCompoundSystemDeflection",
    "TorqueConverterTurbineCompoundSystemDeflection",
    "UnbalancedMassCompoundSystemDeflection",
    "VirtualComponentCompoundSystemDeflection",
    "WormGearCompoundSystemDeflection",
    "WormGearMeshCompoundSystemDeflection",
    "WormGearSetCompoundSystemDeflection",
    "ZerolBevelGearCompoundSystemDeflection",
    "ZerolBevelGearMeshCompoundSystemDeflection",
    "ZerolBevelGearSetCompoundSystemDeflection",
)
