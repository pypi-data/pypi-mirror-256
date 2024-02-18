"""GuideDxfModelSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3531,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2457
    from mastapy.system_model.analyses_and_results.static_loads import _6899


__docformat__ = "restructuredtext en"
__all__ = ("GuideDxfModelSteadyStateSynchronousResponseAtASpeed",)


Self = TypeVar("Self", bound="GuideDxfModelSteadyStateSynchronousResponseAtASpeed")


class GuideDxfModelSteadyStateSynchronousResponseAtASpeed(
    _3531.ComponentSteadyStateSynchronousResponseAtASpeed
):
    """GuideDxfModelSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _GUIDE_DXF_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed"
    )

    class _Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed:
        """Special nested class for casting GuideDxfModelSteadyStateSynchronousResponseAtASpeed to subclasses."""

        def __init__(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
            parent: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ):
            self._parent = parent

        @property
        def component_steady_state_synchronous_response_at_a_speed(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ):
            return self._parent._cast(
                _3531.ComponentSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def part_steady_state_synchronous_response_at_a_speed(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3585,
            )

            return self._parent._cast(_3585.PartSteadyStateSynchronousResponseAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def guide_dxf_model_steady_state_synchronous_response_at_a_speed(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
        ) -> "GuideDxfModelSteadyStateSynchronousResponseAtASpeed":
            return self._parent

        def __getattr__(
            self: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(
        self: Self,
        instance_to_wrap: "GuideDxfModelSteadyStateSynchronousResponseAtASpeed.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2457.GuideDxfModel":
        """mastapy.system_model.part_model.GuideDxfModel

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6899.GuideDxfModelLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "GuideDxfModelSteadyStateSynchronousResponseAtASpeed._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed":
        return self._Cast_GuideDxfModelSteadyStateSynchronousResponseAtASpeed(self)
