"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._4730 import AbstractAssemblyCompoundModalAnalysis
    from ._4731 import AbstractShaftCompoundModalAnalysis
    from ._4732 import AbstractShaftOrHousingCompoundModalAnalysis
    from ._4733 import AbstractShaftToMountableComponentConnectionCompoundModalAnalysis
    from ._4734 import AGMAGleasonConicalGearCompoundModalAnalysis
    from ._4735 import AGMAGleasonConicalGearMeshCompoundModalAnalysis
    from ._4736 import AGMAGleasonConicalGearSetCompoundModalAnalysis
    from ._4737 import AssemblyCompoundModalAnalysis
    from ._4738 import BearingCompoundModalAnalysis
    from ._4739 import BeltConnectionCompoundModalAnalysis
    from ._4740 import BeltDriveCompoundModalAnalysis
    from ._4741 import BevelDifferentialGearCompoundModalAnalysis
    from ._4742 import BevelDifferentialGearMeshCompoundModalAnalysis
    from ._4743 import BevelDifferentialGearSetCompoundModalAnalysis
    from ._4744 import BevelDifferentialPlanetGearCompoundModalAnalysis
    from ._4745 import BevelDifferentialSunGearCompoundModalAnalysis
    from ._4746 import BevelGearCompoundModalAnalysis
    from ._4747 import BevelGearMeshCompoundModalAnalysis
    from ._4748 import BevelGearSetCompoundModalAnalysis
    from ._4749 import BoltCompoundModalAnalysis
    from ._4750 import BoltedJointCompoundModalAnalysis
    from ._4751 import ClutchCompoundModalAnalysis
    from ._4752 import ClutchConnectionCompoundModalAnalysis
    from ._4753 import ClutchHalfCompoundModalAnalysis
    from ._4754 import CoaxialConnectionCompoundModalAnalysis
    from ._4755 import ComponentCompoundModalAnalysis
    from ._4756 import ConceptCouplingCompoundModalAnalysis
    from ._4757 import ConceptCouplingConnectionCompoundModalAnalysis
    from ._4758 import ConceptCouplingHalfCompoundModalAnalysis
    from ._4759 import ConceptGearCompoundModalAnalysis
    from ._4760 import ConceptGearMeshCompoundModalAnalysis
    from ._4761 import ConceptGearSetCompoundModalAnalysis
    from ._4762 import ConicalGearCompoundModalAnalysis
    from ._4763 import ConicalGearMeshCompoundModalAnalysis
    from ._4764 import ConicalGearSetCompoundModalAnalysis
    from ._4765 import ConnectionCompoundModalAnalysis
    from ._4766 import ConnectorCompoundModalAnalysis
    from ._4767 import CouplingCompoundModalAnalysis
    from ._4768 import CouplingConnectionCompoundModalAnalysis
    from ._4769 import CouplingHalfCompoundModalAnalysis
    from ._4770 import CVTBeltConnectionCompoundModalAnalysis
    from ._4771 import CVTCompoundModalAnalysis
    from ._4772 import CVTPulleyCompoundModalAnalysis
    from ._4773 import CycloidalAssemblyCompoundModalAnalysis
    from ._4774 import CycloidalDiscCentralBearingConnectionCompoundModalAnalysis
    from ._4775 import CycloidalDiscCompoundModalAnalysis
    from ._4776 import CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis
    from ._4777 import CylindricalGearCompoundModalAnalysis
    from ._4778 import CylindricalGearMeshCompoundModalAnalysis
    from ._4779 import CylindricalGearSetCompoundModalAnalysis
    from ._4780 import CylindricalPlanetGearCompoundModalAnalysis
    from ._4781 import DatumCompoundModalAnalysis
    from ._4782 import ExternalCADModelCompoundModalAnalysis
    from ._4783 import FaceGearCompoundModalAnalysis
    from ._4784 import FaceGearMeshCompoundModalAnalysis
    from ._4785 import FaceGearSetCompoundModalAnalysis
    from ._4786 import FEPartCompoundModalAnalysis
    from ._4787 import FlexiblePinAssemblyCompoundModalAnalysis
    from ._4788 import GearCompoundModalAnalysis
    from ._4789 import GearMeshCompoundModalAnalysis
    from ._4790 import GearSetCompoundModalAnalysis
    from ._4791 import GuideDxfModelCompoundModalAnalysis
    from ._4792 import HypoidGearCompoundModalAnalysis
    from ._4793 import HypoidGearMeshCompoundModalAnalysis
    from ._4794 import HypoidGearSetCompoundModalAnalysis
    from ._4795 import InterMountableComponentConnectionCompoundModalAnalysis
    from ._4796 import KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis
    from ._4797 import KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis
    from ._4798 import KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis
    from ._4799 import KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis
    from ._4800 import KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis
    from ._4801 import KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis
    from ._4802 import KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis
    from ._4803 import KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis
    from ._4804 import KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis
    from ._4805 import MassDiscCompoundModalAnalysis
    from ._4806 import MeasurementComponentCompoundModalAnalysis
    from ._4807 import MountableComponentCompoundModalAnalysis
    from ._4808 import OilSealCompoundModalAnalysis
    from ._4809 import PartCompoundModalAnalysis
    from ._4810 import PartToPartShearCouplingCompoundModalAnalysis
    from ._4811 import PartToPartShearCouplingConnectionCompoundModalAnalysis
    from ._4812 import PartToPartShearCouplingHalfCompoundModalAnalysis
    from ._4813 import PlanetaryConnectionCompoundModalAnalysis
    from ._4814 import PlanetaryGearSetCompoundModalAnalysis
    from ._4815 import PlanetCarrierCompoundModalAnalysis
    from ._4816 import PointLoadCompoundModalAnalysis
    from ._4817 import PowerLoadCompoundModalAnalysis
    from ._4818 import PulleyCompoundModalAnalysis
    from ._4819 import RingPinsCompoundModalAnalysis
    from ._4820 import RingPinsToDiscConnectionCompoundModalAnalysis
    from ._4821 import RollingRingAssemblyCompoundModalAnalysis
    from ._4822 import RollingRingCompoundModalAnalysis
    from ._4823 import RollingRingConnectionCompoundModalAnalysis
    from ._4824 import RootAssemblyCompoundModalAnalysis
    from ._4825 import ShaftCompoundModalAnalysis
    from ._4826 import ShaftHubConnectionCompoundModalAnalysis
    from ._4827 import ShaftToMountableComponentConnectionCompoundModalAnalysis
    from ._4828 import SpecialisedAssemblyCompoundModalAnalysis
    from ._4829 import SpiralBevelGearCompoundModalAnalysis
    from ._4830 import SpiralBevelGearMeshCompoundModalAnalysis
    from ._4831 import SpiralBevelGearSetCompoundModalAnalysis
    from ._4832 import SpringDamperCompoundModalAnalysis
    from ._4833 import SpringDamperConnectionCompoundModalAnalysis
    from ._4834 import SpringDamperHalfCompoundModalAnalysis
    from ._4835 import StraightBevelDiffGearCompoundModalAnalysis
    from ._4836 import StraightBevelDiffGearMeshCompoundModalAnalysis
    from ._4837 import StraightBevelDiffGearSetCompoundModalAnalysis
    from ._4838 import StraightBevelGearCompoundModalAnalysis
    from ._4839 import StraightBevelGearMeshCompoundModalAnalysis
    from ._4840 import StraightBevelGearSetCompoundModalAnalysis
    from ._4841 import StraightBevelPlanetGearCompoundModalAnalysis
    from ._4842 import StraightBevelSunGearCompoundModalAnalysis
    from ._4843 import SynchroniserCompoundModalAnalysis
    from ._4844 import SynchroniserHalfCompoundModalAnalysis
    from ._4845 import SynchroniserPartCompoundModalAnalysis
    from ._4846 import SynchroniserSleeveCompoundModalAnalysis
    from ._4847 import TorqueConverterCompoundModalAnalysis
    from ._4848 import TorqueConverterConnectionCompoundModalAnalysis
    from ._4849 import TorqueConverterPumpCompoundModalAnalysis
    from ._4850 import TorqueConverterTurbineCompoundModalAnalysis
    from ._4851 import UnbalancedMassCompoundModalAnalysis
    from ._4852 import VirtualComponentCompoundModalAnalysis
    from ._4853 import WormGearCompoundModalAnalysis
    from ._4854 import WormGearMeshCompoundModalAnalysis
    from ._4855 import WormGearSetCompoundModalAnalysis
    from ._4856 import ZerolBevelGearCompoundModalAnalysis
    from ._4857 import ZerolBevelGearMeshCompoundModalAnalysis
    from ._4858 import ZerolBevelGearSetCompoundModalAnalysis
