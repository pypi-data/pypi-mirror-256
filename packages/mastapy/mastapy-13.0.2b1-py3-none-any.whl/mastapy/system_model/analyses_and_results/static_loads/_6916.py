"""KlingelnbergCycloPalloidConicalGearMeshLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6849
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearMeshLoadCase",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.gears import _2320


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshLoadCase",)


Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearMeshLoadCase")


class KlingelnbergCycloPalloidConicalGearMeshLoadCase(_6849.ConicalGearMeshLoadCase):
    """KlingelnbergCycloPalloidConicalGearMeshLoadCase

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase"
    )

    class _Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase:
        """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshLoadCase to subclasses."""

        def __init__(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
            parent: "KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            self._parent = parent

        @property
        def conical_gear_mesh_load_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            return self._parent._cast(_6849.ConicalGearMeshLoadCase)

        @property
        def gear_mesh_load_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6895

            return self._parent._cast(_6895.GearMeshLoadCase)

        @property
        def inter_mountable_component_connection_load_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6914

            return self._parent._cast(_6914.InterMountableComponentConnectionLoadCase)

        @property
        def connection_load_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6852

            return self._parent._cast(_6852.ConnectionLoadCase)

        @property
        def connection_analysis(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6919

            return self._parent._cast(
                _6919.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6922

            return self._parent._cast(
                _6922.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
        ) -> "KlingelnbergCycloPalloidConicalGearMeshLoadCase":
            return self._parent

        def __getattr__(
            self: "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
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
        instance_to_wrap: "KlingelnbergCycloPalloidConicalGearMeshLoadCase.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(
        self: Self,
    ) -> "_2320.KlingelnbergCycloPalloidConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase":
        return self._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase(self)
