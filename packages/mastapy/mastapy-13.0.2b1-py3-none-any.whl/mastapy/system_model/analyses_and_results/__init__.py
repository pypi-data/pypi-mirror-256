"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._2621 import CompoundAnalysis
    from ._2622 import SingleAnalysis
    from ._2623 import AdvancedSystemDeflectionAnalysis
    from ._2624 import AdvancedSystemDeflectionSubAnalysis
    from ._2625 import AdvancedTimeSteppingAnalysisForModulation
    from ._2626 import CompoundParametricStudyToolAnalysis
    from ._2627 import CriticalSpeedAnalysis
    from ._2628 import DynamicAnalysis
    from ._2629 import DynamicModelAtAStiffnessAnalysis
    from ._2630 import DynamicModelForHarmonicAnalysis
    from ._2631 import DynamicModelForModalAnalysis
    from ._2632 import DynamicModelForStabilityAnalysis
    from ._2633 import DynamicModelForSteadyStateSynchronousResponseAnalysis
    from ._2634 import HarmonicAnalysis
    from ._2635 import HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
    from ._2636 import HarmonicAnalysisOfSingleExcitationAnalysis
    from ._2637 import ModalAnalysis
    from ._2638 import ModalAnalysisAtASpeed
    from ._2639 import ModalAnalysisAtAStiffness
    from ._2640 import ModalAnalysisForHarmonicAnalysis
    from ._2641 import MultibodyDynamicsAnalysis
    from ._2642 import ParametricStudyToolAnalysis
    from ._2643 import PowerFlowAnalysis
    from ._2644 import StabilityAnalysis
    from ._2645 import SteadyStateSynchronousResponseAnalysis
    from ._2646 import SteadyStateSynchronousResponseAtASpeedAnalysis
    from ._2647 import SteadyStateSynchronousResponseOnAShaftAnalysis
    from ._2648 import SystemDeflectionAnalysis
    from ._2649 import TorsionalSystemDeflectionAnalysis
    from ._2650 import AnalysisCaseVariable
    from ._2651 import ConnectionAnalysis
    from ._2652 import Context
    from ._2653 import DesignEntityAnalysis
    from ._2654 import DesignEntityGroupAnalysis
    from ._2655 import DesignEntitySingleContextAnalysis
    from ._2659 import PartAnalysis
    from ._2660 import CompoundAdvancedSystemDeflectionAnalysis
    from ._2661 import CompoundAdvancedSystemDeflectionSubAnalysis
    from ._2662 import CompoundAdvancedTimeSteppingAnalysisForModulation
    from ._2663 import CompoundCriticalSpeedAnalysis
    from ._2664 import CompoundDynamicAnalysis
    from ._2665 import CompoundDynamicModelAtAStiffnessAnalysis
    from ._2666 import CompoundDynamicModelForHarmonicAnalysis
    from ._2667 import CompoundDynamicModelForModalAnalysis
    from ._2668 import CompoundDynamicModelForStabilityAnalysis
    from ._2669 import CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis
    from ._2670 import CompoundHarmonicAnalysis
    from ._2671 import (
        CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from ._2672 import CompoundHarmonicAnalysisOfSingleExcitationAnalysis
    from ._2673 import CompoundModalAnalysis
    from ._2674 import CompoundModalAnalysisAtASpeed
    from ._2675 import CompoundModalAnalysisAtAStiffness
    from ._2676 import CompoundModalAnalysisForHarmonicAnalysis
    from ._2677 import CompoundMultibodyDynamicsAnalysis
    from ._2678 import CompoundPowerFlowAnalysis
    from ._2679 import CompoundStabilityAnalysis
    from ._2680 import CompoundSteadyStateSynchronousResponseAnalysis
    from ._2681 import CompoundSteadyStateSynchronousResponseAtASpeedAnalysis
    from ._2682 import CompoundSteadyStateSynchronousResponseOnAShaftAnalysis
    from ._2683 import CompoundSystemDeflectionAnalysis
    from ._2684 import CompoundTorsionalSystemDeflectionAnalysis
    from ._2685 import TESetUpForDynamicAnalysisOptions
    from ._2686 import TimeOptions
else:
    import_structure = {
        "_2621": ["CompoundAnalysis"],
        "_2622": ["SingleAnalysis"],
        "_2623": ["AdvancedSystemDeflectionAnalysis"],
        "_2624": ["AdvancedSystemDeflectionSubAnalysis"],
        "_2625": ["AdvancedTimeSteppingAnalysisForModulation"],
        "_2626": ["CompoundParametricStudyToolAnalysis"],
        "_2627": ["CriticalSpeedAnalysis"],
        "_2628": ["DynamicAnalysis"],
        "_2629": ["DynamicModelAtAStiffnessAnalysis"],
        "_2630": ["DynamicModelForHarmonicAnalysis"],
        "_2631": ["DynamicModelForModalAnalysis"],
        "_2632": ["DynamicModelForStabilityAnalysis"],
        "_2633": ["DynamicModelForSteadyStateSynchronousResponseAnalysis"],
        "_2634": ["HarmonicAnalysis"],
        "_2635": ["HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"],
        "_2636": ["HarmonicAnalysisOfSingleExcitationAnalysis"],
        "_2637": ["ModalAnalysis"],
        "_2638": ["ModalAnalysisAtASpeed"],
        "_2639": ["ModalAnalysisAtAStiffness"],
        "_2640": ["ModalAnalysisForHarmonicAnalysis"],
        "_2641": ["MultibodyDynamicsAnalysis"],
        "_2642": ["ParametricStudyToolAnalysis"],
        "_2643": ["PowerFlowAnalysis"],
        "_2644": ["StabilityAnalysis"],
        "_2645": ["SteadyStateSynchronousResponseAnalysis"],
        "_2646": ["SteadyStateSynchronousResponseAtASpeedAnalysis"],
        "_2647": ["SteadyStateSynchronousResponseOnAShaftAnalysis"],
        "_2648": ["SystemDeflectionAnalysis"],
        "_2649": ["TorsionalSystemDeflectionAnalysis"],
        "_2650": ["AnalysisCaseVariable"],
        "_2651": ["ConnectionAnalysis"],
        "_2652": ["Context"],
        "_2653": ["DesignEntityAnalysis"],
        "_2654": ["DesignEntityGroupAnalysis"],
        "_2655": ["DesignEntitySingleContextAnalysis"],
        "_2659": ["PartAnalysis"],
        "_2660": ["CompoundAdvancedSystemDeflectionAnalysis"],
        "_2661": ["CompoundAdvancedSystemDeflectionSubAnalysis"],
        "_2662": ["CompoundAdvancedTimeSteppingAnalysisForModulation"],
        "_2663": ["CompoundCriticalSpeedAnalysis"],
        "_2664": ["CompoundDynamicAnalysis"],
        "_2665": ["CompoundDynamicModelAtAStiffnessAnalysis"],
        "_2666": ["CompoundDynamicModelForHarmonicAnalysis"],
        "_2667": ["CompoundDynamicModelForModalAnalysis"],
        "_2668": ["CompoundDynamicModelForStabilityAnalysis"],
        "_2669": ["CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis"],
        "_2670": ["CompoundHarmonicAnalysis"],
        "_2671": [
            "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_2672": ["CompoundHarmonicAnalysisOfSingleExcitationAnalysis"],
        "_2673": ["CompoundModalAnalysis"],
        "_2674": ["CompoundModalAnalysisAtASpeed"],
        "_2675": ["CompoundModalAnalysisAtAStiffness"],
        "_2676": ["CompoundModalAnalysisForHarmonicAnalysis"],
        "_2677": ["CompoundMultibodyDynamicsAnalysis"],
        "_2678": ["CompoundPowerFlowAnalysis"],
        "_2679": ["CompoundStabilityAnalysis"],
        "_2680": ["CompoundSteadyStateSynchronousResponseAnalysis"],
        "_2681": ["CompoundSteadyStateSynchronousResponseAtASpeedAnalysis"],
        "_2682": ["CompoundSteadyStateSynchronousResponseOnAShaftAnalysis"],
        "_2683": ["CompoundSystemDeflectionAnalysis"],
        "_2684": ["CompoundTorsionalSystemDeflectionAnalysis"],
        "_2685": ["TESetUpForDynamicAnalysisOptions"],
        "_2686": ["TimeOptions"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "CompoundAnalysis",
    "SingleAnalysis",
    "AdvancedSystemDeflectionAnalysis",
    "AdvancedSystemDeflectionSubAnalysis",
    "AdvancedTimeSteppingAnalysisForModulation",
    "CompoundParametricStudyToolAnalysis",
    "CriticalSpeedAnalysis",
    "DynamicAnalysis",
    "DynamicModelAtAStiffnessAnalysis",
    "DynamicModelForHarmonicAnalysis",
    "DynamicModelForModalAnalysis",
    "DynamicModelForStabilityAnalysis",
    "DynamicModelForSteadyStateSynchronousResponseAnalysis",
    "HarmonicAnalysis",
    "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "HarmonicAnalysisOfSingleExcitationAnalysis",
    "ModalAnalysis",
    "ModalAnalysisAtASpeed",
    "ModalAnalysisAtAStiffness",
    "ModalAnalysisForHarmonicAnalysis",
    "MultibodyDynamicsAnalysis",
    "ParametricStudyToolAnalysis",
    "PowerFlowAnalysis",
    "StabilityAnalysis",
    "SteadyStateSynchronousResponseAnalysis",
    "SteadyStateSynchronousResponseAtASpeedAnalysis",
    "SteadyStateSynchronousResponseOnAShaftAnalysis",
    "SystemDeflectionAnalysis",
    "TorsionalSystemDeflectionAnalysis",
    "AnalysisCaseVariable",
    "ConnectionAnalysis",
    "Context",
    "DesignEntityAnalysis",
    "DesignEntityGroupAnalysis",
    "DesignEntitySingleContextAnalysis",
    "PartAnalysis",
    "CompoundAdvancedSystemDeflectionAnalysis",
    "CompoundAdvancedSystemDeflectionSubAnalysis",
    "CompoundAdvancedTimeSteppingAnalysisForModulation",
    "CompoundCriticalSpeedAnalysis",
    "CompoundDynamicAnalysis",
    "CompoundDynamicModelAtAStiffnessAnalysis",
    "CompoundDynamicModelForHarmonicAnalysis",
    "CompoundDynamicModelForModalAnalysis",
    "CompoundDynamicModelForStabilityAnalysis",
    "CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis",
    "CompoundHarmonicAnalysis",
    "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "CompoundHarmonicAnalysisOfSingleExcitationAnalysis",
    "CompoundModalAnalysis",
    "CompoundModalAnalysisAtASpeed",
    "CompoundModalAnalysisAtAStiffness",
    "CompoundModalAnalysisForHarmonicAnalysis",
    "CompoundMultibodyDynamicsAnalysis",
    "CompoundPowerFlowAnalysis",
    "CompoundStabilityAnalysis",
    "CompoundSteadyStateSynchronousResponseAnalysis",
    "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis",
    "CompoundSteadyStateSynchronousResponseOnAShaftAnalysis",
    "CompoundSystemDeflectionAnalysis",
    "CompoundTorsionalSystemDeflectionAnalysis",
    "TESetUpForDynamicAnalysisOptions",
    "TimeOptions",
)