else:
    import_structure = {
        "_4730": ["AbstractAssemblyCompoundModalAnalysis"],
        "_4731": ["AbstractShaftCompoundModalAnalysis"],
        "_4732": ["AbstractShaftOrHousingCompoundModalAnalysis"],
        "_4733": ["AbstractShaftToMountableComponentConnectionCompoundModalAnalysis"],
        "_4734": ["AGMAGleasonConicalGearCompoundModalAnalysis"],
        "_4735": ["AGMAGleasonConicalGearMeshCompoundModalAnalysis"],
        "_4736": ["AGMAGleasonConicalGearSetCompoundModalAnalysis"],
        "_4737": ["AssemblyCompoundModalAnalysis"],
        "_4738": ["BearingCompoundModalAnalysis"],
        "_4739": ["BeltConnectionCompoundModalAnalysis"],
        "_4740": ["BeltDriveCompoundModalAnalysis"],
        "_4741": ["BevelDifferentialGearCompoundModalAnalysis"],
        "_4742": ["BevelDifferentialGearMeshCompoundModalAnalysis"],
        "_4743": ["BevelDifferentialGearSetCompoundModalAnalysis"],
        "_4744": ["BevelDifferentialPlanetGearCompoundModalAnalysis"],
        "_4745": ["BevelDifferentialSunGearCompoundModalAnalysis"],
        "_4746": ["BevelGearCompoundModalAnalysis"],
        "_4747": ["BevelGearMeshCompoundModalAnalysis"],
        "_4748": ["BevelGearSetCompoundModalAnalysis"],
        "_4749": ["BoltCompoundModalAnalysis"],
        "_4750": ["BoltedJointCompoundModalAnalysis"],
        "_4751": ["ClutchCompoundModalAnalysis"],
        "_4752": ["ClutchConnectionCompoundModalAnalysis"],
        "_4753": ["ClutchHalfCompoundModalAnalysis"],
        "_4754": ["CoaxialConnectionCompoundModalAnalysis"],
        "_4755": ["ComponentCompoundModalAnalysis"],
        "_4756": ["ConceptCouplingCompoundModalAnalysis"],
        "_4757": ["ConceptCouplingConnectionCompoundModalAnalysis"],
        "_4758": ["ConceptCouplingHalfCompoundModalAnalysis"],
        "_4759": ["ConceptGearCompoundModalAnalysis"],
        "_4760": ["ConceptGearMeshCompoundModalAnalysis"],
        "_4761": ["ConceptGearSetCompoundModalAnalysis"],
        "_4762": ["ConicalGearCompoundModalAnalysis"],
        "_4763": ["ConicalGearMeshCompoundModalAnalysis"],
        "_4764": ["ConicalGearSetCompoundModalAnalysis"],
        "_4765": ["ConnectionCompoundModalAnalysis"],
        "_4766": ["ConnectorCompoundModalAnalysis"],
        "_4767": ["CouplingCompoundModalAnalysis"],
        "_4768": ["CouplingConnectionCompoundModalAnalysis"],
        "_4769": ["CouplingHalfCompoundModalAnalysis"],
        "_4770": ["CVTBeltConnectionCompoundModalAnalysis"],
        "_4771": ["CVTCompoundModalAnalysis"],
        "_4772": ["CVTPulleyCompoundModalAnalysis"],
        "_4773": ["CycloidalAssemblyCompoundModalAnalysis"],
        "_4774": ["CycloidalDiscCentralBearingConnectionCompoundModalAnalysis"],
        "_4775": ["CycloidalDiscCompoundModalAnalysis"],
        "_4776": ["CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis"],
        "_4777": ["CylindricalGearCompoundModalAnalysis"],
        "_4778": ["CylindricalGearMeshCompoundModalAnalysis"],
        "_4779": ["CylindricalGearSetCompoundModalAnalysis"],
        "_4780": ["CylindricalPlanetGearCompoundModalAnalysis"],
        "_4781": ["DatumCompoundModalAnalysis"],
        "_4782": ["ExternalCADModelCompoundModalAnalysis"],
        "_4783": ["FaceGearCompoundModalAnalysis"],
        "_4784": ["FaceGearMeshCompoundModalAnalysis"],
        "_4785": ["FaceGearSetCompoundModalAnalysis"],
        "_4786": ["FEPartCompoundModalAnalysis"],
        "_4787": ["FlexiblePinAssemblyCompoundModalAnalysis"],
        "_4788": ["GearCompoundModalAnalysis"],
        "_4789": ["GearMeshCompoundModalAnalysis"],
        "_4790": ["GearSetCompoundModalAnalysis"],
        "_4791": ["GuideDxfModelCompoundModalAnalysis"],
        "_4792": ["HypoidGearCompoundModalAnalysis"],
        "_4793": ["HypoidGearMeshCompoundModalAnalysis"],
        "_4794": ["HypoidGearSetCompoundModalAnalysis"],
        "_4795": ["InterMountableComponentConnectionCompoundModalAnalysis"],
        "_4796": ["KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis"],
        "_4797": ["KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis"],
        "_4798": ["KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis"],
        "_4799": ["KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis"],
        "_4800": ["KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis"],
        "_4801": ["KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis"],
        "_4802": ["KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis"],
        "_4803": ["KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis"],
        "_4804": ["KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis"],
        "_4805": ["MassDiscCompoundModalAnalysis"],
        "_4806": ["MeasurementComponentCompoundModalAnalysis"],
        "_4807": ["MountableComponentCompoundModalAnalysis"],
        "_4808": ["OilSealCompoundModalAnalysis"],
        "_4809": ["PartCompoundModalAnalysis"],
        "_4810": ["PartToPartShearCouplingCompoundModalAnalysis"],
        "_4811": ["PartToPartShearCouplingConnectionCompoundModalAnalysis"],
        "_4812": ["PartToPartShearCouplingHalfCompoundModalAnalysis"],
        "_4813": ["PlanetaryConnectionCompoundModalAnalysis"],
        "_4814": ["PlanetaryGearSetCompoundModalAnalysis"],
        "_4815": ["PlanetCarrierCompoundModalAnalysis"],
        "_4816": ["PointLoadCompoundModalAnalysis"],
        "_4817": ["PowerLoadCompoundModalAnalysis"],
        "_4818": ["PulleyCompoundModalAnalysis"],
        "_4819": ["RingPinsCompoundModalAnalysis"],
        "_4820": ["RingPinsToDiscConnectionCompoundModalAnalysis"],
        "_4821": ["RollingRingAssemblyCompoundModalAnalysis"],
        "_4822": ["RollingRingCompoundModalAnalysis"],
        "_4823": ["RollingRingConnectionCompoundModalAnalysis"],
        "_4824": ["RootAssemblyCompoundModalAnalysis"],
        "_4825": ["ShaftCompoundModalAnalysis"],
        "_4826": ["ShaftHubConnectionCompoundModalAnalysis"],
        "_4827": ["ShaftToMountableComponentConnectionCompoundModalAnalysis"],
        "_4828": ["SpecialisedAssemblyCompoundModalAnalysis"],
        "_4829": ["SpiralBevelGearCompoundModalAnalysis"],
        "_4830": ["SpiralBevelGearMeshCompoundModalAnalysis"],
        "_4831": ["SpiralBevelGearSetCompoundModalAnalysis"],
        "_4832": ["SpringDamperCompoundModalAnalysis"],
        "_4833": ["SpringDamperConnectionCompoundModalAnalysis"],
        "_4834": ["SpringDamperHalfCompoundModalAnalysis"],
        "_4835": ["StraightBevelDiffGearCompoundModalAnalysis"],
        "_4836": ["StraightBevelDiffGearMeshCompoundModalAnalysis"],
        "_4837": ["StraightBevelDiffGearSetCompoundModalAnalysis"],
        "_4838": ["StraightBevelGearCompoundModalAnalysis"],
        "_4839": ["StraightBevelGearMeshCompoundModalAnalysis"],
        "_4840": ["StraightBevelGearSetCompoundModalAnalysis"],
        "_4841": ["StraightBevelPlanetGearCompoundModalAnalysis"],
        "_4842": ["StraightBevelSunGearCompoundModalAnalysis"],
        "_4843": ["SynchroniserCompoundModalAnalysis"],
        "_4844": ["SynchroniserHalfCompoundModalAnalysis"],
        "_4845": ["SynchroniserPartCompoundModalAnalysis"],
        "_4846": ["SynchroniserSleeveCompoundModalAnalysis"],
        "_4847": ["TorqueConverterCompoundModalAnalysis"],
        "_4848": ["TorqueConverterConnectionCompoundModalAnalysis"],
        "_4849": ["TorqueConverterPumpCompoundModalAnalysis"],
        "_4850": ["TorqueConverterTurbineCompoundModalAnalysis"],
        "_4851": ["UnbalancedMassCompoundModalAnalysis"],
        "_4852": ["VirtualComponentCompoundModalAnalysis"],
        "_4853": ["WormGearCompoundModalAnalysis"],
        "_4854": ["WormGearMeshCompoundModalAnalysis"],
        "_4855": ["WormGearSetCompoundModalAnalysis"],
        "_4856": ["ZerolBevelGearCompoundModalAnalysis"],
        "_4857": ["ZerolBevelGearMeshCompoundModalAnalysis"],
        "_4858": ["ZerolBevelGearSetCompoundModalAnalysis"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundModalAnalysis",
    "AbstractShaftCompoundModalAnalysis",
    "AbstractShaftOrHousingCompoundModalAnalysis",
    "AbstractShaftToMountableComponentConnectionCompoundModalAnalysis",
    "AGMAGleasonConicalGearCompoundModalAnalysis",
    "AGMAGleasonConicalGearMeshCompoundModalAnalysis",
    "AGMAGleasonConicalGearSetCompoundModalAnalysis",
    "AssemblyCompoundModalAnalysis",
    "BearingCompoundModalAnalysis",
    "BeltConnectionCompoundModalAnalysis",
    "BeltDriveCompoundModalAnalysis",
    "BevelDifferentialGearCompoundModalAnalysis",
    "BevelDifferentialGearMeshCompoundModalAnalysis",
    "BevelDifferentialGearSetCompoundModalAnalysis",
    "BevelDifferentialPlanetGearCompoundModalAnalysis",
    "BevelDifferentialSunGearCompoundModalAnalysis",
    "BevelGearCompoundModalAnalysis",
    "BevelGearMeshCompoundModalAnalysis",
    "BevelGearSetCompoundModalAnalysis",
    "BoltCompoundModalAnalysis",
    "BoltedJointCompoundModalAnalysis",
    "ClutchCompoundModalAnalysis",
    "ClutchConnectionCompoundModalAnalysis",
    "ClutchHalfCompoundModalAnalysis",
    "CoaxialConnectionCompoundModalAnalysis",
    "ComponentCompoundModalAnalysis",
    "ConceptCouplingCompoundModalAnalysis",
    "ConceptCouplingConnectionCompoundModalAnalysis",
    "ConceptCouplingHalfCompoundModalAnalysis",
    "ConceptGearCompoundModalAnalysis",
    "ConceptGearMeshCompoundModalAnalysis",
    "ConceptGearSetCompoundModalAnalysis",
    "ConicalGearCompoundModalAnalysis",
    "ConicalGearMeshCompoundModalAnalysis",
    "ConicalGearSetCompoundModalAnalysis",
    "ConnectionCompoundModalAnalysis",
    "ConnectorCompoundModalAnalysis",
    "CouplingCompoundModalAnalysis",
    "CouplingConnectionCompoundModalAnalysis",
    "CouplingHalfCompoundModalAnalysis",
    "CVTBeltConnectionCompoundModalAnalysis",
    "CVTCompoundModalAnalysis",
    "CVTPulleyCompoundModalAnalysis",
    "CycloidalAssemblyCompoundModalAnalysis",
    "CycloidalDiscCentralBearingConnectionCompoundModalAnalysis",
    "CycloidalDiscCompoundModalAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysis",
    "CylindricalGearCompoundModalAnalysis",
    "CylindricalGearMeshCompoundModalAnalysis",
    "CylindricalGearSetCompoundModalAnalysis",
    "CylindricalPlanetGearCompoundModalAnalysis",
    "DatumCompoundModalAnalysis",
    "ExternalCADModelCompoundModalAnalysis",
    "FaceGearCompoundModalAnalysis",
    "FaceGearMeshCompoundModalAnalysis",
    "FaceGearSetCompoundModalAnalysis",
    "FEPartCompoundModalAnalysis",
    "FlexiblePinAssemblyCompoundModalAnalysis",
    "GearCompoundModalAnalysis",
    "GearMeshCompoundModalAnalysis",
    "GearSetCompoundModalAnalysis",
    "GuideDxfModelCompoundModalAnalysis",
    "HypoidGearCompoundModalAnalysis",
    "HypoidGearMeshCompoundModalAnalysis",
    "HypoidGearSetCompoundModalAnalysis",
    "InterMountableComponentConnectionCompoundModalAnalysis",
    "KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis",
    "KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis",
    "MassDiscCompoundModalAnalysis",
    "MeasurementComponentCompoundModalAnalysis",
    "MountableComponentCompoundModalAnalysis",
    "OilSealCompoundModalAnalysis",
    "PartCompoundModalAnalysis",
    "PartToPartShearCouplingCompoundModalAnalysis",
    "PartToPartShearCouplingConnectionCompoundModalAnalysis",
    "PartToPartShearCouplingHalfCompoundModalAnalysis",
    "PlanetaryConnectionCompoundModalAnalysis",
    "PlanetaryGearSetCompoundModalAnalysis",
    "PlanetCarrierCompoundModalAnalysis",
    "PointLoadCompoundModalAnalysis",
    "PowerLoadCompoundModalAnalysis",
    "PulleyCompoundModalAnalysis",
    "RingPinsCompoundModalAnalysis",
    "RingPinsToDiscConnectionCompoundModalAnalysis",
    "RollingRingAssemblyCompoundModalAnalysis",
    "RollingRingCompoundModalAnalysis",
    "RollingRingConnectionCompoundModalAnalysis",
    "RootAssemblyCompoundModalAnalysis",
    "ShaftCompoundModalAnalysis",
    "ShaftHubConnectionCompoundModalAnalysis",
    "ShaftToMountableComponentConnectionCompoundModalAnalysis",
    "SpecialisedAssemblyCompoundModalAnalysis",
    "SpiralBevelGearCompoundModalAnalysis",
    "SpiralBevelGearMeshCompoundModalAnalysis",
    "SpiralBevelGearSetCompoundModalAnalysis",
    "SpringDamperCompoundModalAnalysis",
    "SpringDamperConnectionCompoundModalAnalysis",
    "SpringDamperHalfCompoundModalAnalysis",
    "StraightBevelDiffGearCompoundModalAnalysis",
    "StraightBevelDiffGearMeshCompoundModalAnalysis",
    "StraightBevelDiffGearSetCompoundModalAnalysis",
    "StraightBevelGearCompoundModalAnalysis",
    "StraightBevelGearMeshCompoundModalAnalysis",
    "StraightBevelGearSetCompoundModalAnalysis",
    "StraightBevelPlanetGearCompoundModalAnalysis",
    "StraightBevelSunGearCompoundModalAnalysis",
    "SynchroniserCompoundModalAnalysis",
    "SynchroniserHalfCompoundModalAnalysis",
    "SynchroniserPartCompoundModalAnalysis",
    "SynchroniserSleeveCompoundModalAnalysis",
    "TorqueConverterCompoundModalAnalysis",
    "TorqueConverterConnectionCompoundModalAnalysis",
    "TorqueConverterPumpCompoundModalAnalysis",
    "TorqueConverterTurbineCompoundModalAnalysis",
    "UnbalancedMassCompoundModalAnalysis",
    "VirtualComponentCompoundModalAnalysis",
    "WormGearCompoundModalAnalysis",
    "WormGearMeshCompoundModalAnalysis",
    "WormGearSetCompoundModalAnalysis",
    "ZerolBevelGearCompoundModalAnalysis",
    "ZerolBevelGearMeshCompoundModalAnalysis",
    "ZerolBevelGearSetCompoundModalAnalysis",
)
