"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._3765 import AbstractAssemblyStabilityAnalysis
    from ._3766 import AbstractShaftOrHousingStabilityAnalysis
    from ._3767 import AbstractShaftStabilityAnalysis
    from ._3768 import AbstractShaftToMountableComponentConnectionStabilityAnalysis
    from ._3769 import AGMAGleasonConicalGearMeshStabilityAnalysis
    from ._3770 import AGMAGleasonConicalGearSetStabilityAnalysis
    from ._3771 import AGMAGleasonConicalGearStabilityAnalysis
    from ._3772 import AssemblyStabilityAnalysis
    from ._3773 import BearingStabilityAnalysis
    from ._3774 import BeltConnectionStabilityAnalysis
    from ._3775 import BeltDriveStabilityAnalysis
    from ._3776 import BevelDifferentialGearMeshStabilityAnalysis
    from ._3777 import BevelDifferentialGearSetStabilityAnalysis
    from ._3778 import BevelDifferentialGearStabilityAnalysis
    from ._3779 import BevelDifferentialPlanetGearStabilityAnalysis
    from ._3780 import BevelDifferentialSunGearStabilityAnalysis
    from ._3781 import BevelGearMeshStabilityAnalysis
    from ._3782 import BevelGearSetStabilityAnalysis
    from ._3783 import BevelGearStabilityAnalysis
    from ._3784 import BoltedJointStabilityAnalysis
    from ._3785 import BoltStabilityAnalysis
    from ._3786 import ClutchConnectionStabilityAnalysis
    from ._3787 import ClutchHalfStabilityAnalysis
    from ._3788 import ClutchStabilityAnalysis
    from ._3789 import CoaxialConnectionStabilityAnalysis
    from ._3790 import ComponentStabilityAnalysis
    from ._3791 import ConceptCouplingConnectionStabilityAnalysis
    from ._3792 import ConceptCouplingHalfStabilityAnalysis
    from ._3793 import ConceptCouplingStabilityAnalysis
    from ._3794 import ConceptGearMeshStabilityAnalysis
    from ._3795 import ConceptGearSetStabilityAnalysis
    from ._3796 import ConceptGearStabilityAnalysis
    from ._3797 import ConicalGearMeshStabilityAnalysis
    from ._3798 import ConicalGearSetStabilityAnalysis
    from ._3799 import ConicalGearStabilityAnalysis
    from ._3800 import ConnectionStabilityAnalysis
    from ._3801 import ConnectorStabilityAnalysis
    from ._3802 import CouplingConnectionStabilityAnalysis
    from ._3803 import CouplingHalfStabilityAnalysis
    from ._3804 import CouplingStabilityAnalysis
    from ._3805 import CriticalSpeed
    from ._3806 import CVTBeltConnectionStabilityAnalysis
    from ._3807 import CVTPulleyStabilityAnalysis
    from ._3808 import CVTStabilityAnalysis
    from ._3809 import CycloidalAssemblyStabilityAnalysis
    from ._3810 import CycloidalDiscCentralBearingConnectionStabilityAnalysis
    from ._3811 import CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis
    from ._3812 import CycloidalDiscStabilityAnalysis
    from ._3813 import CylindricalGearMeshStabilityAnalysis
    from ._3814 import CylindricalGearSetStabilityAnalysis
    from ._3815 import CylindricalGearStabilityAnalysis
    from ._3816 import CylindricalPlanetGearStabilityAnalysis
    from ._3817 import DatumStabilityAnalysis
    from ._3818 import DynamicModelForStabilityAnalysis
    from ._3819 import ExternalCADModelStabilityAnalysis
    from ._3820 import FaceGearMeshStabilityAnalysis
    from ._3821 import FaceGearSetStabilityAnalysis
    from ._3822 import FaceGearStabilityAnalysis
    from ._3823 import FEPartStabilityAnalysis
    from ._3824 import FlexiblePinAssemblyStabilityAnalysis
    from ._3825 import GearMeshStabilityAnalysis
    from ._3826 import GearSetStabilityAnalysis
    from ._3827 import GearStabilityAnalysis
    from ._3828 import GuideDxfModelStabilityAnalysis
    from ._3829 import HypoidGearMeshStabilityAnalysis
    from ._3830 import HypoidGearSetStabilityAnalysis
    from ._3831 import HypoidGearStabilityAnalysis
    from ._3832 import InterMountableComponentConnectionStabilityAnalysis
    from ._3833 import KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
    from ._3834 import KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
    from ._3835 import KlingelnbergCycloPalloidConicalGearStabilityAnalysis
    from ._3836 import KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis
    from ._3837 import KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis
    from ._3838 import KlingelnbergCycloPalloidHypoidGearStabilityAnalysis
    from ._3839 import KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis
    from ._3840 import KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis
    from ._3841 import KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis
    from ._3842 import MassDiscStabilityAnalysis
    from ._3843 import MeasurementComponentStabilityAnalysis
    from ._3844 import MountableComponentStabilityAnalysis
    from ._3845 import OilSealStabilityAnalysis
    from ._3846 import PartStabilityAnalysis
    from ._3847 import PartToPartShearCouplingConnectionStabilityAnalysis
    from ._3848 import PartToPartShearCouplingHalfStabilityAnalysis
    from ._3849 import PartToPartShearCouplingStabilityAnalysis
    from ._3850 import PlanetaryConnectionStabilityAnalysis
    from ._3851 import PlanetaryGearSetStabilityAnalysis
    from ._3852 import PlanetCarrierStabilityAnalysis
    from ._3853 import PointLoadStabilityAnalysis
    from ._3854 import PowerLoadStabilityAnalysis
    from ._3855 import PulleyStabilityAnalysis
    from ._3856 import RingPinsStabilityAnalysis
    from ._3857 import RingPinsToDiscConnectionStabilityAnalysis
    from ._3858 import RollingRingAssemblyStabilityAnalysis
    from ._3859 import RollingRingConnectionStabilityAnalysis
    from ._3860 import RollingRingStabilityAnalysis
    from ._3861 import RootAssemblyStabilityAnalysis
    from ._3862 import ShaftHubConnectionStabilityAnalysis
    from ._3863 import ShaftStabilityAnalysis
    from ._3864 import ShaftToMountableComponentConnectionStabilityAnalysis
    from ._3865 import SpecialisedAssemblyStabilityAnalysis
    from ._3866 import SpiralBevelGearMeshStabilityAnalysis
    from ._3867 import SpiralBevelGearSetStabilityAnalysis
    from ._3868 import SpiralBevelGearStabilityAnalysis
    from ._3869 import SpringDamperConnectionStabilityAnalysis
    from ._3870 import SpringDamperHalfStabilityAnalysis
    from ._3871 import SpringDamperStabilityAnalysis
    from ._3872 import StabilityAnalysis
    from ._3873 import StabilityAnalysisDrawStyle
    from ._3874 import StabilityAnalysisOptions
    from ._3875 import StraightBevelDiffGearMeshStabilityAnalysis
    from ._3876 import StraightBevelDiffGearSetStabilityAnalysis
    from ._3877 import StraightBevelDiffGearStabilityAnalysis
    from ._3878 import StraightBevelGearMeshStabilityAnalysis
    from ._3879 import StraightBevelGearSetStabilityAnalysis
    from ._3880 import StraightBevelGearStabilityAnalysis
    from ._3881 import StraightBevelPlanetGearStabilityAnalysis
    from ._3882 import StraightBevelSunGearStabilityAnalysis
    from ._3883 import SynchroniserHalfStabilityAnalysis
    from ._3884 import SynchroniserPartStabilityAnalysis
    from ._3885 import SynchroniserSleeveStabilityAnalysis
    from ._3886 import SynchroniserStabilityAnalysis
    from ._3887 import TorqueConverterConnectionStabilityAnalysis
    from ._3888 import TorqueConverterPumpStabilityAnalysis
    from ._3889 import TorqueConverterStabilityAnalysis
    from ._3890 import TorqueConverterTurbineStabilityAnalysis
    from ._3891 import UnbalancedMassStabilityAnalysis
    from ._3892 import VirtualComponentStabilityAnalysis
    from ._3893 import WormGearMeshStabilityAnalysis
    from ._3894 import WormGearSetStabilityAnalysis
    from ._3895 import WormGearStabilityAnalysis
    from ._3896 import ZerolBevelGearMeshStabilityAnalysis
    from ._3897 import ZerolBevelGearSetStabilityAnalysis
    from ._3898 import ZerolBevelGearStabilityAnalysis
