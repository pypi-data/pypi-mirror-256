"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2301 import AGMAGleasonConicalGearMesh
    from ._2302 import AGMAGleasonConicalGearTeethSocket
    from ._2303 import BevelDifferentialGearMesh
    from ._2304 import BevelDifferentialGearTeethSocket
    from ._2305 import BevelGearMesh
    from ._2306 import BevelGearTeethSocket
    from ._2307 import ConceptGearMesh
    from ._2308 import ConceptGearTeethSocket
    from ._2309 import ConicalGearMesh
    from ._2310 import ConicalGearTeethSocket
    from ._2311 import CylindricalGearMesh
    from ._2312 import CylindricalGearTeethSocket
    from ._2313 import FaceGearMesh
    from ._2314 import FaceGearTeethSocket
    from ._2315 import GearMesh
    from ._2316 import GearTeethSocket
    from ._2317 import HypoidGearMesh
    from ._2318 import HypoidGearTeethSocket
    from ._2319 import KlingelnbergConicalGearTeethSocket
    from ._2320 import KlingelnbergCycloPalloidConicalGearMesh
    from ._2321 import KlingelnbergCycloPalloidHypoidGearMesh
    from ._2322 import KlingelnbergCycloPalloidSpiralBevelGearMesh
    from ._2323 import KlingelnbergHypoidGearTeethSocket
    from ._2324 import KlingelnbergSpiralBevelGearTeethSocket
    from ._2325 import SpiralBevelGearMesh
    from ._2326 import SpiralBevelGearTeethSocket
    from ._2327 import StraightBevelDiffGearMesh
    from ._2328 import StraightBevelDiffGearTeethSocket
    from ._2329 import StraightBevelGearMesh
    from ._2330 import StraightBevelGearTeethSocket
    from ._2331 import WormGearMesh
    from ._2332 import WormGearTeethSocket
    from ._2333 import ZerolBevelGearMesh
    from ._2334 import ZerolBevelGearTeethSocket
else:
    import_structure = {
        "_2301": ["AGMAGleasonConicalGearMesh"],
        "_2302": ["AGMAGleasonConicalGearTeethSocket"],
        "_2303": ["BevelDifferentialGearMesh"],
        "_2304": ["BevelDifferentialGearTeethSocket"],
        "_2305": ["BevelGearMesh"],
        "_2306": ["BevelGearTeethSocket"],
        "_2307": ["ConceptGearMesh"],
        "_2308": ["ConceptGearTeethSocket"],
        "_2309": ["ConicalGearMesh"],
        "_2310": ["ConicalGearTeethSocket"],
        "_2311": ["CylindricalGearMesh"],
        "_2312": ["CylindricalGearTeethSocket"],
        "_2313": ["FaceGearMesh"],
        "_2314": ["FaceGearTeethSocket"],
        "_2315": ["GearMesh"],
        "_2316": ["GearTeethSocket"],
        "_2317": ["HypoidGearMesh"],
        "_2318": ["HypoidGearTeethSocket"],
        "_2319": ["KlingelnbergConicalGearTeethSocket"],
        "_2320": ["KlingelnbergCycloPalloidConicalGearMesh"],
        "_2321": ["KlingelnbergCycloPalloidHypoidGearMesh"],
        "_2322": ["KlingelnbergCycloPalloidSpiralBevelGearMesh"],
        "_2323": ["KlingelnbergHypoidGearTeethSocket"],
        "_2324": ["KlingelnbergSpiralBevelGearTeethSocket"],
        "_2325": ["SpiralBevelGearMesh"],
        "_2326": ["SpiralBevelGearTeethSocket"],
        "_2327": ["StraightBevelDiffGearMesh"],
        "_2328": ["StraightBevelDiffGearTeethSocket"],
        "_2329": ["StraightBevelGearMesh"],
        "_2330": ["StraightBevelGearTeethSocket"],
        "_2331": ["WormGearMesh"],
        "_2332": ["WormGearTeethSocket"],
        "_2333": ["ZerolBevelGearMesh"],
        "_2334": ["ZerolBevelGearTeethSocket"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AGMAGleasonConicalGearMesh",
    "AGMAGleasonConicalGearTeethSocket",
    "BevelDifferentialGearMesh",
    "BevelDifferentialGearTeethSocket",
    "BevelGearMesh",
    "BevelGearTeethSocket",
    "ConceptGearMesh",
    "ConceptGearTeethSocket",
    "ConicalGearMesh",
    "ConicalGearTeethSocket",
    "CylindricalGearMesh",
    "CylindricalGearTeethSocket",
    "FaceGearMesh",
    "FaceGearTeethSocket",
    "GearMesh",
    "GearTeethSocket",
    "HypoidGearMesh",
    "HypoidGearTeethSocket",
    "KlingelnbergConicalGearTeethSocket",
    "KlingelnbergCycloPalloidConicalGearMesh",
    "KlingelnbergCycloPalloidHypoidGearMesh",
    "KlingelnbergCycloPalloidSpiralBevelGearMesh",
    "KlingelnbergHypoidGearTeethSocket",
    "KlingelnbergSpiralBevelGearTeethSocket",
    "SpiralBevelGearMesh",
    "SpiralBevelGearTeethSocket",
    "StraightBevelDiffGearMesh",
    "StraightBevelDiffGearTeethSocket",
    "StraightBevelGearMesh",
    "StraightBevelGearTeethSocket",
    "WormGearMesh",
    "WormGearTeethSocket",
    "ZerolBevelGearMesh",
    "ZerolBevelGearTeethSocket",
)
