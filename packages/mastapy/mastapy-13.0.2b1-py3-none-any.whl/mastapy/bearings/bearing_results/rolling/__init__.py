"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1968 import BallBearingAnalysisMethod
    from ._1969 import BallBearingContactCalculation
    from ._1970 import BallBearingRaceContactGeometry
    from ._1971 import DIN7322010Results
    from ._1972 import ForceAtLaminaGroupReportable
    from ._1973 import ForceAtLaminaReportable
    from ._1974 import FrictionModelForGyroscopicMoment
    from ._1975 import InternalClearance
    from ._1976 import ISO14179Settings
    from ._1977 import ISO14179SettingsDatabase
    from ._1978 import ISO14179SettingsPerBearingType
    from ._1979 import ISO153122018Results
    from ._1980 import ISOTR1417912001Results
    from ._1981 import ISOTR141792001Results
    from ._1982 import ISOTR1417922001Results
    from ._1983 import LoadedAbstractSphericalRollerBearingStripLoadResults
    from ._1984 import LoadedAngularContactBallBearingElement
    from ._1985 import LoadedAngularContactBallBearingResults
    from ._1986 import LoadedAngularContactBallBearingRow
    from ._1987 import LoadedAngularContactThrustBallBearingElement
    from ._1988 import LoadedAngularContactThrustBallBearingResults
    from ._1989 import LoadedAngularContactThrustBallBearingRow
    from ._1990 import LoadedAsymmetricSphericalRollerBearingElement
    from ._1991 import LoadedAsymmetricSphericalRollerBearingResults
    from ._1992 import LoadedAsymmetricSphericalRollerBearingRow
    from ._1993 import LoadedAsymmetricSphericalRollerBearingStripLoadResults
    from ._1994 import LoadedAxialThrustCylindricalRollerBearingDutyCycle
    from ._1995 import LoadedAxialThrustCylindricalRollerBearingElement
    from ._1996 import LoadedAxialThrustCylindricalRollerBearingResults
    from ._1997 import LoadedAxialThrustCylindricalRollerBearingRow
    from ._1998 import LoadedAxialThrustNeedleRollerBearingElement
    from ._1999 import LoadedAxialThrustNeedleRollerBearingResults
    from ._2000 import LoadedAxialThrustNeedleRollerBearingRow
    from ._2001 import LoadedBallBearingDutyCycle
    from ._2002 import LoadedBallBearingElement
    from ._2003 import LoadedBallBearingRaceResults
    from ._2004 import LoadedBallBearingResults
    from ._2005 import LoadedBallBearingRow
    from ._2006 import LoadedCrossedRollerBearingElement
    from ._2007 import LoadedCrossedRollerBearingResults
    from ._2008 import LoadedCrossedRollerBearingRow
    from ._2009 import LoadedCylindricalRollerBearingDutyCycle
    from ._2010 import LoadedCylindricalRollerBearingElement
    from ._2011 import LoadedCylindricalRollerBearingResults
    from ._2012 import LoadedCylindricalRollerBearingRow
    from ._2013 import LoadedDeepGrooveBallBearingElement
    from ._2014 import LoadedDeepGrooveBallBearingResults
    from ._2015 import LoadedDeepGrooveBallBearingRow
    from ._2016 import LoadedElement
    from ._2017 import LoadedFourPointContactBallBearingElement
    from ._2018 import LoadedFourPointContactBallBearingRaceResults
    from ._2019 import LoadedFourPointContactBallBearingResults
    from ._2020 import LoadedFourPointContactBallBearingRow
    from ._2021 import LoadedMultiPointContactBallBearingElement
    from ._2022 import LoadedNeedleRollerBearingElement
    from ._2023 import LoadedNeedleRollerBearingResults
    from ._2024 import LoadedNeedleRollerBearingRow
    from ._2025 import LoadedNonBarrelRollerBearingDutyCycle
    from ._2026 import LoadedNonBarrelRollerBearingResults
    from ._2027 import LoadedNonBarrelRollerBearingRow
    from ._2028 import LoadedNonBarrelRollerBearingStripLoadResults
    from ._2029 import LoadedNonBarrelRollerElement
    from ._2030 import LoadedRollerBearingElement
    from ._2031 import LoadedRollerBearingResults
    from ._2032 import LoadedRollerBearingRow
    from ._2033 import LoadedRollerStripLoadResults
    from ._2034 import LoadedRollingBearingRaceResults
    from ._2035 import LoadedRollingBearingResults
    from ._2036 import LoadedRollingBearingRow
    from ._2037 import LoadedSelfAligningBallBearingElement
    from ._2038 import LoadedSelfAligningBallBearingResults
    from ._2039 import LoadedSelfAligningBallBearingRow
    from ._2040 import LoadedSphericalRadialRollerBearingElement
    from ._2041 import LoadedSphericalRollerBearingElement
    from ._2042 import LoadedSphericalRollerRadialBearingResults
    from ._2043 import LoadedSphericalRollerRadialBearingRow
    from ._2044 import LoadedSphericalRollerRadialBearingStripLoadResults
    from ._2045 import LoadedSphericalRollerThrustBearingResults
    from ._2046 import LoadedSphericalRollerThrustBearingRow
    from ._2047 import LoadedSphericalThrustRollerBearingElement
    from ._2048 import LoadedTaperRollerBearingDutyCycle
    from ._2049 import LoadedTaperRollerBearingElement
    from ._2050 import LoadedTaperRollerBearingResults
    from ._2051 import LoadedTaperRollerBearingRow
    from ._2052 import LoadedThreePointContactBallBearingElement
    from ._2053 import LoadedThreePointContactBallBearingResults
    from ._2054 import LoadedThreePointContactBallBearingRow
    from ._2055 import LoadedThrustBallBearingElement
    from ._2056 import LoadedThrustBallBearingResults
    from ._2057 import LoadedThrustBallBearingRow
    from ._2058 import LoadedToroidalRollerBearingElement
    from ._2059 import LoadedToroidalRollerBearingResults
    from ._2060 import LoadedToroidalRollerBearingRow
    from ._2061 import LoadedToroidalRollerBearingStripLoadResults
    from ._2062 import MaximumStaticContactStress
    from ._2063 import MaximumStaticContactStressDutyCycle
    from ._2064 import MaximumStaticContactStressResultsAbstract
    from ._2065 import MaxStripLoadStressObject
    from ._2066 import PermissibleContinuousAxialLoadResults
    from ._2067 import PowerRatingF1EstimationMethod
    from ._2068 import PreloadFactorLookupTable
    from ._2069 import ResultsAtRollerOffset
    from ._2070 import RingForceAndDisplacement
    from ._2071 import RollerAnalysisMethod
    from ._2072 import RollingBearingFrictionCoefficients
    from ._2073 import RollingBearingSpeedResults
    from ._2074 import SMTRibStressResults
    from ._2075 import StressAtPosition
    from ._2076 import ThreePointContactInternalClearance
    from ._2077 import TrackTruncationSafetyFactorResults
