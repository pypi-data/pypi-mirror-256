"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5856 import AbstractSingleWhineAnalysisResultsPropertyAccessor
    from ._5857 import DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic
    from ._5858 import DataPointForResponseOfANodeAtAFrequencyToAHarmonic
    from ._5859 import FEPartHarmonicAnalysisResultsPropertyAccessor
    from ._5860 import FEPartSingleWhineAnalysisResultsPropertyAccessor
    from ._5861 import HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic
    from ._5862 import HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic
    from ._5863 import HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic
    from ._5864 import HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
    from ._5865 import HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic
    from ._5866 import HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic
    from ._5867 import HarmonicAnalysisResultsPropertyAccessor
    from ._5868 import ResultsForMultipleOrders
    from ._5869 import ResultsForMultipleOrdersForFESurface
    from ._5870 import ResultsForMultipleOrdersForGroups
    from ._5871 import ResultsForOrder
    from ._5872 import ResultsForOrderIncludingGroups
    from ._5873 import ResultsForOrderIncludingNodes
    from ._5874 import ResultsForOrderIncludingSurfaces
    from ._5875 import ResultsForResponseOfAComponentOrSurfaceInAHarmonic
    from ._5876 import ResultsForResponseOfANodeOnAHarmonic
    from ._5877 import ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic
    from ._5878 import RootAssemblyHarmonicAnalysisResultsPropertyAccessor
    from ._5879 import RootAssemblySingleWhineAnalysisResultsPropertyAccessor
    from ._5880 import SingleWhineAnalysisResultsPropertyAccessor
else:
    import_structure = {
        "_5856": ["AbstractSingleWhineAnalysisResultsPropertyAccessor"],
        "_5857": ["DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic"],
        "_5858": ["DataPointForResponseOfANodeAtAFrequencyToAHarmonic"],
        "_5859": ["FEPartHarmonicAnalysisResultsPropertyAccessor"],
        "_5860": ["FEPartSingleWhineAnalysisResultsPropertyAccessor"],
        "_5861": ["HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic"],
        "_5862": ["HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic"],
        "_5863": ["HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic"],
        "_5864": ["HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic"],
        "_5865": ["HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic"],
        "_5866": ["HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic"],
        "_5867": ["HarmonicAnalysisResultsPropertyAccessor"],
        "_5868": ["ResultsForMultipleOrders"],
        "_5869": ["ResultsForMultipleOrdersForFESurface"],
        "_5870": ["ResultsForMultipleOrdersForGroups"],
        "_5871": ["ResultsForOrder"],
        "_5872": ["ResultsForOrderIncludingGroups"],
        "_5873": ["ResultsForOrderIncludingNodes"],
        "_5874": ["ResultsForOrderIncludingSurfaces"],
        "_5875": ["ResultsForResponseOfAComponentOrSurfaceInAHarmonic"],
        "_5876": ["ResultsForResponseOfANodeOnAHarmonic"],
        "_5877": ["ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic"],
        "_5878": ["RootAssemblyHarmonicAnalysisResultsPropertyAccessor"],
        "_5879": ["RootAssemblySingleWhineAnalysisResultsPropertyAccessor"],
        "_5880": ["SingleWhineAnalysisResultsPropertyAccessor"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractSingleWhineAnalysisResultsPropertyAccessor",
    "DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic",
    "DataPointForResponseOfANodeAtAFrequencyToAHarmonic",
    "FEPartHarmonicAnalysisResultsPropertyAccessor",
    "FEPartSingleWhineAnalysisResultsPropertyAccessor",
    "HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic",
    "HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic",
    "HarmonicAnalysisResultsBrokenDownByGroupsWithinAHarmonic",
    "HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic",
    "HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic",
    "HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic",
    "HarmonicAnalysisResultsPropertyAccessor",
    "ResultsForMultipleOrders",
    "ResultsForMultipleOrdersForFESurface",
    "ResultsForMultipleOrdersForGroups",
    "ResultsForOrder",
    "ResultsForOrderIncludingGroups",
    "ResultsForOrderIncludingNodes",
    "ResultsForOrderIncludingSurfaces",
    "ResultsForResponseOfAComponentOrSurfaceInAHarmonic",
    "ResultsForResponseOfANodeOnAHarmonic",
    "ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic",
    "RootAssemblyHarmonicAnalysisResultsPropertyAccessor",
    "RootAssemblySingleWhineAnalysisResultsPropertyAccessor",
    "SingleWhineAnalysisResultsPropertyAccessor",
)
