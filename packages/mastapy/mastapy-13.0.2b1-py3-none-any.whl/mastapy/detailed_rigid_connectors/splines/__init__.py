"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1390 import CustomSplineHalfDesign
    from ._1391 import CustomSplineJointDesign
    from ._1392 import DetailedSplineJointSettings
    from ._1393 import DIN5480SplineHalfDesign
    from ._1394 import DIN5480SplineJointDesign
    from ._1395 import DudleyEffectiveLengthApproximationOption
    from ._1396 import FitTypes
    from ._1397 import GBT3478SplineHalfDesign
    from ._1398 import GBT3478SplineJointDesign
    from ._1399 import HeatTreatmentTypes
    from ._1400 import ISO4156SplineHalfDesign
    from ._1401 import ISO4156SplineJointDesign
    from ._1402 import JISB1603SplineJointDesign
    from ._1403 import ManufacturingTypes
    from ._1404 import Modules
    from ._1405 import PressureAngleTypes
    from ._1406 import RootTypes
    from ._1407 import SAEFatigueLifeFactorTypes
    from ._1408 import SAESplineHalfDesign
    from ._1409 import SAESplineJointDesign
    from ._1410 import SAETorqueCycles
    from ._1411 import SplineDesignTypes
    from ._1412 import FinishingMethods
    from ._1413 import SplineFitClassType
    from ._1414 import SplineFixtureTypes
    from ._1415 import SplineHalfDesign
    from ._1416 import SplineJointDesign
    from ._1417 import SplineMaterial
    from ._1418 import SplineRatingTypes
    from ._1419 import SplineToleranceClassTypes
    from ._1420 import StandardSplineHalfDesign
    from ._1421 import StandardSplineJointDesign
else:
    import_structure = {
        "_1390": ["CustomSplineHalfDesign"],
        "_1391": ["CustomSplineJointDesign"],
        "_1392": ["DetailedSplineJointSettings"],
        "_1393": ["DIN5480SplineHalfDesign"],
        "_1394": ["DIN5480SplineJointDesign"],
        "_1395": ["DudleyEffectiveLengthApproximationOption"],
        "_1396": ["FitTypes"],
        "_1397": ["GBT3478SplineHalfDesign"],
        "_1398": ["GBT3478SplineJointDesign"],
        "_1399": ["HeatTreatmentTypes"],
        "_1400": ["ISO4156SplineHalfDesign"],
        "_1401": ["ISO4156SplineJointDesign"],
        "_1402": ["JISB1603SplineJointDesign"],
        "_1403": ["ManufacturingTypes"],
        "_1404": ["Modules"],
        "_1405": ["PressureAngleTypes"],
        "_1406": ["RootTypes"],
        "_1407": ["SAEFatigueLifeFactorTypes"],
        "_1408": ["SAESplineHalfDesign"],
        "_1409": ["SAESplineJointDesign"],
        "_1410": ["SAETorqueCycles"],
        "_1411": ["SplineDesignTypes"],
        "_1412": ["FinishingMethods"],
        "_1413": ["SplineFitClassType"],
        "_1414": ["SplineFixtureTypes"],
        "_1415": ["SplineHalfDesign"],
        "_1416": ["SplineJointDesign"],
        "_1417": ["SplineMaterial"],
        "_1418": ["SplineRatingTypes"],
        "_1419": ["SplineToleranceClassTypes"],
        "_1420": ["StandardSplineHalfDesign"],
        "_1421": ["StandardSplineJointDesign"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "CustomSplineHalfDesign",
    "CustomSplineJointDesign",
    "DetailedSplineJointSettings",
    "DIN5480SplineHalfDesign",
    "DIN5480SplineJointDesign",
    "DudleyEffectiveLengthApproximationOption",
    "FitTypes",
    "GBT3478SplineHalfDesign",
    "GBT3478SplineJointDesign",
    "HeatTreatmentTypes",
    "ISO4156SplineHalfDesign",
    "ISO4156SplineJointDesign",
    "JISB1603SplineJointDesign",
    "ManufacturingTypes",
    "Modules",
    "PressureAngleTypes",
    "RootTypes",
    "SAEFatigueLifeFactorTypes",
    "SAESplineHalfDesign",
    "SAESplineJointDesign",
    "SAETorqueCycles",
    "SplineDesignTypes",
    "FinishingMethods",
    "SplineFitClassType",
    "SplineFixtureTypes",
    "SplineHalfDesign",
    "SplineJointDesign",
    "SplineMaterial",
    "SplineRatingTypes",
    "SplineToleranceClassTypes",
    "StandardSplineHalfDesign",
    "StandardSplineJointDesign",
)
