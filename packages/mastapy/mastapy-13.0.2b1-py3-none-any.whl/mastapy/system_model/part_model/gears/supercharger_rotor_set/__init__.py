"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2557 import BoostPressureInputOptions
    from ._2558 import InputPowerInputOptions
    from ._2559 import PressureRatioInputOptions
    from ._2560 import RotorSetDataInputFileOptions
    from ._2561 import RotorSetMeasuredPoint
    from ._2562 import RotorSpeedInputOptions
    from ._2563 import SuperchargerMap
    from ._2564 import SuperchargerMaps
    from ._2565 import SuperchargerRotorSet
    from ._2566 import SuperchargerRotorSetDatabase
    from ._2567 import YVariableForImportedData
else:
    import_structure = {
        "_2557": ["BoostPressureInputOptions"],
        "_2558": ["InputPowerInputOptions"],
        "_2559": ["PressureRatioInputOptions"],
        "_2560": ["RotorSetDataInputFileOptions"],
        "_2561": ["RotorSetMeasuredPoint"],
        "_2562": ["RotorSpeedInputOptions"],
        "_2563": ["SuperchargerMap"],
        "_2564": ["SuperchargerMaps"],
        "_2565": ["SuperchargerRotorSet"],
        "_2566": ["SuperchargerRotorSetDatabase"],
        "_2567": ["YVariableForImportedData"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "BoostPressureInputOptions",
    "InputPowerInputOptions",
    "PressureRatioInputOptions",
    "RotorSetDataInputFileOptions",
    "RotorSetMeasuredPoint",
    "RotorSpeedInputOptions",
    "SuperchargerMap",
    "SuperchargerMaps",
    "SuperchargerRotorSet",
    "SuperchargerRotorSetDatabase",
    "YVariableForImportedData",
)
