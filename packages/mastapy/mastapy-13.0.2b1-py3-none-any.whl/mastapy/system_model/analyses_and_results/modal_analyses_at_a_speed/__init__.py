"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5119 import AbstractAssemblyModalAnalysisAtASpeed
    from ._5120 import AbstractShaftModalAnalysisAtASpeed
    from ._5121 import AbstractShaftOrHousingModalAnalysisAtASpeed
    from ._5122 import AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed
    from ._5123 import AGMAGleasonConicalGearMeshModalAnalysisAtASpeed
    from ._5124 import AGMAGleasonConicalGearModalAnalysisAtASpeed
    from ._5125 import AGMAGleasonConicalGearSetModalAnalysisAtASpeed
    from ._5126 import AssemblyModalAnalysisAtASpeed
    from ._5127 import BearingModalAnalysisAtASpeed
    from ._5128 import BeltConnectionModalAnalysisAtASpeed
    from ._5129 import BeltDriveModalAnalysisAtASpeed
    from ._5130 import BevelDifferentialGearMeshModalAnalysisAtASpeed
    from ._5131 import BevelDifferentialGearModalAnalysisAtASpeed
    from ._5132 import BevelDifferentialGearSetModalAnalysisAtASpeed
    from ._5133 import BevelDifferentialPlanetGearModalAnalysisAtASpeed
    from ._5134 import BevelDifferentialSunGearModalAnalysisAtASpeed
    from ._5135 import BevelGearMeshModalAnalysisAtASpeed
    from ._5136 import BevelGearModalAnalysisAtASpeed
    from ._5137 import BevelGearSetModalAnalysisAtASpeed
    from ._5138 import BoltedJointModalAnalysisAtASpeed
    from ._5139 import BoltModalAnalysisAtASpeed
    from ._5140 import ClutchConnectionModalAnalysisAtASpeed
    from ._5141 import ClutchHalfModalAnalysisAtASpeed
    from ._5142 import ClutchModalAnalysisAtASpeed
    from ._5143 import CoaxialConnectionModalAnalysisAtASpeed
    from ._5144 import ComponentModalAnalysisAtASpeed
    from ._5145 import ConceptCouplingConnectionModalAnalysisAtASpeed
    from ._5146 import ConceptCouplingHalfModalAnalysisAtASpeed
    from ._5147 import ConceptCouplingModalAnalysisAtASpeed
    from ._5148 import ConceptGearMeshModalAnalysisAtASpeed
    from ._5149 import ConceptGearModalAnalysisAtASpeed
    from ._5150 import ConceptGearSetModalAnalysisAtASpeed
    from ._5151 import ConicalGearMeshModalAnalysisAtASpeed
    from ._5152 import ConicalGearModalAnalysisAtASpeed
    from ._5153 import ConicalGearSetModalAnalysisAtASpeed
    from ._5154 import ConnectionModalAnalysisAtASpeed
    from ._5155 import ConnectorModalAnalysisAtASpeed
    from ._5156 import CouplingConnectionModalAnalysisAtASpeed
    from ._5157 import CouplingHalfModalAnalysisAtASpeed
    from ._5158 import CouplingModalAnalysisAtASpeed
    from ._5159 import CVTBeltConnectionModalAnalysisAtASpeed
    from ._5160 import CVTModalAnalysisAtASpeed
    from ._5161 import CVTPulleyModalAnalysisAtASpeed
    from ._5162 import CycloidalAssemblyModalAnalysisAtASpeed
    from ._5163 import CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed
    from ._5164 import CycloidalDiscModalAnalysisAtASpeed
    from ._5165 import CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed
    from ._5166 import CylindricalGearMeshModalAnalysisAtASpeed
    from ._5167 import CylindricalGearModalAnalysisAtASpeed
    from ._5168 import CylindricalGearSetModalAnalysisAtASpeed
    from ._5169 import CylindricalPlanetGearModalAnalysisAtASpeed
    from ._5170 import DatumModalAnalysisAtASpeed
    from ._5171 import ExternalCADModelModalAnalysisAtASpeed
    from ._5172 import FaceGearMeshModalAnalysisAtASpeed
    from ._5173 import FaceGearModalAnalysisAtASpeed
    from ._5174 import FaceGearSetModalAnalysisAtASpeed
    from ._5175 import FEPartModalAnalysisAtASpeed
    from ._5176 import FlexiblePinAssemblyModalAnalysisAtASpeed
    from ._5177 import GearMeshModalAnalysisAtASpeed
    from ._5178 import GearModalAnalysisAtASpeed
    from ._5179 import GearSetModalAnalysisAtASpeed
    from ._5180 import GuideDxfModelModalAnalysisAtASpeed
    from ._5181 import HypoidGearMeshModalAnalysisAtASpeed
    from ._5182 import HypoidGearModalAnalysisAtASpeed
    from ._5183 import HypoidGearSetModalAnalysisAtASpeed
    from ._5184 import InterMountableComponentConnectionModalAnalysisAtASpeed
    from ._5185 import KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed
    from ._5186 import KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed
    from ._5187 import KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed
    from ._5188 import KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed
    from ._5189 import KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed
    from ._5190 import KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed
    from ._5191 import KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed
    from ._5192 import KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed
    from ._5193 import KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed
    from ._5194 import MassDiscModalAnalysisAtASpeed
    from ._5195 import MeasurementComponentModalAnalysisAtASpeed
    from ._5196 import ModalAnalysisAtASpeed
    from ._5197 import MountableComponentModalAnalysisAtASpeed
    from ._5198 import OilSealModalAnalysisAtASpeed
    from ._5199 import PartModalAnalysisAtASpeed
    from ._5200 import PartToPartShearCouplingConnectionModalAnalysisAtASpeed
    from ._5201 import PartToPartShearCouplingHalfModalAnalysisAtASpeed
    from ._5202 import PartToPartShearCouplingModalAnalysisAtASpeed
    from ._5203 import PlanetaryConnectionModalAnalysisAtASpeed
    from ._5204 import PlanetaryGearSetModalAnalysisAtASpeed
    from ._5205 import PlanetCarrierModalAnalysisAtASpeed
    from ._5206 import PointLoadModalAnalysisAtASpeed
    from ._5207 import PowerLoadModalAnalysisAtASpeed
    from ._5208 import PulleyModalAnalysisAtASpeed
    from ._5209 import RingPinsModalAnalysisAtASpeed
    from ._5210 import RingPinsToDiscConnectionModalAnalysisAtASpeed
    from ._5211 import RollingRingAssemblyModalAnalysisAtASpeed
    from ._5212 import RollingRingConnectionModalAnalysisAtASpeed
    from ._5213 import RollingRingModalAnalysisAtASpeed
    from ._5214 import RootAssemblyModalAnalysisAtASpeed
    from ._5215 import ShaftHubConnectionModalAnalysisAtASpeed
    from ._5216 import ShaftModalAnalysisAtASpeed
    from ._5217 import ShaftToMountableComponentConnectionModalAnalysisAtASpeed
    from ._5218 import SpecialisedAssemblyModalAnalysisAtASpeed
    from ._5219 import SpiralBevelGearMeshModalAnalysisAtASpeed
    from ._5220 import SpiralBevelGearModalAnalysisAtASpeed
    from ._5221 import SpiralBevelGearSetModalAnalysisAtASpeed
    from ._5222 import SpringDamperConnectionModalAnalysisAtASpeed
    from ._5223 import SpringDamperHalfModalAnalysisAtASpeed
    from ._5224 import SpringDamperModalAnalysisAtASpeed
    from ._5225 import StraightBevelDiffGearMeshModalAnalysisAtASpeed
    from ._5226 import StraightBevelDiffGearModalAnalysisAtASpeed
    from ._5227 import StraightBevelDiffGearSetModalAnalysisAtASpeed
    from ._5228 import StraightBevelGearMeshModalAnalysisAtASpeed
    from ._5229 import StraightBevelGearModalAnalysisAtASpeed
    from ._5230 import StraightBevelGearSetModalAnalysisAtASpeed
    from ._5231 import StraightBevelPlanetGearModalAnalysisAtASpeed
    from ._5232 import StraightBevelSunGearModalAnalysisAtASpeed
    from ._5233 import SynchroniserHalfModalAnalysisAtASpeed
    from ._5234 import SynchroniserModalAnalysisAtASpeed
    from ._5235 import SynchroniserPartModalAnalysisAtASpeed
    from ._5236 import SynchroniserSleeveModalAnalysisAtASpeed
    from ._5237 import TorqueConverterConnectionModalAnalysisAtASpeed
    from ._5238 import TorqueConverterModalAnalysisAtASpeed
    from ._5239 import TorqueConverterPumpModalAnalysisAtASpeed
    from ._5240 import TorqueConverterTurbineModalAnalysisAtASpeed
    from ._5241 import UnbalancedMassModalAnalysisAtASpeed
    from ._5242 import VirtualComponentModalAnalysisAtASpeed
    from ._5243 import WormGearMeshModalAnalysisAtASpeed
    from ._5244 import WormGearModalAnalysisAtASpeed
    from ._5245 import WormGearSetModalAnalysisAtASpeed
    from ._5246 import ZerolBevelGearMeshModalAnalysisAtASpeed
    from ._5247 import ZerolBevelGearModalAnalysisAtASpeed
    from ._5248 import ZerolBevelGearSetModalAnalysisAtASpeed
