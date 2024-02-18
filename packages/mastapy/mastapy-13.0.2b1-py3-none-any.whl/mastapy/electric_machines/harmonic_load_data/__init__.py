"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1379 import ElectricMachineHarmonicLoadDataBase
    from ._1380 import ForceDisplayOption
    from ._1381 import HarmonicLoadDataBase
    from ._1382 import HarmonicLoadDataControlExcitationOptionBase
    from ._1383 import HarmonicLoadDataType
    from ._1384 import SpeedDependentHarmonicLoadData
    from ._1385 import StatorToothInterpolator
    from ._1386 import StatorToothLoadInterpolator
    from ._1387 import StatorToothMomentInterpolator
else:
    import_structure = {
        "_1379": ["ElectricMachineHarmonicLoadDataBase"],
        "_1380": ["ForceDisplayOption"],
        "_1381": ["HarmonicLoadDataBase"],
        "_1382": ["HarmonicLoadDataControlExcitationOptionBase"],
        "_1383": ["HarmonicLoadDataType"],
        "_1384": ["SpeedDependentHarmonicLoadData"],
        "_1385": ["StatorToothInterpolator"],
        "_1386": ["StatorToothLoadInterpolator"],
        "_1387": ["StatorToothMomentInterpolator"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ElectricMachineHarmonicLoadDataBase",
    "ForceDisplayOption",
    "HarmonicLoadDataBase",
    "HarmonicLoadDataControlExcitationOptionBase",
    "HarmonicLoadDataType",
    "SpeedDependentHarmonicLoadData",
    "StatorToothInterpolator",
    "StatorToothLoadInterpolator",
    "StatorToothMomentInterpolator",
)
