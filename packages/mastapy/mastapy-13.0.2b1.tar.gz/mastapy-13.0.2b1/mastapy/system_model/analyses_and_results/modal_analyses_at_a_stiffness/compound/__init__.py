"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._4990 import AbstractAssemblyCompoundModalAnalysisAtAStiffness
    from ._4991 import AbstractShaftCompoundModalAnalysisAtAStiffness
    from ._4992 import AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness
    from ._4993 import (
        AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness,
    )
    from ._4994 import AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness
    from ._4995 import AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness
    from ._4996 import AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness
    from ._4997 import AssemblyCompoundModalAnalysisAtAStiffness
    from ._4998 import BearingCompoundModalAnalysisAtAStiffness
    from ._4999 import BeltConnectionCompoundModalAnalysisAtAStiffness
    from ._5000 import BeltDriveCompoundModalAnalysisAtAStiffness
    from ._5001 import BevelDifferentialGearCompoundModalAnalysisAtAStiffness
    from ._5002 import BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness
    from ._5003 import BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness
    from ._5004 import BevelDifferentialPlanetGearCompoundModalAnalysisAtAStiffness
    from ._5005 import BevelDifferentialSunGearCompoundModalAnalysisAtAStiffness
    from ._5006 import BevelGearCompoundModalAnalysisAtAStiffness
    from ._5007 import BevelGearMeshCompoundModalAnalysisAtAStiffness
    from ._5008 import BevelGearSetCompoundModalAnalysisAtAStiffness
    from ._5009 import BoltCompoundModalAnalysisAtAStiffness
    from ._5010 import BoltedJointCompoundModalAnalysisAtAStiffness
    from ._5011 import ClutchCompoundModalAnalysisAtAStiffness
    from ._5012 import ClutchConnectionCompoundModalAnalysisAtAStiffness
    from ._5013 import ClutchHalfCompoundModalAnalysisAtAStiffness
    from ._5014 import CoaxialConnectionCompoundModalAnalysisAtAStiffness
    from ._5015 import ComponentCompoundModalAnalysisAtAStiffness
    from ._5016 import ConceptCouplingCompoundModalAnalysisAtAStiffness
    from ._5017 import ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness
    from ._5018 import ConceptCouplingHalfCompoundModalAnalysisAtAStiffness
    from ._5019 import ConceptGearCompoundModalAnalysisAtAStiffness
    from ._5020 import ConceptGearMeshCompoundModalAnalysisAtAStiffness
    from ._5021 import ConceptGearSetCompoundModalAnalysisAtAStiffness
    from ._5022 import ConicalGearCompoundModalAnalysisAtAStiffness
    from ._5023 import ConicalGearMeshCompoundModalAnalysisAtAStiffness
    from ._5024 import ConicalGearSetCompoundModalAnalysisAtAStiffness
    from ._5025 import ConnectionCompoundModalAnalysisAtAStiffness
    from ._5026 import ConnectorCompoundModalAnalysisAtAStiffness
    from ._5027 import CouplingCompoundModalAnalysisAtAStiffness
    from ._5028 import CouplingConnectionCompoundModalAnalysisAtAStiffness
    from ._5029 import CouplingHalfCompoundModalAnalysisAtAStiffness
    from ._5030 import CVTBeltConnectionCompoundModalAnalysisAtAStiffness
    from ._5031 import CVTCompoundModalAnalysisAtAStiffness
    from ._5032 import CVTPulleyCompoundModalAnalysisAtAStiffness
    from ._5033 import CycloidalAssemblyCompoundModalAnalysisAtAStiffness
    from ._5034 import (
        CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness,
    )
    from ._5035 import CycloidalDiscCompoundModalAnalysisAtAStiffness
    from ._5036 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness,
    )
    from ._5037 import CylindricalGearCompoundModalAnalysisAtAStiffness
    from ._5038 import CylindricalGearMeshCompoundModalAnalysisAtAStiffness
    from ._5039 import CylindricalGearSetCompoundModalAnalysisAtAStiffness
    from ._5040 import CylindricalPlanetGearCompoundModalAnalysisAtAStiffness
    from ._5041 import DatumCompoundModalAnalysisAtAStiffness
    from ._5042 import ExternalCADModelCompoundModalAnalysisAtAStiffness
    from ._5043 import FaceGearCompoundModalAnalysisAtAStiffness
    from ._5044 import FaceGearMeshCompoundModalAnalysisAtAStiffness
    from ._5045 import FaceGearSetCompoundModalAnalysisAtAStiffness
    from ._5046 import FEPartCompoundModalAnalysisAtAStiffness
    from ._5047 import FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness
    from ._5048 import GearCompoundModalAnalysisAtAStiffness
    from ._5049 import GearMeshCompoundModalAnalysisAtAStiffness
    from ._5050 import GearSetCompoundModalAnalysisAtAStiffness
    from ._5051 import GuideDxfModelCompoundModalAnalysisAtAStiffness
    from ._5052 import HypoidGearCompoundModalAnalysisAtAStiffness
    from ._5053 import HypoidGearMeshCompoundModalAnalysisAtAStiffness
    from ._5054 import HypoidGearSetCompoundModalAnalysisAtAStiffness
    from ._5055 import (
        InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness,
    )
    from ._5056 import (
        KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtAStiffness,
    )
    from ._5057 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness,
    )
    from ._5058 import (
        KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness,
    )
    from ._5059 import (
        KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtAStiffness,
    )
    from ._5060 import (
        KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness,
    )
    from ._5061 import (
        KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness,
    )
    from ._5062 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtAStiffness,
    )
    from ._5063 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness,
    )
    from ._5064 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness,
    )
    from ._5065 import MassDiscCompoundModalAnalysisAtAStiffness
    from ._5066 import MeasurementComponentCompoundModalAnalysisAtAStiffness
    from ._5067 import MountableComponentCompoundModalAnalysisAtAStiffness
    from ._5068 import OilSealCompoundModalAnalysisAtAStiffness
    from ._5069 import PartCompoundModalAnalysisAtAStiffness
    from ._5070 import PartToPartShearCouplingCompoundModalAnalysisAtAStiffness
    from ._5071 import (
        PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness,
    )
    from ._5072 import PartToPartShearCouplingHalfCompoundModalAnalysisAtAStiffness
    from ._5073 import PlanetaryConnectionCompoundModalAnalysisAtAStiffness
    from ._5074 import PlanetaryGearSetCompoundModalAnalysisAtAStiffness
    from ._5075 import PlanetCarrierCompoundModalAnalysisAtAStiffness
    from ._5076 import PointLoadCompoundModalAnalysisAtAStiffness
    from ._5077 import PowerLoadCompoundModalAnalysisAtAStiffness
    from ._5078 import PulleyCompoundModalAnalysisAtAStiffness
    from ._5079 import RingPinsCompoundModalAnalysisAtAStiffness
    from ._5080 import RingPinsToDiscConnectionCompoundModalAnalysisAtAStiffness
    from ._5081 import RollingRingAssemblyCompoundModalAnalysisAtAStiffness
    from ._5082 import RollingRingCompoundModalAnalysisAtAStiffness
    from ._5083 import RollingRingConnectionCompoundModalAnalysisAtAStiffness
    from ._5084 import RootAssemblyCompoundModalAnalysisAtAStiffness
    from ._5085 import ShaftCompoundModalAnalysisAtAStiffness
    from ._5086 import ShaftHubConnectionCompoundModalAnalysisAtAStiffness
    from ._5087 import (
        ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness,
    )
    from ._5088 import SpecialisedAssemblyCompoundModalAnalysisAtAStiffness
    from ._5089 import SpiralBevelGearCompoundModalAnalysisAtAStiffness
    from ._5090 import SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness
    from ._5091 import SpiralBevelGearSetCompoundModalAnalysisAtAStiffness
    from ._5092 import SpringDamperCompoundModalAnalysisAtAStiffness
    from ._5093 import SpringDamperConnectionCompoundModalAnalysisAtAStiffness
    from ._5094 import SpringDamperHalfCompoundModalAnalysisAtAStiffness
    from ._5095 import StraightBevelDiffGearCompoundModalAnalysisAtAStiffness
    from ._5096 import StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness
    from ._5097 import StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness
    from ._5098 import StraightBevelGearCompoundModalAnalysisAtAStiffness
    from ._5099 import StraightBevelGearMeshCompoundModalAnalysisAtAStiffness
    from ._5100 import StraightBevelGearSetCompoundModalAnalysisAtAStiffness
    from ._5101 import StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness
    from ._5102 import StraightBevelSunGearCompoundModalAnalysisAtAStiffness
    from ._5103 import SynchroniserCompoundModalAnalysisAtAStiffness
    from ._5104 import SynchroniserHalfCompoundModalAnalysisAtAStiffness
    from ._5105 import SynchroniserPartCompoundModalAnalysisAtAStiffness
    from ._5106 import SynchroniserSleeveCompoundModalAnalysisAtAStiffness
    from ._5107 import TorqueConverterCompoundModalAnalysisAtAStiffness
    from ._5108 import TorqueConverterConnectionCompoundModalAnalysisAtAStiffness
    from ._5109 import TorqueConverterPumpCompoundModalAnalysisAtAStiffness
    from ._5110 import TorqueConverterTurbineCompoundModalAnalysisAtAStiffness
    from ._5111 import UnbalancedMassCompoundModalAnalysisAtAStiffness
    from ._5112 import VirtualComponentCompoundModalAnalysisAtAStiffness
    from ._5113 import WormGearCompoundModalAnalysisAtAStiffness
    from ._5114 import WormGearMeshCompoundModalAnalysisAtAStiffness
    from ._5115 import WormGearSetCompoundModalAnalysisAtAStiffness
    from ._5116 import ZerolBevelGearCompoundModalAnalysisAtAStiffness
    from ._5117 import ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness
    from ._5118 import ZerolBevelGearSetCompoundModalAnalysisAtAStiffness
