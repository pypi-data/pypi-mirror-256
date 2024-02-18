"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._7143 import AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7144 import AbstractShaftCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7145 import (
        AbstractShaftOrHousingCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7146 import (
        AbstractShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7147 import (
        AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7148 import (
        AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7149 import (
        AGMAGleasonConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7150 import AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7151 import BearingCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7152 import BeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7153 import BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7154 import (
        BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7155 import (
        BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7156 import (
        BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7157 import (
        BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7158 import (
        BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7159 import BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7160 import BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7161 import BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7162 import BoltCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7163 import BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7164 import ClutchCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7165 import ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7166 import ClutchHalfCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7167 import (
        CoaxialConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7168 import ComponentCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7169 import ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7170 import (
        ConceptCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7171 import (
        ConceptCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7172 import ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7173 import ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7174 import ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7175 import ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7176 import ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7177 import ConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7178 import ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7179 import ConnectorCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7180 import CouplingCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7181 import (
        CouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7182 import CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7183 import (
        CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7184 import CVTCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7185 import CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7186 import (
        CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7187 import (
        CycloidalDiscCentralBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7188 import CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7189 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7190 import CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7191 import (
        CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7192 import (
        CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7193 import (
        CylindricalPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7194 import DatumCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7195 import ExternalCADModelCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7196 import FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7197 import FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7198 import FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7199 import FEPartCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7200 import (
        FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7201 import GearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7202 import GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7203 import GearSetCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7204 import GuideDxfModelCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7205 import HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7206 import HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7207 import HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7208 import (
        InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7209 import (
        KlingelnbergCycloPalloidConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7210 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7211 import (
        KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7212 import (
        KlingelnbergCycloPalloidHypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7213 import (
        KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7214 import (
        KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7215 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7216 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7217 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7218 import MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7219 import (
        MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7220 import (
        MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7221 import OilSealCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7222 import PartCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7223 import (
        PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7224 import (
        PartToPartShearCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7225 import (
        PartToPartShearCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7226 import (
        PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7227 import PlanetaryGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7228 import PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7229 import PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7230 import PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7231 import PulleyCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7232 import RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7233 import (
        RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7234 import (
        RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7235 import RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7236 import (
        RollingRingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7237 import RootAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7238 import ShaftCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7239 import (
        ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7240 import (
        ShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7241 import (
        SpecialisedAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7242 import SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7243 import (
        SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7244 import (
        SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7245 import SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7246 import (
        SpringDamperConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7247 import SpringDamperHalfCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7248 import (
        StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7249 import (
        StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7250 import (
        StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7251 import (
        StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7252 import (
        StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7253 import (
        StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7254 import (
        StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7255 import (
        StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7256 import SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7257 import SynchroniserHalfCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7258 import SynchroniserPartCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7259 import (
        SynchroniserSleeveCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7260 import TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7261 import (
        TorqueConverterConnectionCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7262 import (
        TorqueConverterPumpCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7263 import (
        TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7264 import UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7265 import VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7266 import WormGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7267 import WormGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7268 import WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7269 import ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
    from ._7270 import (
        ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._7271 import (
        ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation,
    )
else:
    import_structure = {
        "_7143": ["AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7144": ["AbstractShaftCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7145": [
            "AbstractShaftOrHousingCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7146": [
            "AbstractShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7147": [
            "AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7148": [
            "AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7149": [
            "AGMAGleasonConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7150": ["AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7151": ["BearingCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7152": ["BeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7153": ["BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7154": [
            "BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7155": [
            "BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7156": [
            "BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7157": [
            "BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7158": [
            "BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7159": ["BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7160": ["BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7161": ["BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7162": ["BoltCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7163": ["BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7164": ["ClutchCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7165": ["ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7166": ["ClutchHalfCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7167": ["CoaxialConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7168": ["ComponentCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7169": ["ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7170": [
            "ConceptCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7171": [
            "ConceptCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7172": ["ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7173": ["ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7174": ["ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7175": ["ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7176": ["ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7177": ["ConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7178": ["ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7179": ["ConnectorCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7180": ["CouplingCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7181": [
            "CouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7182": ["CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7183": ["CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7184": ["CVTCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7185": ["CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7186": ["CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7187": [
            "CycloidalDiscCentralBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7188": ["CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7189": [
            "CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7190": ["CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7191": [
            "CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7192": [
            "CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7193": [
            "CylindricalPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7194": ["DatumCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7195": ["ExternalCADModelCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7196": ["FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7197": ["FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7198": ["FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7199": ["FEPartCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7200": [
            "FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7201": ["GearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7202": ["GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7203": ["GearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7204": ["GuideDxfModelCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7205": ["HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7206": ["HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7207": ["HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7208": [
            "InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7209": [
            "KlingelnbergCycloPalloidConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7210": [
            "KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7211": [
            "KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7212": [
            "KlingelnbergCycloPalloidHypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7213": [
            "KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7214": [
            "KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7215": [
            "KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7216": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7217": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7218": ["MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7219": [
            "MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7220": [
            "MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7221": ["OilSealCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7222": ["PartCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7223": [
            "PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7224": [
            "PartToPartShearCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7225": [
            "PartToPartShearCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7226": [
            "PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7227": ["PlanetaryGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7228": ["PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7229": ["PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7230": ["PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7231": ["PulleyCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7232": ["RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7233": [
            "RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7234": [
            "RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7235": ["RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7236": [
            "RollingRingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7237": ["RootAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7238": ["ShaftCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7239": [
            "ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7240": [
            "ShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7241": [
            "SpecialisedAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7242": ["SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7243": [
            "SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7244": [
            "SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7245": ["SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7246": [
            "SpringDamperConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7247": ["SpringDamperHalfCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7248": [
            "StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7249": [
            "StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7250": [
            "StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7251": ["StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7252": [
            "StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7253": [
            "StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7254": [
            "StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7255": [
            "StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7256": ["SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7257": ["SynchroniserHalfCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7258": ["SynchroniserPartCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7259": [
            "SynchroniserSleeveCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7260": ["TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7261": [
            "TorqueConverterConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7262": [
            "TorqueConverterPumpCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7263": [
            "TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7264": ["UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7265": ["VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7266": ["WormGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7267": ["WormGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7268": ["WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7269": ["ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_7270": [
            "ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_7271": ["ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "AbstractShaftCompoundAdvancedTimeSteppingAnalysisForModulation",
    "AbstractShaftOrHousingCompoundAdvancedTimeSteppingAnalysisForModulation",
    "AbstractShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "AGMAGleasonConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "AssemblyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BearingCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BevelDifferentialSunGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BoltCompoundAdvancedTimeSteppingAnalysisForModulation",
    "BoltedJointCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ClutchCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ClutchHalfCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CoaxialConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConceptCouplingCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConceptCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConceptCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConceptGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConceptGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ConnectorCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CouplingCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CVTCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CVTPulleyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CycloidalAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CycloidalDiscCentralBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CycloidalDiscCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CylindricalGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CylindricalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "CylindricalPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "DatumCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ExternalCADModelCompoundAdvancedTimeSteppingAnalysisForModulation",
    "FaceGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "FaceGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "FEPartCompoundAdvancedTimeSteppingAnalysisForModulation",
    "FlexiblePinAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "GearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "GearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "GuideDxfModelCompoundAdvancedTimeSteppingAnalysisForModulation",
    "HypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "HypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidHypoidGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation",
    "MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
    "MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
    "OilSealCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PartCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PartToPartShearCouplingCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PartToPartShearCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PartToPartShearCouplingHalfCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PlanetaryGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PlanetCarrierCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation",
    "PulleyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "RingPinsCompoundAdvancedTimeSteppingAnalysisForModulation",
    "RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "RollingRingAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "RollingRingCompoundAdvancedTimeSteppingAnalysisForModulation",
    "RollingRingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "RootAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ShaftCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ShaftHubConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SpecialisedAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SpiralBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SpiralBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SpringDamperCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SpringDamperConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SpringDamperHalfCompoundAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelDiffGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelDiffGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelPlanetGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "StraightBevelSunGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SynchroniserCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SynchroniserHalfCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SynchroniserPartCompoundAdvancedTimeSteppingAnalysisForModulation",
    "SynchroniserSleeveCompoundAdvancedTimeSteppingAnalysisForModulation",
    "TorqueConverterCompoundAdvancedTimeSteppingAnalysisForModulation",
    "TorqueConverterConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    "TorqueConverterPumpCompoundAdvancedTimeSteppingAnalysisForModulation",
    "TorqueConverterTurbineCompoundAdvancedTimeSteppingAnalysisForModulation",
    "UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation",
    "VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
    "WormGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "WormGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "WormGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    "ZerolBevelGearSetCompoundAdvancedTimeSteppingAnalysisForModulation",
)
