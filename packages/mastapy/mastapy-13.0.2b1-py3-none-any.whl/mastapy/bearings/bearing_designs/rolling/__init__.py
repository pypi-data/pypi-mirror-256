"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2137 import AngularContactBallBearing
    from ._2138 import AngularContactThrustBallBearing
    from ._2139 import AsymmetricSphericalRollerBearing
    from ._2140 import AxialThrustCylindricalRollerBearing
    from ._2141 import AxialThrustNeedleRollerBearing
    from ._2142 import BallBearing
    from ._2143 import BallBearingShoulderDefinition
    from ._2144 import BarrelRollerBearing
    from ._2145 import BearingProtection
    from ._2146 import BearingProtectionDetailsModifier
    from ._2147 import BearingProtectionLevel
    from ._2148 import BearingTypeExtraInformation
    from ._2149 import CageBridgeShape
    from ._2150 import CrossedRollerBearing
    from ._2151 import CylindricalRollerBearing
    from ._2152 import DeepGrooveBallBearing
    from ._2153 import DiameterSeries
    from ._2154 import FatigueLoadLimitCalculationMethodEnum
    from ._2155 import FourPointContactAngleDefinition
    from ._2156 import FourPointContactBallBearing
    from ._2157 import GeometricConstants
    from ._2158 import GeometricConstantsForRollingFrictionalMoments
    from ._2159 import GeometricConstantsForSlidingFrictionalMoments
    from ._2160 import HeightSeries
    from ._2161 import MultiPointContactBallBearing
    from ._2162 import NeedleRollerBearing
    from ._2163 import NonBarrelRollerBearing
    from ._2164 import RollerBearing
    from ._2165 import RollerEndShape
    from ._2166 import RollerRibDetail
    from ._2167 import RollingBearing
    from ._2168 import SelfAligningBallBearing
    from ._2169 import SKFSealFrictionalMomentConstants
    from ._2170 import SleeveType
    from ._2171 import SphericalRollerBearing
    from ._2172 import SphericalRollerThrustBearing
    from ._2173 import TaperRollerBearing
    from ._2174 import ThreePointContactBallBearing
    from ._2175 import ThrustBallBearing
    from ._2176 import ToroidalRollerBearing
    from ._2177 import WidthSeries
else:
    import_structure = {
        "_2137": ["AngularContactBallBearing"],
        "_2138": ["AngularContactThrustBallBearing"],
        "_2139": ["AsymmetricSphericalRollerBearing"],
        "_2140": ["AxialThrustCylindricalRollerBearing"],
        "_2141": ["AxialThrustNeedleRollerBearing"],
        "_2142": ["BallBearing"],
        "_2143": ["BallBearingShoulderDefinition"],
        "_2144": ["BarrelRollerBearing"],
        "_2145": ["BearingProtection"],
        "_2146": ["BearingProtectionDetailsModifier"],
        "_2147": ["BearingProtectionLevel"],
        "_2148": ["BearingTypeExtraInformation"],
        "_2149": ["CageBridgeShape"],
        "_2150": ["CrossedRollerBearing"],
        "_2151": ["CylindricalRollerBearing"],
        "_2152": ["DeepGrooveBallBearing"],
        "_2153": ["DiameterSeries"],
        "_2154": ["FatigueLoadLimitCalculationMethodEnum"],
        "_2155": ["FourPointContactAngleDefinition"],
        "_2156": ["FourPointContactBallBearing"],
        "_2157": ["GeometricConstants"],
        "_2158": ["GeometricConstantsForRollingFrictionalMoments"],
        "_2159": ["GeometricConstantsForSlidingFrictionalMoments"],
        "_2160": ["HeightSeries"],
        "_2161": ["MultiPointContactBallBearing"],
        "_2162": ["NeedleRollerBearing"],
        "_2163": ["NonBarrelRollerBearing"],
        "_2164": ["RollerBearing"],
        "_2165": ["RollerEndShape"],
        "_2166": ["RollerRibDetail"],
        "_2167": ["RollingBearing"],
        "_2168": ["SelfAligningBallBearing"],
        "_2169": ["SKFSealFrictionalMomentConstants"],
        "_2170": ["SleeveType"],
        "_2171": ["SphericalRollerBearing"],
        "_2172": ["SphericalRollerThrustBearing"],
        "_2173": ["TaperRollerBearing"],
        "_2174": ["ThreePointContactBallBearing"],
        "_2175": ["ThrustBallBearing"],
        "_2176": ["ToroidalRollerBearing"],
        "_2177": ["WidthSeries"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AngularContactBallBearing",
    "AngularContactThrustBallBearing",
    "AsymmetricSphericalRollerBearing",
    "AxialThrustCylindricalRollerBearing",
    "AxialThrustNeedleRollerBearing",
    "BallBearing",
    "BallBearingShoulderDefinition",
    "BarrelRollerBearing",
    "BearingProtection",
    "BearingProtectionDetailsModifier",
    "BearingProtectionLevel",
    "BearingTypeExtraInformation",
    "CageBridgeShape",
    "CrossedRollerBearing",
    "CylindricalRollerBearing",
    "DeepGrooveBallBearing",
    "DiameterSeries",
    "FatigueLoadLimitCalculationMethodEnum",
    "FourPointContactAngleDefinition",
    "FourPointContactBallBearing",
    "GeometricConstants",
    "GeometricConstantsForRollingFrictionalMoments",
    "GeometricConstantsForSlidingFrictionalMoments",
    "HeightSeries",
    "MultiPointContactBallBearing",
    "NeedleRollerBearing",
    "NonBarrelRollerBearing",
    "RollerBearing",
    "RollerEndShape",
    "RollerRibDetail",
    "RollingBearing",
    "SelfAligningBallBearing",
    "SKFSealFrictionalMomentConstants",
    "SleeveType",
    "SphericalRollerBearing",
    "SphericalRollerThrustBearing",
    "TaperRollerBearing",
    "ThreePointContactBallBearing",
    "ThrustBallBearing",
    "ToroidalRollerBearing",
    "WidthSeries",
)
