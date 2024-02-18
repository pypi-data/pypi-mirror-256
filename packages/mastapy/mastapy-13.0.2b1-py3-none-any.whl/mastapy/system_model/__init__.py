"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2202 import Design
    from ._2203 import ComponentDampingOption
    from ._2204 import ConceptCouplingSpeedRatioSpecificationMethod
    from ._2205 import DesignEntity
    from ._2206 import DesignEntityId
    from ._2207 import DesignSettings
    from ._2208 import DutyCycleImporter
    from ._2209 import DutyCycleImporterDesignEntityMatch
    from ._2210 import ElectricMachineGroup
    from ._2211 import ExternalFullFELoader
    from ._2212 import HypoidWindUpRemovalMethod
    from ._2213 import IncludeDutyCycleOption
    from ._2214 import MASTASettings
    from ._2215 import MemorySummary
    from ._2216 import MeshStiffnessModel
    from ._2217 import PlanetPinManufacturingErrorsCoordinateSystem
    from ._2218 import PowerLoadDragTorqueSpecificationMethod
    from ._2219 import PowerLoadInputTorqueSpecificationMethod
    from ._2220 import PowerLoadPIDControlSpeedInputType
    from ._2221 import PowerLoadType
    from ._2222 import RelativeComponentAlignment
    from ._2223 import RelativeOffsetOption
    from ._2224 import SystemReporting
    from ._2225 import ThermalExpansionOptionForGroundedNodes
    from ._2226 import TransmissionTemperatureSet
else:
    import_structure = {
        "_2202": ["Design"],
        "_2203": ["ComponentDampingOption"],
        "_2204": ["ConceptCouplingSpeedRatioSpecificationMethod"],
        "_2205": ["DesignEntity"],
        "_2206": ["DesignEntityId"],
        "_2207": ["DesignSettings"],
        "_2208": ["DutyCycleImporter"],
        "_2209": ["DutyCycleImporterDesignEntityMatch"],
        "_2210": ["ElectricMachineGroup"],
        "_2211": ["ExternalFullFELoader"],
        "_2212": ["HypoidWindUpRemovalMethod"],
        "_2213": ["IncludeDutyCycleOption"],
        "_2214": ["MASTASettings"],
        "_2215": ["MemorySummary"],
        "_2216": ["MeshStiffnessModel"],
        "_2217": ["PlanetPinManufacturingErrorsCoordinateSystem"],
        "_2218": ["PowerLoadDragTorqueSpecificationMethod"],
        "_2219": ["PowerLoadInputTorqueSpecificationMethod"],
        "_2220": ["PowerLoadPIDControlSpeedInputType"],
        "_2221": ["PowerLoadType"],
        "_2222": ["RelativeComponentAlignment"],
        "_2223": ["RelativeOffsetOption"],
        "_2224": ["SystemReporting"],
        "_2225": ["ThermalExpansionOptionForGroundedNodes"],
        "_2226": ["TransmissionTemperatureSet"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Design",
    "ComponentDampingOption",
    "ConceptCouplingSpeedRatioSpecificationMethod",
    "DesignEntity",
    "DesignEntityId",
    "DesignSettings",
    "DutyCycleImporter",
    "DutyCycleImporterDesignEntityMatch",
    "ElectricMachineGroup",
    "ExternalFullFELoader",
    "HypoidWindUpRemovalMethod",
    "IncludeDutyCycleOption",
    "MASTASettings",
    "MemorySummary",
    "MeshStiffnessModel",
    "PlanetPinManufacturingErrorsCoordinateSystem",
    "PowerLoadDragTorqueSpecificationMethod",
    "PowerLoadInputTorqueSpecificationMethod",
    "PowerLoadPIDControlSpeedInputType",
    "PowerLoadType",
    "RelativeComponentAlignment",
    "RelativeOffsetOption",
    "SystemReporting",
    "ThermalExpansionOptionForGroundedNodes",
    "TransmissionTemperatureSet",
)
