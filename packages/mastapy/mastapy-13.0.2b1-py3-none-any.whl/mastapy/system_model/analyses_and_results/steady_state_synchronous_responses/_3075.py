"""RingPinsSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3063,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_RING_PINS_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "RingPinsSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.cycloidal import _2572
    from mastapy.system_model.analyses_and_results.static_loads import _6946


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsSteadyStateSynchronousResponse",)


Self = TypeVar("Self", bound="RingPinsSteadyStateSynchronousResponse")


class RingPinsSteadyStateSynchronousResponse(
    _3063.MountableComponentSteadyStateSynchronousResponse
):
    """RingPinsSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _RING_PINS_STEADY_STATE_SYNCHRONOUS_RESPONSE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_RingPinsSteadyStateSynchronousResponse"
    )

    class _Cast_RingPinsSteadyStateSynchronousResponse:
        """Special nested class for casting RingPinsSteadyStateSynchronousResponse to subclasses."""

        def __init__(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
            parent: "RingPinsSteadyStateSynchronousResponse",
        ):
            self._parent = parent

        @property
        def mountable_component_steady_state_synchronous_response(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ):
            return self._parent._cast(
                _3063.MountableComponentSteadyStateSynchronousResponse
            )

        @property
        def component_steady_state_synchronous_response(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3010,
            )

            return self._parent._cast(_3010.ComponentSteadyStateSynchronousResponse)

        @property
        def part_steady_state_synchronous_response(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3065,
            )

            return self._parent._cast(_3065.PartSteadyStateSynchronousResponse)

        @property
        def part_static_load_analysis_case(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def ring_pins_steady_state_synchronous_response(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
        ) -> "RingPinsSteadyStateSynchronousResponse":
            return self._parent

        def __getattr__(
            self: "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse",
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
        self: Self, instance_to_wrap: "RingPinsSteadyStateSynchronousResponse.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2572.RingPins":
        """mastapy.system_model.part_model.cycloidal.RingPins

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6946.RingPinsLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase

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
    ) -> "RingPinsSteadyStateSynchronousResponse._Cast_RingPinsSteadyStateSynchronousResponse":
        return self._Cast_RingPinsSteadyStateSynchronousResponse(self)
