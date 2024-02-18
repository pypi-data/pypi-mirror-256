"""StraightBevelPlanetGearSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3096,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "StraightBevelPlanetGearSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2551


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelPlanetGearSteadyStateSynchronousResponse",)


Self = TypeVar("Self", bound="StraightBevelPlanetGearSteadyStateSynchronousResponse")


class StraightBevelPlanetGearSteadyStateSynchronousResponse(
    _3096.StraightBevelDiffGearSteadyStateSynchronousResponse
):
    """StraightBevelPlanetGearSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse"
    )

    class _Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse:
        """Special nested class for casting StraightBevelPlanetGearSteadyStateSynchronousResponse to subclasses."""

        def __init__(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
            parent: "StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            self._parent = parent

        @property
        def straight_bevel_diff_gear_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            return self._parent._cast(
                _3096.StraightBevelDiffGearSteadyStateSynchronousResponse
            )

        @property
        def bevel_gear_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3003,
            )

            return self._parent._cast(_3003.BevelGearSteadyStateSynchronousResponse)

        @property
        def agma_gleason_conical_gear_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _2991,
            )

            return self._parent._cast(
                _2991.AGMAGleasonConicalGearSteadyStateSynchronousResponse
            )

        @property
        def conical_gear_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3019,
            )

            return self._parent._cast(_3019.ConicalGearSteadyStateSynchronousResponse)

        @property
        def gear_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3046,
            )

            return self._parent._cast(_3046.GearSteadyStateSynchronousResponse)

        @property
        def mountable_component_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3063,
            )

            return self._parent._cast(
                _3063.MountableComponentSteadyStateSynchronousResponse
            )

        @property
        def component_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3010,
            )

            return self._parent._cast(_3010.ComponentSteadyStateSynchronousResponse)

        @property
        def part_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3065,
            )

            return self._parent._cast(_3065.PartSteadyStateSynchronousResponse)

        @property
        def part_static_load_analysis_case(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def straight_bevel_planet_gear_steady_state_synchronous_response(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
        ) -> "StraightBevelPlanetGearSteadyStateSynchronousResponse":
            return self._parent

        def __getattr__(
            self: "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse",
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
        instance_to_wrap: "StraightBevelPlanetGearSteadyStateSynchronousResponse.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2551.StraightBevelPlanetGear":
        """mastapy.system_model.part_model.gears.StraightBevelPlanetGear

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
    ) -> "StraightBevelPlanetGearSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse":
        return self._Cast_StraightBevelPlanetGearSteadyStateSynchronousResponse(self)
