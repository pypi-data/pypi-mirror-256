"""RootAssemblySteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _2992,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "RootAssemblySteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2476
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3091,
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblySteadyStateSynchronousResponse",)


Self = TypeVar("Self", bound="RootAssemblySteadyStateSynchronousResponse")


class RootAssemblySteadyStateSynchronousResponse(
    _2992.AssemblySteadyStateSynchronousResponse
):
    """RootAssemblySteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_RootAssemblySteadyStateSynchronousResponse"
    )

    class _Cast_RootAssemblySteadyStateSynchronousResponse:
        """Special nested class for casting RootAssemblySteadyStateSynchronousResponse to subclasses."""

        def __init__(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
            parent: "RootAssemblySteadyStateSynchronousResponse",
        ):
            self._parent = parent

        @property
        def assembly_steady_state_synchronous_response(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ):
            return self._parent._cast(_2992.AssemblySteadyStateSynchronousResponse)

        @property
        def abstract_assembly_steady_state_synchronous_response(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _2985,
            )

            return self._parent._cast(
                _2985.AbstractAssemblySteadyStateSynchronousResponse
            )

        @property
        def part_steady_state_synchronous_response(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3065,
            )

            return self._parent._cast(_3065.PartSteadyStateSynchronousResponse)

        @property
        def part_static_load_analysis_case(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def root_assembly_steady_state_synchronous_response(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
        ) -> "RootAssemblySteadyStateSynchronousResponse":
            return self._parent

        def __getattr__(
            self: "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse",
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
        self: Self, instance_to_wrap: "RootAssemblySteadyStateSynchronousResponse.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2476.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def steady_state_synchronous_response_inputs(
        self: Self,
    ) -> "_3091.SteadyStateSynchronousResponse":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.SteadyStateSynchronousResponse

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SteadyStateSynchronousResponseInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "RootAssemblySteadyStateSynchronousResponse._Cast_RootAssemblySteadyStateSynchronousResponse":
        return self._Cast_RootAssemblySteadyStateSynchronousResponse(self)
