"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1490 import Range
    from ._1491 import AcousticWeighting
    from ._1492 import AlignmentAxis
    from ._1493 import Axis
    from ._1494 import CirclesOnAxis
    from ._1495 import ComplexMatrix
    from ._1496 import ComplexPartDisplayOption
    from ._1497 import ComplexVector
    from ._1498 import ComplexVector3D
    from ._1499 import ComplexVector6D
    from ._1500 import CoordinateSystem3D
    from ._1501 import CoordinateSystemEditor
    from ._1502 import CoordinateSystemForRotation
    from ._1503 import CoordinateSystemForRotationOrigin
    from ._1504 import DataPrecision
    from ._1505 import DegreeOfFreedom
    from ._1506 import DynamicsResponseScalarResult
    from ._1507 import DynamicsResponseScaling
    from ._1508 import Eigenmode
    from ._1509 import Eigenmodes
    from ._1510 import EulerParameters
    from ._1511 import ExtrapolationOptions
    from ._1512 import FacetedBody
    from ._1513 import FacetedSurface
    from ._1514 import FourierSeries
    from ._1515 import GenericMatrix
    from ._1516 import GriddedSurface
    from ._1517 import HarmonicValue
    from ._1518 import InertiaTensor
    from ._1519 import MassProperties
    from ._1520 import MaxMinMean
    from ._1521 import ComplexMagnitudeMethod
    from ._1522 import MultipleFourierSeriesInterpolator
    from ._1523 import Named2DLocation
    from ._1524 import PIDControlUpdateMethod
    from ._1525 import Quaternion
    from ._1526 import RealMatrix
    from ._1527 import RealVector
    from ._1528 import ResultOptionsFor3DVector
    from ._1529 import RotationAxis
    from ._1530 import RoundedOrder
    from ._1531 import SinCurve
    from ._1532 import SquareMatrix
    from ._1533 import StressPoint
    from ._1534 import TransformMatrix3D
    from ._1535 import TranslationRotation
    from ._1536 import Vector2DListAccessor
    from ._1537 import Vector6D
else:
    import_structure = {
        "_1490": ["Range"],
        "_1491": ["AcousticWeighting"],
        "_1492": ["AlignmentAxis"],
        "_1493": ["Axis"],
        "_1494": ["CirclesOnAxis"],
        "_1495": ["ComplexMatrix"],
        "_1496": ["ComplexPartDisplayOption"],
        "_1497": ["ComplexVector"],
        "_1498": ["ComplexVector3D"],
        "_1499": ["ComplexVector6D"],
        "_1500": ["CoordinateSystem3D"],
        "_1501": ["CoordinateSystemEditor"],
        "_1502": ["CoordinateSystemForRotation"],
        "_1503": ["CoordinateSystemForRotationOrigin"],
        "_1504": ["DataPrecision"],
        "_1505": ["DegreeOfFreedom"],
        "_1506": ["DynamicsResponseScalarResult"],
        "_1507": ["DynamicsResponseScaling"],
        "_1508": ["Eigenmode"],
        "_1509": ["Eigenmodes"],
        "_1510": ["EulerParameters"],
        "_1511": ["ExtrapolationOptions"],
        "_1512": ["FacetedBody"],
        "_1513": ["FacetedSurface"],
        "_1514": ["FourierSeries"],
        "_1515": ["GenericMatrix"],
        "_1516": ["GriddedSurface"],
        "_1517": ["HarmonicValue"],
        "_1518": ["InertiaTensor"],
        "_1519": ["MassProperties"],
        "_1520": ["MaxMinMean"],
        "_1521": ["ComplexMagnitudeMethod"],
        "_1522": ["MultipleFourierSeriesInterpolator"],
        "_1523": ["Named2DLocation"],
        "_1524": ["PIDControlUpdateMethod"],
        "_1525": ["Quaternion"],
        "_1526": ["RealMatrix"],
        "_1527": ["RealVector"],
        "_1528": ["ResultOptionsFor3DVector"],
        "_1529": ["RotationAxis"],
        "_1530": ["RoundedOrder"],
        "_1531": ["SinCurve"],
        "_1532": ["SquareMatrix"],
        "_1533": ["StressPoint"],
        "_1534": ["TransformMatrix3D"],
        "_1535": ["TranslationRotation"],
        "_1536": ["Vector2DListAccessor"],
        "_1537": ["Vector6D"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Range",
    "AcousticWeighting",
    "AlignmentAxis",
    "Axis",
    "CirclesOnAxis",
    "ComplexMatrix",
    "ComplexPartDisplayOption",
    "ComplexVector",
    "ComplexVector3D",
    "ComplexVector6D",
    "CoordinateSystem3D",
    "CoordinateSystemEditor",
    "CoordinateSystemForRotation",
    "CoordinateSystemForRotationOrigin",
    "DataPrecision",
    "DegreeOfFreedom",
    "DynamicsResponseScalarResult",
    "DynamicsResponseScaling",
    "Eigenmode",
    "Eigenmodes",
    "EulerParameters",
    "ExtrapolationOptions",
    "FacetedBody",
    "FacetedSurface",
    "FourierSeries",
    "GenericMatrix",
    "GriddedSurface",
    "HarmonicValue",
    "InertiaTensor",
    "MassProperties",
    "MaxMinMean",
    "ComplexMagnitudeMethod",
    "MultipleFourierSeriesInterpolator",
    "Named2DLocation",
    "PIDControlUpdateMethod",
    "Quaternion",
    "RealMatrix",
    "RealVector",
    "ResultOptionsFor3DVector",
    "RotationAxis",
    "RoundedOrder",
    "SinCurve",
    "SquareMatrix",
    "StressPoint",
    "TransformMatrix3D",
    "TranslationRotation",
    "Vector2DListAccessor",
    "Vector6D",
)
