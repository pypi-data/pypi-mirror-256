"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5660 import AbstractDesignStateLoadCaseGroup
    from ._5661 import AbstractLoadCaseGroup
    from ._5662 import AbstractStaticLoadCaseGroup
    from ._5663 import ClutchEngagementStatus
    from ._5664 import ConceptSynchroGearEngagementStatus
    from ._5665 import DesignState
    from ._5666 import DutyCycle
    from ._5667 import GenericClutchEngagementStatus
    from ._5668 import LoadCaseGroupHistograms
    from ._5669 import SubGroupInSingleDesignState
    from ._5670 import SystemOptimisationGearSet
    from ._5671 import SystemOptimiserGearSetOptimisation
    from ._5672 import SystemOptimiserTargets
    from ._5673 import TimeSeriesLoadCaseGroup
else:
    import_structure = {
        "_5660": ["AbstractDesignStateLoadCaseGroup"],
        "_5661": ["AbstractLoadCaseGroup"],
        "_5662": ["AbstractStaticLoadCaseGroup"],
        "_5663": ["ClutchEngagementStatus"],
        "_5664": ["ConceptSynchroGearEngagementStatus"],
        "_5665": ["DesignState"],
        "_5666": ["DutyCycle"],
        "_5667": ["GenericClutchEngagementStatus"],
        "_5668": ["LoadCaseGroupHistograms"],
        "_5669": ["SubGroupInSingleDesignState"],
        "_5670": ["SystemOptimisationGearSet"],
        "_5671": ["SystemOptimiserGearSetOptimisation"],
        "_5672": ["SystemOptimiserTargets"],
        "_5673": ["TimeSeriesLoadCaseGroup"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractDesignStateLoadCaseGroup",
    "AbstractLoadCaseGroup",
    "AbstractStaticLoadCaseGroup",
    "ClutchEngagementStatus",
    "ConceptSynchroGearEngagementStatus",
    "DesignState",
    "DutyCycle",
    "GenericClutchEngagementStatus",
    "LoadCaseGroupHistograms",
    "SubGroupInSingleDesignState",
    "SystemOptimisationGearSet",
    "SystemOptimiserGearSetOptimisation",
    "SystemOptimiserTargets",
    "TimeSeriesLoadCaseGroup",
)
