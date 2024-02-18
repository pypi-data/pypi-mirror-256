"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2344 import ClutchConnection
    from ._2345 import ClutchSocket
    from ._2346 import ConceptCouplingConnection
    from ._2347 import ConceptCouplingSocket
    from ._2348 import CouplingConnection
    from ._2349 import CouplingSocket
    from ._2350 import PartToPartShearCouplingConnection
    from ._2351 import PartToPartShearCouplingSocket
    from ._2352 import SpringDamperConnection
    from ._2353 import SpringDamperSocket
    from ._2354 import TorqueConverterConnection
    from ._2355 import TorqueConverterPumpSocket
    from ._2356 import TorqueConverterTurbineSocket
else:
    import_structure = {
        "_2344": ["ClutchConnection"],
        "_2345": ["ClutchSocket"],
        "_2346": ["ConceptCouplingConnection"],
        "_2347": ["ConceptCouplingSocket"],
        "_2348": ["CouplingConnection"],
        "_2349": ["CouplingSocket"],
        "_2350": ["PartToPartShearCouplingConnection"],
        "_2351": ["PartToPartShearCouplingSocket"],
        "_2352": ["SpringDamperConnection"],
        "_2353": ["SpringDamperSocket"],
        "_2354": ["TorqueConverterConnection"],
        "_2355": ["TorqueConverterPumpSocket"],
        "_2356": ["TorqueConverterTurbineSocket"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "ClutchConnection",
    "ClutchSocket",
    "ConceptCouplingConnection",
    "ConceptCouplingSocket",
    "CouplingConnection",
    "CouplingSocket",
    "PartToPartShearCouplingConnection",
    "PartToPartShearCouplingSocket",
    "SpringDamperConnection",
    "SpringDamperSocket",
    "TorqueConverterConnection",
    "TorqueConverterPumpSocket",
    "TorqueConverterTurbineSocket",
)