else:
    import_structure = {
        "_1968": ["BallBearingAnalysisMethod"],
        "_1969": ["BallBearingContactCalculation"],
        "_1970": ["BallBearingRaceContactGeometry"],
        "_1971": ["DIN7322010Results"],
        "_1972": ["ForceAtLaminaGroupReportable"],
        "_1973": ["ForceAtLaminaReportable"],
        "_1974": ["FrictionModelForGyroscopicMoment"],
        "_1975": ["InternalClearance"],
        "_1976": ["ISO14179Settings"],
        "_1977": ["ISO14179SettingsDatabase"],
        "_1978": ["ISO14179SettingsPerBearingType"],
        "_1979": ["ISO153122018Results"],
        "_1980": ["ISOTR1417912001Results"],
        "_1981": ["ISOTR141792001Results"],
        "_1982": ["ISOTR1417922001Results"],
        "_1983": ["LoadedAbstractSphericalRollerBearingStripLoadResults"],
        "_1984": ["LoadedAngularContactBallBearingElement"],
        "_1985": ["LoadedAngularContactBallBearingResults"],
        "_1986": ["LoadedAngularContactBallBearingRow"],
        "_1987": ["LoadedAngularContactThrustBallBearingElement"],
        "_1988": ["LoadedAngularContactThrustBallBearingResults"],
        "_1989": ["LoadedAngularContactThrustBallBearingRow"],
        "_1990": ["LoadedAsymmetricSphericalRollerBearingElement"],
        "_1991": ["LoadedAsymmetricSphericalRollerBearingResults"],
        "_1992": ["LoadedAsymmetricSphericalRollerBearingRow"],
        "_1993": ["LoadedAsymmetricSphericalRollerBearingStripLoadResults"],
        "_1994": ["LoadedAxialThrustCylindricalRollerBearingDutyCycle"],
        "_1995": ["LoadedAxialThrustCylindricalRollerBearingElement"],
        "_1996": ["LoadedAxialThrustCylindricalRollerBearingResults"],
        "_1997": ["LoadedAxialThrustCylindricalRollerBearingRow"],
        "_1998": ["LoadedAxialThrustNeedleRollerBearingElement"],
        "_1999": ["LoadedAxialThrustNeedleRollerBearingResults"],
        "_2000": ["LoadedAxialThrustNeedleRollerBearingRow"],
        "_2001": ["LoadedBallBearingDutyCycle"],
        "_2002": ["LoadedBallBearingElement"],
        "_2003": ["LoadedBallBearingRaceResults"],
        "_2004": ["LoadedBallBearingResults"],
        "_2005": ["LoadedBallBearingRow"],
        "_2006": ["LoadedCrossedRollerBearingElement"],
        "_2007": ["LoadedCrossedRollerBearingResults"],
        "_2008": ["LoadedCrossedRollerBearingRow"],
        "_2009": ["LoadedCylindricalRollerBearingDutyCycle"],
        "_2010": ["LoadedCylindricalRollerBearingElement"],
        "_2011": ["LoadedCylindricalRollerBearingResults"],
        "_2012": ["LoadedCylindricalRollerBearingRow"],
        "_2013": ["LoadedDeepGrooveBallBearingElement"],
        "_2014": ["LoadedDeepGrooveBallBearingResults"],
        "_2015": ["LoadedDeepGrooveBallBearingRow"],
        "_2016": ["LoadedElement"],
        "_2017": ["LoadedFourPointContactBallBearingElement"],
        "_2018": ["LoadedFourPointContactBallBearingRaceResults"],
        "_2019": ["LoadedFourPointContactBallBearingResults"],
        "_2020": ["LoadedFourPointContactBallBearingRow"],
        "_2021": ["LoadedMultiPointContactBallBearingElement"],
        "_2022": ["LoadedNeedleRollerBearingElement"],
        "_2023": ["LoadedNeedleRollerBearingResults"],
        "_2024": ["LoadedNeedleRollerBearingRow"],
        "_2025": ["LoadedNonBarrelRollerBearingDutyCycle"],
        "_2026": ["LoadedNonBarrelRollerBearingResults"],
        "_2027": ["LoadedNonBarrelRollerBearingRow"],
        "_2028": ["LoadedNonBarrelRollerBearingStripLoadResults"],
        "_2029": ["LoadedNonBarrelRollerElement"],
        "_2030": ["LoadedRollerBearingElement"],
        "_2031": ["LoadedRollerBearingResults"],
        "_2032": ["LoadedRollerBearingRow"],
        "_2033": ["LoadedRollerStripLoadResults"],
        "_2034": ["LoadedRollingBearingRaceResults"],
        "_2035": ["LoadedRollingBearingResults"],
        "_2036": ["LoadedRollingBearingRow"],
        "_2037": ["LoadedSelfAligningBallBearingElement"],
        "_2038": ["LoadedSelfAligningBallBearingResults"],
        "_2039": ["LoadedSelfAligningBallBearingRow"],
        "_2040": ["LoadedSphericalRadialRollerBearingElement"],
        "_2041": ["LoadedSphericalRollerBearingElement"],
        "_2042": ["LoadedSphericalRollerRadialBearingResults"],
        "_2043": ["LoadedSphericalRollerRadialBearingRow"],
        "_2044": ["LoadedSphericalRollerRadialBearingStripLoadResults"],
        "_2045": ["LoadedSphericalRollerThrustBearingResults"],
        "_2046": ["LoadedSphericalRollerThrustBearingRow"],
        "_2047": ["LoadedSphericalThrustRollerBearingElement"],
        "_2048": ["LoadedTaperRollerBearingDutyCycle"],
        "_2049": ["LoadedTaperRollerBearingElement"],
        "_2050": ["LoadedTaperRollerBearingResults"],
        "_2051": ["LoadedTaperRollerBearingRow"],
        "_2052": ["LoadedThreePointContactBallBearingElement"],
        "_2053": ["LoadedThreePointContactBallBearingResults"],
        "_2054": ["LoadedThreePointContactBallBearingRow"],
        "_2055": ["LoadedThrustBallBearingElement"],
        "_2056": ["LoadedThrustBallBearingResults"],
        "_2057": ["LoadedThrustBallBearingRow"],
        "_2058": ["LoadedToroidalRollerBearingElement"],
        "_2059": ["LoadedToroidalRollerBearingResults"],
        "_2060": ["LoadedToroidalRollerBearingRow"],
        "_2061": ["LoadedToroidalRollerBearingStripLoadResults"],
        "_2062": ["MaximumStaticContactStress"],
        "_2063": ["MaximumStaticContactStressDutyCycle"],
        "_2064": ["MaximumStaticContactStressResultsAbstract"],
        "_2065": ["MaxStripLoadStressObject"],
        "_2066": ["PermissibleContinuousAxialLoadResults"],
        "_2067": ["PowerRatingF1EstimationMethod"],
        "_2068": ["PreloadFactorLookupTable"],
        "_2069": ["ResultsAtRollerOffset"],
        "_2070": ["RingForceAndDisplacement"],
        "_2071": ["RollerAnalysisMethod"],
        "_2072": ["RollingBearingFrictionCoefficients"],
        "_2073": ["RollingBearingSpeedResults"],
        "_2074": ["SMTRibStressResults"],
        "_2075": ["StressAtPosition"],
        "_2076": ["ThreePointContactInternalClearance"],
        "_2077": ["TrackTruncationSafetyFactorResults"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BallBearingAnalysisMethod",
    "BallBearingContactCalculation",
    "BallBearingRaceContactGeometry",
    "DIN7322010Results",
    "ForceAtLaminaGroupReportable",
    "ForceAtLaminaReportable",
    "FrictionModelForGyroscopicMoment",
    "InternalClearance",
    "ISO14179Settings",
    "ISO14179SettingsDatabase",
    "ISO14179SettingsPerBearingType",
    "ISO153122018Results",
    "ISOTR1417912001Results",
    "ISOTR141792001Results",
    "ISOTR1417922001Results",
    "LoadedAbstractSphericalRollerBearingStripLoadResults",
    "LoadedAngularContactBallBearingElement",
    "LoadedAngularContactBallBearingResults",
    "LoadedAngularContactBallBearingRow",
    "LoadedAngularContactThrustBallBearingElement",
    "LoadedAngularContactThrustBallBearingResults",
    "LoadedAngularContactThrustBallBearingRow",
    "LoadedAsymmetricSphericalRollerBearingElement",
    "LoadedAsymmetricSphericalRollerBearingResults",
    "LoadedAsymmetricSphericalRollerBearingRow",
    "LoadedAsymmetricSphericalRollerBearingStripLoadResults",
    "LoadedAxialThrustCylindricalRollerBearingDutyCycle",
    "LoadedAxialThrustCylindricalRollerBearingElement",
    "LoadedAxialThrustCylindricalRollerBearingResults",
    "LoadedAxialThrustCylindricalRollerBearingRow",
    "LoadedAxialThrustNeedleRollerBearingElement",
    "LoadedAxialThrustNeedleRollerBearingResults",
    "LoadedAxialThrustNeedleRollerBearingRow",
    "LoadedBallBearingDutyCycle",
    "LoadedBallBearingElement",
    "LoadedBallBearingRaceResults",
    "LoadedBallBearingResults",
    "LoadedBallBearingRow",
    "LoadedCrossedRollerBearingElement",
    "LoadedCrossedRollerBearingResults",
    "LoadedCrossedRollerBearingRow",
    "LoadedCylindricalRollerBearingDutyCycle",
    "LoadedCylindricalRollerBearingElement",
    "LoadedCylindricalRollerBearingResults",
    "LoadedCylindricalRollerBearingRow",
    "LoadedDeepGrooveBallBearingElement",
    "LoadedDeepGrooveBallBearingResults",
    "LoadedDeepGrooveBallBearingRow",
    "LoadedElement",
    "LoadedFourPointContactBallBearingElement",
    "LoadedFourPointContactBallBearingRaceResults",
    "LoadedFourPointContactBallBearingResults",
    "LoadedFourPointContactBallBearingRow",
    "LoadedMultiPointContactBallBearingElement",
    "LoadedNeedleRollerBearingElement",
    "LoadedNeedleRollerBearingResults",
    "LoadedNeedleRollerBearingRow",
    "LoadedNonBarrelRollerBearingDutyCycle",
    "LoadedNonBarrelRollerBearingResults",
    "LoadedNonBarrelRollerBearingRow",
    "LoadedNonBarrelRollerBearingStripLoadResults",
    "LoadedNonBarrelRollerElement",
    "LoadedRollerBearingElement",
    "LoadedRollerBearingResults",
    "LoadedRollerBearingRow",
    "LoadedRollerStripLoadResults",
    "LoadedRollingBearingRaceResults",
    "LoadedRollingBearingResults",
    "LoadedRollingBearingRow",
    "LoadedSelfAligningBallBearingElement",
    "LoadedSelfAligningBallBearingResults",
    "LoadedSelfAligningBallBearingRow",
    "LoadedSphericalRadialRollerBearingElement",
    "LoadedSphericalRollerBearingElement",
    "LoadedSphericalRollerRadialBearingResults",
    "LoadedSphericalRollerRadialBearingRow",
    "LoadedSphericalRollerRadialBearingStripLoadResults",
    "LoadedSphericalRollerThrustBearingResults",
    "LoadedSphericalRollerThrustBearingRow",
    "LoadedSphericalThrustRollerBearingElement",
    "LoadedTaperRollerBearingDutyCycle",
    "LoadedTaperRollerBearingElement",
    "LoadedTaperRollerBearingResults",
    "LoadedTaperRollerBearingRow",
    "LoadedThreePointContactBallBearingElement",
    "LoadedThreePointContactBallBearingResults",
    "LoadedThreePointContactBallBearingRow",
    "LoadedThrustBallBearingElement",
    "LoadedThrustBallBearingResults",
    "LoadedThrustBallBearingRow",
    "LoadedToroidalRollerBearingElement",
    "LoadedToroidalRollerBearingResults",
    "LoadedToroidalRollerBearingRow",
    "LoadedToroidalRollerBearingStripLoadResults",
    "MaximumStaticContactStress",
    "MaximumStaticContactStressDutyCycle",
    "MaximumStaticContactStressResultsAbstract",
    "MaxStripLoadStressObject",
    "PermissibleContinuousAxialLoadResults",
    "PowerRatingF1EstimationMethod",
    "PreloadFactorLookupTable",
    "ResultsAtRollerOffset",
    "RingForceAndDisplacement",
    "RollerAnalysisMethod",
    "RollingBearingFrictionCoefficients",
    "RollingBearingSpeedResults",
    "SMTRibStressResults",
    "StressAtPosition",
    "ThreePointContactInternalClearance",
    "TrackTruncationSafetyFactorResults",
)
