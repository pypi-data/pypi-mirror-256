"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1466 import AxialLoadType
    from ._1467 import BoltedJointMaterial
    from ._1468 import BoltedJointMaterialDatabase
    from ._1469 import BoltGeometry
    from ._1470 import BoltGeometryDatabase
    from ._1471 import BoltMaterial
    from ._1472 import BoltMaterialDatabase
    from ._1473 import BoltSection
    from ._1474 import BoltShankType
    from ._1475 import BoltTypes
    from ._1476 import ClampedSection
    from ._1477 import ClampedSectionMaterialDatabase
    from ._1478 import DetailedBoltDesign
    from ._1479 import DetailedBoltedJointDesign
    from ._1480 import HeadCapTypes
    from ._1481 import JointGeometries
    from ._1482 import JointTypes
    from ._1483 import LoadedBolt
    from ._1484 import RolledBeforeOrAfterHeatTreatment
    from ._1485 import StandardSizes
    from ._1486 import StrengthGrades
    from ._1487 import ThreadTypes
    from ._1488 import TighteningTechniques
else:
    import_structure = {
        "_1466": ["AxialLoadType"],
        "_1467": ["BoltedJointMaterial"],
        "_1468": ["BoltedJointMaterialDatabase"],
        "_1469": ["BoltGeometry"],
        "_1470": ["BoltGeometryDatabase"],
        "_1471": ["BoltMaterial"],
        "_1472": ["BoltMaterialDatabase"],
        "_1473": ["BoltSection"],
        "_1474": ["BoltShankType"],
        "_1475": ["BoltTypes"],
        "_1476": ["ClampedSection"],
        "_1477": ["ClampedSectionMaterialDatabase"],
        "_1478": ["DetailedBoltDesign"],
        "_1479": ["DetailedBoltedJointDesign"],
        "_1480": ["HeadCapTypes"],
        "_1481": ["JointGeometries"],
        "_1482": ["JointTypes"],
        "_1483": ["LoadedBolt"],
        "_1484": ["RolledBeforeOrAfterHeatTreatment"],
        "_1485": ["StandardSizes"],
        "_1486": ["StrengthGrades"],
        "_1487": ["ThreadTypes"],
        "_1488": ["TighteningTechniques"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AxialLoadType",
    "BoltedJointMaterial",
    "BoltedJointMaterialDatabase",
    "BoltGeometry",
    "BoltGeometryDatabase",
    "BoltMaterial",
    "BoltMaterialDatabase",
    "BoltSection",
    "BoltShankType",
    "BoltTypes",
    "ClampedSection",
    "ClampedSectionMaterialDatabase",
    "DetailedBoltDesign",
    "DetailedBoltedJointDesign",
    "HeadCapTypes",
    "JointGeometries",
    "JointTypes",
    "LoadedBolt",
    "RolledBeforeOrAfterHeatTreatment",
    "StandardSizes",
    "StrengthGrades",
    "ThreadTypes",
    "TighteningTechniques",
)
