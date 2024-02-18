"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._6806 import LoadCase
    from ._6807 import StaticLoadCase
    from ._6808 import TimeSeriesLoadCase
    from ._6809 import AbstractAssemblyLoadCase
    from ._6810 import AbstractShaftLoadCase
    from ._6811 import AbstractShaftOrHousingLoadCase
    from ._6812 import AbstractShaftToMountableComponentConnectionLoadCase
    from ._6813 import AdditionalAccelerationOptions
    from ._6814 import AdvancedTimeSteppingAnalysisForModulationStaticLoadCase
    from ._6815 import AdvancedTimeSteppingAnalysisForModulationType
    from ._6816 import AGMAGleasonConicalGearLoadCase
    from ._6817 import AGMAGleasonConicalGearMeshLoadCase
    from ._6818 import AGMAGleasonConicalGearSetLoadCase
    from ._6819 import AllRingPinsManufacturingError
    from ._6820 import AnalysisType
    from ._6821 import AssemblyLoadCase
    from ._6822 import BearingLoadCase
    from ._6823 import BeltConnectionLoadCase
    from ._6824 import BeltDriveLoadCase
    from ._6825 import BevelDifferentialGearLoadCase
    from ._6826 import BevelDifferentialGearMeshLoadCase
    from ._6827 import BevelDifferentialGearSetLoadCase
    from ._6828 import BevelDifferentialPlanetGearLoadCase
    from ._6829 import BevelDifferentialSunGearLoadCase
    from ._6830 import BevelGearLoadCase
    from ._6831 import BevelGearMeshLoadCase
    from ._6832 import BevelGearSetLoadCase
    from ._6833 import BoltedJointLoadCase
    from ._6834 import BoltLoadCase
    from ._6835 import ClutchConnectionLoadCase
    from ._6836 import ClutchHalfLoadCase
    from ._6837 import ClutchLoadCase
    from ._6838 import CMSElementFaceGroupWithSelectionOption
    from ._6839 import CoaxialConnectionLoadCase
    from ._6840 import ComponentLoadCase
    from ._6841 import ConceptCouplingConnectionLoadCase
    from ._6842 import ConceptCouplingHalfLoadCase
    from ._6843 import ConceptCouplingLoadCase
    from ._6844 import ConceptGearLoadCase
    from ._6845 import ConceptGearMeshLoadCase
    from ._6846 import ConceptGearSetLoadCase
    from ._6847 import ConicalGearLoadCase
    from ._6848 import ConicalGearManufactureError
    from ._6849 import ConicalGearMeshLoadCase
    from ._6850 import ConicalGearSetHarmonicLoadData
    from ._6851 import ConicalGearSetLoadCase
    from ._6852 import ConnectionLoadCase
    from ._6853 import ConnectorLoadCase
    from ._6854 import CouplingConnectionLoadCase
    from ._6855 import CouplingHalfLoadCase
    from ._6856 import CouplingLoadCase
    from ._6857 import CVTBeltConnectionLoadCase
    from ._6858 import CVTLoadCase
    from ._6859 import CVTPulleyLoadCase
    from ._6860 import CycloidalAssemblyLoadCase
    from ._6861 import CycloidalDiscCentralBearingConnectionLoadCase
    from ._6862 import CycloidalDiscLoadCase
    from ._6863 import CycloidalDiscPlanetaryBearingConnectionLoadCase
    from ._6864 import CylindricalGearLoadCase
    from ._6865 import CylindricalGearManufactureError
    from ._6866 import CylindricalGearMeshLoadCase
    from ._6867 import CylindricalGearSetHarmonicLoadData
    from ._6868 import CylindricalGearSetLoadCase
    from ._6869 import CylindricalPlanetGearLoadCase
    from ._6870 import DataFromMotorPackagePerMeanTorque
    from ._6871 import DataFromMotorPackagePerSpeed
    from ._6872 import DatumLoadCase
    from ._6873 import ElectricMachineDataImportType
    from ._6874 import ElectricMachineHarmonicLoadData
    from ._6875 import ElectricMachineHarmonicLoadDataFromExcel
    from ._6876 import ElectricMachineHarmonicLoadDataFromFlux
    from ._6877 import ElectricMachineHarmonicLoadDataFromJMAG
    from ._6878 import ElectricMachineHarmonicLoadDataFromMASTA
    from ._6879 import ElectricMachineHarmonicLoadDataFromMotorCAD
    from ._6880 import ElectricMachineHarmonicLoadDataFromMotorPackages
    from ._6881 import ElectricMachineHarmonicLoadExcelImportOptions
    from ._6882 import ElectricMachineHarmonicLoadFluxImportOptions
    from ._6883 import ElectricMachineHarmonicLoadImportOptionsBase
    from ._6884 import ElectricMachineHarmonicLoadJMAGImportOptions
    from ._6885 import ElectricMachineHarmonicLoadMotorCADImportOptions
    from ._6886 import ExternalCADModelLoadCase
    from ._6887 import FaceGearLoadCase
    from ._6888 import FaceGearMeshLoadCase
    from ._6889 import FaceGearSetLoadCase
    from ._6890 import FEPartLoadCase
    from ._6891 import FlexiblePinAssemblyLoadCase
    from ._6892 import ForceAndTorqueScalingFactor
    from ._6893 import GearLoadCase
    from ._6894 import GearManufactureError
    from ._6895 import GearMeshLoadCase
    from ._6896 import GearMeshTEOrderType
    from ._6897 import GearSetHarmonicLoadData
    from ._6898 import GearSetLoadCase
    from ._6899 import GuideDxfModelLoadCase
    from ._6900 import HarmonicExcitationType
    from ._6901 import HarmonicLoadDataCSVImport
    from ._6902 import HarmonicLoadDataExcelImport
    from ._6903 import HarmonicLoadDataFluxImport
    from ._6904 import HarmonicLoadDataImportBase
    from ._6905 import HarmonicLoadDataImportFromMotorPackages
    from ._6906 import HarmonicLoadDataJMAGImport
    from ._6907 import HarmonicLoadDataMotorCADImport
    from ._6908 import HypoidGearLoadCase
    from ._6909 import HypoidGearMeshLoadCase
    from ._6910 import HypoidGearSetLoadCase
    from ._6911 import ImportType
    from ._6912 import InformationAtRingPinToDiscContactPointFromGeometry
    from ._6913 import InnerDiameterReference
    from ._6914 import InterMountableComponentConnectionLoadCase
    from ._6915 import KlingelnbergCycloPalloidConicalGearLoadCase
    from ._6916 import KlingelnbergCycloPalloidConicalGearMeshLoadCase
    from ._6917 import KlingelnbergCycloPalloidConicalGearSetLoadCase
    from ._6918 import KlingelnbergCycloPalloidHypoidGearLoadCase
    from ._6919 import KlingelnbergCycloPalloidHypoidGearMeshLoadCase
    from ._6920 import KlingelnbergCycloPalloidHypoidGearSetLoadCase
    from ._6921 import KlingelnbergCycloPalloidSpiralBevelGearLoadCase
    from ._6922 import KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
    from ._6923 import KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
    from ._6924 import MassDiscLoadCase
    from ._6925 import MeasurementComponentLoadCase
    from ._6926 import MeshStiffnessSource
    from ._6927 import MountableComponentLoadCase
    from ._6928 import NamedSpeed
    from ._6929 import OilSealLoadCase
    from ._6930 import ParametricStudyType
    from ._6931 import PartLoadCase
    from ._6932 import PartToPartShearCouplingConnectionLoadCase
    from ._6933 import PartToPartShearCouplingHalfLoadCase
    from ._6934 import PartToPartShearCouplingLoadCase
    from ._6935 import PlanetaryConnectionLoadCase
    from ._6936 import PlanetaryGearSetLoadCase
    from ._6937 import PlanetarySocketManufactureError
    from ._6938 import PlanetCarrierLoadCase
    from ._6939 import PlanetManufactureError
    from ._6940 import PointLoadHarmonicLoadData
    from ._6941 import PointLoadLoadCase
    from ._6942 import PowerLoadLoadCase
    from ._6943 import PulleyLoadCase
    from ._6944 import ResetMicroGeometryOptions
    from ._6945 import RingPinManufacturingError
    from ._6946 import RingPinsLoadCase
    from ._6947 import RingPinsToDiscConnectionLoadCase
    from ._6948 import RollingRingAssemblyLoadCase
    from ._6949 import RollingRingConnectionLoadCase
    from ._6950 import RollingRingLoadCase
    from ._6951 import RootAssemblyLoadCase
    from ._6952 import ShaftHubConnectionLoadCase
    from ._6953 import ShaftLoadCase
    from ._6954 import ShaftToMountableComponentConnectionLoadCase
    from ._6955 import SpecialisedAssemblyLoadCase
    from ._6956 import SpiralBevelGearLoadCase
    from ._6957 import SpiralBevelGearMeshLoadCase
    from ._6958 import SpiralBevelGearSetLoadCase
    from ._6959 import SpringDamperConnectionLoadCase
    from ._6960 import SpringDamperHalfLoadCase
    from ._6961 import SpringDamperLoadCase
    from ._6962 import StraightBevelDiffGearLoadCase
    from ._6963 import StraightBevelDiffGearMeshLoadCase
    from ._6964 import StraightBevelDiffGearSetLoadCase
    from ._6965 import StraightBevelGearLoadCase
    from ._6966 import StraightBevelGearMeshLoadCase
    from ._6967 import StraightBevelGearSetLoadCase
    from ._6968 import StraightBevelPlanetGearLoadCase
    from ._6969 import StraightBevelSunGearLoadCase
    from ._6970 import SynchroniserHalfLoadCase
    from ._6971 import SynchroniserLoadCase
    from ._6972 import SynchroniserPartLoadCase
    from ._6973 import SynchroniserSleeveLoadCase
    from ._6974 import TEExcitationType
    from ._6975 import TorqueConverterConnectionLoadCase
    from ._6976 import TorqueConverterLoadCase
    from ._6977 import TorqueConverterPumpLoadCase
    from ._6978 import TorqueConverterTurbineLoadCase
    from ._6979 import TorqueRippleInputType
    from ._6980 import TorqueSpecificationForSystemDeflection
    from ._6981 import TransmissionEfficiencySettings
    from ._6982 import UnbalancedMassHarmonicLoadData
    from ._6983 import UnbalancedMassLoadCase
    from ._6984 import VirtualComponentLoadCase
    from ._6985 import WormGearLoadCase
    from ._6986 import WormGearMeshLoadCase
    from ._6987 import WormGearSetLoadCase
    from ._6988 import ZerolBevelGearLoadCase
    from ._6989 import ZerolBevelGearMeshLoadCase
    from ._6990 import ZerolBevelGearSetLoadCase
