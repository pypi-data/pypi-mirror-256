"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._5531 import AbstractAssemblyCompoundMultibodyDynamicsAnalysis
    from ._5532 import AbstractShaftCompoundMultibodyDynamicsAnalysis
    from ._5533 import AbstractShaftOrHousingCompoundMultibodyDynamicsAnalysis
    from ._5534 import (
        AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis,
    )
    from ._5535 import AGMAGleasonConicalGearCompoundMultibodyDynamicsAnalysis
    from ._5536 import AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5537 import AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis
    from ._5538 import AssemblyCompoundMultibodyDynamicsAnalysis
    from ._5539 import BearingCompoundMultibodyDynamicsAnalysis
    from ._5540 import BeltConnectionCompoundMultibodyDynamicsAnalysis
    from ._5541 import BeltDriveCompoundMultibodyDynamicsAnalysis
    from ._5542 import BevelDifferentialGearCompoundMultibodyDynamicsAnalysis
    from ._5543 import BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5544 import BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis
    from ._5545 import BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis
    from ._5546 import BevelDifferentialSunGearCompoundMultibodyDynamicsAnalysis
    from ._5547 import BevelGearCompoundMultibodyDynamicsAnalysis
    from ._5548 import BevelGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5549 import BevelGearSetCompoundMultibodyDynamicsAnalysis
    from ._5550 import BoltCompoundMultibodyDynamicsAnalysis
    from ._5551 import BoltedJointCompoundMultibodyDynamicsAnalysis
    from ._5552 import ClutchCompoundMultibodyDynamicsAnalysis
    from ._5553 import ClutchConnectionCompoundMultibodyDynamicsAnalysis
    from ._5554 import ClutchHalfCompoundMultibodyDynamicsAnalysis
    from ._5555 import CoaxialConnectionCompoundMultibodyDynamicsAnalysis
    from ._5556 import ComponentCompoundMultibodyDynamicsAnalysis
    from ._5557 import ConceptCouplingCompoundMultibodyDynamicsAnalysis
    from ._5558 import ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis
    from ._5559 import ConceptCouplingHalfCompoundMultibodyDynamicsAnalysis
    from ._5560 import ConceptGearCompoundMultibodyDynamicsAnalysis
    from ._5561 import ConceptGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5562 import ConceptGearSetCompoundMultibodyDynamicsAnalysis
    from ._5563 import ConicalGearCompoundMultibodyDynamicsAnalysis
    from ._5564 import ConicalGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5565 import ConicalGearSetCompoundMultibodyDynamicsAnalysis
    from ._5566 import ConnectionCompoundMultibodyDynamicsAnalysis
    from ._5567 import ConnectorCompoundMultibodyDynamicsAnalysis
    from ._5568 import CouplingCompoundMultibodyDynamicsAnalysis
    from ._5569 import CouplingConnectionCompoundMultibodyDynamicsAnalysis
    from ._5570 import CouplingHalfCompoundMultibodyDynamicsAnalysis
    from ._5571 import CVTBeltConnectionCompoundMultibodyDynamicsAnalysis
    from ._5572 import CVTCompoundMultibodyDynamicsAnalysis
    from ._5573 import CVTPulleyCompoundMultibodyDynamicsAnalysis
    from ._5574 import CycloidalAssemblyCompoundMultibodyDynamicsAnalysis
    from ._5575 import (
        CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis,
    )
    from ._5576 import CycloidalDiscCompoundMultibodyDynamicsAnalysis
    from ._5577 import (
        CycloidalDiscPlanetaryBearingConnectionCompoundMultibodyDynamicsAnalysis,
    )
    from ._5578 import CylindricalGearCompoundMultibodyDynamicsAnalysis
    from ._5579 import CylindricalGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5580 import CylindricalGearSetCompoundMultibodyDynamicsAnalysis
    from ._5581 import CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis
    from ._5582 import DatumCompoundMultibodyDynamicsAnalysis
    from ._5583 import ExternalCADModelCompoundMultibodyDynamicsAnalysis
    from ._5584 import FaceGearCompoundMultibodyDynamicsAnalysis
    from ._5585 import FaceGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5586 import FaceGearSetCompoundMultibodyDynamicsAnalysis
    from ._5587 import FEPartCompoundMultibodyDynamicsAnalysis
    from ._5588 import FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis
    from ._5589 import GearCompoundMultibodyDynamicsAnalysis
    from ._5590 import GearMeshCompoundMultibodyDynamicsAnalysis
    from ._5591 import GearSetCompoundMultibodyDynamicsAnalysis
    from ._5592 import GuideDxfModelCompoundMultibodyDynamicsAnalysis
    from ._5593 import HypoidGearCompoundMultibodyDynamicsAnalysis
    from ._5594 import HypoidGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5595 import HypoidGearSetCompoundMultibodyDynamicsAnalysis
    from ._5596 import (
        InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis,
    )
    from ._5597 import (
        KlingelnbergCycloPalloidConicalGearCompoundMultibodyDynamicsAnalysis,
    )
    from ._5598 import (
        KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis,
    )
    from ._5599 import (
        KlingelnbergCycloPalloidConicalGearSetCompoundMultibodyDynamicsAnalysis,
    )
    from ._5600 import (
        KlingelnbergCycloPalloidHypoidGearCompoundMultibodyDynamicsAnalysis,
    )
    from ._5601 import (
        KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis,
    )
    from ._5602 import (
        KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis,
    )
    from ._5603 import (
        KlingelnbergCycloPalloidSpiralBevelGearCompoundMultibodyDynamicsAnalysis,
    )
    from ._5604 import (
        KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis,
    )
    from ._5605 import (
        KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis,
    )
    from ._5606 import MassDiscCompoundMultibodyDynamicsAnalysis
    from ._5607 import MeasurementComponentCompoundMultibodyDynamicsAnalysis
    from ._5608 import MountableComponentCompoundMultibodyDynamicsAnalysis
    from ._5609 import OilSealCompoundMultibodyDynamicsAnalysis
    from ._5610 import PartCompoundMultibodyDynamicsAnalysis
    from ._5611 import PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis
    from ._5612 import (
        PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis,
    )
    from ._5613 import PartToPartShearCouplingHalfCompoundMultibodyDynamicsAnalysis
    from ._5614 import PlanetaryConnectionCompoundMultibodyDynamicsAnalysis
    from ._5615 import PlanetaryGearSetCompoundMultibodyDynamicsAnalysis
    from ._5616 import PlanetCarrierCompoundMultibodyDynamicsAnalysis
    from ._5617 import PointLoadCompoundMultibodyDynamicsAnalysis
    from ._5618 import PowerLoadCompoundMultibodyDynamicsAnalysis
    from ._5619 import PulleyCompoundMultibodyDynamicsAnalysis
    from ._5620 import RingPinsCompoundMultibodyDynamicsAnalysis
    from ._5621 import RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis
    from ._5622 import RollingRingAssemblyCompoundMultibodyDynamicsAnalysis
    from ._5623 import RollingRingCompoundMultibodyDynamicsAnalysis
    from ._5624 import RollingRingConnectionCompoundMultibodyDynamicsAnalysis
    from ._5625 import RootAssemblyCompoundMultibodyDynamicsAnalysis
    from ._5626 import ShaftCompoundMultibodyDynamicsAnalysis
    from ._5627 import ShaftHubConnectionCompoundMultibodyDynamicsAnalysis
    from ._5628 import (
        ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis,
    )
    from ._5629 import SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis
    from ._5630 import SpiralBevelGearCompoundMultibodyDynamicsAnalysis
    from ._5631 import SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5632 import SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis
    from ._5633 import SpringDamperCompoundMultibodyDynamicsAnalysis
    from ._5634 import SpringDamperConnectionCompoundMultibodyDynamicsAnalysis
    from ._5635 import SpringDamperHalfCompoundMultibodyDynamicsAnalysis
    from ._5636 import StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis
    from ._5637 import StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5638 import StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis
    from ._5639 import StraightBevelGearCompoundMultibodyDynamicsAnalysis
    from ._5640 import StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5641 import StraightBevelGearSetCompoundMultibodyDynamicsAnalysis
    from ._5642 import StraightBevelPlanetGearCompoundMultibodyDynamicsAnalysis
    from ._5643 import StraightBevelSunGearCompoundMultibodyDynamicsAnalysis
    from ._5644 import SynchroniserCompoundMultibodyDynamicsAnalysis
    from ._5645 import SynchroniserHalfCompoundMultibodyDynamicsAnalysis
    from ._5646 import SynchroniserPartCompoundMultibodyDynamicsAnalysis
    from ._5647 import SynchroniserSleeveCompoundMultibodyDynamicsAnalysis
    from ._5648 import TorqueConverterCompoundMultibodyDynamicsAnalysis
    from ._5649 import TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis
    from ._5650 import TorqueConverterPumpCompoundMultibodyDynamicsAnalysis
    from ._5651 import TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis
    from ._5652 import UnbalancedMassCompoundMultibodyDynamicsAnalysis
    from ._5653 import VirtualComponentCompoundMultibodyDynamicsAnalysis
    from ._5654 import WormGearCompoundMultibodyDynamicsAnalysis
    from ._5655 import WormGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5656 import WormGearSetCompoundMultibodyDynamicsAnalysis
    from ._5657 import ZerolBevelGearCompoundMultibodyDynamicsAnalysis
    from ._5658 import ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis
    from ._5659 import ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis
