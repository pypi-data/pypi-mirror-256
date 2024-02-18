"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._6991 import AdditionalForcesObtainedFrom
    from ._6992 import BoostPressureLoadCaseInputOptions
    from ._6993 import DesignStateOptions
    from ._6994 import DestinationDesignState
    from ._6995 import ForceInputOptions
    from ._6996 import GearRatioInputOptions
    from ._6997 import LoadCaseNameOptions
    from ._6998 import MomentInputOptions
    from ._6999 import MultiTimeSeriesDataInputFileOptions
    from ._7000 import PointLoadInputOptions
    from ._7001 import PowerLoadInputOptions
    from ._7002 import RampOrSteadyStateInputOptions
    from ._7003 import SpeedInputOptions
    from ._7004 import TimeSeriesImporter
    from ._7005 import TimeStepInputOptions
    from ._7006 import TorqueInputOptions
    from ._7007 import TorqueValuesObtainedFrom
else:
    import_structure = {
        "_6991": ["AdditionalForcesObtainedFrom"],
        "_6992": ["BoostPressureLoadCaseInputOptions"],
        "_6993": ["DesignStateOptions"],
        "_6994": ["DestinationDesignState"],
        "_6995": ["ForceInputOptions"],
        "_6996": ["GearRatioInputOptions"],
        "_6997": ["LoadCaseNameOptions"],
        "_6998": ["MomentInputOptions"],
        "_6999": ["MultiTimeSeriesDataInputFileOptions"],
        "_7000": ["PointLoadInputOptions"],
        "_7001": ["PowerLoadInputOptions"],
        "_7002": ["RampOrSteadyStateInputOptions"],
        "_7003": ["SpeedInputOptions"],
        "_7004": ["TimeSeriesImporter"],
        "_7005": ["TimeStepInputOptions"],
        "_7006": ["TorqueInputOptions"],
        "_7007": ["TorqueValuesObtainedFrom"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AdditionalForcesObtainedFrom",
    "BoostPressureLoadCaseInputOptions",
    "DesignStateOptions",
    "DestinationDesignState",
    "ForceInputOptions",
    "GearRatioInputOptions",
    "LoadCaseNameOptions",
    "MomentInputOptions",
    "MultiTimeSeriesDataInputFileOptions",
    "PointLoadInputOptions",
    "PowerLoadInputOptions",
    "RampOrSteadyStateInputOptions",
    "SpeedInputOptions",
    "TimeSeriesImporter",
    "TimeStepInputOptions",
    "TorqueInputOptions",
    "TorqueValuesObtainedFrom",
)
