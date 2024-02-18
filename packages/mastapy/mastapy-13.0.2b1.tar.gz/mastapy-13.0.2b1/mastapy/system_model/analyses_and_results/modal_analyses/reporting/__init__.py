"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._4718 import CalculateFullFEResultsForMode
    from ._4719 import CampbellDiagramReport
    from ._4720 import ComponentPerModeResult
    from ._4721 import DesignEntityModalAnalysisGroupResults
    from ._4722 import ModalCMSResultsForModeAndFE
    from ._4723 import PerModeResultsReport
    from ._4724 import RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis
    from ._4725 import RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis
    from ._4726 import RigidlyConnectedDesignEntityGroupModalAnalysis
    from ._4727 import ShaftPerModeResult
    from ._4728 import SingleExcitationResultsModalAnalysis
    from ._4729 import SingleModeResults
else:
    import_structure = {
        "_4718": ["CalculateFullFEResultsForMode"],
        "_4719": ["CampbellDiagramReport"],
        "_4720": ["ComponentPerModeResult"],
        "_4721": ["DesignEntityModalAnalysisGroupResults"],
        "_4722": ["ModalCMSResultsForModeAndFE"],
        "_4723": ["PerModeResultsReport"],
        "_4724": ["RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis"],
        "_4725": ["RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis"],
        "_4726": ["RigidlyConnectedDesignEntityGroupModalAnalysis"],
        "_4727": ["ShaftPerModeResult"],
        "_4728": ["SingleExcitationResultsModalAnalysis"],
        "_4729": ["SingleModeResults"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "CalculateFullFEResultsForMode",
    "CampbellDiagramReport",
    "ComponentPerModeResult",
    "DesignEntityModalAnalysisGroupResults",
    "ModalCMSResultsForModeAndFE",
    "PerModeResultsReport",
    "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis",
    "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis",
    "RigidlyConnectedDesignEntityGroupModalAnalysis",
    "ShaftPerModeResult",
    "SingleExcitationResultsModalAnalysis",
    "SingleModeResults",
)
