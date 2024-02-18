"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1903 import BearingConnectionComponent
    from ._1904 import InternalClearanceClass
    from ._1905 import BearingToleranceClass
    from ._1906 import BearingToleranceDefinitionOptions
    from ._1907 import FitType
    from ._1908 import InnerRingTolerance
    from ._1909 import InnerSupportTolerance
    from ._1910 import InterferenceDetail
    from ._1911 import InterferenceTolerance
    from ._1912 import ITDesignation
    from ._1913 import MountingSleeveDiameterDetail
    from ._1914 import OuterRingTolerance
    from ._1915 import OuterSupportTolerance
    from ._1916 import RaceDetail
    from ._1917 import RaceRoundnessAtAngle
    from ._1918 import RadialSpecificationMethod
    from ._1919 import RingTolerance
    from ._1920 import RoundnessSpecification
    from ._1921 import RoundnessSpecificationType
    from ._1922 import SupportDetail
    from ._1923 import SupportMaterialSource
    from ._1924 import SupportTolerance
    from ._1925 import SupportToleranceLocationDesignation
    from ._1926 import ToleranceCombination
    from ._1927 import TypeOfFit
else:
    import_structure = {
        "_1903": ["BearingConnectionComponent"],
        "_1904": ["InternalClearanceClass"],
        "_1905": ["BearingToleranceClass"],
        "_1906": ["BearingToleranceDefinitionOptions"],
        "_1907": ["FitType"],
        "_1908": ["InnerRingTolerance"],
        "_1909": ["InnerSupportTolerance"],
        "_1910": ["InterferenceDetail"],
        "_1911": ["InterferenceTolerance"],
        "_1912": ["ITDesignation"],
        "_1913": ["MountingSleeveDiameterDetail"],
        "_1914": ["OuterRingTolerance"],
        "_1915": ["OuterSupportTolerance"],
        "_1916": ["RaceDetail"],
        "_1917": ["RaceRoundnessAtAngle"],
        "_1918": ["RadialSpecificationMethod"],
        "_1919": ["RingTolerance"],
        "_1920": ["RoundnessSpecification"],
        "_1921": ["RoundnessSpecificationType"],
        "_1922": ["SupportDetail"],
        "_1923": ["SupportMaterialSource"],
        "_1924": ["SupportTolerance"],
        "_1925": ["SupportToleranceLocationDesignation"],
        "_1926": ["ToleranceCombination"],
        "_1927": ["TypeOfFit"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BearingConnectionComponent",
    "InternalClearanceClass",
    "BearingToleranceClass",
    "BearingToleranceDefinitionOptions",
    "FitType",
    "InnerRingTolerance",
    "InnerSupportTolerance",
    "InterferenceDetail",
    "InterferenceTolerance",
    "ITDesignation",
    "MountingSleeveDiameterDetail",
    "OuterRingTolerance",
    "OuterSupportTolerance",
    "RaceDetail",
    "RaceRoundnessAtAngle",
    "RadialSpecificationMethod",
    "RingTolerance",
    "RoundnessSpecification",
    "RoundnessSpecificationType",
    "SupportDetail",
    "SupportMaterialSource",
    "SupportTolerance",
    "SupportToleranceLocationDesignation",
    "ToleranceCombination",
    "TypeOfFit",
)
