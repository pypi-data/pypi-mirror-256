"""RootAssemblySteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3513,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "RootAssemblySteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2476
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3611,
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblySteadyStateSynchronousResponseAtASpeed",)


Self = TypeVar("Self", bound="RootAssemblySteadyStateSynchronousResponseAtASpeed")


class RootAssemblySteadyStateSynchronousResponseAtASpeed(
    _3513.AssemblySteadyStateSynchronousResponseAtASpeed
):
    """RootAssemblySteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed"
    )

    class _Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed:
        """Special nested class for casting RootAssemblySteadyStateSynchronousResponseAtASpeed to subclasses."""

        def __init__(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
            parent: "RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            self._parent = parent

        @property
        def assembly_steady_state_synchronous_response_at_a_speed(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            return self._parent._cast(
                _3513.AssemblySteadyStateSynchronousResponseAtASpeed
            )

        @property
        def abstract_assembly_steady_state_synchronous_response_at_a_speed(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3506,
            )

            return self._parent._cast(
                _3506.AbstractAssemblySteadyStateSynchronousResponseAtASpeed
            )

        @property
        def part_steady_state_synchronous_response_at_a_speed(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3585,
            )

            return self._parent._cast(_3585.PartSteadyStateSynchronousResponseAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def root_assembly_steady_state_synchronous_response_at_a_speed(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "RootAssemblySteadyStateSynchronousResponseAtASpeed":
            return self._parent

        def __getattr__(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
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
        instance_to_wrap: "RootAssemblySteadyStateSynchronousResponseAtASpeed.TYPE",
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
    def steady_state_synchronous_response_at_a_speed_inputs(
        self: Self,
    ) -> "_3611.SteadyStateSynchronousResponseAtASpeed":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.SteadyStateSynchronousResponseAtASpeed

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SteadyStateSynchronousResponseAtASpeedInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed":
        return self._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed(self)
