"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._7008 import AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation
    from ._7009 import AbstractShaftAdvancedTimeSteppingAnalysisForModulation
    from ._7010 import AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation
    from ._7011 import (
        AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7012 import AdvancedTimeSteppingAnalysisForModulation
    from ._7013 import AtsamExcitationsOrOthers
    from ._7014 import AtsamNaturalFrequencyViewOption
    from ._7015 import AdvancedTimeSteppingAnalysisForModulationOptions
    from ._7016 import AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation
    from ._7017 import (
        AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7018 import (
        AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7019 import AssemblyAdvancedTimeSteppingAnalysisForModulation
    from ._7020 import ATSAMResultsVsLargeTimeStepSettings
    from ._7021 import BearingAdvancedTimeSteppingAnalysisForModulation
    from ._7022 import BeltConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7023 import BeltDriveAdvancedTimeSteppingAnalysisForModulation
    from ._7024 import BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation
    from ._7025 import (
        BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7026 import BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7027 import (
        BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7028 import BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation
    from ._7029 import BevelGearAdvancedTimeSteppingAnalysisForModulation
    from ._7030 import BevelGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7031 import BevelGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7032 import BoltAdvancedTimeSteppingAnalysisForModulation
    from ._7033 import BoltedJointAdvancedTimeSteppingAnalysisForModulation
    from ._7034 import ClutchAdvancedTimeSteppingAnalysisForModulation
    from ._7035 import ClutchConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7036 import ClutchHalfAdvancedTimeSteppingAnalysisForModulation
    from ._7037 import CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7038 import ComponentAdvancedTimeSteppingAnalysisForModulation
    from ._7039 import ConceptCouplingAdvancedTimeSteppingAnalysisForModulation
    from ._7040 import (
        ConceptCouplingConnectionAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7041 import ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation
    from ._7042 import ConceptGearAdvancedTimeSteppingAnalysisForModulation
    from ._7043 import ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7044 import ConceptGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7045 import ConicalGearAdvancedTimeSteppingAnalysisForModulation
    from ._7046 import ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7047 import ConicalGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7048 import ConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7049 import ConnectorAdvancedTimeSteppingAnalysisForModulation
    from ._7050 import CouplingAdvancedTimeSteppingAnalysisForModulation
    from ._7051 import CouplingConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7052 import CouplingHalfAdvancedTimeSteppingAnalysisForModulation
    from ._7053 import CVTAdvancedTimeSteppingAnalysisForModulation
    from ._7054 import CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7055 import CVTPulleyAdvancedTimeSteppingAnalysisForModulation
    from ._7056 import CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation
    from ._7057 import CycloidalDiscAdvancedTimeSteppingAnalysisForModulation
    from ._7058 import (
        CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7059 import (
        CycloidalDiscPlanetaryBearingConnectionAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7060 import CylindricalGearAdvancedTimeSteppingAnalysisForModulation
    from ._7061 import CylindricalGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7062 import CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7063 import CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation
    from ._7064 import DatumAdvancedTimeSteppingAnalysisForModulation
    from ._7065 import ExternalCADModelAdvancedTimeSteppingAnalysisForModulation
    from ._7066 import FaceGearAdvancedTimeSteppingAnalysisForModulation
    from ._7067 import FaceGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7068 import FaceGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7069 import FEPartAdvancedTimeSteppingAnalysisForModulation
    from ._7070 import FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation
    from ._7071 import GearAdvancedTimeSteppingAnalysisForModulation
    from ._7072 import GearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7073 import GearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7074 import GuideDxfModelAdvancedTimeSteppingAnalysisForModulation
    from ._7075 import (
        HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7076 import HypoidGearAdvancedTimeSteppingAnalysisForModulation
    from ._7077 import HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7078 import HypoidGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7079 import (
        InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7080 import (
        KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7081 import (
        KlingelnbergCycloPalloidConicalGearMeshAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7082 import (
        KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7083 import (
        KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7084 import (
        KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7085 import (
        KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7086 import (
        KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7087 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7088 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7089 import MassDiscAdvancedTimeSteppingAnalysisForModulation
    from ._7090 import MeasurementComponentAdvancedTimeSteppingAnalysisForModulation
    from ._7091 import MountableComponentAdvancedTimeSteppingAnalysisForModulation
    from ._7092 import OilSealAdvancedTimeSteppingAnalysisForModulation
    from ._7093 import PartAdvancedTimeSteppingAnalysisForModulation
    from ._7094 import PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation
    from ._7095 import (
        PartToPartShearCouplingConnectionAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7096 import (
        PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7097 import PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7098 import PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7099 import PlanetCarrierAdvancedTimeSteppingAnalysisForModulation
    from ._7100 import PointLoadAdvancedTimeSteppingAnalysisForModulation
    from ._7101 import PowerLoadAdvancedTimeSteppingAnalysisForModulation
    from ._7102 import PulleyAdvancedTimeSteppingAnalysisForModulation
    from ._7103 import RingPinsAdvancedTimeSteppingAnalysisForModulation
    from ._7104 import RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7105 import RollingRingAdvancedTimeSteppingAnalysisForModulation
    from ._7106 import RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation
    from ._7107 import RollingRingConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7108 import RootAssemblyAdvancedTimeSteppingAnalysisForModulation
    from ._7109 import ShaftAdvancedTimeSteppingAnalysisForModulation
    from ._7110 import ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7111 import (
        ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7112 import SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
    from ._7113 import SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
    from ._7114 import SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7115 import SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7116 import SpringDamperAdvancedTimeSteppingAnalysisForModulation
    from ._7117 import SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation
    from ._7118 import SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation
    from ._7119 import StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation
    from ._7120 import (
        StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7121 import StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7122 import StraightBevelGearAdvancedTimeSteppingAnalysisForModulation
    from ._7123 import StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7124 import StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7125 import StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation
    from ._7126 import StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation
    from ._7127 import SynchroniserAdvancedTimeSteppingAnalysisForModulation
    from ._7128 import SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation
    from ._7129 import SynchroniserPartAdvancedTimeSteppingAnalysisForModulation
    from ._7130 import SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation
    from ._7131 import TorqueConverterAdvancedTimeSteppingAnalysisForModulation
    from ._7132 import (
        TorqueConverterConnectionAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7133 import TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation
    from ._7134 import TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation
    from ._7135 import UnbalancedMassAdvancedTimeSteppingAnalysisForModulation
    from ._7136 import VirtualComponentAdvancedTimeSteppingAnalysisForModulation
    from ._7137 import WormGearAdvancedTimeSteppingAnalysisForModulation
    from ._7138 import WormGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7139 import WormGearSetAdvancedTimeSteppingAnalysisForModulation
    from ._7140 import ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation
    from ._7141 import ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
    from ._7142 import ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation
else:
    import_structure = {
        "_7008": ["AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation"],
        "_7009": ["AbstractShaftAdvancedTimeSteppingAnalysisForModulation"],
        "_7010": ["AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation"],
        "_7011": [
            "AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7012": ["AdvancedTimeSteppingAnalysisForModulation"],
        "_7013": ["AtsamExcitationsOrOthers"],
        "_7014": ["AtsamNaturalFrequencyViewOption"],
        "_7015": ["AdvancedTimeSteppingAnalysisForModulationOptions"],
        "_7016": ["AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7017": [
            "AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7018": ["AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7019": ["AssemblyAdvancedTimeSteppingAnalysisForModulation"],
        "_7020": ["ATSAMResultsVsLargeTimeStepSettings"],
        "_7021": ["BearingAdvancedTimeSteppingAnalysisForModulation"],
        "_7022": ["BeltConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7023": ["BeltDriveAdvancedTimeSteppingAnalysisForModulation"],
        "_7024": ["BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7025": ["BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7026": ["BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7027": [
            "BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7028": ["BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7029": ["BevelGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7030": ["BevelGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7031": ["BevelGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7032": ["BoltAdvancedTimeSteppingAnalysisForModulation"],
        "_7033": ["BoltedJointAdvancedTimeSteppingAnalysisForModulation"],
        "_7034": ["ClutchAdvancedTimeSteppingAnalysisForModulation"],
        "_7035": ["ClutchConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7036": ["ClutchHalfAdvancedTimeSteppingAnalysisForModulation"],
        "_7037": ["CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7038": ["ComponentAdvancedTimeSteppingAnalysisForModulation"],
        "_7039": ["ConceptCouplingAdvancedTimeSteppingAnalysisForModulation"],
        "_7040": ["ConceptCouplingConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7041": ["ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation"],
        "_7042": ["ConceptGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7043": ["ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7044": ["ConceptGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7045": ["ConicalGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7046": ["ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7047": ["ConicalGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7048": ["ConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7049": ["ConnectorAdvancedTimeSteppingAnalysisForModulation"],
        "_7050": ["CouplingAdvancedTimeSteppingAnalysisForModulation"],
        "_7051": ["CouplingConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7052": ["CouplingHalfAdvancedTimeSteppingAnalysisForModulation"],
        "_7053": ["CVTAdvancedTimeSteppingAnalysisForModulation"],
        "_7054": ["CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7055": ["CVTPulleyAdvancedTimeSteppingAnalysisForModulation"],
        "_7056": ["CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation"],
        "_7057": ["CycloidalDiscAdvancedTimeSteppingAnalysisForModulation"],
        "_7058": [
            "CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7059": [
            "CycloidalDiscPlanetaryBearingConnectionAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7060": ["CylindricalGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7061": ["CylindricalGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7062": ["CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7063": ["CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7064": ["DatumAdvancedTimeSteppingAnalysisForModulation"],
        "_7065": ["ExternalCADModelAdvancedTimeSteppingAnalysisForModulation"],
        "_7066": ["FaceGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7067": ["FaceGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7068": ["FaceGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7069": ["FEPartAdvancedTimeSteppingAnalysisForModulation"],
        "_7070": ["FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation"],
        "_7071": ["GearAdvancedTimeSteppingAnalysisForModulation"],
        "_7072": ["GearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7073": ["GearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7074": ["GuideDxfModelAdvancedTimeSteppingAnalysisForModulation"],
        "_7075": [
            "HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7076": ["HypoidGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7077": ["HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7078": ["HypoidGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7079": [
            "InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7080": [
            "KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7081": [
            "KlingelnbergCycloPalloidConicalGearMeshAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7082": [
            "KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7083": [
            "KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7084": [
            "KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7085": [
            "KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7086": [
            "KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7087": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7088": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7089": ["MassDiscAdvancedTimeSteppingAnalysisForModulation"],
        "_7090": ["MeasurementComponentAdvancedTimeSteppingAnalysisForModulation"],
        "_7091": ["MountableComponentAdvancedTimeSteppingAnalysisForModulation"],
        "_7092": ["OilSealAdvancedTimeSteppingAnalysisForModulation"],
        "_7093": ["PartAdvancedTimeSteppingAnalysisForModulation"],
        "_7094": ["PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation"],
        "_7095": [
            "PartToPartShearCouplingConnectionAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7096": [
            "PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7097": ["PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7098": ["PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7099": ["PlanetCarrierAdvancedTimeSteppingAnalysisForModulation"],
        "_7100": ["PointLoadAdvancedTimeSteppingAnalysisForModulation"],
        "_7101": ["PowerLoadAdvancedTimeSteppingAnalysisForModulation"],
        "_7102": ["PulleyAdvancedTimeSteppingAnalysisForModulation"],
        "_7103": ["RingPinsAdvancedTimeSteppingAnalysisForModulation"],
        "_7104": ["RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7105": ["RollingRingAdvancedTimeSteppingAnalysisForModulation"],
        "_7106": ["RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation"],
        "_7107": ["RollingRingConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7108": ["RootAssemblyAdvancedTimeSteppingAnalysisForModulation"],
        "_7109": ["ShaftAdvancedTimeSteppingAnalysisForModulation"],
        "_7110": ["ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7111": [
            "ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7112": ["SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation"],
        "_7113": ["SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7114": ["SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7115": ["SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7116": ["SpringDamperAdvancedTimeSteppingAnalysisForModulation"],
        "_7117": ["SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7118": ["SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation"],
        "_7119": ["StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7120": ["StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7121": ["StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7122": ["StraightBevelGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7123": ["StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7124": ["StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7125": ["StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7126": ["StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7127": ["SynchroniserAdvancedTimeSteppingAnalysisForModulation"],
        "_7128": ["SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation"],
        "_7129": ["SynchroniserPartAdvancedTimeSteppingAnalysisForModulation"],
        "_7130": ["SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation"],
        "_7131": ["TorqueConverterAdvancedTimeSteppingAnalysisForModulation"],
        "_7132": ["TorqueConverterConnectionAdvancedTimeSteppingAnalysisForModulation"],
        "_7133": ["TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation"],
        "_7134": ["TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation"],
        "_7135": ["UnbalancedMassAdvancedTimeSteppingAnalysisForModulation"],
        "_7136": ["VirtualComponentAdvancedTimeSteppingAnalysisForModulation"],
        "_7137": ["WormGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7138": ["WormGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7139": ["WormGearSetAdvancedTimeSteppingAnalysisForModulation"],
        "_7140": ["ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation"],
        "_7141": ["ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation"],
        "_7142": ["ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation",
    "AbstractShaftAdvancedTimeSteppingAnalysisForModulation",
    "AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation",
    "AbstractShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation",
    "AdvancedTimeSteppingAnalysisForModulation",
    "AtsamExcitationsOrOthers",
    "AtsamNaturalFrequencyViewOption",
    "AdvancedTimeSteppingAnalysisForModulationOptions",
    "AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation",
    "AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "AGMAGleasonConicalGearSetAdvancedTimeSteppingAnalysisForModulation",
    "AssemblyAdvancedTimeSteppingAnalysisForModulation",
    "ATSAMResultsVsLargeTimeStepSettings",
    "BearingAdvancedTimeSteppingAnalysisForModulation",
    "BeltConnectionAdvancedTimeSteppingAnalysisForModulation",
    "BeltDriveAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation",
    "BevelGearAdvancedTimeSteppingAnalysisForModulation",
    "BevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "BevelGearSetAdvancedTimeSteppingAnalysisForModulation",
    "BoltAdvancedTimeSteppingAnalysisForModulation",
    "BoltedJointAdvancedTimeSteppingAnalysisForModulation",
    "ClutchAdvancedTimeSteppingAnalysisForModulation",
    "ClutchConnectionAdvancedTimeSteppingAnalysisForModulation",
    "ClutchHalfAdvancedTimeSteppingAnalysisForModulation",
    "CoaxialConnectionAdvancedTimeSteppingAnalysisForModulation",
    "ComponentAdvancedTimeSteppingAnalysisForModulation",
    "ConceptCouplingAdvancedTimeSteppingAnalysisForModulation",
    "ConceptCouplingConnectionAdvancedTimeSteppingAnalysisForModulation",
    "ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation",
    "ConceptGearAdvancedTimeSteppingAnalysisForModulation",
    "ConceptGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "ConceptGearSetAdvancedTimeSteppingAnalysisForModulation",
    "ConicalGearAdvancedTimeSteppingAnalysisForModulation",
    "ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "ConicalGearSetAdvancedTimeSteppingAnalysisForModulation",
    "ConnectionAdvancedTimeSteppingAnalysisForModulation",
    "ConnectorAdvancedTimeSteppingAnalysisForModulation",
    "CouplingAdvancedTimeSteppingAnalysisForModulation",
    "CouplingConnectionAdvancedTimeSteppingAnalysisForModulation",
    "CouplingHalfAdvancedTimeSteppingAnalysisForModulation",
    "CVTAdvancedTimeSteppingAnalysisForModulation",
    "CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation",
    "CVTPulleyAdvancedTimeSteppingAnalysisForModulation",
    "CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation",
    "CycloidalDiscAdvancedTimeSteppingAnalysisForModulation",
    "CycloidalDiscCentralBearingConnectionAdvancedTimeSteppingAnalysisForModulation",
    "CycloidalDiscPlanetaryBearingConnectionAdvancedTimeSteppingAnalysisForModulation",
    "CylindricalGearAdvancedTimeSteppingAnalysisForModulation",
    "CylindricalGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation",
    "CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation",
    "DatumAdvancedTimeSteppingAnalysisForModulation",
    "ExternalCADModelAdvancedTimeSteppingAnalysisForModulation",
    "FaceGearAdvancedTimeSteppingAnalysisForModulation",
    "FaceGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "FaceGearSetAdvancedTimeSteppingAnalysisForModulation",
    "FEPartAdvancedTimeSteppingAnalysisForModulation",
    "FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation",
    "GearAdvancedTimeSteppingAnalysisForModulation",
    "GearMeshAdvancedTimeSteppingAnalysisForModulation",
    "GearSetAdvancedTimeSteppingAnalysisForModulation",
    "GuideDxfModelAdvancedTimeSteppingAnalysisForModulation",
    "HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation",
    "HypoidGearAdvancedTimeSteppingAnalysisForModulation",
    "HypoidGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "HypoidGearSetAdvancedTimeSteppingAnalysisForModulation",
    "InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidConicalGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation",
    "MassDiscAdvancedTimeSteppingAnalysisForModulation",
    "MeasurementComponentAdvancedTimeSteppingAnalysisForModulation",
    "MountableComponentAdvancedTimeSteppingAnalysisForModulation",
    "OilSealAdvancedTimeSteppingAnalysisForModulation",
    "PartAdvancedTimeSteppingAnalysisForModulation",
    "PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation",
    "PartToPartShearCouplingConnectionAdvancedTimeSteppingAnalysisForModulation",
    "PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation",
    "PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation",
    "PlanetaryGearSetAdvancedTimeSteppingAnalysisForModulation",
    "PlanetCarrierAdvancedTimeSteppingAnalysisForModulation",
    "PointLoadAdvancedTimeSteppingAnalysisForModulation",
    "PowerLoadAdvancedTimeSteppingAnalysisForModulation",
    "PulleyAdvancedTimeSteppingAnalysisForModulation",
    "RingPinsAdvancedTimeSteppingAnalysisForModulation",
    "RingPinsToDiscConnectionAdvancedTimeSteppingAnalysisForModulation",
    "RollingRingAdvancedTimeSteppingAnalysisForModulation",
    "RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation",
    "RollingRingConnectionAdvancedTimeSteppingAnalysisForModulation",
    "RootAssemblyAdvancedTimeSteppingAnalysisForModulation",
    "ShaftAdvancedTimeSteppingAnalysisForModulation",
    "ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation",
    "ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation",
    "SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation",
    "SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation",
    "SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation",
    "SpringDamperAdvancedTimeSteppingAnalysisForModulation",
    "SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation",
    "SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelGearAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation",
    "SynchroniserAdvancedTimeSteppingAnalysisForModulation",
    "SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation",
    "SynchroniserPartAdvancedTimeSteppingAnalysisForModulation",
    "SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation",
    "TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
    "TorqueConverterConnectionAdvancedTimeSteppingAnalysisForModulation",
    "TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation",
    "TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation",
    "UnbalancedMassAdvancedTimeSteppingAnalysisForModulation",
    "VirtualComponentAdvancedTimeSteppingAnalysisForModulation",
    "WormGearAdvancedTimeSteppingAnalysisForModulation",
    "WormGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "WormGearSetAdvancedTimeSteppingAnalysisForModulation",
    "ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation",
    "ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
    "ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation",
)
