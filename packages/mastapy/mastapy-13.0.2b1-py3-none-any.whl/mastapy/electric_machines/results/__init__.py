"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1322 import DynamicForceResults
    from ._1323 import EfficiencyResults
    from ._1324 import ElectricMachineDQModel
    from ._1325 import ElectricMachineMechanicalResults
    from ._1326 import ElectricMachineMechanicalResultsViewable
    from ._1327 import ElectricMachineResults
    from ._1328 import ElectricMachineResultsForConductorTurn
    from ._1329 import ElectricMachineResultsForConductorTurnAtTimeStep
    from ._1330 import ElectricMachineResultsForLineToLine
    from ._1331 import ElectricMachineResultsForOpenCircuitAndOnLoad
    from ._1332 import ElectricMachineResultsForPhase
    from ._1333 import ElectricMachineResultsForPhaseAtTimeStep
    from ._1334 import ElectricMachineResultsForStatorToothAtTimeStep
    from ._1335 import ElectricMachineResultsLineToLineAtTimeStep
    from ._1336 import ElectricMachineResultsTimeStep
    from ._1337 import ElectricMachineResultsTimeStepAtLocation
    from ._1338 import ElectricMachineResultsViewable
    from ._1339 import ElectricMachineForceViewOptions
    from ._1341 import LinearDQModel
    from ._1342 import MaximumTorqueResultsPoints
    from ._1343 import NonLinearDQModel
    from ._1344 import NonLinearDQModelGeneratorSettings
    from ._1345 import OnLoadElectricMachineResults
    from ._1346 import OpenCircuitElectricMachineResults
else:
    import_structure = {
        "_1322": ["DynamicForceResults"],
        "_1323": ["EfficiencyResults"],
        "_1324": ["ElectricMachineDQModel"],
        "_1325": ["ElectricMachineMechanicalResults"],
        "_1326": ["ElectricMachineMechanicalResultsViewable"],
        "_1327": ["ElectricMachineResults"],
        "_1328": ["ElectricMachineResultsForConductorTurn"],
        "_1329": ["ElectricMachineResultsForConductorTurnAtTimeStep"],
        "_1330": ["ElectricMachineResultsForLineToLine"],
        "_1331": ["ElectricMachineResultsForOpenCircuitAndOnLoad"],
        "_1332": ["ElectricMachineResultsForPhase"],
        "_1333": ["ElectricMachineResultsForPhaseAtTimeStep"],
        "_1334": ["ElectricMachineResultsForStatorToothAtTimeStep"],
        "_1335": ["ElectricMachineResultsLineToLineAtTimeStep"],
        "_1336": ["ElectricMachineResultsTimeStep"],
        "_1337": ["ElectricMachineResultsTimeStepAtLocation"],
        "_1338": ["ElectricMachineResultsViewable"],
        "_1339": ["ElectricMachineForceViewOptions"],
        "_1341": ["LinearDQModel"],
        "_1342": ["MaximumTorqueResultsPoints"],
        "_1343": ["NonLinearDQModel"],
        "_1344": ["NonLinearDQModelGeneratorSettings"],
        "_1345": ["OnLoadElectricMachineResults"],
        "_1346": ["OpenCircuitElectricMachineResults"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "DynamicForceResults",
    "EfficiencyResults",
    "ElectricMachineDQModel",
    "ElectricMachineMechanicalResults",
    "ElectricMachineMechanicalResultsViewable",
    "ElectricMachineResults",
    "ElectricMachineResultsForConductorTurn",
    "ElectricMachineResultsForConductorTurnAtTimeStep",
    "ElectricMachineResultsForLineToLine",
    "ElectricMachineResultsForOpenCircuitAndOnLoad",
    "ElectricMachineResultsForPhase",
    "ElectricMachineResultsForPhaseAtTimeStep",
    "ElectricMachineResultsForStatorToothAtTimeStep",
    "ElectricMachineResultsLineToLineAtTimeStep",
    "ElectricMachineResultsTimeStep",
    "ElectricMachineResultsTimeStepAtLocation",
    "ElectricMachineResultsViewable",
    "ElectricMachineForceViewOptions",
    "LinearDQModel",
    "MaximumTorqueResultsPoints",
    "NonLinearDQModel",
    "NonLinearDQModelGeneratorSettings",
    "OnLoadElectricMachineResults",
    "OpenCircuitElectricMachineResults",
)
