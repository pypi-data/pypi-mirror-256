"""WormGearMeshSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3044,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "WormGearMeshSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.gears import _2331
    from mastapy.system_model.analyses_and_results.static_loads import _6986


__docformat__ = "restructuredtext en"
__all__ = ("WormGearMeshSteadyStateSynchronousResponse",)


Self = TypeVar("Self", bound="WormGearMeshSteadyStateSynchronousResponse")


class WormGearMeshSteadyStateSynchronousResponse(
    _3044.GearMeshSteadyStateSynchronousResponse
):
    """WormGearMeshSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_WormGearMeshSteadyStateSynchronousResponse"
    )

    class _Cast_WormGearMeshSteadyStateSynchronousResponse:
        """Special nested class for casting WormGearMeshSteadyStateSynchronousResponse to subclasses."""

        def __init__(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
            parent: "WormGearMeshSteadyStateSynchronousResponse",
        ):
            self._parent = parent

        @property
        def gear_mesh_steady_state_synchronous_response(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ):
            return self._parent._cast(_3044.GearMeshSteadyStateSynchronousResponse)

        @property
        def inter_mountable_component_connection_steady_state_synchronous_response(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3051,
            )

            return self._parent._cast(
                _3051.InterMountableComponentConnectionSteadyStateSynchronousResponse
            )

        @property
        def connection_steady_state_synchronous_response(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3020,
            )

            return self._parent._cast(_3020.ConnectionSteadyStateSynchronousResponse)

        @property
        def connection_static_load_analysis_case(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def worm_gear_mesh_steady_state_synchronous_response(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
        ) -> "WormGearMeshSteadyStateSynchronousResponse":
            return self._parent

        def __getattr__(
            self: "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse",
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
        self: Self, instance_to_wrap: "WormGearMeshSteadyStateSynchronousResponse.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2331.WormGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.WormGearMesh

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: Self) -> "_6986.WormGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "WormGearMeshSteadyStateSynchronousResponse._Cast_WormGearMeshSteadyStateSynchronousResponse":
        return self._Cast_WormGearMeshSteadyStateSynchronousResponse(self)
