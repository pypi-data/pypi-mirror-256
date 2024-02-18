"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2357 import AlignConnectedComponentOptions
    from ._2358 import AlignmentMethod
    from ._2359 import AlignmentMethodForRaceBearing
    from ._2360 import AlignmentUsingAxialNodePositions
    from ._2361 import AngleSource
    from ._2362 import BaseFEWithSelection
    from ._2363 import BatchOperations
    from ._2364 import BearingNodeAlignmentOption
    from ._2365 import BearingNodeOption
    from ._2366 import BearingRaceNodeLink
    from ._2367 import BearingRacePosition
    from ._2368 import ComponentOrientationOption
    from ._2369 import ContactPairWithSelection
    from ._2370 import CoordinateSystemWithSelection
    from ._2371 import CreateConnectedComponentOptions
    from ._2372 import DegreeOfFreedomBoundaryCondition
    from ._2373 import DegreeOfFreedomBoundaryConditionAngular
    from ._2374 import DegreeOfFreedomBoundaryConditionLinear
    from ._2375 import ElectricMachineDataSet
    from ._2376 import ElectricMachineDynamicLoadData
    from ._2377 import ElementFaceGroupWithSelection
    from ._2378 import ElementPropertiesWithSelection
    from ._2379 import FEEntityGroupWithSelection
    from ._2380 import FEExportSettings
    from ._2381 import FEPartDRIVASurfaceSelection
    from ._2382 import FEPartWithBatchOptions
    from ._2383 import FEStiffnessGeometry
    from ._2384 import FEStiffnessTester
    from ._2385 import FESubstructure
    from ._2386 import FESubstructureExportOptions
    from ._2387 import FESubstructureNode
    from ._2388 import FESubstructureNodeModeShape
    from ._2389 import FESubstructureNodeModeShapes
    from ._2390 import FESubstructureType
    from ._2391 import FESubstructureWithBatchOptions
    from ._2392 import FESubstructureWithSelection
    from ._2393 import FESubstructureWithSelectionComponents
    from ._2394 import FESubstructureWithSelectionForHarmonicAnalysis
    from ._2395 import FESubstructureWithSelectionForModalAnalysis
    from ._2396 import FESubstructureWithSelectionForStaticAnalysis
    from ._2397 import GearMeshingOptions
    from ._2398 import IndependentMASTACreatedCondensationNode
    from ._2399 import LinkComponentAxialPositionErrorReporter
    from ._2400 import LinkNodeSource
    from ._2401 import MaterialPropertiesWithSelection
    from ._2402 import NodeBoundaryConditionStaticAnalysis
    from ._2403 import NodeGroupWithSelection
    from ._2404 import NodeSelectionDepthOption
    from ._2405 import OptionsWhenExternalFEFileAlreadyExists
    from ._2406 import PerLinkExportOptions
    from ._2407 import PerNodeExportOptions
    from ._2408 import RaceBearingFE
    from ._2409 import RaceBearingFESystemDeflection
    from ._2410 import RaceBearingFEWithSelection
    from ._2411 import ReplacedShaftSelectionHelper
    from ._2412 import SystemDeflectionFEExportOptions
    from ._2413 import ThermalExpansionOption
else:
    import_structure = {
        "_2357": ["AlignConnectedComponentOptions"],
        "_2358": ["AlignmentMethod"],
        "_2359": ["AlignmentMethodForRaceBearing"],
        "_2360": ["AlignmentUsingAxialNodePositions"],
        "_2361": ["AngleSource"],
        "_2362": ["BaseFEWithSelection"],
        "_2363": ["BatchOperations"],
        "_2364": ["BearingNodeAlignmentOption"],
        "_2365": ["BearingNodeOption"],
        "_2366": ["BearingRaceNodeLink"],
        "_2367": ["BearingRacePosition"],
        "_2368": ["ComponentOrientationOption"],
        "_2369": ["ContactPairWithSelection"],
        "_2370": ["CoordinateSystemWithSelection"],
        "_2371": ["CreateConnectedComponentOptions"],
        "_2372": ["DegreeOfFreedomBoundaryCondition"],
        "_2373": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_2374": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_2375": ["ElectricMachineDataSet"],
        "_2376": ["ElectricMachineDynamicLoadData"],
        "_2377": ["ElementFaceGroupWithSelection"],
        "_2378": ["ElementPropertiesWithSelection"],
        "_2379": ["FEEntityGroupWithSelection"],
        "_2380": ["FEExportSettings"],
        "_2381": ["FEPartDRIVASurfaceSelection"],
        "_2382": ["FEPartWithBatchOptions"],
        "_2383": ["FEStiffnessGeometry"],
        "_2384": ["FEStiffnessTester"],
        "_2385": ["FESubstructure"],
        "_2386": ["FESubstructureExportOptions"],
        "_2387": ["FESubstructureNode"],
        "_2388": ["FESubstructureNodeModeShape"],
        "_2389": ["FESubstructureNodeModeShapes"],
        "_2390": ["FESubstructureType"],
        "_2391": ["FESubstructureWithBatchOptions"],
        "_2392": ["FESubstructureWithSelection"],
        "_2393": ["FESubstructureWithSelectionComponents"],
        "_2394": ["FESubstructureWithSelectionForHarmonicAnalysis"],
        "_2395": ["FESubstructureWithSelectionForModalAnalysis"],
        "_2396": ["FESubstructureWithSelectionForStaticAnalysis"],
        "_2397": ["GearMeshingOptions"],
        "_2398": ["IndependentMASTACreatedCondensationNode"],
        "_2399": ["LinkComponentAxialPositionErrorReporter"],
        "_2400": ["LinkNodeSource"],
        "_2401": ["MaterialPropertiesWithSelection"],
        "_2402": ["NodeBoundaryConditionStaticAnalysis"],
        "_2403": ["NodeGroupWithSelection"],
        "_2404": ["NodeSelectionDepthOption"],
        "_2405": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_2406": ["PerLinkExportOptions"],
        "_2407": ["PerNodeExportOptions"],
        "_2408": ["RaceBearingFE"],
        "_2409": ["RaceBearingFESystemDeflection"],
        "_2410": ["RaceBearingFEWithSelection"],
        "_2411": ["ReplacedShaftSelectionHelper"],
        "_2412": ["SystemDeflectionFEExportOptions"],
        "_2413": ["ThermalExpansionOption"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "PerNodeExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
