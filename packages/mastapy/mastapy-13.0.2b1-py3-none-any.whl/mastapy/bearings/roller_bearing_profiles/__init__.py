"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1929 import ProfileDataToUse
    from ._1930 import ProfileSet
    from ._1931 import ProfileToFit
    from ._1932 import RollerBearingConicalProfile
    from ._1933 import RollerBearingCrownedProfile
    from ._1934 import RollerBearingDinLundbergProfile
    from ._1935 import RollerBearingFlatProfile
    from ._1936 import RollerBearingJohnsGoharProfile
    from ._1937 import RollerBearingLundbergProfile
    from ._1938 import RollerBearingProfile
    from ._1939 import RollerBearingUserSpecifiedProfile
    from ._1940 import RollerRaceProfilePoint
    from ._1941 import UserSpecifiedProfilePoint
    from ._1942 import UserSpecifiedRollerRaceProfilePoint
else:
    import_structure = {
        "_1929": ["ProfileDataToUse"],
        "_1930": ["ProfileSet"],
        "_1931": ["ProfileToFit"],
        "_1932": ["RollerBearingConicalProfile"],
        "_1933": ["RollerBearingCrownedProfile"],
        "_1934": ["RollerBearingDinLundbergProfile"],
        "_1935": ["RollerBearingFlatProfile"],
        "_1936": ["RollerBearingJohnsGoharProfile"],
        "_1937": ["RollerBearingLundbergProfile"],
        "_1938": ["RollerBearingProfile"],
        "_1939": ["RollerBearingUserSpecifiedProfile"],
        "_1940": ["RollerRaceProfilePoint"],
        "_1941": ["UserSpecifiedProfilePoint"],
        "_1942": ["UserSpecifiedRollerRaceProfilePoint"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ProfileDataToUse",
    "ProfileSet",
    "ProfileToFit",
    "RollerBearingConicalProfile",
    "RollerBearingCrownedProfile",
    "RollerBearingDinLundbergProfile",
    "RollerBearingFlatProfile",
    "RollerBearingJohnsGoharProfile",
    "RollerBearingLundbergProfile",
    "RollerBearingProfile",
    "RollerBearingUserSpecifiedProfile",
    "RollerRaceProfilePoint",
    "UserSpecifiedProfilePoint",
    "UserSpecifiedRollerRaceProfilePoint",
)
