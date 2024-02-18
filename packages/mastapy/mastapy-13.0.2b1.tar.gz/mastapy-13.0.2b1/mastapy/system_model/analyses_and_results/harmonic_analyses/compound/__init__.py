"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5881 import AbstractAssemblyCompoundHarmonicAnalysis
    from ._5882 import AbstractShaftCompoundHarmonicAnalysis
    from ._5883 import AbstractShaftOrHousingCompoundHarmonicAnalysis
    from ._5884 import (
        AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis,
    )
    from ._5885 import AGMAGleasonConicalGearCompoundHarmonicAnalysis
    from ._5886 import AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis
    from ._5887 import AGMAGleasonConicalGearSetCompoundHarmonicAnalysis
    from ._5888 import AssemblyCompoundHarmonicAnalysis
    from ._5889 import BearingCompoundHarmonicAnalysis
    from ._5890 import BeltConnectionCompoundHarmonicAnalysis
    from ._5891 import BeltDriveCompoundHarmonicAnalysis
    from ._5892 import BevelDifferentialGearCompoundHarmonicAnalysis
    from ._5893 import BevelDifferentialGearMeshCompoundHarmonicAnalysis
    from ._5894 import BevelDifferentialGearSetCompoundHarmonicAnalysis
    from ._5895 import BevelDifferentialPlanetGearCompoundHarmonicAnalysis
    from ._5896 import BevelDifferentialSunGearCompoundHarmonicAnalysis
    from ._5897 import BevelGearCompoundHarmonicAnalysis
    from ._5898 import BevelGearMeshCompoundHarmonicAnalysis
    from ._5899 import BevelGearSetCompoundHarmonicAnalysis
    from ._5900 import BoltCompoundHarmonicAnalysis
    from ._5901 import BoltedJointCompoundHarmonicAnalysis
    from ._5902 import ClutchCompoundHarmonicAnalysis
    from ._5903 import ClutchConnectionCompoundHarmonicAnalysis
    from ._5904 import ClutchHalfCompoundHarmonicAnalysis
    from ._5905 import CoaxialConnectionCompoundHarmonicAnalysis
    from ._5906 import ComponentCompoundHarmonicAnalysis
    from ._5907 import ConceptCouplingCompoundHarmonicAnalysis
    from ._5908 import ConceptCouplingConnectionCompoundHarmonicAnalysis
    from ._5909 import ConceptCouplingHalfCompoundHarmonicAnalysis
    from ._5910 import ConceptGearCompoundHarmonicAnalysis
    from ._5911 import ConceptGearMeshCompoundHarmonicAnalysis
    from ._5912 import ConceptGearSetCompoundHarmonicAnalysis
    from ._5913 import ConicalGearCompoundHarmonicAnalysis
    from ._5914 import ConicalGearMeshCompoundHarmonicAnalysis
    from ._5915 import ConicalGearSetCompoundHarmonicAnalysis
    from ._5916 import ConnectionCompoundHarmonicAnalysis
    from ._5917 import ConnectorCompoundHarmonicAnalysis
    from ._5918 import CouplingCompoundHarmonicAnalysis
    from ._5919 import CouplingConnectionCompoundHarmonicAnalysis
    from ._5920 import CouplingHalfCompoundHarmonicAnalysis
    from ._5921 import CVTBeltConnectionCompoundHarmonicAnalysis
    from ._5922 import CVTCompoundHarmonicAnalysis
    from ._5923 import CVTPulleyCompoundHarmonicAnalysis
    from ._5924 import CycloidalAssemblyCompoundHarmonicAnalysis
    from ._5925 import CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis
    from ._5926 import CycloidalDiscCompoundHarmonicAnalysis
    from ._5927 import CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis
    from ._5928 import CylindricalGearCompoundHarmonicAnalysis
    from ._5929 import CylindricalGearMeshCompoundHarmonicAnalysis
    from ._5930 import CylindricalGearSetCompoundHarmonicAnalysis
    from ._5931 import CylindricalPlanetGearCompoundHarmonicAnalysis
    from ._5932 import DatumCompoundHarmonicAnalysis
    from ._5933 import ExternalCADModelCompoundHarmonicAnalysis
    from ._5934 import FaceGearCompoundHarmonicAnalysis
    from ._5935 import FaceGearMeshCompoundHarmonicAnalysis
    from ._5936 import FaceGearSetCompoundHarmonicAnalysis
    from ._5937 import FEPartCompoundHarmonicAnalysis
    from ._5938 import FlexiblePinAssemblyCompoundHarmonicAnalysis
    from ._5939 import GearCompoundHarmonicAnalysis
    from ._5940 import GearMeshCompoundHarmonicAnalysis
    from ._5941 import GearSetCompoundHarmonicAnalysis
    from ._5942 import GuideDxfModelCompoundHarmonicAnalysis
    from ._5943 import HypoidGearCompoundHarmonicAnalysis
    from ._5944 import HypoidGearMeshCompoundHarmonicAnalysis
    from ._5945 import HypoidGearSetCompoundHarmonicAnalysis
    from ._5946 import InterMountableComponentConnectionCompoundHarmonicAnalysis
    from ._5947 import KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis
    from ._5948 import KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis
    from ._5949 import KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis
    from ._5950 import KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis
    from ._5951 import KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis
    from ._5952 import KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis
    from ._5953 import KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis
    from ._5954 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis,
    )
    from ._5955 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis,
    )
    from ._5956 import MassDiscCompoundHarmonicAnalysis
    from ._5957 import MeasurementComponentCompoundHarmonicAnalysis
    from ._5958 import MountableComponentCompoundHarmonicAnalysis
    from ._5959 import OilSealCompoundHarmonicAnalysis
    from ._5960 import PartCompoundHarmonicAnalysis
    from ._5961 import PartToPartShearCouplingCompoundHarmonicAnalysis
    from ._5962 import PartToPartShearCouplingConnectionCompoundHarmonicAnalysis
    from ._5963 import PartToPartShearCouplingHalfCompoundHarmonicAnalysis
    from ._5964 import PlanetaryConnectionCompoundHarmonicAnalysis
    from ._5965 import PlanetaryGearSetCompoundHarmonicAnalysis
    from ._5966 import PlanetCarrierCompoundHarmonicAnalysis
    from ._5967 import PointLoadCompoundHarmonicAnalysis
    from ._5968 import PowerLoadCompoundHarmonicAnalysis
    from ._5969 import PulleyCompoundHarmonicAnalysis
    from ._5970 import RingPinsCompoundHarmonicAnalysis
    from ._5971 import RingPinsToDiscConnectionCompoundHarmonicAnalysis
    from ._5972 import RollingRingAssemblyCompoundHarmonicAnalysis
    from ._5973 import RollingRingCompoundHarmonicAnalysis
    from ._5974 import RollingRingConnectionCompoundHarmonicAnalysis
    from ._5975 import RootAssemblyCompoundHarmonicAnalysis
    from ._5976 import ShaftCompoundHarmonicAnalysis
    from ._5977 import ShaftHubConnectionCompoundHarmonicAnalysis
    from ._5978 import ShaftToMountableComponentConnectionCompoundHarmonicAnalysis
    from ._5979 import SpecialisedAssemblyCompoundHarmonicAnalysis
    from ._5980 import SpiralBevelGearCompoundHarmonicAnalysis
    from ._5981 import SpiralBevelGearMeshCompoundHarmonicAnalysis
    from ._5982 import SpiralBevelGearSetCompoundHarmonicAnalysis
    from ._5983 import SpringDamperCompoundHarmonicAnalysis
    from ._5984 import SpringDamperConnectionCompoundHarmonicAnalysis
    from ._5985 import SpringDamperHalfCompoundHarmonicAnalysis
    from ._5986 import StraightBevelDiffGearCompoundHarmonicAnalysis
    from ._5987 import StraightBevelDiffGearMeshCompoundHarmonicAnalysis
    from ._5988 import StraightBevelDiffGearSetCompoundHarmonicAnalysis
    from ._5989 import StraightBevelGearCompoundHarmonicAnalysis
    from ._5990 import StraightBevelGearMeshCompoundHarmonicAnalysis
    from ._5991 import StraightBevelGearSetCompoundHarmonicAnalysis
    from ._5992 import StraightBevelPlanetGearCompoundHarmonicAnalysis
    from ._5993 import StraightBevelSunGearCompoundHarmonicAnalysis
    from ._5994 import SynchroniserCompoundHarmonicAnalysis
    from ._5995 import SynchroniserHalfCompoundHarmonicAnalysis
    from ._5996 import SynchroniserPartCompoundHarmonicAnalysis
    from ._5997 import SynchroniserSleeveCompoundHarmonicAnalysis
    from ._5998 import TorqueConverterCompoundHarmonicAnalysis
    from ._5999 import TorqueConverterConnectionCompoundHarmonicAnalysis
    from ._6000 import TorqueConverterPumpCompoundHarmonicAnalysis
    from ._6001 import TorqueConverterTurbineCompoundHarmonicAnalysis
    from ._6002 import UnbalancedMassCompoundHarmonicAnalysis
    from ._6003 import VirtualComponentCompoundHarmonicAnalysis
    from ._6004 import WormGearCompoundHarmonicAnalysis
    from ._6005 import WormGearMeshCompoundHarmonicAnalysis
    from ._6006 import WormGearSetCompoundHarmonicAnalysis
    from ._6007 import ZerolBevelGearCompoundHarmonicAnalysis
    from ._6008 import ZerolBevelGearMeshCompoundHarmonicAnalysis
    from ._6009 import ZerolBevelGearSetCompoundHarmonicAnalysis