else:
    import_structure = {
        "_4990": ["AbstractAssemblyCompoundModalAnalysisAtAStiffness"],
        "_4991": ["AbstractShaftCompoundModalAnalysisAtAStiffness"],
        "_4992": ["AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness"],
        "_4993": [
            "AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness"
        ],
        "_4994": ["AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness"],
        "_4995": ["AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness"],
        "_4996": ["AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness"],
        "_4997": ["AssemblyCompoundModalAnalysisAtAStiffness"],
        "_4998": ["BearingCompoundModalAnalysisAtAStiffness"],
        "_4999": ["BeltConnectionCompoundModalAnalysisAtAStiffness"],
        "_5000": ["BeltDriveCompoundModalAnalysisAtAStiffness"],
        "_5001": ["BevelDifferentialGearCompoundModalAnalysisAtAStiffness"],
        "_5002": ["BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5003": ["BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness"],
        "_5004": ["BevelDifferentialPlanetGearCompoundModalAnalysisAtAStiffness"],
        "_5005": ["BevelDifferentialSunGearCompoundModalAnalysisAtAStiffness"],
        "_5006": ["BevelGearCompoundModalAnalysisAtAStiffness"],
        "_5007": ["BevelGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5008": ["BevelGearSetCompoundModalAnalysisAtAStiffness"],
        "_5009": ["BoltCompoundModalAnalysisAtAStiffness"],
        "_5010": ["BoltedJointCompoundModalAnalysisAtAStiffness"],
        "_5011": ["ClutchCompoundModalAnalysisAtAStiffness"],
        "_5012": ["ClutchConnectionCompoundModalAnalysisAtAStiffness"],
        "_5013": ["ClutchHalfCompoundModalAnalysisAtAStiffness"],
        "_5014": ["CoaxialConnectionCompoundModalAnalysisAtAStiffness"],
        "_5015": ["ComponentCompoundModalAnalysisAtAStiffness"],
        "_5016": ["ConceptCouplingCompoundModalAnalysisAtAStiffness"],
        "_5017": ["ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness"],
        "_5018": ["ConceptCouplingHalfCompoundModalAnalysisAtAStiffness"],
        "_5019": ["ConceptGearCompoundModalAnalysisAtAStiffness"],
        "_5020": ["ConceptGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5021": ["ConceptGearSetCompoundModalAnalysisAtAStiffness"],
        "_5022": ["ConicalGearCompoundModalAnalysisAtAStiffness"],
        "_5023": ["ConicalGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5024": ["ConicalGearSetCompoundModalAnalysisAtAStiffness"],
        "_5025": ["ConnectionCompoundModalAnalysisAtAStiffness"],
        "_5026": ["ConnectorCompoundModalAnalysisAtAStiffness"],
        "_5027": ["CouplingCompoundModalAnalysisAtAStiffness"],
        "_5028": ["CouplingConnectionCompoundModalAnalysisAtAStiffness"],
        "_5029": ["CouplingHalfCompoundModalAnalysisAtAStiffness"],
        "_5030": ["CVTBeltConnectionCompoundModalAnalysisAtAStiffness"],
        "_5031": ["CVTCompoundModalAnalysisAtAStiffness"],
        "_5032": ["CVTPulleyCompoundModalAnalysisAtAStiffness"],
        "_5033": ["CycloidalAssemblyCompoundModalAnalysisAtAStiffness"],
        "_5034": [
            "CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness"
        ],
        "_5035": ["CycloidalDiscCompoundModalAnalysisAtAStiffness"],
        "_5036": [
            "CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness"
        ],
        "_5037": ["CylindricalGearCompoundModalAnalysisAtAStiffness"],
        "_5038": ["CylindricalGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5039": ["CylindricalGearSetCompoundModalAnalysisAtAStiffness"],
        "_5040": ["CylindricalPlanetGearCompoundModalAnalysisAtAStiffness"],
        "_5041": ["DatumCompoundModalAnalysisAtAStiffness"],
        "_5042": ["ExternalCADModelCompoundModalAnalysisAtAStiffness"],
        "_5043": ["FaceGearCompoundModalAnalysisAtAStiffness"],
        "_5044": ["FaceGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5045": ["FaceGearSetCompoundModalAnalysisAtAStiffness"],
        "_5046": ["FEPartCompoundModalAnalysisAtAStiffness"],
        "_5047": ["FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness"],
        "_5048": ["GearCompoundModalAnalysisAtAStiffness"],
        "_5049": ["GearMeshCompoundModalAnalysisAtAStiffness"],
        "_5050": ["GearSetCompoundModalAnalysisAtAStiffness"],
        "_5051": ["GuideDxfModelCompoundModalAnalysisAtAStiffness"],
        "_5052": ["HypoidGearCompoundModalAnalysisAtAStiffness"],
        "_5053": ["HypoidGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5054": ["HypoidGearSetCompoundModalAnalysisAtAStiffness"],
        "_5055": ["InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness"],
        "_5056": [
            "KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtAStiffness"
        ],
        "_5057": [
            "KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness"
        ],
        "_5058": [
            "KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness"
        ],
        "_5059": [
            "KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtAStiffness"
        ],
        "_5060": [
            "KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness"
        ],
        "_5061": [
            "KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness"
        ],
        "_5062": [
            "KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtAStiffness"
        ],
        "_5063": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness"
        ],
        "_5064": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness"
        ],
        "_5065": ["MassDiscCompoundModalAnalysisAtAStiffness"],
        "_5066": ["MeasurementComponentCompoundModalAnalysisAtAStiffness"],
        "_5067": ["MountableComponentCompoundModalAnalysisAtAStiffness"],
        "_5068": ["OilSealCompoundModalAnalysisAtAStiffness"],
        "_5069": ["PartCompoundModalAnalysisAtAStiffness"],
        "_5070": ["PartToPartShearCouplingCompoundModalAnalysisAtAStiffness"],
        "_5071": ["PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness"],
        "_5072": ["PartToPartShearCouplingHalfCompoundModalAnalysisAtAStiffness"],
        "_5073": ["PlanetaryConnectionCompoundModalAnalysisAtAStiffness"],
        "_5074": ["PlanetaryGearSetCompoundModalAnalysisAtAStiffness"],
        "_5075": ["PlanetCarrierCompoundModalAnalysisAtAStiffness"],
        "_5076": ["PointLoadCompoundModalAnalysisAtAStiffness"],
        "_5077": ["PowerLoadCompoundModalAnalysisAtAStiffness"],
        "_5078": ["PulleyCompoundModalAnalysisAtAStiffness"],
        "_5079": ["RingPinsCompoundModalAnalysisAtAStiffness"],
        "_5080": ["RingPinsToDiscConnectionCompoundModalAnalysisAtAStiffness"],
        "_5081": ["RollingRingAssemblyCompoundModalAnalysisAtAStiffness"],
        "_5082": ["RollingRingCompoundModalAnalysisAtAStiffness"],
        "_5083": ["RollingRingConnectionCompoundModalAnalysisAtAStiffness"],
        "_5084": ["RootAssemblyCompoundModalAnalysisAtAStiffness"],
        "_5085": ["ShaftCompoundModalAnalysisAtAStiffness"],
        "_5086": ["ShaftHubConnectionCompoundModalAnalysisAtAStiffness"],
        "_5087": [
            "ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness"
        ],
        "_5088": ["SpecialisedAssemblyCompoundModalAnalysisAtAStiffness"],
        "_5089": ["SpiralBevelGearCompoundModalAnalysisAtAStiffness"],
        "_5090": ["SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5091": ["SpiralBevelGearSetCompoundModalAnalysisAtAStiffness"],
        "_5092": ["SpringDamperCompoundModalAnalysisAtAStiffness"],
        "_5093": ["SpringDamperConnectionCompoundModalAnalysisAtAStiffness"],
        "_5094": ["SpringDamperHalfCompoundModalAnalysisAtAStiffness"],
        "_5095": ["StraightBevelDiffGearCompoundModalAnalysisAtAStiffness"],
        "_5096": ["StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5097": ["StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness"],
        "_5098": ["StraightBevelGearCompoundModalAnalysisAtAStiffness"],
        "_5099": ["StraightBevelGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5100": ["StraightBevelGearSetCompoundModalAnalysisAtAStiffness"],
        "_5101": ["StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness"],
        "_5102": ["StraightBevelSunGearCompoundModalAnalysisAtAStiffness"],
        "_5103": ["SynchroniserCompoundModalAnalysisAtAStiffness"],
        "_5104": ["SynchroniserHalfCompoundModalAnalysisAtAStiffness"],
        "_5105": ["SynchroniserPartCompoundModalAnalysisAtAStiffness"],
        "_5106": ["SynchroniserSleeveCompoundModalAnalysisAtAStiffness"],
        "_5107": ["TorqueConverterCompoundModalAnalysisAtAStiffness"],
        "_5108": ["TorqueConverterConnectionCompoundModalAnalysisAtAStiffness"],
        "_5109": ["TorqueConverterPumpCompoundModalAnalysisAtAStiffness"],
        "_5110": ["TorqueConverterTurbineCompoundModalAnalysisAtAStiffness"],
        "_5111": ["UnbalancedMassCompoundModalAnalysisAtAStiffness"],
        "_5112": ["VirtualComponentCompoundModalAnalysisAtAStiffness"],
        "_5113": ["WormGearCompoundModalAnalysisAtAStiffness"],
        "_5114": ["WormGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5115": ["WormGearSetCompoundModalAnalysisAtAStiffness"],
        "_5116": ["ZerolBevelGearCompoundModalAnalysisAtAStiffness"],
        "_5117": ["ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness"],
        "_5118": ["ZerolBevelGearSetCompoundModalAnalysisAtAStiffness"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundModalAnalysisAtAStiffness",
    "AbstractShaftCompoundModalAnalysisAtAStiffness",
    "AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness",
    "AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness",
    "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
    "AGMAGleasonConicalGearMeshCompoundModalAnalysisAtAStiffness",
    "AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness",
    "AssemblyCompoundModalAnalysisAtAStiffness",
    "BearingCompoundModalAnalysisAtAStiffness",
    "BeltConnectionCompoundModalAnalysisAtAStiffness",
    "BeltDriveCompoundModalAnalysisAtAStiffness",
    "BevelDifferentialGearCompoundModalAnalysisAtAStiffness",
    "BevelDifferentialGearMeshCompoundModalAnalysisAtAStiffness",
    "BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness",
    "BevelDifferentialPlanetGearCompoundModalAnalysisAtAStiffness",
    "BevelDifferentialSunGearCompoundModalAnalysisAtAStiffness",
    "BevelGearCompoundModalAnalysisAtAStiffness",
    "BevelGearMeshCompoundModalAnalysisAtAStiffness",
    "BevelGearSetCompoundModalAnalysisAtAStiffness",
    "BoltCompoundModalAnalysisAtAStiffness",
    "BoltedJointCompoundModalAnalysisAtAStiffness",
    "ClutchCompoundModalAnalysisAtAStiffness",
    "ClutchConnectionCompoundModalAnalysisAtAStiffness",
    "ClutchHalfCompoundModalAnalysisAtAStiffness",
    "CoaxialConnectionCompoundModalAnalysisAtAStiffness",
    "ComponentCompoundModalAnalysisAtAStiffness",
    "ConceptCouplingCompoundModalAnalysisAtAStiffness",
    "ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness",
    "ConceptCouplingHalfCompoundModalAnalysisAtAStiffness",
    "ConceptGearCompoundModalAnalysisAtAStiffness",
    "ConceptGearMeshCompoundModalAnalysisAtAStiffness",
    "ConceptGearSetCompoundModalAnalysisAtAStiffness",
    "ConicalGearCompoundModalAnalysisAtAStiffness",
    "ConicalGearMeshCompoundModalAnalysisAtAStiffness",
    "ConicalGearSetCompoundModalAnalysisAtAStiffness",
    "ConnectionCompoundModalAnalysisAtAStiffness",
    "ConnectorCompoundModalAnalysisAtAStiffness",
    "CouplingCompoundModalAnalysisAtAStiffness",
    "CouplingConnectionCompoundModalAnalysisAtAStiffness",
    "CouplingHalfCompoundModalAnalysisAtAStiffness",
    "CVTBeltConnectionCompoundModalAnalysisAtAStiffness",
    "CVTCompoundModalAnalysisAtAStiffness",
    "CVTPulleyCompoundModalAnalysisAtAStiffness",
    "CycloidalAssemblyCompoundModalAnalysisAtAStiffness",
    "CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtAStiffness",
    "CycloidalDiscCompoundModalAnalysisAtAStiffness",
    "CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness",
    "CylindricalGearCompoundModalAnalysisAtAStiffness",
    "CylindricalGearMeshCompoundModalAnalysisAtAStiffness",
    "CylindricalGearSetCompoundModalAnalysisAtAStiffness",
    "CylindricalPlanetGearCompoundModalAnalysisAtAStiffness",
    "DatumCompoundModalAnalysisAtAStiffness",
    "ExternalCADModelCompoundModalAnalysisAtAStiffness",
    "FaceGearCompoundModalAnalysisAtAStiffness",
    "FaceGearMeshCompoundModalAnalysisAtAStiffness",
    "FaceGearSetCompoundModalAnalysisAtAStiffness",
    "FEPartCompoundModalAnalysisAtAStiffness",
    "FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness",
    "GearCompoundModalAnalysisAtAStiffness",
    "GearMeshCompoundModalAnalysisAtAStiffness",
    "GearSetCompoundModalAnalysisAtAStiffness",
    "GuideDxfModelCompoundModalAnalysisAtAStiffness",
    "HypoidGearCompoundModalAnalysisAtAStiffness",
    "HypoidGearMeshCompoundModalAnalysisAtAStiffness",
    "HypoidGearSetCompoundModalAnalysisAtAStiffness",
    "InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness",
    "MassDiscCompoundModalAnalysisAtAStiffness",
    "MeasurementComponentCompoundModalAnalysisAtAStiffness",
    "MountableComponentCompoundModalAnalysisAtAStiffness",
    "OilSealCompoundModalAnalysisAtAStiffness",
    "PartCompoundModalAnalysisAtAStiffness",
    "PartToPartShearCouplingCompoundModalAnalysisAtAStiffness",
    "PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness",
    "PartToPartShearCouplingHalfCompoundModalAnalysisAtAStiffness",
    "PlanetaryConnectionCompoundModalAnalysisAtAStiffness",
    "PlanetaryGearSetCompoundModalAnalysisAtAStiffness",
    "PlanetCarrierCompoundModalAnalysisAtAStiffness",
    "PointLoadCompoundModalAnalysisAtAStiffness",
    "PowerLoadCompoundModalAnalysisAtAStiffness",
    "PulleyCompoundModalAnalysisAtAStiffness",
    "RingPinsCompoundModalAnalysisAtAStiffness",
    "RingPinsToDiscConnectionCompoundModalAnalysisAtAStiffness",
    "RollingRingAssemblyCompoundModalAnalysisAtAStiffness",
    "RollingRingCompoundModalAnalysisAtAStiffness",
    "RollingRingConnectionCompoundModalAnalysisAtAStiffness",
    "RootAssemblyCompoundModalAnalysisAtAStiffness",
    "ShaftCompoundModalAnalysisAtAStiffness",
    "ShaftHubConnectionCompoundModalAnalysisAtAStiffness",
    "ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness",
    "SpecialisedAssemblyCompoundModalAnalysisAtAStiffness",
    "SpiralBevelGearCompoundModalAnalysisAtAStiffness",
    "SpiralBevelGearMeshCompoundModalAnalysisAtAStiffness",
    "SpiralBevelGearSetCompoundModalAnalysisAtAStiffness",
    "SpringDamperCompoundModalAnalysisAtAStiffness",
    "SpringDamperConnectionCompoundModalAnalysisAtAStiffness",
    "SpringDamperHalfCompoundModalAnalysisAtAStiffness",
    "StraightBevelDiffGearCompoundModalAnalysisAtAStiffness",
    "StraightBevelDiffGearMeshCompoundModalAnalysisAtAStiffness",
    "StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness",
    "StraightBevelGearCompoundModalAnalysisAtAStiffness",
    "StraightBevelGearMeshCompoundModalAnalysisAtAStiffness",
    "StraightBevelGearSetCompoundModalAnalysisAtAStiffness",
    "StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness",
    "StraightBevelSunGearCompoundModalAnalysisAtAStiffness",
    "SynchroniserCompoundModalAnalysisAtAStiffness",
    "SynchroniserHalfCompoundModalAnalysisAtAStiffness",
    "SynchroniserPartCompoundModalAnalysisAtAStiffness",
    "SynchroniserSleeveCompoundModalAnalysisAtAStiffness",
    "TorqueConverterCompoundModalAnalysisAtAStiffness",
    "TorqueConverterConnectionCompoundModalAnalysisAtAStiffness",
    "TorqueConverterPumpCompoundModalAnalysisAtAStiffness",
    "TorqueConverterTurbineCompoundModalAnalysisAtAStiffness",
    "UnbalancedMassCompoundModalAnalysisAtAStiffness",
    "VirtualComponentCompoundModalAnalysisAtAStiffness",
    "WormGearCompoundModalAnalysisAtAStiffness",
    "WormGearMeshCompoundModalAnalysisAtAStiffness",
    "WormGearSetCompoundModalAnalysisAtAStiffness",
    "ZerolBevelGearCompoundModalAnalysisAtAStiffness",
    "ZerolBevelGearMeshCompoundModalAnalysisAtAStiffness",
    "ZerolBevelGearSetCompoundModalAnalysisAtAStiffness",
)
