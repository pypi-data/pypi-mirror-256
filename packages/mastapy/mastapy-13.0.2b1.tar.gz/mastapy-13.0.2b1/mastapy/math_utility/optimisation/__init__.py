"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1540 import AbstractOptimisable
    from ._1541 import DesignSpaceSearchStrategyDatabase
    from ._1542 import InputSetter
    from ._1543 import MicroGeometryDesignSpaceSearchStrategyDatabase
    from ._1544 import Optimisable
    from ._1545 import OptimisationHistory
    from ._1546 import OptimizationInput
    from ._1547 import OptimizationVariable
    from ._1548 import ParetoOptimisationFilter
    from ._1549 import ParetoOptimisationInput
    from ._1550 import ParetoOptimisationOutput
    from ._1551 import ParetoOptimisationStrategy
    from ._1552 import ParetoOptimisationStrategyBars
    from ._1553 import ParetoOptimisationStrategyChartInformation
    from ._1554 import ParetoOptimisationStrategyDatabase
    from ._1555 import ParetoOptimisationVariable
    from ._1556 import ParetoOptimisationVariableBase
    from ._1557 import PropertyTargetForDominantCandidateSearch
    from ._1558 import ReportingOptimizationInput
    from ._1559 import SpecifyOptimisationInputAs
    from ._1560 import TargetingPropertyTo
else:
    import_structure = {
        "_1540": ["AbstractOptimisable"],
        "_1541": ["DesignSpaceSearchStrategyDatabase"],
        "_1542": ["InputSetter"],
        "_1543": ["MicroGeometryDesignSpaceSearchStrategyDatabase"],
        "_1544": ["Optimisable"],
        "_1545": ["OptimisationHistory"],
        "_1546": ["OptimizationInput"],
        "_1547": ["OptimizationVariable"],
        "_1548": ["ParetoOptimisationFilter"],
        "_1549": ["ParetoOptimisationInput"],
        "_1550": ["ParetoOptimisationOutput"],
        "_1551": ["ParetoOptimisationStrategy"],
        "_1552": ["ParetoOptimisationStrategyBars"],
        "_1553": ["ParetoOptimisationStrategyChartInformation"],
        "_1554": ["ParetoOptimisationStrategyDatabase"],
        "_1555": ["ParetoOptimisationVariable"],
        "_1556": ["ParetoOptimisationVariableBase"],
        "_1557": ["PropertyTargetForDominantCandidateSearch"],
        "_1558": ["ReportingOptimizationInput"],
        "_1559": ["SpecifyOptimisationInputAs"],
        "_1560": ["TargetingPropertyTo"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractOptimisable",
    "DesignSpaceSearchStrategyDatabase",
    "InputSetter",
    "MicroGeometryDesignSpaceSearchStrategyDatabase",
    "Optimisable",
    "OptimisationHistory",
    "OptimizationInput",
    "OptimizationVariable",
    "ParetoOptimisationFilter",
    "ParetoOptimisationInput",
    "ParetoOptimisationOutput",
    "ParetoOptimisationStrategy",
    "ParetoOptimisationStrategyBars",
    "ParetoOptimisationStrategyChartInformation",
    "ParetoOptimisationStrategyDatabase",
    "ParetoOptimisationVariable",
    "ParetoOptimisationVariableBase",
    "PropertyTargetForDominantCandidateSearch",
    "ReportingOptimizationInput",
    "SpecifyOptimisationInputAs",
    "TargetingPropertyTo",
)
