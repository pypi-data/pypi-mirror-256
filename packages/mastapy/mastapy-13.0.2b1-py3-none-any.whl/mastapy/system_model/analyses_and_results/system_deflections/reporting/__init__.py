"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2844 import CylindricalGearMeshMisalignmentValue
    from ._2845 import FlexibleGearChart
    from ._2846 import GearInMeshDeflectionResults
    from ._2847 import MeshDeflectionResults
    from ._2848 import PlanetCarrierWindup
    from ._2849 import PlanetPinWindup
    from ._2850 import RigidlyConnectedComponentGroupSystemDeflection
    from ._2851 import ShaftSystemDeflectionSectionsReport
    from ._2852 import SplineFlankContactReporting
else:
    import_structure = {
        "_2844": ["CylindricalGearMeshMisalignmentValue"],
        "_2845": ["FlexibleGearChart"],
        "_2846": ["GearInMeshDeflectionResults"],
        "_2847": ["MeshDeflectionResults"],
        "_2848": ["PlanetCarrierWindup"],
        "_2849": ["PlanetPinWindup"],
        "_2850": ["RigidlyConnectedComponentGroupSystemDeflection"],
        "_2851": ["ShaftSystemDeflectionSectionsReport"],
        "_2852": ["SplineFlankContactReporting"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "CylindricalGearMeshMisalignmentValue",
    "FlexibleGearChart",
    "GearInMeshDeflectionResults",
    "MeshDeflectionResults",
    "PlanetCarrierWindup",
    "PlanetPinWindup",
    "RigidlyConnectedComponentGroupSystemDeflection",
    "ShaftSystemDeflectionSectionsReport",
    "SplineFlankContactReporting",
)
