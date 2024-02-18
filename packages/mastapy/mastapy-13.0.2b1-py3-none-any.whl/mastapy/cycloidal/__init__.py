"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1452 import ContactSpecification
    from ._1453 import CrowningSpecificationMethod
    from ._1454 import CycloidalAssemblyDesign
    from ._1455 import CycloidalDiscDesign
    from ._1456 import CycloidalDiscDesignExporter
    from ._1457 import CycloidalDiscMaterial
    from ._1458 import CycloidalDiscMaterialDatabase
    from ._1459 import CycloidalDiscModificationsSpecification
    from ._1460 import DirectionOfMeasuredModifications
    from ._1461 import GeometryToExport
    from ._1462 import NamedDiscPhase
    from ._1463 import RingPinsDesign
    from ._1464 import RingPinsMaterial
    from ._1465 import RingPinsMaterialDatabase
else:
    import_structure = {
        "_1452": ["ContactSpecification"],
        "_1453": ["CrowningSpecificationMethod"],
        "_1454": ["CycloidalAssemblyDesign"],
        "_1455": ["CycloidalDiscDesign"],
        "_1456": ["CycloidalDiscDesignExporter"],
        "_1457": ["CycloidalDiscMaterial"],
        "_1458": ["CycloidalDiscMaterialDatabase"],
        "_1459": ["CycloidalDiscModificationsSpecification"],
        "_1460": ["DirectionOfMeasuredModifications"],
        "_1461": ["GeometryToExport"],
        "_1462": ["NamedDiscPhase"],
        "_1463": ["RingPinsDesign"],
        "_1464": ["RingPinsMaterial"],
        "_1465": ["RingPinsMaterialDatabase"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ContactSpecification",
    "CrowningSpecificationMethod",
    "CycloidalAssemblyDesign",
    "CycloidalDiscDesign",
    "CycloidalDiscDesignExporter",
    "CycloidalDiscMaterial",
    "CycloidalDiscMaterialDatabase",
    "CycloidalDiscModificationsSpecification",
    "DirectionOfMeasuredModifications",
    "GeometryToExport",
    "NamedDiscPhase",
    "RingPinsDesign",
    "RingPinsMaterial",
    "RingPinsMaterialDatabase",
)