else:
    import_structure = {
        "_5119": ["AbstractAssemblyModalAnalysisAtASpeed"],
        "_5120": ["AbstractShaftModalAnalysisAtASpeed"],
        "_5121": ["AbstractShaftOrHousingModalAnalysisAtASpeed"],
        "_5122": ["AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed"],
        "_5123": ["AGMAGleasonConicalGearMeshModalAnalysisAtASpeed"],
        "_5124": ["AGMAGleasonConicalGearModalAnalysisAtASpeed"],
        "_5125": ["AGMAGleasonConicalGearSetModalAnalysisAtASpeed"],
        "_5126": ["AssemblyModalAnalysisAtASpeed"],
        "_5127": ["BearingModalAnalysisAtASpeed"],
        "_5128": ["BeltConnectionModalAnalysisAtASpeed"],
        "_5129": ["BeltDriveModalAnalysisAtASpeed"],
        "_5130": ["BevelDifferentialGearMeshModalAnalysisAtASpeed"],
        "_5131": ["BevelDifferentialGearModalAnalysisAtASpeed"],
        "_5132": ["BevelDifferentialGearSetModalAnalysisAtASpeed"],
        "_5133": ["BevelDifferentialPlanetGearModalAnalysisAtASpeed"],
        "_5134": ["BevelDifferentialSunGearModalAnalysisAtASpeed"],
        "_5135": ["BevelGearMeshModalAnalysisAtASpeed"],
        "_5136": ["BevelGearModalAnalysisAtASpeed"],
        "_5137": ["BevelGearSetModalAnalysisAtASpeed"],
        "_5138": ["BoltedJointModalAnalysisAtASpeed"],
        "_5139": ["BoltModalAnalysisAtASpeed"],
        "_5140": ["ClutchConnectionModalAnalysisAtASpeed"],
        "_5141": ["ClutchHalfModalAnalysisAtASpeed"],
        "_5142": ["ClutchModalAnalysisAtASpeed"],
        "_5143": ["CoaxialConnectionModalAnalysisAtASpeed"],
        "_5144": ["ComponentModalAnalysisAtASpeed"],
        "_5145": ["ConceptCouplingConnectionModalAnalysisAtASpeed"],
        "_5146": ["ConceptCouplingHalfModalAnalysisAtASpeed"],
        "_5147": ["ConceptCouplingModalAnalysisAtASpeed"],
        "_5148": ["ConceptGearMeshModalAnalysisAtASpeed"],
        "_5149": ["ConceptGearModalAnalysisAtASpeed"],
        "_5150": ["ConceptGearSetModalAnalysisAtASpeed"],
        "_5151": ["ConicalGearMeshModalAnalysisAtASpeed"],
        "_5152": ["ConicalGearModalAnalysisAtASpeed"],
        "_5153": ["ConicalGearSetModalAnalysisAtASpeed"],
        "_5154": ["ConnectionModalAnalysisAtASpeed"],
        "_5155": ["ConnectorModalAnalysisAtASpeed"],
        "_5156": ["CouplingConnectionModalAnalysisAtASpeed"],
        "_5157": ["CouplingHalfModalAnalysisAtASpeed"],
        "_5158": ["CouplingModalAnalysisAtASpeed"],
        "_5159": ["CVTBeltConnectionModalAnalysisAtASpeed"],
        "_5160": ["CVTModalAnalysisAtASpeed"],
        "_5161": ["CVTPulleyModalAnalysisAtASpeed"],
        "_5162": ["CycloidalAssemblyModalAnalysisAtASpeed"],
        "_5163": ["CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed"],
        "_5164": ["CycloidalDiscModalAnalysisAtASpeed"],
        "_5165": ["CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed"],
        "_5166": ["CylindricalGearMeshModalAnalysisAtASpeed"],
        "_5167": ["CylindricalGearModalAnalysisAtASpeed"],
        "_5168": ["CylindricalGearSetModalAnalysisAtASpeed"],
        "_5169": ["CylindricalPlanetGearModalAnalysisAtASpeed"],
        "_5170": ["DatumModalAnalysisAtASpeed"],
        "_5171": ["ExternalCADModelModalAnalysisAtASpeed"],
        "_5172": ["FaceGearMeshModalAnalysisAtASpeed"],
        "_5173": ["FaceGearModalAnalysisAtASpeed"],
        "_5174": ["FaceGearSetModalAnalysisAtASpeed"],
        "_5175": ["FEPartModalAnalysisAtASpeed"],
        "_5176": ["FlexiblePinAssemblyModalAnalysisAtASpeed"],
        "_5177": ["GearMeshModalAnalysisAtASpeed"],
        "_5178": ["GearModalAnalysisAtASpeed"],
        "_5179": ["GearSetModalAnalysisAtASpeed"],
        "_5180": ["GuideDxfModelModalAnalysisAtASpeed"],
        "_5181": ["HypoidGearMeshModalAnalysisAtASpeed"],
        "_5182": ["HypoidGearModalAnalysisAtASpeed"],
        "_5183": ["HypoidGearSetModalAnalysisAtASpeed"],
        "_5184": ["InterMountableComponentConnectionModalAnalysisAtASpeed"],
        "_5185": ["KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed"],
        "_5186": ["KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed"],
        "_5187": ["KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed"],
        "_5188": ["KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed"],
        "_5189": ["KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed"],
        "_5190": ["KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed"],
        "_5191": ["KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed"],
        "_5192": ["KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed"],
        "_5193": ["KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed"],
        "_5194": ["MassDiscModalAnalysisAtASpeed"],
        "_5195": ["MeasurementComponentModalAnalysisAtASpeed"],
        "_5196": ["ModalAnalysisAtASpeed"],
        "_5197": ["MountableComponentModalAnalysisAtASpeed"],
        "_5198": ["OilSealModalAnalysisAtASpeed"],
        "_5199": ["PartModalAnalysisAtASpeed"],
        "_5200": ["PartToPartShearCouplingConnectionModalAnalysisAtASpeed"],
        "_5201": ["PartToPartShearCouplingHalfModalAnalysisAtASpeed"],
        "_5202": ["PartToPartShearCouplingModalAnalysisAtASpeed"],
        "_5203": ["PlanetaryConnectionModalAnalysisAtASpeed"],
        "_5204": ["PlanetaryGearSetModalAnalysisAtASpeed"],
        "_5205": ["PlanetCarrierModalAnalysisAtASpeed"],
        "_5206": ["PointLoadModalAnalysisAtASpeed"],
        "_5207": ["PowerLoadModalAnalysisAtASpeed"],
        "_5208": ["PulleyModalAnalysisAtASpeed"],
        "_5209": ["RingPinsModalAnalysisAtASpeed"],
        "_5210": ["RingPinsToDiscConnectionModalAnalysisAtASpeed"],
        "_5211": ["RollingRingAssemblyModalAnalysisAtASpeed"],
        "_5212": ["RollingRingConnectionModalAnalysisAtASpeed"],
        "_5213": ["RollingRingModalAnalysisAtASpeed"],
        "_5214": ["RootAssemblyModalAnalysisAtASpeed"],
        "_5215": ["ShaftHubConnectionModalAnalysisAtASpeed"],
        "_5216": ["ShaftModalAnalysisAtASpeed"],
        "_5217": ["ShaftToMountableComponentConnectionModalAnalysisAtASpeed"],
        "_5218": ["SpecialisedAssemblyModalAnalysisAtASpeed"],
        "_5219": ["SpiralBevelGearMeshModalAnalysisAtASpeed"],
        "_5220": ["SpiralBevelGearModalAnalysisAtASpeed"],
        "_5221": ["SpiralBevelGearSetModalAnalysisAtASpeed"],
        "_5222": ["SpringDamperConnectionModalAnalysisAtASpeed"],
        "_5223": ["SpringDamperHalfModalAnalysisAtASpeed"],
        "_5224": ["SpringDamperModalAnalysisAtASpeed"],
        "_5225": ["StraightBevelDiffGearMeshModalAnalysisAtASpeed"],
        "_5226": ["StraightBevelDiffGearModalAnalysisAtASpeed"],
        "_5227": ["StraightBevelDiffGearSetModalAnalysisAtASpeed"],
        "_5228": ["StraightBevelGearMeshModalAnalysisAtASpeed"],
        "_5229": ["StraightBevelGearModalAnalysisAtASpeed"],
        "_5230": ["StraightBevelGearSetModalAnalysisAtASpeed"],
        "_5231": ["StraightBevelPlanetGearModalAnalysisAtASpeed"],
        "_5232": ["StraightBevelSunGearModalAnalysisAtASpeed"],
        "_5233": ["SynchroniserHalfModalAnalysisAtASpeed"],
        "_5234": ["SynchroniserModalAnalysisAtASpeed"],
        "_5235": ["SynchroniserPartModalAnalysisAtASpeed"],
        "_5236": ["SynchroniserSleeveModalAnalysisAtASpeed"],
        "_5237": ["TorqueConverterConnectionModalAnalysisAtASpeed"],
        "_5238": ["TorqueConverterModalAnalysisAtASpeed"],
        "_5239": ["TorqueConverterPumpModalAnalysisAtASpeed"],
        "_5240": ["TorqueConverterTurbineModalAnalysisAtASpeed"],
        "_5241": ["UnbalancedMassModalAnalysisAtASpeed"],
        "_5242": ["VirtualComponentModalAnalysisAtASpeed"],
        "_5243": ["WormGearMeshModalAnalysisAtASpeed"],
        "_5244": ["WormGearModalAnalysisAtASpeed"],
        "_5245": ["WormGearSetModalAnalysisAtASpeed"],
        "_5246": ["ZerolBevelGearMeshModalAnalysisAtASpeed"],
        "_5247": ["ZerolBevelGearModalAnalysisAtASpeed"],
        "_5248": ["ZerolBevelGearSetModalAnalysisAtASpeed"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyModalAnalysisAtASpeed",
    "AbstractShaftModalAnalysisAtASpeed",
    "AbstractShaftOrHousingModalAnalysisAtASpeed",
    "AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed",
    "AGMAGleasonConicalGearMeshModalAnalysisAtASpeed",
    "AGMAGleasonConicalGearModalAnalysisAtASpeed",
    "AGMAGleasonConicalGearSetModalAnalysisAtASpeed",
    "AssemblyModalAnalysisAtASpeed",
    "BearingModalAnalysisAtASpeed",
    "BeltConnectionModalAnalysisAtASpeed",
    "BeltDriveModalAnalysisAtASpeed",
    "BevelDifferentialGearMeshModalAnalysisAtASpeed",
    "BevelDifferentialGearModalAnalysisAtASpeed",
    "BevelDifferentialGearSetModalAnalysisAtASpeed",
    "BevelDifferentialPlanetGearModalAnalysisAtASpeed",
    "BevelDifferentialSunGearModalAnalysisAtASpeed",
    "BevelGearMeshModalAnalysisAtASpeed",
    "BevelGearModalAnalysisAtASpeed",
    "BevelGearSetModalAnalysisAtASpeed",
    "BoltedJointModalAnalysisAtASpeed",
    "BoltModalAnalysisAtASpeed",
    "ClutchConnectionModalAnalysisAtASpeed",
    "ClutchHalfModalAnalysisAtASpeed",
    "ClutchModalAnalysisAtASpeed",
    "CoaxialConnectionModalAnalysisAtASpeed",
    "ComponentModalAnalysisAtASpeed",
    "ConceptCouplingConnectionModalAnalysisAtASpeed",
    "ConceptCouplingHalfModalAnalysisAtASpeed",
    "ConceptCouplingModalAnalysisAtASpeed",
    "ConceptGearMeshModalAnalysisAtASpeed",
    "ConceptGearModalAnalysisAtASpeed",
    "ConceptGearSetModalAnalysisAtASpeed",
    "ConicalGearMeshModalAnalysisAtASpeed",
    "ConicalGearModalAnalysisAtASpeed",
    "ConicalGearSetModalAnalysisAtASpeed",
    "ConnectionModalAnalysisAtASpeed",
    "ConnectorModalAnalysisAtASpeed",
    "CouplingConnectionModalAnalysisAtASpeed",
    "CouplingHalfModalAnalysisAtASpeed",
    "CouplingModalAnalysisAtASpeed",
    "CVTBeltConnectionModalAnalysisAtASpeed",
    "CVTModalAnalysisAtASpeed",
    "CVTPulleyModalAnalysisAtASpeed",
    "CycloidalAssemblyModalAnalysisAtASpeed",
    "CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed",
    "CycloidalDiscModalAnalysisAtASpeed",
    "CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed",
    "CylindricalGearMeshModalAnalysisAtASpeed",
    "CylindricalGearModalAnalysisAtASpeed",
    "CylindricalGearSetModalAnalysisAtASpeed",
    "CylindricalPlanetGearModalAnalysisAtASpeed",
    "DatumModalAnalysisAtASpeed",
    "ExternalCADModelModalAnalysisAtASpeed",
    "FaceGearMeshModalAnalysisAtASpeed",
    "FaceGearModalAnalysisAtASpeed",
    "FaceGearSetModalAnalysisAtASpeed",
    "FEPartModalAnalysisAtASpeed",
    "FlexiblePinAssemblyModalAnalysisAtASpeed",
    "GearMeshModalAnalysisAtASpeed",
    "GearModalAnalysisAtASpeed",
    "GearSetModalAnalysisAtASpeed",
    "GuideDxfModelModalAnalysisAtASpeed",
    "HypoidGearMeshModalAnalysisAtASpeed",
    "HypoidGearModalAnalysisAtASpeed",
    "HypoidGearSetModalAnalysisAtASpeed",
    "InterMountableComponentConnectionModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed",
    "KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed",
    "MassDiscModalAnalysisAtASpeed",
    "MeasurementComponentModalAnalysisAtASpeed",
    "ModalAnalysisAtASpeed",
    "MountableComponentModalAnalysisAtASpeed",
    "OilSealModalAnalysisAtASpeed",
    "PartModalAnalysisAtASpeed",
    "PartToPartShearCouplingConnectionModalAnalysisAtASpeed",
    "PartToPartShearCouplingHalfModalAnalysisAtASpeed",
    "PartToPartShearCouplingModalAnalysisAtASpeed",
    "PlanetaryConnectionModalAnalysisAtASpeed",
    "PlanetaryGearSetModalAnalysisAtASpeed",
    "PlanetCarrierModalAnalysisAtASpeed",
    "PointLoadModalAnalysisAtASpeed",
    "PowerLoadModalAnalysisAtASpeed",
    "PulleyModalAnalysisAtASpeed",
    "RingPinsModalAnalysisAtASpeed",
    "RingPinsToDiscConnectionModalAnalysisAtASpeed",
    "RollingRingAssemblyModalAnalysisAtASpeed",
    "RollingRingConnectionModalAnalysisAtASpeed",
    "RollingRingModalAnalysisAtASpeed",
    "RootAssemblyModalAnalysisAtASpeed",
    "ShaftHubConnectionModalAnalysisAtASpeed",
    "ShaftModalAnalysisAtASpeed",
    "ShaftToMountableComponentConnectionModalAnalysisAtASpeed",
    "SpecialisedAssemblyModalAnalysisAtASpeed",
    "SpiralBevelGearMeshModalAnalysisAtASpeed",
    "SpiralBevelGearModalAnalysisAtASpeed",
    "SpiralBevelGearSetModalAnalysisAtASpeed",
    "SpringDamperConnectionModalAnalysisAtASpeed",
    "SpringDamperHalfModalAnalysisAtASpeed",
    "SpringDamperModalAnalysisAtASpeed",
    "StraightBevelDiffGearMeshModalAnalysisAtASpeed",
    "StraightBevelDiffGearModalAnalysisAtASpeed",
    "StraightBevelDiffGearSetModalAnalysisAtASpeed",
    "StraightBevelGearMeshModalAnalysisAtASpeed",
    "StraightBevelGearModalAnalysisAtASpeed",
    "StraightBevelGearSetModalAnalysisAtASpeed",
    "StraightBevelPlanetGearModalAnalysisAtASpeed",
    "StraightBevelSunGearModalAnalysisAtASpeed",
    "SynchroniserHalfModalAnalysisAtASpeed",
    "SynchroniserModalAnalysisAtASpeed",
    "SynchroniserPartModalAnalysisAtASpeed",
    "SynchroniserSleeveModalAnalysisAtASpeed",
    "TorqueConverterConnectionModalAnalysisAtASpeed",
    "TorqueConverterModalAnalysisAtASpeed",
    "TorqueConverterPumpModalAnalysisAtASpeed",
    "TorqueConverterTurbineModalAnalysisAtASpeed",
    "UnbalancedMassModalAnalysisAtASpeed",
    "VirtualComponentModalAnalysisAtASpeed",
    "WormGearMeshModalAnalysisAtASpeed",
    "WormGearModalAnalysisAtASpeed",
    "WormGearSetModalAnalysisAtASpeed",
    "ZerolBevelGearMeshModalAnalysisAtASpeed",
    "ZerolBevelGearModalAnalysisAtASpeed",
    "ZerolBevelGearSetModalAnalysisAtASpeed",
)
