"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2183 import AxialFeedJournalBearing
    from ._2184 import AxialGrooveJournalBearing
    from ._2185 import AxialHoleJournalBearing
    from ._2186 import CircumferentialFeedJournalBearing
    from ._2187 import CylindricalHousingJournalBearing
    from ._2188 import MachineryEncasedJournalBearing
    from ._2189 import PadFluidFilmBearing
    from ._2190 import PedestalJournalBearing
    from ._2191 import PlainGreaseFilledJournalBearing
    from ._2192 import PlainGreaseFilledJournalBearingHousingType
    from ._2193 import PlainJournalBearing
    from ._2194 import PlainJournalHousing
    from ._2195 import PlainOilFedJournalBearing
    from ._2196 import TiltingPadJournalBearing
    from ._2197 import TiltingPadThrustBearing
else:
    import_structure = {
        "_2183": ["AxialFeedJournalBearing"],
        "_2184": ["AxialGrooveJournalBearing"],
        "_2185": ["AxialHoleJournalBearing"],
        "_2186": ["CircumferentialFeedJournalBearing"],
        "_2187": ["CylindricalHousingJournalBearing"],
        "_2188": ["MachineryEncasedJournalBearing"],
        "_2189": ["PadFluidFilmBearing"],
        "_2190": ["PedestalJournalBearing"],
        "_2191": ["PlainGreaseFilledJournalBearing"],
        "_2192": ["PlainGreaseFilledJournalBearingHousingType"],
        "_2193": ["PlainJournalBearing"],
        "_2194": ["PlainJournalHousing"],
        "_2195": ["PlainOilFedJournalBearing"],
        "_2196": ["TiltingPadJournalBearing"],
        "_2197": ["TiltingPadThrustBearing"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AxialFeedJournalBearing",
    "AxialGrooveJournalBearing",
    "AxialHoleJournalBearing",
    "CircumferentialFeedJournalBearing",
    "CylindricalHousingJournalBearing",
    "MachineryEncasedJournalBearing",
    "PadFluidFilmBearing",
    "PedestalJournalBearing",
    "PlainGreaseFilledJournalBearing",
    "PlainGreaseFilledJournalBearingHousingType",
    "PlainJournalBearing",
    "PlainJournalHousing",
    "PlainOilFedJournalBearing",
    "TiltingPadJournalBearing",
    "TiltingPadThrustBearing",
)
