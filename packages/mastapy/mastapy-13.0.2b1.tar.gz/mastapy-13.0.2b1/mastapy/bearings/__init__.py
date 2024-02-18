"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1871 import BearingCatalog
    from ._1872 import BasicDynamicLoadRatingCalculationMethod
    from ._1873 import BasicStaticLoadRatingCalculationMethod
    from ._1874 import BearingCageMaterial
    from ._1875 import BearingDampingMatrixOption
    from ._1876 import BearingLoadCaseResultsForPST
    from ._1877 import BearingLoadCaseResultsLightweight
    from ._1878 import BearingMeasurementType
    from ._1879 import BearingModel
    from ._1880 import BearingRow
    from ._1881 import BearingSettings
    from ._1882 import BearingSettingsDatabase
    from ._1883 import BearingSettingsItem
    from ._1884 import BearingStiffnessMatrixOption
    from ._1885 import ExponentAndReductionFactorsInISO16281Calculation
    from ._1886 import FluidFilmTemperatureOptions
    from ._1887 import HybridSteelAll
    from ._1888 import JournalBearingType
    from ._1889 import JournalOilFeedType
    from ._1890 import MountingPointSurfaceFinishes
    from ._1891 import OuterRingMounting
    from ._1892 import RatingLife
    from ._1893 import RollerBearingProfileTypes
    from ._1894 import RollingBearingArrangement
    from ._1895 import RollingBearingDatabase
    from ._1896 import RollingBearingKey
    from ._1897 import RollingBearingRaceType
    from ._1898 import RollingBearingType
    from ._1899 import RotationalDirections
    from ._1900 import SealLocation
    from ._1901 import SKFSettings
    from ._1902 import TiltingPadTypes
else:
    import_structure = {
        "_1871": ["BearingCatalog"],
        "_1872": ["BasicDynamicLoadRatingCalculationMethod"],
        "_1873": ["BasicStaticLoadRatingCalculationMethod"],
        "_1874": ["BearingCageMaterial"],
        "_1875": ["BearingDampingMatrixOption"],
        "_1876": ["BearingLoadCaseResultsForPST"],
        "_1877": ["BearingLoadCaseResultsLightweight"],
        "_1878": ["BearingMeasurementType"],
        "_1879": ["BearingModel"],
        "_1880": ["BearingRow"],
        "_1881": ["BearingSettings"],
        "_1882": ["BearingSettingsDatabase"],
        "_1883": ["BearingSettingsItem"],
        "_1884": ["BearingStiffnessMatrixOption"],
        "_1885": ["ExponentAndReductionFactorsInISO16281Calculation"],
        "_1886": ["FluidFilmTemperatureOptions"],
        "_1887": ["HybridSteelAll"],
        "_1888": ["JournalBearingType"],
        "_1889": ["JournalOilFeedType"],
        "_1890": ["MountingPointSurfaceFinishes"],
        "_1891": ["OuterRingMounting"],
        "_1892": ["RatingLife"],
        "_1893": ["RollerBearingProfileTypes"],
        "_1894": ["RollingBearingArrangement"],
        "_1895": ["RollingBearingDatabase"],
        "_1896": ["RollingBearingKey"],
        "_1897": ["RollingBearingRaceType"],
        "_1898": ["RollingBearingType"],
        "_1899": ["RotationalDirections"],
        "_1900": ["SealLocation"],
        "_1901": ["SKFSettings"],
        "_1902": ["TiltingPadTypes"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BearingCatalog",
    "BasicDynamicLoadRatingCalculationMethod",
    "BasicStaticLoadRatingCalculationMethod",
    "BearingCageMaterial",
    "BearingDampingMatrixOption",
    "BearingLoadCaseResultsForPST",
    "BearingLoadCaseResultsLightweight",
    "BearingMeasurementType",
    "BearingModel",
    "BearingRow",
    "BearingSettings",
    "BearingSettingsDatabase",
    "BearingSettingsItem",
    "BearingStiffnessMatrixOption",
    "ExponentAndReductionFactorsInISO16281Calculation",
    "FluidFilmTemperatureOptions",
    "HybridSteelAll",
    "JournalBearingType",
    "JournalOilFeedType",
    "MountingPointSurfaceFinishes",
    "OuterRingMounting",
    "RatingLife",
    "RollerBearingProfileTypes",
    "RollingBearingArrangement",
    "RollingBearingDatabase",
    "RollingBearingKey",
    "RollingBearingRaceType",
    "RollingBearingType",
    "RotationalDirections",
    "SealLocation",
    "SKFSettings",
    "TiltingPadTypes",
)
