"""AnalysisCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results import _2652
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ANALYSIS_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases", "AnalysisCase"
)

if TYPE_CHECKING:
    from mastapy.utility import _1580
    from mastapy.system_model import _2205
    from mastapy.system_model.analyses_and_results import _2653


__docformat__ = "restructuredtext en"
__all__ = ("AnalysisCase",)


Self = TypeVar("Self", bound="AnalysisCase")


class AnalysisCase(_2652.Context):
    """AnalysisCase

    This is a mastapy class.
    """

    TYPE = _ANALYSIS_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_AnalysisCase")

    class _Cast_AnalysisCase:
        """Special nested class for casting AnalysisCase to subclasses."""

        def __init__(self: "AnalysisCase._Cast_AnalysisCase", parent: "AnalysisCase"):
            self._parent = parent

        @property
        def context(self: "AnalysisCase._Cast_AnalysisCase"):
            return self._parent._cast(_2652.Context)

        @property
        def system_deflection(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2827,
            )

            return self._parent._cast(_2827.SystemDeflection)

        @property
        def torsional_system_deflection(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2834,
            )

            return self._parent._cast(_2834.TorsionalSystemDeflection)

        @property
        def dynamic_model_for_steady_state_synchronous_response(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3037,
            )

            return self._parent._cast(
                _3037.DynamicModelForSteadyStateSynchronousResponse
            )

        @property
        def steady_state_synchronous_response(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3091,
            )

            return self._parent._cast(_3091.SteadyStateSynchronousResponse)

        @property
        def steady_state_synchronous_response_on_a_shaft(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3352,
            )

            return self._parent._cast(_3352.SteadyStateSynchronousResponseOnAShaft)

        @property
        def steady_state_synchronous_response_at_a_speed(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3611,
            )

            return self._parent._cast(_3611.SteadyStateSynchronousResponseAtASpeed)

        @property
        def dynamic_model_for_stability_analysis(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3818,
            )

            return self._parent._cast(_3818.DynamicModelForStabilityAnalysis)

        @property
        def stability_analysis(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3872,
            )

            return self._parent._cast(_3872.StabilityAnalysis)

        @property
        def power_flow(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.power_flows import _4124

            return self._parent._cast(_4124.PowerFlow)

        @property
        def parametric_study_tool(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4390,
            )

            return self._parent._cast(_4390.ParametricStudyTool)

        @property
        def dynamic_model_for_modal_analysis(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4627

            return self._parent._cast(_4627.DynamicModelForModalAnalysis)

        @property
        def modal_analysis(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4656

            return self._parent._cast(_4656.ModalAnalysis)

        @property
        def dynamic_model_at_a_stiffness(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4911,
            )

            return self._parent._cast(_4911.DynamicModelAtAStiffness)

        @property
        def modal_analysis_at_a_stiffness(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4937,
            )

            return self._parent._cast(_4937.ModalAnalysisAtAStiffness)

        @property
        def modal_analysis_at_a_speed(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5196,
            )

            return self._parent._cast(_5196.ModalAnalysisAtASpeed)

        @property
        def multibody_dynamics_analysis(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5467

            return self._parent._cast(_5467.MultibodyDynamicsAnalysis)

        @property
        def dynamic_model_for_harmonic_analysis(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5734,
            )

            return self._parent._cast(_5734.DynamicModelForHarmonicAnalysis)

        @property
        def harmonic_analysis(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5763,
            )

            return self._parent._cast(_5763.HarmonicAnalysis)

        @property
        def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5767,
            )

            return self._parent._cast(
                _5767.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def harmonic_analysis_of_single_excitation(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6072,
            )

            return self._parent._cast(_6072.HarmonicAnalysisOfSingleExcitation)

        @property
        def modal_analysis_for_harmonic_analysis(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6088,
            )

            return self._parent._cast(_6088.ModalAnalysisForHarmonicAnalysis)

        @property
        def dynamic_analysis(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6331

            return self._parent._cast(_6331.DynamicAnalysis)

        @property
        def critical_speed_analysis(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.critical_speed_analyses import (
                _6585,
            )

            return self._parent._cast(_6585.CriticalSpeedAnalysis)

        @property
        def advanced_time_stepping_analysis_for_modulation(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7012,
            )

            return self._parent._cast(_7012.AdvancedTimeSteppingAnalysisForModulation)

        @property
        def advanced_system_deflection(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7276,
            )

            return self._parent._cast(_7276.AdvancedSystemDeflection)

        @property
        def advanced_system_deflection_sub_analysis(
            self: "AnalysisCase._Cast_AnalysisCase",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7278,
            )

            return self._parent._cast(_7278.AdvancedSystemDeflectionSubAnalysis)

        @property
        def compound_analysis_case(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7539

            return self._parent._cast(_7539.CompoundAnalysisCase)

        @property
        def fe_analysis(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.FEAnalysis)

        @property
        def static_load_analysis_case(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7552

            return self._parent._cast(_7552.StaticLoadAnalysisCase)

        @property
        def time_series_load_analysis_case(self: "AnalysisCase._Cast_AnalysisCase"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7553

            return self._parent._cast(_7553.TimeSeriesLoadAnalysisCase)

        @property
        def analysis_case(self: "AnalysisCase._Cast_AnalysisCase") -> "AnalysisCase":
            return self._parent

        def __getattr__(self: "AnalysisCase._Cast_AnalysisCase", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "AnalysisCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_setup_time(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AnalysisSetupTime

        if temp is None:
            return 0.0

        return temp

    @property
    def load_case_name(self: Self) -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = self.wrapped.LoadCaseName

        if temp is None:
            return ""

        return temp

    @property
    def analysis_run_information(self: Self) -> "_1580.AnalysisRunInformation":
        """mastapy.utility.AnalysisRunInformation

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AnalysisRunInformation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results_ready(self: Self) -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ResultsReady

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def results_for(
        self: Self, design_entity: "_2205.DesignEntity"
    ) -> "_2653.DesignEntityAnalysis":
        """mastapy.system_model.analyses_and_results.DesignEntityAnalysis

        Args:
            design_entity (mastapy.system_model.DesignEntity)
        """
        method_result = self.wrapped.ResultsFor(
            design_entity.wrapped if design_entity else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def perform_analysis(self: Self):
        """Method does not return."""
        self.wrapped.PerformAnalysis()

    @property
    def cast_to(self: Self) -> "AnalysisCase._Cast_AnalysisCase":
        return self._Cast_AnalysisCase(self)