else:
    import_structure = {
        "_3765": ["AbstractAssemblyStabilityAnalysis"],
        "_3766": ["AbstractShaftOrHousingStabilityAnalysis"],
        "_3767": ["AbstractShaftStabilityAnalysis"],
        "_3768": ["AbstractShaftToMountableComponentConnectionStabilityAnalysis"],
        "_3769": ["AGMAGleasonConicalGearMeshStabilityAnalysis"],
        "_3770": ["AGMAGleasonConicalGearSetStabilityAnalysis"],
        "_3771": ["AGMAGleasonConicalGearStabilityAnalysis"],
        "_3772": ["AssemblyStabilityAnalysis"],
        "_3773": ["BearingStabilityAnalysis"],
        "_3774": ["BeltConnectionStabilityAnalysis"],
        "_3775": ["BeltDriveStabilityAnalysis"],
        "_3776": ["BevelDifferentialGearMeshStabilityAnalysis"],
        "_3777": ["BevelDifferentialGearSetStabilityAnalysis"],
        "_3778": ["BevelDifferentialGearStabilityAnalysis"],
        "_3779": ["BevelDifferentialPlanetGearStabilityAnalysis"],
        "_3780": ["BevelDifferentialSunGearStabilityAnalysis"],
        "_3781": ["BevelGearMeshStabilityAnalysis"],
        "_3782": ["BevelGearSetStabilityAnalysis"],
        "_3783": ["BevelGearStabilityAnalysis"],
        "_3784": ["BoltedJointStabilityAnalysis"],
        "_3785": ["BoltStabilityAnalysis"],
        "_3786": ["ClutchConnectionStabilityAnalysis"],
        "_3787": ["ClutchHalfStabilityAnalysis"],
        "_3788": ["ClutchStabilityAnalysis"],
        "_3789": ["CoaxialConnectionStabilityAnalysis"],
        "_3790": ["ComponentStabilityAnalysis"],
        "_3791": ["ConceptCouplingConnectionStabilityAnalysis"],
        "_3792": ["ConceptCouplingHalfStabilityAnalysis"],
        "_3793": ["ConceptCouplingStabilityAnalysis"],
        "_3794": ["ConceptGearMeshStabilityAnalysis"],
        "_3795": ["ConceptGearSetStabilityAnalysis"],
        "_3796": ["ConceptGearStabilityAnalysis"],
        "_3797": ["ConicalGearMeshStabilityAnalysis"],
        "_3798": ["ConicalGearSetStabilityAnalysis"],
        "_3799": ["ConicalGearStabilityAnalysis"],
        "_3800": ["ConnectionStabilityAnalysis"],
        "_3801": ["ConnectorStabilityAnalysis"],
        "_3802": ["CouplingConnectionStabilityAnalysis"],
        "_3803": ["CouplingHalfStabilityAnalysis"],
        "_3804": ["CouplingStabilityAnalysis"],
        "_3805": ["CriticalSpeed"],
        "_3806": ["CVTBeltConnectionStabilityAnalysis"],
        "_3807": ["CVTPulleyStabilityAnalysis"],
        "_3808": ["CVTStabilityAnalysis"],
        "_3809": ["CycloidalAssemblyStabilityAnalysis"],
        "_3810": ["CycloidalDiscCentralBearingConnectionStabilityAnalysis"],
        "_3811": ["CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis"],
        "_3812": ["CycloidalDiscStabilityAnalysis"],
        "_3813": ["CylindricalGearMeshStabilityAnalysis"],
        "_3814": ["CylindricalGearSetStabilityAnalysis"],
        "_3815": ["CylindricalGearStabilityAnalysis"],
        "_3816": ["CylindricalPlanetGearStabilityAnalysis"],
        "_3817": ["DatumStabilityAnalysis"],
        "_3818": ["DynamicModelForStabilityAnalysis"],
        "_3819": ["ExternalCADModelStabilityAnalysis"],
        "_3820": ["FaceGearMeshStabilityAnalysis"],
        "_3821": ["FaceGearSetStabilityAnalysis"],
        "_3822": ["FaceGearStabilityAnalysis"],
        "_3823": ["FEPartStabilityAnalysis"],
        "_3824": ["FlexiblePinAssemblyStabilityAnalysis"],
        "_3825": ["GearMeshStabilityAnalysis"],
        "_3826": ["GearSetStabilityAnalysis"],
        "_3827": ["GearStabilityAnalysis"],
        "_3828": ["GuideDxfModelStabilityAnalysis"],
        "_3829": ["HypoidGearMeshStabilityAnalysis"],
        "_3830": ["HypoidGearSetStabilityAnalysis"],
        "_3831": ["HypoidGearStabilityAnalysis"],
        "_3832": ["InterMountableComponentConnectionStabilityAnalysis"],
        "_3833": ["KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"],
        "_3834": ["KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis"],
        "_3835": ["KlingelnbergCycloPalloidConicalGearStabilityAnalysis"],
        "_3836": ["KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis"],
        "_3837": ["KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis"],
        "_3838": ["KlingelnbergCycloPalloidHypoidGearStabilityAnalysis"],
        "_3839": ["KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis"],
        "_3840": ["KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis"],
        "_3841": ["KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis"],
        "_3842": ["MassDiscStabilityAnalysis"],
        "_3843": ["MeasurementComponentStabilityAnalysis"],
        "_3844": ["MountableComponentStabilityAnalysis"],
        "_3845": ["OilSealStabilityAnalysis"],
        "_3846": ["PartStabilityAnalysis"],
        "_3847": ["PartToPartShearCouplingConnectionStabilityAnalysis"],
        "_3848": ["PartToPartShearCouplingHalfStabilityAnalysis"],
        "_3849": ["PartToPartShearCouplingStabilityAnalysis"],
        "_3850": ["PlanetaryConnectionStabilityAnalysis"],
        "_3851": ["PlanetaryGearSetStabilityAnalysis"],
        "_3852": ["PlanetCarrierStabilityAnalysis"],
        "_3853": ["PointLoadStabilityAnalysis"],
        "_3854": ["PowerLoadStabilityAnalysis"],
        "_3855": ["PulleyStabilityAnalysis"],
        "_3856": ["RingPinsStabilityAnalysis"],
        "_3857": ["RingPinsToDiscConnectionStabilityAnalysis"],
        "_3858": ["RollingRingAssemblyStabilityAnalysis"],
        "_3859": ["RollingRingConnectionStabilityAnalysis"],
        "_3860": ["RollingRingStabilityAnalysis"],
        "_3861": ["RootAssemblyStabilityAnalysis"],
        "_3862": ["ShaftHubConnectionStabilityAnalysis"],
        "_3863": ["ShaftStabilityAnalysis"],
        "_3864": ["ShaftToMountableComponentConnectionStabilityAnalysis"],
        "_3865": ["SpecialisedAssemblyStabilityAnalysis"],
        "_3866": ["SpiralBevelGearMeshStabilityAnalysis"],
        "_3867": ["SpiralBevelGearSetStabilityAnalysis"],
        "_3868": ["SpiralBevelGearStabilityAnalysis"],
        "_3869": ["SpringDamperConnectionStabilityAnalysis"],
        "_3870": ["SpringDamperHalfStabilityAnalysis"],
        "_3871": ["SpringDamperStabilityAnalysis"],
        "_3872": ["StabilityAnalysis"],
        "_3873": ["StabilityAnalysisDrawStyle"],
        "_3874": ["StabilityAnalysisOptions"],
        "_3875": ["StraightBevelDiffGearMeshStabilityAnalysis"],
        "_3876": ["StraightBevelDiffGearSetStabilityAnalysis"],
        "_3877": ["StraightBevelDiffGearStabilityAnalysis"],
        "_3878": ["StraightBevelGearMeshStabilityAnalysis"],
        "_3879": ["StraightBevelGearSetStabilityAnalysis"],
        "_3880": ["StraightBevelGearStabilityAnalysis"],
        "_3881": ["StraightBevelPlanetGearStabilityAnalysis"],
        "_3882": ["StraightBevelSunGearStabilityAnalysis"],
        "_3883": ["SynchroniserHalfStabilityAnalysis"],
        "_3884": ["SynchroniserPartStabilityAnalysis"],
        "_3885": ["SynchroniserSleeveStabilityAnalysis"],
        "_3886": ["SynchroniserStabilityAnalysis"],
        "_3887": ["TorqueConverterConnectionStabilityAnalysis"],
        "_3888": ["TorqueConverterPumpStabilityAnalysis"],
        "_3889": ["TorqueConverterStabilityAnalysis"],
        "_3890": ["TorqueConverterTurbineStabilityAnalysis"],
        "_3891": ["UnbalancedMassStabilityAnalysis"],
        "_3892": ["VirtualComponentStabilityAnalysis"],
        "_3893": ["WormGearMeshStabilityAnalysis"],
        "_3894": ["WormGearSetStabilityAnalysis"],
        "_3895": ["WormGearStabilityAnalysis"],
        "_3896": ["ZerolBevelGearMeshStabilityAnalysis"],
        "_3897": ["ZerolBevelGearSetStabilityAnalysis"],
        "_3898": ["ZerolBevelGearStabilityAnalysis"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyStabilityAnalysis",
    "AbstractShaftOrHousingStabilityAnalysis",
    "AbstractShaftStabilityAnalysis",
    "AbstractShaftToMountableComponentConnectionStabilityAnalysis",
    "AGMAGleasonConicalGearMeshStabilityAnalysis",
    "AGMAGleasonConicalGearSetStabilityAnalysis",
    "AGMAGleasonConicalGearStabilityAnalysis",
    "AssemblyStabilityAnalysis",
    "BearingStabilityAnalysis",
    "BeltConnectionStabilityAnalysis",
    "BeltDriveStabilityAnalysis",
    "BevelDifferentialGearMeshStabilityAnalysis",
    "BevelDifferentialGearSetStabilityAnalysis",
    "BevelDifferentialGearStabilityAnalysis",
    "BevelDifferentialPlanetGearStabilityAnalysis",
    "BevelDifferentialSunGearStabilityAnalysis",
    "BevelGearMeshStabilityAnalysis",
    "BevelGearSetStabilityAnalysis",
    "BevelGearStabilityAnalysis",
    "BoltedJointStabilityAnalysis",
    "BoltStabilityAnalysis",
    "ClutchConnectionStabilityAnalysis",
    "ClutchHalfStabilityAnalysis",
    "ClutchStabilityAnalysis",
    "CoaxialConnectionStabilityAnalysis",
    "ComponentStabilityAnalysis",
    "ConceptCouplingConnectionStabilityAnalysis",
    "ConceptCouplingHalfStabilityAnalysis",
    "ConceptCouplingStabilityAnalysis",
    "ConceptGearMeshStabilityAnalysis",
    "ConceptGearSetStabilityAnalysis",
    "ConceptGearStabilityAnalysis",
    "ConicalGearMeshStabilityAnalysis",
    "ConicalGearSetStabilityAnalysis",
    "ConicalGearStabilityAnalysis",
    "ConnectionStabilityAnalysis",
    "ConnectorStabilityAnalysis",
    "CouplingConnectionStabilityAnalysis",
    "CouplingHalfStabilityAnalysis",
    "CouplingStabilityAnalysis",
    "CriticalSpeed",
    "CVTBeltConnectionStabilityAnalysis",
    "CVTPulleyStabilityAnalysis",
    "CVTStabilityAnalysis",
    "CycloidalAssemblyStabilityAnalysis",
    "CycloidalDiscCentralBearingConnectionStabilityAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis",
    "CycloidalDiscStabilityAnalysis",
    "CylindricalGearMeshStabilityAnalysis",
    "CylindricalGearSetStabilityAnalysis",
    "CylindricalGearStabilityAnalysis",
    "CylindricalPlanetGearStabilityAnalysis",
    "DatumStabilityAnalysis",
    "DynamicModelForStabilityAnalysis",
    "ExternalCADModelStabilityAnalysis",
    "FaceGearMeshStabilityAnalysis",
    "FaceGearSetStabilityAnalysis",
    "FaceGearStabilityAnalysis",
    "FEPartStabilityAnalysis",
    "FlexiblePinAssemblyStabilityAnalysis",
    "GearMeshStabilityAnalysis",
    "GearSetStabilityAnalysis",
    "GearStabilityAnalysis",
    "GuideDxfModelStabilityAnalysis",
    "HypoidGearMeshStabilityAnalysis",
    "HypoidGearSetStabilityAnalysis",
    "HypoidGearStabilityAnalysis",
    "InterMountableComponentConnectionStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidConicalGearStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidHypoidGearStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis",
    "MassDiscStabilityAnalysis",
    "MeasurementComponentStabilityAnalysis",
    "MountableComponentStabilityAnalysis",
    "OilSealStabilityAnalysis",
    "PartStabilityAnalysis",
    "PartToPartShearCouplingConnectionStabilityAnalysis",
    "PartToPartShearCouplingHalfStabilityAnalysis",
    "PartToPartShearCouplingStabilityAnalysis",
    "PlanetaryConnectionStabilityAnalysis",
    "PlanetaryGearSetStabilityAnalysis",
    "PlanetCarrierStabilityAnalysis",
    "PointLoadStabilityAnalysis",
    "PowerLoadStabilityAnalysis",
    "PulleyStabilityAnalysis",
    "RingPinsStabilityAnalysis",
    "RingPinsToDiscConnectionStabilityAnalysis",
    "RollingRingAssemblyStabilityAnalysis",
    "RollingRingConnectionStabilityAnalysis",
    "RollingRingStabilityAnalysis",
    "RootAssemblyStabilityAnalysis",
    "ShaftHubConnectionStabilityAnalysis",
    "ShaftStabilityAnalysis",
    "ShaftToMountableComponentConnectionStabilityAnalysis",
    "SpecialisedAssemblyStabilityAnalysis",
    "SpiralBevelGearMeshStabilityAnalysis",
    "SpiralBevelGearSetStabilityAnalysis",
    "SpiralBevelGearStabilityAnalysis",
    "SpringDamperConnectionStabilityAnalysis",
    "SpringDamperHalfStabilityAnalysis",
    "SpringDamperStabilityAnalysis",
    "StabilityAnalysis",
    "StabilityAnalysisDrawStyle",
    "StabilityAnalysisOptions",
    "StraightBevelDiffGearMeshStabilityAnalysis",
    "StraightBevelDiffGearSetStabilityAnalysis",
    "StraightBevelDiffGearStabilityAnalysis",
    "StraightBevelGearMeshStabilityAnalysis",
    "StraightBevelGearSetStabilityAnalysis",
    "StraightBevelGearStabilityAnalysis",
    "StraightBevelPlanetGearStabilityAnalysis",
    "StraightBevelSunGearStabilityAnalysis",
    "SynchroniserHalfStabilityAnalysis",
    "SynchroniserPartStabilityAnalysis",
    "SynchroniserSleeveStabilityAnalysis",
    "SynchroniserStabilityAnalysis",
    "TorqueConverterConnectionStabilityAnalysis",
    "TorqueConverterPumpStabilityAnalysis",
    "TorqueConverterStabilityAnalysis",
    "TorqueConverterTurbineStabilityAnalysis",
    "UnbalancedMassStabilityAnalysis",
    "VirtualComponentStabilityAnalysis",
    "WormGearMeshStabilityAnalysis",
    "WormGearSetStabilityAnalysis",
    "WormGearStabilityAnalysis",
    "ZerolBevelGearMeshStabilityAnalysis",
    "ZerolBevelGearSetStabilityAnalysis",
    "ZerolBevelGearStabilityAnalysis",
)
