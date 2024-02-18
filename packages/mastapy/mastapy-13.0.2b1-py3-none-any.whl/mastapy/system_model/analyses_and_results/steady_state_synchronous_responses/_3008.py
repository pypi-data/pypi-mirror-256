"""ClutchSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3024,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CLUTCH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "ClutchSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2580
    from mastapy.system_model.analyses_and_results.static_loads import _6837


__docformat__ = "restructuredtext en"
__all__ = ("ClutchSteadyStateSynchronousResponse",)


Self = TypeVar("Self", bound="ClutchSteadyStateSynchronousResponse")


class ClutchSteadyStateSynchronousResponse(
    _3024.CouplingSteadyStateSynchronousResponse
):
    """ClutchSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _CLUTCH_STEADY_STATE_SYNCHRONOUS_RESPONSE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ClutchSteadyStateSynchronousResponse")

    class _Cast_ClutchSteadyStateSynchronousResponse:
        """Special nested class for casting ClutchSteadyStateSynchronousResponse to subclasses."""

        def __init__(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
            parent: "ClutchSteadyStateSynchronousResponse",
        ):
            self._parent = parent

        @property
        def coupling_steady_state_synchronous_response(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            return self._parent._cast(_3024.CouplingSteadyStateSynchronousResponse)

        @property
        def specialised_assembly_steady_state_synchronous_response(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3084,
            )

            return self._parent._cast(
                _3084.SpecialisedAssemblySteadyStateSynchronousResponse
            )

        @property
        def abstract_assembly_steady_state_synchronous_response(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _2985,
            )

            return self._parent._cast(
                _2985.AbstractAssemblySteadyStateSynchronousResponse
            )

        @property
        def part_steady_state_synchronous_response(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3065,
            )

            return self._parent._cast(_3065.PartSteadyStateSynchronousResponse)

        @property
        def part_static_load_analysis_case(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_steady_state_synchronous_response(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
        ) -> "ClutchSteadyStateSynchronousResponse":
            return self._parent

        def __getattr__(
            self: "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse",
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
        self: Self, instance_to_wrap: "ClutchSteadyStateSynchronousResponse.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2580.Clutch":
        """mastapy.system_model.part_model.couplings.Clutch

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6837.ClutchLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "ClutchSteadyStateSynchronousResponse._Cast_ClutchSteadyStateSynchronousResponse":
        return self._Cast_ClutchSteadyStateSynchronousResponse(self)
