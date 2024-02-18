"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1243 import AbstractStator
    from ._1244 import AbstractToothAndSlot
    from ._1245 import AirGapPartition
    from ._1246 import CADConductor
    from ._1247 import CADElectricMachineDetail
    from ._1248 import CADMagnetDetails
    from ._1249 import CADMagnetsForLayer
    from ._1250 import CADRotor
    from ._1251 import CADStator
    from ._1252 import CADToothAndSlot
    from ._1253 import Coil
    from ._1254 import CoilPositionInSlot
    from ._1255 import CoolingDuctLayerSpecification
    from ._1256 import CoolingDuctShape
    from ._1257 import CoreLossBuildFactorSpecificationMethod
    from ._1258 import CoreLossCoefficients
    from ._1259 import DoubleLayerWindingSlotPositions
    from ._1260 import DQAxisConvention
    from ._1261 import Eccentricity
    from ._1262 import ElectricMachineDetail
    from ._1263 import ElectricMachineDetailInitialInformation
    from ._1264 import ElectricMachineMechanicalAnalysisMeshingOptions
    from ._1265 import ElectricMachineMeshingOptions
    from ._1266 import ElectricMachineMeshingOptionsBase
    from ._1267 import ElectricMachineSetup
    from ._1268 import ElectricMachineType
    from ._1269 import FillFactorSpecificationMethod
    from ._1270 import FluxBarrierOrWeb
    from ._1271 import FluxBarrierStyle
    from ._1272 import HairpinConductor
    from ._1273 import HarmonicLoadDataControlExcitationOptionForElectricMachineMode
    from ._1274 import IndividualConductorSpecificationSource
    from ._1275 import InteriorPermanentMagnetAndSynchronousReluctanceRotor
    from ._1276 import InteriorPermanentMagnetMachine
    from ._1277 import IronLossCoefficientSpecificationMethod
    from ._1278 import MagnetClearance
    from ._1279 import MagnetConfiguration
    from ._1280 import MagnetData
    from ._1281 import MagnetDesign
    from ._1282 import MagnetForLayer
    from ._1283 import MagnetisationDirection
    from ._1284 import MagnetMaterial
    from ._1285 import MagnetMaterialDatabase
    from ._1286 import MotorRotorSideFaceDetail
    from ._1287 import NonCADElectricMachineDetail
    from ._1288 import NotchShape
    from ._1289 import NotchSpecification
    from ._1290 import PermanentMagnetAssistedSynchronousReluctanceMachine
    from ._1291 import PermanentMagnetRotor
    from ._1292 import Phase
    from ._1293 import RegionID
    from ._1294 import Rotor
    from ._1295 import RotorInternalLayerSpecification
    from ._1296 import RotorSkewSlice
    from ._1297 import RotorType
    from ._1298 import SingleOrDoubleLayerWindings
    from ._1299 import SlotSectionDetail
    from ._1300 import Stator
    from ._1301 import StatorCutOutSpecification
    from ._1302 import StatorRotorMaterial
    from ._1303 import StatorRotorMaterialDatabase
    from ._1304 import SurfacePermanentMagnetMachine
    from ._1305 import SurfacePermanentMagnetRotor
    from ._1306 import SynchronousReluctanceMachine
    from ._1307 import ToothAndSlot
    from ._1308 import ToothSlotStyle
    from ._1309 import ToothTaperSpecification
    from ._1310 import TwoDimensionalFEModelForAnalysis
    from ._1311 import UShapedLayerSpecification
    from ._1312 import VShapedMagnetLayerSpecification
    from ._1313 import WindingConductor
    from ._1314 import WindingConnection
    from ._1315 import WindingMaterial
    from ._1316 import WindingMaterialDatabase
    from ._1317 import Windings
    from ._1318 import WindingsViewer
    from ._1319 import WindingType
    from ._1320 import WireSizeSpecificationMethod
    from ._1321 import WoundFieldSynchronousMachine
