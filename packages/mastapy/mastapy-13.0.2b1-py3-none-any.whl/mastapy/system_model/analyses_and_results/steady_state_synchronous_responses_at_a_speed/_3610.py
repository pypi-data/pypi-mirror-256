"""SpringDamperSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3545,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "SpringDamperSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2602
    from mastapy.system_model.analyses_and_results.static_loads import _6961


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperSteadyStateSynchronousResponseAtASpeed",)


Self = TypeVar("Self", bound="SpringDamperSteadyStateSynchronousResponseAtASpeed")


class SpringDamperSteadyStateSynchronousResponseAtASpeed(
    _3545.CouplingSteadyStateSynchronousResponseAtASpeed
):
    """SpringDamperSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed"
    )

    class _Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed:
        """Special nested class for casting SpringDamperSteadyStateSynchronousResponseAtASpeed to subclasses."""

        def __init__(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
            parent: "SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            self._parent = parent

        @property
        def coupling_steady_state_synchronous_response_at_a_speed(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            return self._parent._cast(
                _3545.CouplingSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def specialised_assembly_steady_state_synchronous_response_at_a_speed(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3604,
            )

            return self._parent._cast(
                _3604.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed
            )

        @property
        def abstract_assembly_steady_state_synchronous_response_at_a_speed(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3506,
            )

            return self._parent._cast(
                _3506.AbstractAssemblySteadyStateSynchronousResponseAtASpeed
            )

        @property
        def part_steady_state_synchronous_response_at_a_speed(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3585,
            )

            return self._parent._cast(_3585.PartSteadyStateSynchronousResponseAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def spring_damper_steady_state_synchronous_response_at_a_speed(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
        ) -> "SpringDamperSteadyStateSynchronousResponseAtASpeed":
            return self._parent

        def __getattr__(
            self: "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed",
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
        instance_to_wrap: "SpringDamperSteadyStateSynchronousResponseAtASpeed.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2602.SpringDamper":
        """mastapy.system_model.part_model.couplings.SpringDamper

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6961.SpringDamperLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase

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
    ) -> "SpringDamperSteadyStateSynchronousResponseAtASpeed._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed":
        return self._Cast_SpringDamperSteadyStateSynchronousResponseAtASpeed(self)
