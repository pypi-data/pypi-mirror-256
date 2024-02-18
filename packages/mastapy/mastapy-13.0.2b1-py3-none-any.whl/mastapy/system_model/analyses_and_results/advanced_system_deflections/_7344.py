"""KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7308
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
        "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
    )
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.gears import _2320


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",)


Self = TypeVar(
    "Self", bound="KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection"
)


class KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection(
    _7308.ConicalGearMeshAdvancedSystemDeflection
):
    """KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
    )

    class _Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection:
        """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
            parent: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def conical_gear_mesh_advanced_system_deflection(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            return self._parent._cast(_7308.ConicalGearMeshAdvancedSystemDeflection)

        @property
        def gear_mesh_advanced_system_deflection(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7336,
            )

            return self._parent._cast(_7336.GearMeshAdvancedSystemDeflection)

        @property
        def inter_mountable_component_connection_advanced_system_deflection(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7342,
            )

            return self._parent._cast(
                _7342.InterMountableComponentConnectionAdvancedSystemDeflection
            )

        @property
        def connection_advanced_system_deflection(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7310,
            )

            return self._parent._cast(_7310.ConnectionAdvancedSystemDeflection)

        @property
        def connection_static_load_analysis_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh_advanced_system_deflection(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7347,
            )

            return self._parent._cast(
                _7347.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_advanced_system_deflection(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7350,
            )

            return self._parent._cast(
                _7350.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh_advanced_system_deflection(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
        ) -> "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection",
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
        instance_to_wrap: "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection.TYPE",
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
    ) -> "KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection":
        return (
            self._Cast_KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection(
                self
            )
        )