else:
    import_structure = {
        "_1243": ["AbstractStator"],
        "_1244": ["AbstractToothAndSlot"],
        "_1245": ["AirGapPartition"],
        "_1246": ["CADConductor"],
        "_1247": ["CADElectricMachineDetail"],
        "_1248": ["CADMagnetDetails"],
        "_1249": ["CADMagnetsForLayer"],
        "_1250": ["CADRotor"],
        "_1251": ["CADStator"],
        "_1252": ["CADToothAndSlot"],
        "_1253": ["Coil"],
        "_1254": ["CoilPositionInSlot"],
        "_1255": ["CoolingDuctLayerSpecification"],
        "_1256": ["CoolingDuctShape"],
        "_1257": ["CoreLossBuildFactorSpecificationMethod"],
        "_1258": ["CoreLossCoefficients"],
        "_1259": ["DoubleLayerWindingSlotPositions"],
        "_1260": ["DQAxisConvention"],
        "_1261": ["Eccentricity"],
        "_1262": ["ElectricMachineDetail"],
        "_1263": ["ElectricMachineDetailInitialInformation"],
        "_1264": ["ElectricMachineMechanicalAnalysisMeshingOptions"],
        "_1265": ["ElectricMachineMeshingOptions"],
        "_1266": ["ElectricMachineMeshingOptionsBase"],
        "_1267": ["ElectricMachineSetup"],
        "_1268": ["ElectricMachineType"],
        "_1269": ["FillFactorSpecificationMethod"],
        "_1270": ["FluxBarrierOrWeb"],
        "_1271": ["FluxBarrierStyle"],
        "_1272": ["HairpinConductor"],
        "_1273": ["HarmonicLoadDataControlExcitationOptionForElectricMachineMode"],
        "_1274": ["IndividualConductorSpecificationSource"],
        "_1275": ["InteriorPermanentMagnetAndSynchronousReluctanceRotor"],
        "_1276": ["InteriorPermanentMagnetMachine"],
        "_1277": ["IronLossCoefficientSpecificationMethod"],
        "_1278": ["MagnetClearance"],
        "_1279": ["MagnetConfiguration"],
        "_1280": ["MagnetData"],
        "_1281": ["MagnetDesign"],
        "_1282": ["MagnetForLayer"],
        "_1283": ["MagnetisationDirection"],
        "_1284": ["MagnetMaterial"],
        "_1285": ["MagnetMaterialDatabase"],
        "_1286": ["MotorRotorSideFaceDetail"],
        "_1287": ["NonCADElectricMachineDetail"],
        "_1288": ["NotchShape"],
        "_1289": ["NotchSpecification"],
        "_1290": ["PermanentMagnetAssistedSynchronousReluctanceMachine"],
        "_1291": ["PermanentMagnetRotor"],
        "_1292": ["Phase"],
        "_1293": ["RegionID"],
        "_1294": ["Rotor"],
        "_1295": ["RotorInternalLayerSpecification"],
        "_1296": ["RotorSkewSlice"],
        "_1297": ["RotorType"],
        "_1298": ["SingleOrDoubleLayerWindings"],
        "_1299": ["SlotSectionDetail"],
        "_1300": ["Stator"],
        "_1301": ["StatorCutOutSpecification"],
        "_1302": ["StatorRotorMaterial"],
        "_1303": ["StatorRotorMaterialDatabase"],
        "_1304": ["SurfacePermanentMagnetMachine"],
        "_1305": ["SurfacePermanentMagnetRotor"],
        "_1306": ["SynchronousReluctanceMachine"],
        "_1307": ["ToothAndSlot"],
        "_1308": ["ToothSlotStyle"],
        "_1309": ["ToothTaperSpecification"],
        "_1310": ["TwoDimensionalFEModelForAnalysis"],
        "_1311": ["UShapedLayerSpecification"],
        "_1312": ["VShapedMagnetLayerSpecification"],
        "_1313": ["WindingConductor"],
        "_1314": ["WindingConnection"],
        "_1315": ["WindingMaterial"],
        "_1316": ["WindingMaterialDatabase"],
        "_1317": ["Windings"],
        "_1318": ["WindingsViewer"],
        "_1319": ["WindingType"],
        "_1320": ["WireSizeSpecificationMethod"],
        "_1321": ["WoundFieldSynchronousMachine"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractStator",
    "AbstractToothAndSlot",
    "AirGapPartition",
    "CADConductor",
    "CADElectricMachineDetail",
    "CADMagnetDetails",
    "CADMagnetsForLayer",
    "CADRotor",
    "CADStator",
    "CADToothAndSlot",
    "Coil",
    "CoilPositionInSlot",
    "CoolingDuctLayerSpecification",
    "CoolingDuctShape",
    "CoreLossBuildFactorSpecificationMethod",
    "CoreLossCoefficients",
    "DoubleLayerWindingSlotPositions",
    "DQAxisConvention",
    "Eccentricity",
    "ElectricMachineDetail",
    "ElectricMachineDetailInitialInformation",
    "ElectricMachineMechanicalAnalysisMeshingOptions",
    "ElectricMachineMeshingOptions",
    "ElectricMachineMeshingOptionsBase",
    "ElectricMachineSetup",
    "ElectricMachineType",
    "FillFactorSpecificationMethod",
    "FluxBarrierOrWeb",
    "FluxBarrierStyle",
    "HairpinConductor",
    "HarmonicLoadDataControlExcitationOptionForElectricMachineMode",
    "IndividualConductorSpecificationSource",
    "InteriorPermanentMagnetAndSynchronousReluctanceRotor",
    "InteriorPermanentMagnetMachine",
    "IronLossCoefficientSpecificationMethod",
    "MagnetClearance",
    "MagnetConfiguration",
    "MagnetData",
    "MagnetDesign",
    "MagnetForLayer",
    "MagnetisationDirection",
    "MagnetMaterial",
    "MagnetMaterialDatabase",
    "MotorRotorSideFaceDetail",
    "NonCADElectricMachineDetail",
    "NotchShape",
    "NotchSpecification",
    "PermanentMagnetAssistedSynchronousReluctanceMachine",
    "PermanentMagnetRotor",
    "Phase",
    "RegionID",
    "Rotor",
    "RotorInternalLayerSpecification",
    "RotorSkewSlice",
    "RotorType",
    "SingleOrDoubleLayerWindings",
    "SlotSectionDetail",
    "Stator",
    "StatorCutOutSpecification",
    "StatorRotorMaterial",
    "StatorRotorMaterialDatabase",
    "SurfacePermanentMagnetMachine",
    "SurfacePermanentMagnetRotor",
    "SynchronousReluctanceMachine",
    "ToothAndSlot",
    "ToothSlotStyle",
    "ToothTaperSpecification",
    "TwoDimensionalFEModelForAnalysis",
    "UShapedLayerSpecification",
    "VShapedMagnetLayerSpecification",
    "WindingConductor",
    "WindingConnection",
    "WindingMaterial",
    "WindingMaterialDatabase",
    "Windings",
    "WindingsViewer",
    "WindingType",
    "WireSizeSpecificationMethod",
    "WoundFieldSynchronousMachine",
)
