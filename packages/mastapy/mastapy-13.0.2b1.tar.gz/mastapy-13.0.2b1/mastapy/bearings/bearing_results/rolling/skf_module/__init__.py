"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2078 import AdjustedSpeed
    from ._2079 import AdjustmentFactors
    from ._2080 import BearingLoads
    from ._2081 import BearingRatingLife
    from ._2082 import DynamicAxialLoadCarryingCapacity
    from ._2083 import Frequencies
    from ._2084 import FrequencyOfOverRolling
    from ._2085 import Friction
    from ._2086 import FrictionalMoment
    from ._2087 import FrictionSources
    from ._2088 import Grease
    from ._2089 import GreaseLifeAndRelubricationInterval
    from ._2090 import GreaseQuantity
    from ._2091 import InitialFill
    from ._2092 import LifeModel
    from ._2093 import MinimumLoad
    from ._2094 import OperatingViscosity
    from ._2095 import PermissibleAxialLoad
    from ._2096 import RotationalFrequency
    from ._2097 import SKFAuthentication
    from ._2098 import SKFCalculationResult
    from ._2099 import SKFCredentials
    from ._2100 import SKFModuleResults
    from ._2101 import StaticSafetyFactors
    from ._2102 import Viscosities
else:
    import_structure = {
        "_2078": ["AdjustedSpeed"],
        "_2079": ["AdjustmentFactors"],
        "_2080": ["BearingLoads"],
        "_2081": ["BearingRatingLife"],
        "_2082": ["DynamicAxialLoadCarryingCapacity"],
        "_2083": ["Frequencies"],
        "_2084": ["FrequencyOfOverRolling"],
        "_2085": ["Friction"],
        "_2086": ["FrictionalMoment"],
        "_2087": ["FrictionSources"],
        "_2088": ["Grease"],
        "_2089": ["GreaseLifeAndRelubricationInterval"],
        "_2090": ["GreaseQuantity"],
        "_2091": ["InitialFill"],
        "_2092": ["LifeModel"],
        "_2093": ["MinimumLoad"],
        "_2094": ["OperatingViscosity"],
        "_2095": ["PermissibleAxialLoad"],
        "_2096": ["RotationalFrequency"],
        "_2097": ["SKFAuthentication"],
        "_2098": ["SKFCalculationResult"],
        "_2099": ["SKFCredentials"],
        "_2100": ["SKFModuleResults"],
        "_2101": ["StaticSafetyFactors"],
        "_2102": ["Viscosities"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AdjustedSpeed",
    "AdjustmentFactors",
    "BearingLoads",
    "BearingRatingLife",
    "DynamicAxialLoadCarryingCapacity",
    "Frequencies",
    "FrequencyOfOverRolling",
    "Friction",
    "FrictionalMoment",
    "FrictionSources",
    "Grease",
    "GreaseLifeAndRelubricationInterval",
    "GreaseQuantity",
    "InitialFill",
    "LifeModel",
    "MinimumLoad",
    "OperatingViscosity",
    "PermissibleAxialLoad",
    "RotationalFrequency",
    "SKFAuthentication",
    "SKFCalculationResult",
    "SKFCredentials",
    "SKFModuleResults",
    "StaticSafetyFactors",
    "Viscosities",
)
