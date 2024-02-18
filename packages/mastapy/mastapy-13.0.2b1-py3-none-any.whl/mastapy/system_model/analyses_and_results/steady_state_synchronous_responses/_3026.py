"""CVTPulleySteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3074,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "CVTPulleySteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2589


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleySteadyStateSynchronousResponse",)


Self = TypeVar("Self", bound="CVTPulleySteadyStateSynchronousResponse")


class CVTPulleySteadyStateSynchronousResponse(
    _3074.PulleySteadyStateSynchronousResponse
):
    """CVTPulleySteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_STEADY_STATE_SYNCHRONOUS_RESPONSE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CVTPulleySteadyStateSynchronousResponse"
    )

    class _Cast_CVTPulleySteadyStateSynchronousResponse:
        """Special nested class for casting CVTPulleySteadyStateSynchronousResponse to subclasses."""

        def __init__(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
            parent: "CVTPulleySteadyStateSynchronousResponse",
        ):
            self._parent = parent

        @property
        def pulley_steady_state_synchronous_response(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            return self._parent._cast(_3074.PulleySteadyStateSynchronousResponse)

        @property
        def coupling_half_steady_state_synchronous_response(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3023,
            )

            return self._parent._cast(_3023.CouplingHalfSteadyStateSynchronousResponse)

        @property
        def mountable_component_steady_state_synchronous_response(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3063,
            )

            return self._parent._cast(
                _3063.MountableComponentSteadyStateSynchronousResponse
            )

        @property
        def component_steady_state_synchronous_response(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3010,
            )

            return self._parent._cast(_3010.ComponentSteadyStateSynchronousResponse)

        @property
        def part_steady_state_synchronous_response(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3065,
            )

            return self._parent._cast(_3065.PartSteadyStateSynchronousResponse)

        @property
        def part_static_load_analysis_case(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cvt_pulley_steady_state_synchronous_response(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
        ) -> "CVTPulleySteadyStateSynchronousResponse":
            return self._parent

        def __getattr__(
            self: "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse",
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
        self: Self, instance_to_wrap: "CVTPulleySteadyStateSynchronousResponse.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2589.CVTPulley":
        """mastapy.system_model.part_model.couplings.CVTPulley

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CVTPulleySteadyStateSynchronousResponse._Cast_CVTPulleySteadyStateSynchronousResponse":
        return self._Cast_CVTPulleySteadyStateSynchronousResponse(self)
