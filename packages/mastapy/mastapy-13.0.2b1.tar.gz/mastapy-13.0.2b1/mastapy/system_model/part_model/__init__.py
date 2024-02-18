"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2435 import Assembly
    from ._2436 import AbstractAssembly
    from ._2437 import AbstractShaft
    from ._2438 import AbstractShaftOrHousing
    from ._2439 import AGMALoadSharingTableApplicationLevel
    from ._2440 import AxialInternalClearanceTolerance
    from ._2441 import Bearing
    from ._2442 import BearingF0InputMethod
    from ._2443 import BearingRaceMountingOptions
    from ._2444 import Bolt
    from ._2445 import BoltedJoint
    from ._2446 import Component
    from ._2447 import ComponentsConnectedResult
    from ._2448 import ConnectedSockets
    from ._2449 import Connector
    from ._2450 import Datum
    from ._2451 import ElectricMachineSearchRegionSpecificationMethod
    from ._2452 import EnginePartLoad
    from ._2453 import EngineSpeed
    from ._2454 import ExternalCADModel
    from ._2455 import FEPart
    from ._2456 import FlexiblePinAssembly
    from ._2457 import GuideDxfModel
    from ._2458 import GuideImage
    from ._2459 import GuideModelUsage
    from ._2460 import InnerBearingRaceMountingOptions
    from ._2461 import InternalClearanceTolerance
    from ._2462 import LoadSharingModes
    from ._2463 import LoadSharingSettings
    from ._2464 import MassDisc
    from ._2465 import MeasurementComponent
    from ._2466 import MountableComponent
    from ._2467 import OilLevelSpecification
    from ._2468 import OilSeal
    from ._2469 import OuterBearingRaceMountingOptions
    from ._2470 import Part
    from ._2471 import PlanetCarrier
    from ._2472 import PlanetCarrierSettings
    from ._2473 import PointLoad
    from ._2474 import PowerLoad
    from ._2475 import RadialInternalClearanceTolerance
    from ._2476 import RootAssembly
    from ._2477 import ShaftDiameterModificationDueToRollingBearingRing
    from ._2478 import SpecialisedAssembly
    from ._2479 import UnbalancedMass
    from ._2480 import UnbalancedMassInclusionOption
    from ._2481 import VirtualComponent
    from ._2482 import WindTurbineBladeModeDetails
    from ._2483 import WindTurbineSingleBladeDetails
else:
    import_structure = {
        "_2435": ["Assembly"],
        "_2436": ["AbstractAssembly"],
        "_2437": ["AbstractShaft"],
        "_2438": ["AbstractShaftOrHousing"],
        "_2439": ["AGMALoadSharingTableApplicationLevel"],
        "_2440": ["AxialInternalClearanceTolerance"],
        "_2441": ["Bearing"],
        "_2442": ["BearingF0InputMethod"],
        "_2443": ["BearingRaceMountingOptions"],
        "_2444": ["Bolt"],
        "_2445": ["BoltedJoint"],
        "_2446": ["Component"],
        "_2447": ["ComponentsConnectedResult"],
        "_2448": ["ConnectedSockets"],
        "_2449": ["Connector"],
        "_2450": ["Datum"],
        "_2451": ["ElectricMachineSearchRegionSpecificationMethod"],
        "_2452": ["EnginePartLoad"],
        "_2453": ["EngineSpeed"],
        "_2454": ["ExternalCADModel"],
        "_2455": ["FEPart"],
        "_2456": ["FlexiblePinAssembly"],
        "_2457": ["GuideDxfModel"],
        "_2458": ["GuideImage"],
        "_2459": ["GuideModelUsage"],
        "_2460": ["InnerBearingRaceMountingOptions"],
        "_2461": ["InternalClearanceTolerance"],
        "_2462": ["LoadSharingModes"],
        "_2463": ["LoadSharingSettings"],
        "_2464": ["MassDisc"],
        "_2465": ["MeasurementComponent"],
        "_2466": ["MountableComponent"],
        "_2467": ["OilLevelSpecification"],
        "_2468": ["OilSeal"],
        "_2469": ["OuterBearingRaceMountingOptions"],
        "_2470": ["Part"],
        "_2471": ["PlanetCarrier"],
        "_2472": ["PlanetCarrierSettings"],
        "_2473": ["PointLoad"],
        "_2474": ["PowerLoad"],
        "_2475": ["RadialInternalClearanceTolerance"],
        "_2476": ["RootAssembly"],
        "_2477": ["ShaftDiameterModificationDueToRollingBearingRing"],
        "_2478": ["SpecialisedAssembly"],
        "_2479": ["UnbalancedMass"],
        "_2480": ["UnbalancedMassInclusionOption"],
        "_2481": ["VirtualComponent"],
        "_2482": ["WindTurbineBladeModeDetails"],
        "_2483": ["WindTurbineSingleBladeDetails"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Assembly",
    "AbstractAssembly",
    "AbstractShaft",
    "AbstractShaftOrHousing",
    "AGMALoadSharingTableApplicationLevel",
    "AxialInternalClearanceTolerance",
    "Bearing",
    "BearingF0InputMethod",
    "BearingRaceMountingOptions",
    "Bolt",
    "BoltedJoint",
    "Component",
    "ComponentsConnectedResult",
    "ConnectedSockets",
    "Connector",
    "Datum",
    "ElectricMachineSearchRegionSpecificationMethod",
    "EnginePartLoad",
    "EngineSpeed",
    "ExternalCADModel",
    "FEPart",
    "FlexiblePinAssembly",
    "GuideDxfModel",
    "GuideImage",
    "GuideModelUsage",
    "InnerBearingRaceMountingOptions",
    "InternalClearanceTolerance",
    "LoadSharingModes",
    "LoadSharingSettings",
    "MassDisc",
    "MeasurementComponent",
    "MountableComponent",
    "OilLevelSpecification",
    "OilSeal",
    "OuterBearingRaceMountingOptions",
    "Part",
    "PlanetCarrier",
    "PlanetCarrierSettings",
    "PointLoad",
    "PowerLoad",
    "RadialInternalClearanceTolerance",
    "RootAssembly",
    "ShaftDiameterModificationDueToRollingBearingRing",
    "SpecialisedAssembly",
    "UnbalancedMass",
    "UnbalancedMassInclusionOption",
    "VirtualComponent",
    "WindTurbineBladeModeDetails",
    "WindTurbineSingleBladeDetails",
)
