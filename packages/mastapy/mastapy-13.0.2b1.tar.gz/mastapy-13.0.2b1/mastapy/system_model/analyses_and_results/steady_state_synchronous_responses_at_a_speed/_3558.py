"""ExternalCADModelSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3531,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2454
    from mastapy.system_model.analyses_and_results.static_loads import _6886


__docformat__ = "restructuredtext en"
__all__ = ("ExternalCADModelSteadyStateSynchronousResponseAtASpeed",)


Self = TypeVar("Self", bound="ExternalCADModelSteadyStateSynchronousResponseAtASpeed")


class ExternalCADModelSteadyStateSynchronousResponseAtASpeed(
    _3531.ComponentSteadyStateSynchronousResponseAtASpeed
):
    """ExternalCADModelSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _EXTERNAL_CAD_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
    )

    class _Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed:
        """Special nested class for casting ExternalCADModelSteadyStateSynchronousResponseAtASpeed to subclasses."""

        def __init__(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
            parent: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ):
            self._parent = parent

        @property
        def component_steady_state_synchronous_response_at_a_speed(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ):
            return self._parent._cast(
                _3531.ComponentSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def part_steady_state_synchronous_response_at_a_speed(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3585,
            )

            return self._parent._cast(_3585.PartSteadyStateSynchronousResponseAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def external_cad_model_steady_state_synchronous_response_at_a_speed(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
        ) -> "ExternalCADModelSteadyStateSynchronousResponseAtASpeed":
            return self._parent

        def __getattr__(
            self: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed",
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
        instance_to_wrap: "ExternalCADModelSteadyStateSynchronousResponseAtASpeed.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2454.ExternalCADModel":
        """mastapy.system_model.part_model.ExternalCADModel

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6886.ExternalCADModelLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase

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
    ) -> "ExternalCADModelSteadyStateSynchronousResponseAtASpeed._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed":
        return self._Cast_ExternalCADModelSteadyStateSynchronousResponseAtASpeed(self)
