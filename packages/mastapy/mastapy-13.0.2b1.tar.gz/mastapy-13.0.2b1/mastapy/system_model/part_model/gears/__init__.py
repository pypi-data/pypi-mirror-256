"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2512 import ActiveCylindricalGearSetDesignSelection
    from ._2513 import ActiveGearSetDesignSelection
    from ._2514 import ActiveGearSetDesignSelectionGroup
    from ._2515 import AGMAGleasonConicalGear
    from ._2516 import AGMAGleasonConicalGearSet
    from ._2517 import BevelDifferentialGear
    from ._2518 import BevelDifferentialGearSet
    from ._2519 import BevelDifferentialPlanetGear
    from ._2520 import BevelDifferentialSunGear
    from ._2521 import BevelGear
    from ._2522 import BevelGearSet
    from ._2523 import ConceptGear
    from ._2524 import ConceptGearSet
    from ._2525 import ConicalGear
    from ._2526 import ConicalGearSet
    from ._2527 import CylindricalGear
    from ._2528 import CylindricalGearSet
    from ._2529 import CylindricalPlanetGear
    from ._2530 import FaceGear
    from ._2531 import FaceGearSet
    from ._2532 import Gear
    from ._2533 import GearOrientations
    from ._2534 import GearSet
    from ._2535 import GearSetConfiguration
    from ._2536 import HypoidGear
    from ._2537 import HypoidGearSet
    from ._2538 import KlingelnbergCycloPalloidConicalGear
    from ._2539 import KlingelnbergCycloPalloidConicalGearSet
    from ._2540 import KlingelnbergCycloPalloidHypoidGear
    from ._2541 import KlingelnbergCycloPalloidHypoidGearSet
    from ._2542 import KlingelnbergCycloPalloidSpiralBevelGear
    from ._2543 import KlingelnbergCycloPalloidSpiralBevelGearSet
    from ._2544 import PlanetaryGearSet
    from ._2545 import SpiralBevelGear
    from ._2546 import SpiralBevelGearSet
    from ._2547 import StraightBevelDiffGear
    from ._2548 import StraightBevelDiffGearSet
    from ._2549 import StraightBevelGear
    from ._2550 import StraightBevelGearSet
    from ._2551 import StraightBevelPlanetGear
    from ._2552 import StraightBevelSunGear
    from ._2553 import WormGear
    from ._2554 import WormGearSet
    from ._2555 import ZerolBevelGear
    from ._2556 import ZerolBevelGearSet
else:
    import_structure = {
        "_2512": ["ActiveCylindricalGearSetDesignSelection"],
        "_2513": ["ActiveGearSetDesignSelection"],
        "_2514": ["ActiveGearSetDesignSelectionGroup"],
        "_2515": ["AGMAGleasonConicalGear"],
        "_2516": ["AGMAGleasonConicalGearSet"],
        "_2517": ["BevelDifferentialGear"],
        "_2518": ["BevelDifferentialGearSet"],
        "_2519": ["BevelDifferentialPlanetGear"],
        "_2520": ["BevelDifferentialSunGear"],
        "_2521": ["BevelGear"],
        "_2522": ["BevelGearSet"],
        "_2523": ["ConceptGear"],
        "_2524": ["ConceptGearSet"],
        "_2525": ["ConicalGear"],
        "_2526": ["ConicalGearSet"],
        "_2527": ["CylindricalGear"],
        "_2528": ["CylindricalGearSet"],
        "_2529": ["CylindricalPlanetGear"],
        "_2530": ["FaceGear"],
        "_2531": ["FaceGearSet"],
        "_2532": ["Gear"],
        "_2533": ["GearOrientations"],
        "_2534": ["GearSet"],
        "_2535": ["GearSetConfiguration"],
        "_2536": ["HypoidGear"],
        "_2537": ["HypoidGearSet"],
        "_2538": ["KlingelnbergCycloPalloidConicalGear"],
        "_2539": ["KlingelnbergCycloPalloidConicalGearSet"],
        "_2540": ["KlingelnbergCycloPalloidHypoidGear"],
        "_2541": ["KlingelnbergCycloPalloidHypoidGearSet"],
        "_2542": ["KlingelnbergCycloPalloidSpiralBevelGear"],
        "_2543": ["KlingelnbergCycloPalloidSpiralBevelGearSet"],
        "_2544": ["PlanetaryGearSet"],
        "_2545": ["SpiralBevelGear"],
        "_2546": ["SpiralBevelGearSet"],
        "_2547": ["StraightBevelDiffGear"],
        "_2548": ["StraightBevelDiffGearSet"],
        "_2549": ["StraightBevelGear"],
        "_2550": ["StraightBevelGearSet"],
        "_2551": ["StraightBevelPlanetGear"],
        "_2552": ["StraightBevelSunGear"],
        "_2553": ["WormGear"],
        "_2554": ["WormGearSet"],
        "_2555": ["ZerolBevelGear"],
        "_2556": ["ZerolBevelGearSet"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ActiveCylindricalGearSetDesignSelection",
    "ActiveGearSetDesignSelection",
    "ActiveGearSetDesignSelectionGroup",
    "AGMAGleasonConicalGear",
    "AGMAGleasonConicalGearSet",
    "BevelDifferentialGear",
    "BevelDifferentialGearSet",
    "BevelDifferentialPlanetGear",
    "BevelDifferentialSunGear",
    "BevelGear",
    "BevelGearSet",
    "ConceptGear",
    "ConceptGearSet",
    "ConicalGear",
    "ConicalGearSet",
    "CylindricalGear",
    "CylindricalGearSet",
    "CylindricalPlanetGear",
    "FaceGear",
    "FaceGearSet",
    "Gear",
    "GearOrientations",
    "GearSet",
    "GearSetConfiguration",
    "HypoidGear",
    "HypoidGearSet",
    "KlingelnbergCycloPalloidConicalGear",
    "KlingelnbergCycloPalloidConicalGearSet",
    "KlingelnbergCycloPalloidHypoidGear",
    "KlingelnbergCycloPalloidHypoidGearSet",
    "KlingelnbergCycloPalloidSpiralBevelGear",
    "KlingelnbergCycloPalloidSpiralBevelGearSet",
    "PlanetaryGearSet",
    "SpiralBevelGear",
    "SpiralBevelGearSet",
    "StraightBevelDiffGear",
    "StraightBevelDiffGearSet",
    "StraightBevelGear",
    "StraightBevelGearSet",
    "StraightBevelPlanetGear",
    "StraightBevelSunGear",
    "WormGear",
    "WormGearSet",
    "ZerolBevelGear",
    "ZerolBevelGearSet",
)
