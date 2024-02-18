"""AGMAGleasonConicalGearMeshSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2726
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "AGMAGleasonConicalGearMeshSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.gears import _2301
    from mastapy.system_model.analyses_and_results.power_flows import _4038


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshSystemDeflection",)


Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshSystemDeflection")


class AGMAGleasonConicalGearMeshSystemDeflection(_2726.ConicalGearMeshSystemDeflection):
    """AGMAGleasonConicalGearMeshSystemDeflection

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_AGMAGleasonConicalGearMeshSystemDeflection"
    )

    class _Cast_AGMAGleasonConicalGearMeshSystemDeflection:
        """Special nested class for casting AGMAGleasonConicalGearMeshSystemDeflection to subclasses."""

        def __init__(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
            parent: "AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            self._parent = parent

        @property
        def conical_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            return self._parent._cast(_2726.ConicalGearMeshSystemDeflection)

        @property
        def gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2761,
            )

            return self._parent._cast(_2761.GearMeshSystemDeflection)

        @property
        def inter_mountable_component_connection_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2769,
            )

            return self._parent._cast(
                _2769.InterMountableComponentConnectionSystemDeflection
            )

        @property
        def connection_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2729,
            )

            return self._parent._cast(_2729.ConnectionSystemDeflection)

        @property
        def connection_fe_analysis(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.ConnectionFEAnalysis)

        @property
        def connection_static_load_analysis_case(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2703,
            )

            return self._parent._cast(_2703.BevelDifferentialGearMeshSystemDeflection)

        @property
        def bevel_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2708,
            )

            return self._parent._cast(_2708.BevelGearMeshSystemDeflection)

        @property
        def hypoid_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2765,
            )

            return self._parent._cast(_2765.HypoidGearMeshSystemDeflection)

        @property
        def spiral_bevel_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2809,
            )

            return self._parent._cast(_2809.SpiralBevelGearMeshSystemDeflection)

        @property
        def straight_bevel_diff_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2815,
            )

            return self._parent._cast(_2815.StraightBevelDiffGearMeshSystemDeflection)

        @property
        def straight_bevel_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2818,
            )

            return self._parent._cast(_2818.StraightBevelGearMeshSystemDeflection)

        @property
        def zerol_bevel_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2841,
            )

            return self._parent._cast(_2841.ZerolBevelGearMeshSystemDeflection)

        @property
        def agma_gleason_conical_gear_mesh_system_deflection(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
        ) -> "AGMAGleasonConicalGearMeshSystemDeflection":
            return self._parent

        def __getattr__(
            self: "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection",
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
        self: Self, instance_to_wrap: "AGMAGleasonConicalGearMeshSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2301.AGMAGleasonConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: Self) -> "_4038.AGMAGleasonConicalGearMeshPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearMeshPowerFlow

        Note:
            This property is readonly.
        """
        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "AGMAGleasonConicalGearMeshSystemDeflection._Cast_AGMAGleasonConicalGearMeshSystemDeflection":
        return self._Cast_AGMAGleasonConicalGearMeshSystemDeflection(self)