else:
    import_structure = {
        "_5881": ["AbstractAssemblyCompoundHarmonicAnalysis"],
        "_5882": ["AbstractShaftCompoundHarmonicAnalysis"],
        "_5883": ["AbstractShaftOrHousingCompoundHarmonicAnalysis"],
        "_5884": [
            "AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis"
        ],
        "_5885": ["AGMAGleasonConicalGearCompoundHarmonicAnalysis"],
        "_5886": ["AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis"],
        "_5887": ["AGMAGleasonConicalGearSetCompoundHarmonicAnalysis"],
        "_5888": ["AssemblyCompoundHarmonicAnalysis"],
        "_5889": ["BearingCompoundHarmonicAnalysis"],
        "_5890": ["BeltConnectionCompoundHarmonicAnalysis"],
        "_5891": ["BeltDriveCompoundHarmonicAnalysis"],
        "_5892": ["BevelDifferentialGearCompoundHarmonicAnalysis"],
        "_5893": ["BevelDifferentialGearMeshCompoundHarmonicAnalysis"],
        "_5894": ["BevelDifferentialGearSetCompoundHarmonicAnalysis"],
        "_5895": ["BevelDifferentialPlanetGearCompoundHarmonicAnalysis"],
        "_5896": ["BevelDifferentialSunGearCompoundHarmonicAnalysis"],
        "_5897": ["BevelGearCompoundHarmonicAnalysis"],
        "_5898": ["BevelGearMeshCompoundHarmonicAnalysis"],
        "_5899": ["BevelGearSetCompoundHarmonicAnalysis"],
        "_5900": ["BoltCompoundHarmonicAnalysis"],
        "_5901": ["BoltedJointCompoundHarmonicAnalysis"],
        "_5902": ["ClutchCompoundHarmonicAnalysis"],
        "_5903": ["ClutchConnectionCompoundHarmonicAnalysis"],
        "_5904": ["ClutchHalfCompoundHarmonicAnalysis"],
        "_5905": ["CoaxialConnectionCompoundHarmonicAnalysis"],
        "_5906": ["ComponentCompoundHarmonicAnalysis"],
        "_5907": ["ConceptCouplingCompoundHarmonicAnalysis"],
        "_5908": ["ConceptCouplingConnectionCompoundHarmonicAnalysis"],
        "_5909": ["ConceptCouplingHalfCompoundHarmonicAnalysis"],
        "_5910": ["ConceptGearCompoundHarmonicAnalysis"],
        "_5911": ["ConceptGearMeshCompoundHarmonicAnalysis"],
        "_5912": ["ConceptGearSetCompoundHarmonicAnalysis"],
        "_5913": ["ConicalGearCompoundHarmonicAnalysis"],
        "_5914": ["ConicalGearMeshCompoundHarmonicAnalysis"],
        "_5915": ["ConicalGearSetCompoundHarmonicAnalysis"],
        "_5916": ["ConnectionCompoundHarmonicAnalysis"],
        "_5917": ["ConnectorCompoundHarmonicAnalysis"],
        "_5918": ["CouplingCompoundHarmonicAnalysis"],
        "_5919": ["CouplingConnectionCompoundHarmonicAnalysis"],
        "_5920": ["CouplingHalfCompoundHarmonicAnalysis"],
        "_5921": ["CVTBeltConnectionCompoundHarmonicAnalysis"],
        "_5922": ["CVTCompoundHarmonicAnalysis"],
        "_5923": ["CVTPulleyCompoundHarmonicAnalysis"],
        "_5924": ["CycloidalAssemblyCompoundHarmonicAnalysis"],
        "_5925": ["CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis"],
        "_5926": ["CycloidalDiscCompoundHarmonicAnalysis"],
        "_5927": ["CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis"],
        "_5928": ["CylindricalGearCompoundHarmonicAnalysis"],
        "_5929": ["CylindricalGearMeshCompoundHarmonicAnalysis"],
        "_5930": ["CylindricalGearSetCompoundHarmonicAnalysis"],
        "_5931": ["CylindricalPlanetGearCompoundHarmonicAnalysis"],
        "_5932": ["DatumCompoundHarmonicAnalysis"],
        "_5933": ["ExternalCADModelCompoundHarmonicAnalysis"],
        "_5934": ["FaceGearCompoundHarmonicAnalysis"],
        "_5935": ["FaceGearMeshCompoundHarmonicAnalysis"],
        "_5936": ["FaceGearSetCompoundHarmonicAnalysis"],
        "_5937": ["FEPartCompoundHarmonicAnalysis"],
        "_5938": ["FlexiblePinAssemblyCompoundHarmonicAnalysis"],
        "_5939": ["GearCompoundHarmonicAnalysis"],
        "_5940": ["GearMeshCompoundHarmonicAnalysis"],
        "_5941": ["GearSetCompoundHarmonicAnalysis"],
        "_5942": ["GuideDxfModelCompoundHarmonicAnalysis"],
        "_5943": ["HypoidGearCompoundHarmonicAnalysis"],
        "_5944": ["HypoidGearMeshCompoundHarmonicAnalysis"],
        "_5945": ["HypoidGearSetCompoundHarmonicAnalysis"],
        "_5946": ["InterMountableComponentConnectionCompoundHarmonicAnalysis"],
        "_5947": ["KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis"],
        "_5948": ["KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis"],
        "_5949": ["KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis"],
        "_5950": ["KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis"],
        "_5951": ["KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis"],
        "_5952": ["KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis"],
        "_5953": ["KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis"],
        "_5954": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis"
        ],
        "_5955": ["KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis"],
        "_5956": ["MassDiscCompoundHarmonicAnalysis"],
        "_5957": ["MeasurementComponentCompoundHarmonicAnalysis"],
        "_5958": ["MountableComponentCompoundHarmonicAnalysis"],
        "_5959": ["OilSealCompoundHarmonicAnalysis"],
        "_5960": ["PartCompoundHarmonicAnalysis"],
        "_5961": ["PartToPartShearCouplingCompoundHarmonicAnalysis"],
        "_5962": ["PartToPartShearCouplingConnectionCompoundHarmonicAnalysis"],
        "_5963": ["PartToPartShearCouplingHalfCompoundHarmonicAnalysis"],
        "_5964": ["PlanetaryConnectionCompoundHarmonicAnalysis"],
        "_5965": ["PlanetaryGearSetCompoundHarmonicAnalysis"],
        "_5966": ["PlanetCarrierCompoundHarmonicAnalysis"],
        "_5967": ["PointLoadCompoundHarmonicAnalysis"],
        "_5968": ["PowerLoadCompoundHarmonicAnalysis"],
        "_5969": ["PulleyCompoundHarmonicAnalysis"],
        "_5970": ["RingPinsCompoundHarmonicAnalysis"],
        "_5971": ["RingPinsToDiscConnectionCompoundHarmonicAnalysis"],
        "_5972": ["RollingRingAssemblyCompoundHarmonicAnalysis"],
        "_5973": ["RollingRingCompoundHarmonicAnalysis"],
        "_5974": ["RollingRingConnectionCompoundHarmonicAnalysis"],
        "_5975": ["RootAssemblyCompoundHarmonicAnalysis"],
        "_5976": ["ShaftCompoundHarmonicAnalysis"],
        "_5977": ["ShaftHubConnectionCompoundHarmonicAnalysis"],
        "_5978": ["ShaftToMountableComponentConnectionCompoundHarmonicAnalysis"],
        "_5979": ["SpecialisedAssemblyCompoundHarmonicAnalysis"],
        "_5980": ["SpiralBevelGearCompoundHarmonicAnalysis"],
        "_5981": ["SpiralBevelGearMeshCompoundHarmonicAnalysis"],
        "_5982": ["SpiralBevelGearSetCompoundHarmonicAnalysis"],
        "_5983": ["SpringDamperCompoundHarmonicAnalysis"],
        "_5984": ["SpringDamperConnectionCompoundHarmonicAnalysis"],
        "_5985": ["SpringDamperHalfCompoundHarmonicAnalysis"],
        "_5986": ["StraightBevelDiffGearCompoundHarmonicAnalysis"],
        "_5987": ["StraightBevelDiffGearMeshCompoundHarmonicAnalysis"],
        "_5988": ["StraightBevelDiffGearSetCompoundHarmonicAnalysis"],
        "_5989": ["StraightBevelGearCompoundHarmonicAnalysis"],
        "_5990": ["StraightBevelGearMeshCompoundHarmonicAnalysis"],
        "_5991": ["StraightBevelGearSetCompoundHarmonicAnalysis"],
        "_5992": ["StraightBevelPlanetGearCompoundHarmonicAnalysis"],
        "_5993": ["StraightBevelSunGearCompoundHarmonicAnalysis"],
        "_5994": ["SynchroniserCompoundHarmonicAnalysis"],
        "_5995": ["SynchroniserHalfCompoundHarmonicAnalysis"],
        "_5996": ["SynchroniserPartCompoundHarmonicAnalysis"],
        "_5997": ["SynchroniserSleeveCompoundHarmonicAnalysis"],
        "_5998": ["TorqueConverterCompoundHarmonicAnalysis"],
        "_5999": ["TorqueConverterConnectionCompoundHarmonicAnalysis"],
        "_6000": ["TorqueConverterPumpCompoundHarmonicAnalysis"],
        "_6001": ["TorqueConverterTurbineCompoundHarmonicAnalysis"],
        "_6002": ["UnbalancedMassCompoundHarmonicAnalysis"],
        "_6003": ["VirtualComponentCompoundHarmonicAnalysis"],
        "_6004": ["WormGearCompoundHarmonicAnalysis"],
        "_6005": ["WormGearMeshCompoundHarmonicAnalysis"],
        "_6006": ["WormGearSetCompoundHarmonicAnalysis"],
        "_6007": ["ZerolBevelGearCompoundHarmonicAnalysis"],
        "_6008": ["ZerolBevelGearMeshCompoundHarmonicAnalysis"],
        "_6009": ["ZerolBevelGearSetCompoundHarmonicAnalysis"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundHarmonicAnalysis",
    "AbstractShaftCompoundHarmonicAnalysis",
    "AbstractShaftOrHousingCompoundHarmonicAnalysis",
    "AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis",
    "AGMAGleasonConicalGearCompoundHarmonicAnalysis",
    "AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis",
    "AGMAGleasonConicalGearSetCompoundHarmonicAnalysis",
    "AssemblyCompoundHarmonicAnalysis",
    "BearingCompoundHarmonicAnalysis",
    "BeltConnectionCompoundHarmonicAnalysis",
    "BeltDriveCompoundHarmonicAnalysis",
    "BevelDifferentialGearCompoundHarmonicAnalysis",
    "BevelDifferentialGearMeshCompoundHarmonicAnalysis",
    "BevelDifferentialGearSetCompoundHarmonicAnalysis",
    "BevelDifferentialPlanetGearCompoundHarmonicAnalysis",
    "BevelDifferentialSunGearCompoundHarmonicAnalysis",
    "BevelGearCompoundHarmonicAnalysis",
    "BevelGearMeshCompoundHarmonicAnalysis",
    "BevelGearSetCompoundHarmonicAnalysis",
    "BoltCompoundHarmonicAnalysis",
    "BoltedJointCompoundHarmonicAnalysis",
    "ClutchCompoundHarmonicAnalysis",
    "ClutchConnectionCompoundHarmonicAnalysis",
    "ClutchHalfCompoundHarmonicAnalysis",
    "CoaxialConnectionCompoundHarmonicAnalysis",
    "ComponentCompoundHarmonicAnalysis",
    "ConceptCouplingCompoundHarmonicAnalysis",
    "ConceptCouplingConnectionCompoundHarmonicAnalysis",
    "ConceptCouplingHalfCompoundHarmonicAnalysis",
    "ConceptGearCompoundHarmonicAnalysis",
    "ConceptGearMeshCompoundHarmonicAnalysis",
    "ConceptGearSetCompoundHarmonicAnalysis",
    "ConicalGearCompoundHarmonicAnalysis",
    "ConicalGearMeshCompoundHarmonicAnalysis",
    "ConicalGearSetCompoundHarmonicAnalysis",
    "ConnectionCompoundHarmonicAnalysis",
    "ConnectorCompoundHarmonicAnalysis",
    "CouplingCompoundHarmonicAnalysis",
    "CouplingConnectionCompoundHarmonicAnalysis",
    "CouplingHalfCompoundHarmonicAnalysis",
    "CVTBeltConnectionCompoundHarmonicAnalysis",
    "CVTCompoundHarmonicAnalysis",
    "CVTPulleyCompoundHarmonicAnalysis",
    "CycloidalAssemblyCompoundHarmonicAnalysis",
    "CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis",
    "CycloidalDiscCompoundHarmonicAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis",
    "CylindricalGearCompoundHarmonicAnalysis",
    "CylindricalGearMeshCompoundHarmonicAnalysis",
    "CylindricalGearSetCompoundHarmonicAnalysis",
    "CylindricalPlanetGearCompoundHarmonicAnalysis",
    "DatumCompoundHarmonicAnalysis",
    "ExternalCADModelCompoundHarmonicAnalysis",
    "FaceGearCompoundHarmonicAnalysis",
    "FaceGearMeshCompoundHarmonicAnalysis",
    "FaceGearSetCompoundHarmonicAnalysis",
    "FEPartCompoundHarmonicAnalysis",
    "FlexiblePinAssemblyCompoundHarmonicAnalysis",
    "GearCompoundHarmonicAnalysis",
    "GearMeshCompoundHarmonicAnalysis",
    "GearSetCompoundHarmonicAnalysis",
    "GuideDxfModelCompoundHarmonicAnalysis",
    "HypoidGearCompoundHarmonicAnalysis",
    "HypoidGearMeshCompoundHarmonicAnalysis",
    "HypoidGearSetCompoundHarmonicAnalysis",
    "InterMountableComponentConnectionCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis",
    "MassDiscCompoundHarmonicAnalysis",
    "MeasurementComponentCompoundHarmonicAnalysis",
    "MountableComponentCompoundHarmonicAnalysis",
    "OilSealCompoundHarmonicAnalysis",
    "PartCompoundHarmonicAnalysis",
    "PartToPartShearCouplingCompoundHarmonicAnalysis",
    "PartToPartShearCouplingConnectionCompoundHarmonicAnalysis",
    "PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
    "PlanetaryConnectionCompoundHarmonicAnalysis",
    "PlanetaryGearSetCompoundHarmonicAnalysis",
    "PlanetCarrierCompoundHarmonicAnalysis",
    "PointLoadCompoundHarmonicAnalysis",
    "PowerLoadCompoundHarmonicAnalysis",
    "PulleyCompoundHarmonicAnalysis",
    "RingPinsCompoundHarmonicAnalysis",
    "RingPinsToDiscConnectionCompoundHarmonicAnalysis",
    "RollingRingAssemblyCompoundHarmonicAnalysis",
    "RollingRingCompoundHarmonicAnalysis",
    "RollingRingConnectionCompoundHarmonicAnalysis",
    "RootAssemblyCompoundHarmonicAnalysis",
    "ShaftCompoundHarmonicAnalysis",
    "ShaftHubConnectionCompoundHarmonicAnalysis",
    "ShaftToMountableComponentConnectionCompoundHarmonicAnalysis",
    "SpecialisedAssemblyCompoundHarmonicAnalysis",
    "SpiralBevelGearCompoundHarmonicAnalysis",
    "SpiralBevelGearMeshCompoundHarmonicAnalysis",
    "SpiralBevelGearSetCompoundHarmonicAnalysis",
    "SpringDamperCompoundHarmonicAnalysis",
    "SpringDamperConnectionCompoundHarmonicAnalysis",
    "SpringDamperHalfCompoundHarmonicAnalysis",
    "StraightBevelDiffGearCompoundHarmonicAnalysis",
    "StraightBevelDiffGearMeshCompoundHarmonicAnalysis",
    "StraightBevelDiffGearSetCompoundHarmonicAnalysis",
    "StraightBevelGearCompoundHarmonicAnalysis",
    "StraightBevelGearMeshCompoundHarmonicAnalysis",
    "StraightBevelGearSetCompoundHarmonicAnalysis",
    "StraightBevelPlanetGearCompoundHarmonicAnalysis",
    "StraightBevelSunGearCompoundHarmonicAnalysis",
    "SynchroniserCompoundHarmonicAnalysis",
    "SynchroniserHalfCompoundHarmonicAnalysis",
    "SynchroniserPartCompoundHarmonicAnalysis",
    "SynchroniserSleeveCompoundHarmonicAnalysis",
    "TorqueConverterCompoundHarmonicAnalysis",
    "TorqueConverterConnectionCompoundHarmonicAnalysis",
    "TorqueConverterPumpCompoundHarmonicAnalysis",
    "TorqueConverterTurbineCompoundHarmonicAnalysis",
    "UnbalancedMassCompoundHarmonicAnalysis",
    "VirtualComponentCompoundHarmonicAnalysis",
    "WormGearCompoundHarmonicAnalysis",
    "WormGearMeshCompoundHarmonicAnalysis",
    "WormGearSetCompoundHarmonicAnalysis",
    "ZerolBevelGearCompoundHarmonicAnalysis",
    "ZerolBevelGearMeshCompoundHarmonicAnalysis",
    "ZerolBevelGearSetCompoundHarmonicAnalysis",
)