else:
    import_structure = {
        "_6806": ["LoadCase"],
        "_6807": ["StaticLoadCase"],
        "_6808": ["TimeSeriesLoadCase"],
        "_6809": ["AbstractAssemblyLoadCase"],
        "_6810": ["AbstractShaftLoadCase"],
        "_6811": ["AbstractShaftOrHousingLoadCase"],
        "_6812": ["AbstractShaftToMountableComponentConnectionLoadCase"],
        "_6813": ["AdditionalAccelerationOptions"],
        "_6814": ["AdvancedTimeSteppingAnalysisForModulationStaticLoadCase"],
        "_6815": ["AdvancedTimeSteppingAnalysisForModulationType"],
        "_6816": ["AGMAGleasonConicalGearLoadCase"],
        "_6817": ["AGMAGleasonConicalGearMeshLoadCase"],
        "_6818": ["AGMAGleasonConicalGearSetLoadCase"],
        "_6819": ["AllRingPinsManufacturingError"],
        "_6820": ["AnalysisType"],
        "_6821": ["AssemblyLoadCase"],
        "_6822": ["BearingLoadCase"],
        "_6823": ["BeltConnectionLoadCase"],
        "_6824": ["BeltDriveLoadCase"],
        "_6825": ["BevelDifferentialGearLoadCase"],
        "_6826": ["BevelDifferentialGearMeshLoadCase"],
        "_6827": ["BevelDifferentialGearSetLoadCase"],
        "_6828": ["BevelDifferentialPlanetGearLoadCase"],
        "_6829": ["BevelDifferentialSunGearLoadCase"],
        "_6830": ["BevelGearLoadCase"],
        "_6831": ["BevelGearMeshLoadCase"],
        "_6832": ["BevelGearSetLoadCase"],
        "_6833": ["BoltedJointLoadCase"],
        "_6834": ["BoltLoadCase"],
        "_6835": ["ClutchConnectionLoadCase"],
        "_6836": ["ClutchHalfLoadCase"],
        "_6837": ["ClutchLoadCase"],
        "_6838": ["CMSElementFaceGroupWithSelectionOption"],
        "_6839": ["CoaxialConnectionLoadCase"],
        "_6840": ["ComponentLoadCase"],
        "_6841": ["ConceptCouplingConnectionLoadCase"],
        "_6842": ["ConceptCouplingHalfLoadCase"],
        "_6843": ["ConceptCouplingLoadCase"],
        "_6844": ["ConceptGearLoadCase"],
        "_6845": ["ConceptGearMeshLoadCase"],
        "_6846": ["ConceptGearSetLoadCase"],
        "_6847": ["ConicalGearLoadCase"],
        "_6848": ["ConicalGearManufactureError"],
        "_6849": ["ConicalGearMeshLoadCase"],
        "_6850": ["ConicalGearSetHarmonicLoadData"],
        "_6851": ["ConicalGearSetLoadCase"],
        "_6852": ["ConnectionLoadCase"],
        "_6853": ["ConnectorLoadCase"],
        "_6854": ["CouplingConnectionLoadCase"],
        "_6855": ["CouplingHalfLoadCase"],
        "_6856": ["CouplingLoadCase"],
        "_6857": ["CVTBeltConnectionLoadCase"],
        "_6858": ["CVTLoadCase"],
        "_6859": ["CVTPulleyLoadCase"],
        "_6860": ["CycloidalAssemblyLoadCase"],
        "_6861": ["CycloidalDiscCentralBearingConnectionLoadCase"],
        "_6862": ["CycloidalDiscLoadCase"],
        "_6863": ["CycloidalDiscPlanetaryBearingConnectionLoadCase"],
        "_6864": ["CylindricalGearLoadCase"],
        "_6865": ["CylindricalGearManufactureError"],
        "_6866": ["CylindricalGearMeshLoadCase"],
        "_6867": ["CylindricalGearSetHarmonicLoadData"],
        "_6868": ["CylindricalGearSetLoadCase"],
        "_6869": ["CylindricalPlanetGearLoadCase"],
        "_6870": ["DataFromMotorPackagePerMeanTorque"],
        "_6871": ["DataFromMotorPackagePerSpeed"],
        "_6872": ["DatumLoadCase"],
        "_6873": ["ElectricMachineDataImportType"],
        "_6874": ["ElectricMachineHarmonicLoadData"],
        "_6875": ["ElectricMachineHarmonicLoadDataFromExcel"],
        "_6876": ["ElectricMachineHarmonicLoadDataFromFlux"],
        "_6877": ["ElectricMachineHarmonicLoadDataFromJMAG"],
        "_6878": ["ElectricMachineHarmonicLoadDataFromMASTA"],
        "_6879": ["ElectricMachineHarmonicLoadDataFromMotorCAD"],
        "_6880": ["ElectricMachineHarmonicLoadDataFromMotorPackages"],
        "_6881": ["ElectricMachineHarmonicLoadExcelImportOptions"],
        "_6882": ["ElectricMachineHarmonicLoadFluxImportOptions"],
        "_6883": ["ElectricMachineHarmonicLoadImportOptionsBase"],
        "_6884": ["ElectricMachineHarmonicLoadJMAGImportOptions"],
        "_6885": ["ElectricMachineHarmonicLoadMotorCADImportOptions"],
        "_6886": ["ExternalCADModelLoadCase"],
        "_6887": ["FaceGearLoadCase"],
        "_6888": ["FaceGearMeshLoadCase"],
        "_6889": ["FaceGearSetLoadCase"],
        "_6890": ["FEPartLoadCase"],
        "_6891": ["FlexiblePinAssemblyLoadCase"],
        "_6892": ["ForceAndTorqueScalingFactor"],
        "_6893": ["GearLoadCase"],
        "_6894": ["GearManufactureError"],
        "_6895": ["GearMeshLoadCase"],
        "_6896": ["GearMeshTEOrderType"],
        "_6897": ["GearSetHarmonicLoadData"],
        "_6898": ["GearSetLoadCase"],
        "_6899": ["GuideDxfModelLoadCase"],
        "_6900": ["HarmonicExcitationType"],
        "_6901": ["HarmonicLoadDataCSVImport"],
        "_6902": ["HarmonicLoadDataExcelImport"],
        "_6903": ["HarmonicLoadDataFluxImport"],
        "_6904": ["HarmonicLoadDataImportBase"],
        "_6905": ["HarmonicLoadDataImportFromMotorPackages"],
        "_6906": ["HarmonicLoadDataJMAGImport"],
        "_6907": ["HarmonicLoadDataMotorCADImport"],
        "_6908": ["HypoidGearLoadCase"],
        "_6909": ["HypoidGearMeshLoadCase"],
        "_6910": ["HypoidGearSetLoadCase"],
        "_6911": ["ImportType"],
        "_6912": ["InformationAtRingPinToDiscContactPointFromGeometry"],
        "_6913": ["InnerDiameterReference"],
        "_6914": ["InterMountableComponentConnectionLoadCase"],
        "_6915": ["KlingelnbergCycloPalloidConicalGearLoadCase"],
        "_6916": ["KlingelnbergCycloPalloidConicalGearMeshLoadCase"],
        "_6917": ["KlingelnbergCycloPalloidConicalGearSetLoadCase"],
        "_6918": ["KlingelnbergCycloPalloidHypoidGearLoadCase"],
        "_6919": ["KlingelnbergCycloPalloidHypoidGearMeshLoadCase"],
        "_6920": ["KlingelnbergCycloPalloidHypoidGearSetLoadCase"],
        "_6921": ["KlingelnbergCycloPalloidSpiralBevelGearLoadCase"],
        "_6922": ["KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase"],
        "_6923": ["KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase"],
        "_6924": ["MassDiscLoadCase"],
        "_6925": ["MeasurementComponentLoadCase"],
        "_6926": ["MeshStiffnessSource"],
        "_6927": ["MountableComponentLoadCase"],
        "_6928": ["NamedSpeed"],
        "_6929": ["OilSealLoadCase"],
        "_6930": ["ParametricStudyType"],
        "_6931": ["PartLoadCase"],
        "_6932": ["PartToPartShearCouplingConnectionLoadCase"],
        "_6933": ["PartToPartShearCouplingHalfLoadCase"],
        "_6934": ["PartToPartShearCouplingLoadCase"],
        "_6935": ["PlanetaryConnectionLoadCase"],
        "_6936": ["PlanetaryGearSetLoadCase"],
        "_6937": ["PlanetarySocketManufactureError"],
        "_6938": ["PlanetCarrierLoadCase"],
        "_6939": ["PlanetManufactureError"],
        "_6940": ["PointLoadHarmonicLoadData"],
        "_6941": ["PointLoadLoadCase"],
        "_6942": ["PowerLoadLoadCase"],
        "_6943": ["PulleyLoadCase"],
        "_6944": ["ResetMicroGeometryOptions"],
        "_6945": ["RingPinManufacturingError"],
        "_6946": ["RingPinsLoadCase"],
        "_6947": ["RingPinsToDiscConnectionLoadCase"],
        "_6948": ["RollingRingAssemblyLoadCase"],
        "_6949": ["RollingRingConnectionLoadCase"],
        "_6950": ["RollingRingLoadCase"],
        "_6951": ["RootAssemblyLoadCase"],
        "_6952": ["ShaftHubConnectionLoadCase"],
        "_6953": ["ShaftLoadCase"],
        "_6954": ["ShaftToMountableComponentConnectionLoadCase"],
        "_6955": ["SpecialisedAssemblyLoadCase"],
        "_6956": ["SpiralBevelGearLoadCase"],
        "_6957": ["SpiralBevelGearMeshLoadCase"],
        "_6958": ["SpiralBevelGearSetLoadCase"],
        "_6959": ["SpringDamperConnectionLoadCase"],
        "_6960": ["SpringDamperHalfLoadCase"],
        "_6961": ["SpringDamperLoadCase"],
        "_6962": ["StraightBevelDiffGearLoadCase"],
        "_6963": ["StraightBevelDiffGearMeshLoadCase"],
        "_6964": ["StraightBevelDiffGearSetLoadCase"],
        "_6965": ["StraightBevelGearLoadCase"],
        "_6966": ["StraightBevelGearMeshLoadCase"],
        "_6967": ["StraightBevelGearSetLoadCase"],
        "_6968": ["StraightBevelPlanetGearLoadCase"],
        "_6969": ["StraightBevelSunGearLoadCase"],
        "_6970": ["SynchroniserHalfLoadCase"],
        "_6971": ["SynchroniserLoadCase"],
        "_6972": ["SynchroniserPartLoadCase"],
        "_6973": ["SynchroniserSleeveLoadCase"],
        "_6974": ["TEExcitationType"],
        "_6975": ["TorqueConverterConnectionLoadCase"],
        "_6976": ["TorqueConverterLoadCase"],
        "_6977": ["TorqueConverterPumpLoadCase"],
        "_6978": ["TorqueConverterTurbineLoadCase"],
        "_6979": ["TorqueRippleInputType"],
        "_6980": ["TorqueSpecificationForSystemDeflection"],
        "_6981": ["TransmissionEfficiencySettings"],
        "_6982": ["UnbalancedMassHarmonicLoadData"],
        "_6983": ["UnbalancedMassLoadCase"],
        "_6984": ["VirtualComponentLoadCase"],
        "_6985": ["WormGearLoadCase"],
        "_6986": ["WormGearMeshLoadCase"],
        "_6987": ["WormGearSetLoadCase"],
        "_6988": ["ZerolBevelGearLoadCase"],
        "_6989": ["ZerolBevelGearMeshLoadCase"],
        "_6990": ["ZerolBevelGearSetLoadCase"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "LoadCase",
    "StaticLoadCase",
    "TimeSeriesLoadCase",
    "AbstractAssemblyLoadCase",
    "AbstractShaftLoadCase",
    "AbstractShaftOrHousingLoadCase",
    "AbstractShaftToMountableComponentConnectionLoadCase",
    "AdditionalAccelerationOptions",
    "AdvancedTimeSteppingAnalysisForModulationStaticLoadCase",
    "AdvancedTimeSteppingAnalysisForModulationType",
    "AGMAGleasonConicalGearLoadCase",
    "AGMAGleasonConicalGearMeshLoadCase",
    "AGMAGleasonConicalGearSetLoadCase",
    "AllRingPinsManufacturingError",
    "AnalysisType",
    "AssemblyLoadCase",
    "BearingLoadCase",
    "BeltConnectionLoadCase",
    "BeltDriveLoadCase",
    "BevelDifferentialGearLoadCase",
    "BevelDifferentialGearMeshLoadCase",
    "BevelDifferentialGearSetLoadCase",
    "BevelDifferentialPlanetGearLoadCase",
    "BevelDifferentialSunGearLoadCase",
    "BevelGearLoadCase",
    "BevelGearMeshLoadCase",
    "BevelGearSetLoadCase",
    "BoltedJointLoadCase",
    "BoltLoadCase",
    "ClutchConnectionLoadCase",
    "ClutchHalfLoadCase",
    "ClutchLoadCase",
    "CMSElementFaceGroupWithSelectionOption",
    "CoaxialConnectionLoadCase",
    "ComponentLoadCase",
    "ConceptCouplingConnectionLoadCase",
    "ConceptCouplingHalfLoadCase",
    "ConceptCouplingLoadCase",
    "ConceptGearLoadCase",
    "ConceptGearMeshLoadCase",
    "ConceptGearSetLoadCase",
    "ConicalGearLoadCase",
    "ConicalGearManufactureError",
    "ConicalGearMeshLoadCase",
    "ConicalGearSetHarmonicLoadData",
    "ConicalGearSetLoadCase",
    "ConnectionLoadCase",
    "ConnectorLoadCase",
    "CouplingConnectionLoadCase",
    "CouplingHalfLoadCase",
    "CouplingLoadCase",
    "CVTBeltConnectionLoadCase",
    "CVTLoadCase",
    "CVTPulleyLoadCase",
    "CycloidalAssemblyLoadCase",
    "CycloidalDiscCentralBearingConnectionLoadCase",
    "CycloidalDiscLoadCase",
    "CycloidalDiscPlanetaryBearingConnectionLoadCase",
    "CylindricalGearLoadCase",
    "CylindricalGearManufactureError",
    "CylindricalGearMeshLoadCase",
    "CylindricalGearSetHarmonicLoadData",
    "CylindricalGearSetLoadCase",
    "CylindricalPlanetGearLoadCase",
    "DataFromMotorPackagePerMeanTorque",
    "DataFromMotorPackagePerSpeed",
    "DatumLoadCase",
    "ElectricMachineDataImportType",
    "ElectricMachineHarmonicLoadData",
    "ElectricMachineHarmonicLoadDataFromExcel",
    "ElectricMachineHarmonicLoadDataFromFlux",
    "ElectricMachineHarmonicLoadDataFromJMAG",
    "ElectricMachineHarmonicLoadDataFromMASTA",
    "ElectricMachineHarmonicLoadDataFromMotorCAD",
    "ElectricMachineHarmonicLoadDataFromMotorPackages",
    "ElectricMachineHarmonicLoadExcelImportOptions",
    "ElectricMachineHarmonicLoadFluxImportOptions",
    "ElectricMachineHarmonicLoadImportOptionsBase",
    "ElectricMachineHarmonicLoadJMAGImportOptions",
    "ElectricMachineHarmonicLoadMotorCADImportOptions",
    "ExternalCADModelLoadCase",
    "FaceGearLoadCase",
    "FaceGearMeshLoadCase",
    "FaceGearSetLoadCase",
    "FEPartLoadCase",
    "FlexiblePinAssemblyLoadCase",
    "ForceAndTorqueScalingFactor",
    "GearLoadCase",
    "GearManufactureError",
    "GearMeshLoadCase",
    "GearMeshTEOrderType",
    "GearSetHarmonicLoadData",
    "GearSetLoadCase",
    "GuideDxfModelLoadCase",
    "HarmonicExcitationType",
    "HarmonicLoadDataCSVImport",
    "HarmonicLoadDataExcelImport",
    "HarmonicLoadDataFluxImport",
    "HarmonicLoadDataImportBase",
    "HarmonicLoadDataImportFromMotorPackages",
    "HarmonicLoadDataJMAGImport",
    "HarmonicLoadDataMotorCADImport",
    "HypoidGearLoadCase",
    "HypoidGearMeshLoadCase",
    "HypoidGearSetLoadCase",
    "ImportType",
    "InformationAtRingPinToDiscContactPointFromGeometry",
    "InnerDiameterReference",
    "InterMountableComponentConnectionLoadCase",
    "KlingelnbergCycloPalloidConicalGearLoadCase",
    "KlingelnbergCycloPalloidConicalGearMeshLoadCase",
    "KlingelnbergCycloPalloidConicalGearSetLoadCase",
    "KlingelnbergCycloPalloidHypoidGearLoadCase",
    "KlingelnbergCycloPalloidHypoidGearMeshLoadCase",
    "KlingelnbergCycloPalloidHypoidGearSetLoadCase",
    "KlingelnbergCycloPalloidSpiralBevelGearLoadCase",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase",
    "KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase",
    "MassDiscLoadCase",
    "MeasurementComponentLoadCase",
    "MeshStiffnessSource",
    "MountableComponentLoadCase",
    "NamedSpeed",
    "OilSealLoadCase",
    "ParametricStudyType",
    "PartLoadCase",
    "PartToPartShearCouplingConnectionLoadCase",
    "PartToPartShearCouplingHalfLoadCase",
    "PartToPartShearCouplingLoadCase",
    "PlanetaryConnectionLoadCase",
    "PlanetaryGearSetLoadCase",
    "PlanetarySocketManufactureError",
    "PlanetCarrierLoadCase",
    "PlanetManufactureError",
    "PointLoadHarmonicLoadData",
    "PointLoadLoadCase",
    "PowerLoadLoadCase",
    "PulleyLoadCase",
    "ResetMicroGeometryOptions",
    "RingPinManufacturingError",
    "RingPinsLoadCase",
    "RingPinsToDiscConnectionLoadCase",
    "RollingRingAssemblyLoadCase",
    "RollingRingConnectionLoadCase",
    "RollingRingLoadCase",
    "RootAssemblyLoadCase",
    "ShaftHubConnectionLoadCase",
    "ShaftLoadCase",
    "ShaftToMountableComponentConnectionLoadCase",
    "SpecialisedAssemblyLoadCase",
    "SpiralBevelGearLoadCase",
    "SpiralBevelGearMeshLoadCase",
    "SpiralBevelGearSetLoadCase",
    "SpringDamperConnectionLoadCase",
    "SpringDamperHalfLoadCase",
    "SpringDamperLoadCase",
    "StraightBevelDiffGearLoadCase",
    "StraightBevelDiffGearMeshLoadCase",
    "StraightBevelDiffGearSetLoadCase",
    "StraightBevelGearLoadCase",
    "StraightBevelGearMeshLoadCase",
    "StraightBevelGearSetLoadCase",
    "StraightBevelPlanetGearLoadCase",
    "StraightBevelSunGearLoadCase",
    "SynchroniserHalfLoadCase",
    "SynchroniserLoadCase",
    "SynchroniserPartLoadCase",
    "SynchroniserSleeveLoadCase",
    "TEExcitationType",
    "TorqueConverterConnectionLoadCase",
    "TorqueConverterLoadCase",
    "TorqueConverterPumpLoadCase",
    "TorqueConverterTurbineLoadCase",
    "TorqueRippleInputType",
    "TorqueSpecificationForSystemDeflection",
    "TransmissionEfficiencySettings",
    "UnbalancedMassHarmonicLoadData",
    "UnbalancedMassLoadCase",
    "VirtualComponentLoadCase",
    "WormGearLoadCase",
    "WormGearMeshLoadCase",
    "WormGearSetLoadCase",
    "ZerolBevelGearLoadCase",
    "ZerolBevelGearMeshLoadCase",
    "ZerolBevelGearSetLoadCase",
)
