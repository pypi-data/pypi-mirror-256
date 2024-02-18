"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1347 import BasicDynamicForceLoadCase
    from ._1348 import DynamicForceAnalysis
    from ._1349 import DynamicForceLoadCase
    from ._1350 import DynamicForcesOperatingPoint
    from ._1351 import EfficiencyMapAnalysis
    from ._1352 import EfficiencyMapLoadCase
    from ._1353 import ElectricMachineAnalysis
    from ._1354 import ElectricMachineBasicMechanicalLossSettings
    from ._1355 import ElectricMachineControlStrategy
    from ._1356 import ElectricMachineEfficiencyMapSettings
    from ._1357 import ElectricMachineFEAnalysis
    from ._1358 import ElectricMachineFEMechanicalAnalysis
    from ._1359 import ElectricMachineLoadCase
    from ._1360 import ElectricMachineLoadCaseBase
    from ._1361 import ElectricMachineLoadCaseGroup
    from ._1362 import ElectricMachineMechanicalLoadCase
    from ._1363 import EndWindingInductanceMethod
    from ._1364 import LeadingOrLagging
    from ._1365 import LoadCaseType
    from ._1366 import LoadCaseTypeSelector
    from ._1367 import MotoringOrGenerating
    from ._1368 import NonLinearDQModelMultipleOperatingPointsLoadCase
    from ._1369 import NumberOfStepsPerOperatingPointSpecificationMethod
    from ._1370 import OperatingPointsSpecificationMethod
    from ._1371 import SingleOperatingPointAnalysis
    from ._1372 import SlotDetailForAnalysis
    from ._1373 import SpecifyTorqueOrCurrent
    from ._1374 import SpeedPointsDistribution
    from ._1375 import SpeedTorqueCurveAnalysis
    from ._1376 import SpeedTorqueCurveLoadCase
    from ._1377 import SpeedTorqueLoadCase
    from ._1378 import Temperatures
else:
    import_structure = {
        "_1347": ["BasicDynamicForceLoadCase"],
        "_1348": ["DynamicForceAnalysis"],
        "_1349": ["DynamicForceLoadCase"],
        "_1350": ["DynamicForcesOperatingPoint"],
        "_1351": ["EfficiencyMapAnalysis"],
        "_1352": ["EfficiencyMapLoadCase"],
        "_1353": ["ElectricMachineAnalysis"],
        "_1354": ["ElectricMachineBasicMechanicalLossSettings"],
        "_1355": ["ElectricMachineControlStrategy"],
        "_1356": ["ElectricMachineEfficiencyMapSettings"],
        "_1357": ["ElectricMachineFEAnalysis"],
        "_1358": ["ElectricMachineFEMechanicalAnalysis"],
        "_1359": ["ElectricMachineLoadCase"],
        "_1360": ["ElectricMachineLoadCaseBase"],
        "_1361": ["ElectricMachineLoadCaseGroup"],
        "_1362": ["ElectricMachineMechanicalLoadCase"],
        "_1363": ["EndWindingInductanceMethod"],
        "_1364": ["LeadingOrLagging"],
        "_1365": ["LoadCaseType"],
        "_1366": ["LoadCaseTypeSelector"],
        "_1367": ["MotoringOrGenerating"],
        "_1368": ["NonLinearDQModelMultipleOperatingPointsLoadCase"],
        "_1369": ["NumberOfStepsPerOperatingPointSpecificationMethod"],
        "_1370": ["OperatingPointsSpecificationMethod"],
        "_1371": ["SingleOperatingPointAnalysis"],
        "_1372": ["SlotDetailForAnalysis"],
        "_1373": ["SpecifyTorqueOrCurrent"],
        "_1374": ["SpeedPointsDistribution"],
        "_1375": ["SpeedTorqueCurveAnalysis"],
        "_1376": ["SpeedTorqueCurveLoadCase"],
        "_1377": ["SpeedTorqueLoadCase"],
        "_1378": ["Temperatures"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BasicDynamicForceLoadCase",
    "DynamicForceAnalysis",
    "DynamicForceLoadCase",
    "DynamicForcesOperatingPoint",
    "EfficiencyMapAnalysis",
    "EfficiencyMapLoadCase",
    "ElectricMachineAnalysis",
    "ElectricMachineBasicMechanicalLossSettings",
    "ElectricMachineControlStrategy",
    "ElectricMachineEfficiencyMapSettings",
    "ElectricMachineFEAnalysis",
    "ElectricMachineFEMechanicalAnalysis",
    "ElectricMachineLoadCase",
    "ElectricMachineLoadCaseBase",
    "ElectricMachineLoadCaseGroup",
    "ElectricMachineMechanicalLoadCase",
    "EndWindingInductanceMethod",
    "LeadingOrLagging",
    "LoadCaseType",
    "LoadCaseTypeSelector",
    "MotoringOrGenerating",
    "NonLinearDQModelMultipleOperatingPointsLoadCase",
    "NumberOfStepsPerOperatingPointSpecificationMethod",
    "OperatingPointsSpecificationMethod",
    "SingleOperatingPointAnalysis",
    "SlotDetailForAnalysis",
    "SpecifyTorqueOrCurrent",
    "SpeedPointsDistribution",
    "SpeedTorqueCurveAnalysis",
    "SpeedTorqueCurveLoadCase",
    "SpeedTorqueLoadCase",
    "Temperatures",
)