else:
    import_structure = {
        "_5531": ["AbstractAssemblyCompoundMultibodyDynamicsAnalysis"],
        "_5532": ["AbstractShaftCompoundMultibodyDynamicsAnalysis"],
        "_5533": ["AbstractShaftOrHousingCompoundMultibodyDynamicsAnalysis"],
        "_5534": [
            "AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis"
        ],
        "_5535": ["AGMAGleasonConicalGearCompoundMultibodyDynamicsAnalysis"],
        "_5536": ["AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5537": ["AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5538": ["AssemblyCompoundMultibodyDynamicsAnalysis"],
        "_5539": ["BearingCompoundMultibodyDynamicsAnalysis"],
        "_5540": ["BeltConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5541": ["BeltDriveCompoundMultibodyDynamicsAnalysis"],
        "_5542": ["BevelDifferentialGearCompoundMultibodyDynamicsAnalysis"],
        "_5543": ["BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5544": ["BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5545": ["BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis"],
        "_5546": ["BevelDifferentialSunGearCompoundMultibodyDynamicsAnalysis"],
        "_5547": ["BevelGearCompoundMultibodyDynamicsAnalysis"],
        "_5548": ["BevelGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5549": ["BevelGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5550": ["BoltCompoundMultibodyDynamicsAnalysis"],
        "_5551": ["BoltedJointCompoundMultibodyDynamicsAnalysis"],
        "_5552": ["ClutchCompoundMultibodyDynamicsAnalysis"],
        "_5553": ["ClutchConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5554": ["ClutchHalfCompoundMultibodyDynamicsAnalysis"],
        "_5555": ["CoaxialConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5556": ["ComponentCompoundMultibodyDynamicsAnalysis"],
        "_5557": ["ConceptCouplingCompoundMultibodyDynamicsAnalysis"],
        "_5558": ["ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5559": ["ConceptCouplingHalfCompoundMultibodyDynamicsAnalysis"],
        "_5560": ["ConceptGearCompoundMultibodyDynamicsAnalysis"],
        "_5561": ["ConceptGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5562": ["ConceptGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5563": ["ConicalGearCompoundMultibodyDynamicsAnalysis"],
        "_5564": ["ConicalGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5565": ["ConicalGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5566": ["ConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5567": ["ConnectorCompoundMultibodyDynamicsAnalysis"],
        "_5568": ["CouplingCompoundMultibodyDynamicsAnalysis"],
        "_5569": ["CouplingConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5570": ["CouplingHalfCompoundMultibodyDynamicsAnalysis"],
        "_5571": ["CVTBeltConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5572": ["CVTCompoundMultibodyDynamicsAnalysis"],
        "_5573": ["CVTPulleyCompoundMultibodyDynamicsAnalysis"],
        "_5574": ["CycloidalAssemblyCompoundMultibodyDynamicsAnalysis"],
        "_5575": [
            "CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis"
        ],
        "_5576": ["CycloidalDiscCompoundMultibodyDynamicsAnalysis"],
        "_5577": [
            "CycloidalDiscPlanetaryBearingConnectionCompoundMultibodyDynamicsAnalysis"
        ],
        "_5578": ["CylindricalGearCompoundMultibodyDynamicsAnalysis"],
        "_5579": ["CylindricalGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5580": ["CylindricalGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5581": ["CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis"],
        "_5582": ["DatumCompoundMultibodyDynamicsAnalysis"],
        "_5583": ["ExternalCADModelCompoundMultibodyDynamicsAnalysis"],
        "_5584": ["FaceGearCompoundMultibodyDynamicsAnalysis"],
        "_5585": ["FaceGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5586": ["FaceGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5587": ["FEPartCompoundMultibodyDynamicsAnalysis"],
        "_5588": ["FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis"],
        "_5589": ["GearCompoundMultibodyDynamicsAnalysis"],
        "_5590": ["GearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5591": ["GearSetCompoundMultibodyDynamicsAnalysis"],
        "_5592": ["GuideDxfModelCompoundMultibodyDynamicsAnalysis"],
        "_5593": ["HypoidGearCompoundMultibodyDynamicsAnalysis"],
        "_5594": ["HypoidGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5595": ["HypoidGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5596": ["InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5597": [
            "KlingelnbergCycloPalloidConicalGearCompoundMultibodyDynamicsAnalysis"
        ],
        "_5598": [
            "KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis"
        ],
        "_5599": [
            "KlingelnbergCycloPalloidConicalGearSetCompoundMultibodyDynamicsAnalysis"
        ],
        "_5600": [
            "KlingelnbergCycloPalloidHypoidGearCompoundMultibodyDynamicsAnalysis"
        ],
        "_5601": [
            "KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis"
        ],
        "_5602": [
            "KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis"
        ],
        "_5603": [
            "KlingelnbergCycloPalloidSpiralBevelGearCompoundMultibodyDynamicsAnalysis"
        ],
        "_5604": [
            "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis"
        ],
        "_5605": [
            "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis"
        ],
        "_5606": ["MassDiscCompoundMultibodyDynamicsAnalysis"],
        "_5607": ["MeasurementComponentCompoundMultibodyDynamicsAnalysis"],
        "_5608": ["MountableComponentCompoundMultibodyDynamicsAnalysis"],
        "_5609": ["OilSealCompoundMultibodyDynamicsAnalysis"],
        "_5610": ["PartCompoundMultibodyDynamicsAnalysis"],
        "_5611": ["PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis"],
        "_5612": ["PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5613": ["PartToPartShearCouplingHalfCompoundMultibodyDynamicsAnalysis"],
        "_5614": ["PlanetaryConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5615": ["PlanetaryGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5616": ["PlanetCarrierCompoundMultibodyDynamicsAnalysis"],
        "_5617": ["PointLoadCompoundMultibodyDynamicsAnalysis"],
        "_5618": ["PowerLoadCompoundMultibodyDynamicsAnalysis"],
        "_5619": ["PulleyCompoundMultibodyDynamicsAnalysis"],
        "_5620": ["RingPinsCompoundMultibodyDynamicsAnalysis"],
        "_5621": ["RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5622": ["RollingRingAssemblyCompoundMultibodyDynamicsAnalysis"],
        "_5623": ["RollingRingCompoundMultibodyDynamicsAnalysis"],
        "_5624": ["RollingRingConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5625": ["RootAssemblyCompoundMultibodyDynamicsAnalysis"],
        "_5626": ["ShaftCompoundMultibodyDynamicsAnalysis"],
        "_5627": ["ShaftHubConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5628": [
            "ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis"
        ],
        "_5629": ["SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis"],
        "_5630": ["SpiralBevelGearCompoundMultibodyDynamicsAnalysis"],
        "_5631": ["SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5632": ["SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5633": ["SpringDamperCompoundMultibodyDynamicsAnalysis"],
        "_5634": ["SpringDamperConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5635": ["SpringDamperHalfCompoundMultibodyDynamicsAnalysis"],
        "_5636": ["StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis"],
        "_5637": ["StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5638": ["StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5639": ["StraightBevelGearCompoundMultibodyDynamicsAnalysis"],
        "_5640": ["StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5641": ["StraightBevelGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5642": ["StraightBevelPlanetGearCompoundMultibodyDynamicsAnalysis"],
        "_5643": ["StraightBevelSunGearCompoundMultibodyDynamicsAnalysis"],
        "_5644": ["SynchroniserCompoundMultibodyDynamicsAnalysis"],
        "_5645": ["SynchroniserHalfCompoundMultibodyDynamicsAnalysis"],
        "_5646": ["SynchroniserPartCompoundMultibodyDynamicsAnalysis"],
        "_5647": ["SynchroniserSleeveCompoundMultibodyDynamicsAnalysis"],
        "_5648": ["TorqueConverterCompoundMultibodyDynamicsAnalysis"],
        "_5649": ["TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis"],
        "_5650": ["TorqueConverterPumpCompoundMultibodyDynamicsAnalysis"],
        "_5651": ["TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis"],
        "_5652": ["UnbalancedMassCompoundMultibodyDynamicsAnalysis"],
        "_5653": ["VirtualComponentCompoundMultibodyDynamicsAnalysis"],
        "_5654": ["WormGearCompoundMultibodyDynamicsAnalysis"],
        "_5655": ["WormGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5656": ["WormGearSetCompoundMultibodyDynamicsAnalysis"],
        "_5657": ["ZerolBevelGearCompoundMultibodyDynamicsAnalysis"],
        "_5658": ["ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis"],
        "_5659": ["ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AbstractAssemblyCompoundMultibodyDynamicsAnalysis",
    "AbstractShaftCompoundMultibodyDynamicsAnalysis",
    "AbstractShaftOrHousingCompoundMultibodyDynamicsAnalysis",
    "AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
    "AGMAGleasonConicalGearCompoundMultibodyDynamicsAnalysis",
    "AGMAGleasonConicalGearMeshCompoundMultibodyDynamicsAnalysis",
    "AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis",
    "AssemblyCompoundMultibodyDynamicsAnalysis",
    "BearingCompoundMultibodyDynamicsAnalysis",
    "BeltConnectionCompoundMultibodyDynamicsAnalysis",
    "BeltDriveCompoundMultibodyDynamicsAnalysis",
    "BevelDifferentialGearCompoundMultibodyDynamicsAnalysis",
    "BevelDifferentialGearMeshCompoundMultibodyDynamicsAnalysis",
    "BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis",
    "BevelDifferentialPlanetGearCompoundMultibodyDynamicsAnalysis",
    "BevelDifferentialSunGearCompoundMultibodyDynamicsAnalysis",
    "BevelGearCompoundMultibodyDynamicsAnalysis",
    "BevelGearMeshCompoundMultibodyDynamicsAnalysis",
    "BevelGearSetCompoundMultibodyDynamicsAnalysis",
    "BoltCompoundMultibodyDynamicsAnalysis",
    "BoltedJointCompoundMultibodyDynamicsAnalysis",
    "ClutchCompoundMultibodyDynamicsAnalysis",
    "ClutchConnectionCompoundMultibodyDynamicsAnalysis",
    "ClutchHalfCompoundMultibodyDynamicsAnalysis",
    "CoaxialConnectionCompoundMultibodyDynamicsAnalysis",
    "ComponentCompoundMultibodyDynamicsAnalysis",
    "ConceptCouplingCompoundMultibodyDynamicsAnalysis",
    "ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis",
    "ConceptCouplingHalfCompoundMultibodyDynamicsAnalysis",
    "ConceptGearCompoundMultibodyDynamicsAnalysis",
    "ConceptGearMeshCompoundMultibodyDynamicsAnalysis",
    "ConceptGearSetCompoundMultibodyDynamicsAnalysis",
    "ConicalGearCompoundMultibodyDynamicsAnalysis",
    "ConicalGearMeshCompoundMultibodyDynamicsAnalysis",
    "ConicalGearSetCompoundMultibodyDynamicsAnalysis",
    "ConnectionCompoundMultibodyDynamicsAnalysis",
    "ConnectorCompoundMultibodyDynamicsAnalysis",
    "CouplingCompoundMultibodyDynamicsAnalysis",
    "CouplingConnectionCompoundMultibodyDynamicsAnalysis",
    "CouplingHalfCompoundMultibodyDynamicsAnalysis",
    "CVTBeltConnectionCompoundMultibodyDynamicsAnalysis",
    "CVTCompoundMultibodyDynamicsAnalysis",
    "CVTPulleyCompoundMultibodyDynamicsAnalysis",
    "CycloidalAssemblyCompoundMultibodyDynamicsAnalysis",
    "CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis",
    "CycloidalDiscCompoundMultibodyDynamicsAnalysis",
    "CycloidalDiscPlanetaryBearingConnectionCompoundMultibodyDynamicsAnalysis",
    "CylindricalGearCompoundMultibodyDynamicsAnalysis",
    "CylindricalGearMeshCompoundMultibodyDynamicsAnalysis",
    "CylindricalGearSetCompoundMultibodyDynamicsAnalysis",
    "CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis",
    "DatumCompoundMultibodyDynamicsAnalysis",
    "ExternalCADModelCompoundMultibodyDynamicsAnalysis",
    "FaceGearCompoundMultibodyDynamicsAnalysis",
    "FaceGearMeshCompoundMultibodyDynamicsAnalysis",
    "FaceGearSetCompoundMultibodyDynamicsAnalysis",
    "FEPartCompoundMultibodyDynamicsAnalysis",
    "FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis",
    "GearCompoundMultibodyDynamicsAnalysis",
    "GearMeshCompoundMultibodyDynamicsAnalysis",
    "GearSetCompoundMultibodyDynamicsAnalysis",
    "GuideDxfModelCompoundMultibodyDynamicsAnalysis",
    "HypoidGearCompoundMultibodyDynamicsAnalysis",
    "HypoidGearMeshCompoundMultibodyDynamicsAnalysis",
    "HypoidGearSetCompoundMultibodyDynamicsAnalysis",
    "InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidConicalGearCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidConicalGearSetCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidHypoidGearCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis",
    "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis",
    "MassDiscCompoundMultibodyDynamicsAnalysis",
    "MeasurementComponentCompoundMultibodyDynamicsAnalysis",
    "MountableComponentCompoundMultibodyDynamicsAnalysis",
    "OilSealCompoundMultibodyDynamicsAnalysis",
    "PartCompoundMultibodyDynamicsAnalysis",
    "PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis",
    "PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis",
    "PartToPartShearCouplingHalfCompoundMultibodyDynamicsAnalysis",
    "PlanetaryConnectionCompoundMultibodyDynamicsAnalysis",
    "PlanetaryGearSetCompoundMultibodyDynamicsAnalysis",
    "PlanetCarrierCompoundMultibodyDynamicsAnalysis",
    "PointLoadCompoundMultibodyDynamicsAnalysis",
    "PowerLoadCompoundMultibodyDynamicsAnalysis",
    "PulleyCompoundMultibodyDynamicsAnalysis",
    "RingPinsCompoundMultibodyDynamicsAnalysis",
    "RingPinsToDiscConnectionCompoundMultibodyDynamicsAnalysis",
    "RollingRingAssemblyCompoundMultibodyDynamicsAnalysis",
    "RollingRingCompoundMultibodyDynamicsAnalysis",
    "RollingRingConnectionCompoundMultibodyDynamicsAnalysis",
    "RootAssemblyCompoundMultibodyDynamicsAnalysis",
    "ShaftCompoundMultibodyDynamicsAnalysis",
    "ShaftHubConnectionCompoundMultibodyDynamicsAnalysis",
    "ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
    "SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis",
    "SpiralBevelGearCompoundMultibodyDynamicsAnalysis",
    "SpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis",
    "SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis",
    "SpringDamperCompoundMultibodyDynamicsAnalysis",
    "SpringDamperConnectionCompoundMultibodyDynamicsAnalysis",
    "SpringDamperHalfCompoundMultibodyDynamicsAnalysis",
    "StraightBevelDiffGearCompoundMultibodyDynamicsAnalysis",
    "StraightBevelDiffGearMeshCompoundMultibodyDynamicsAnalysis",
    "StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis",
    "StraightBevelGearCompoundMultibodyDynamicsAnalysis",
    "StraightBevelGearMeshCompoundMultibodyDynamicsAnalysis",
    "StraightBevelGearSetCompoundMultibodyDynamicsAnalysis",
    "StraightBevelPlanetGearCompoundMultibodyDynamicsAnalysis",
    "StraightBevelSunGearCompoundMultibodyDynamicsAnalysis",
    "SynchroniserCompoundMultibodyDynamicsAnalysis",
    "SynchroniserHalfCompoundMultibodyDynamicsAnalysis",
    "SynchroniserPartCompoundMultibodyDynamicsAnalysis",
    "SynchroniserSleeveCompoundMultibodyDynamicsAnalysis",
    "TorqueConverterCompoundMultibodyDynamicsAnalysis",
    "TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis",
    "TorqueConverterPumpCompoundMultibodyDynamicsAnalysis",
    "TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis",
    "UnbalancedMassCompoundMultibodyDynamicsAnalysis",
    "VirtualComponentCompoundMultibodyDynamicsAnalysis",
    "WormGearCompoundMultibodyDynamicsAnalysis",
    "WormGearMeshCompoundMultibodyDynamicsAnalysis",
    "WormGearSetCompoundMultibodyDynamicsAnalysis",
    "ZerolBevelGearCompoundMultibodyDynamicsAnalysis",
    "ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis",
    "ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis",
)
