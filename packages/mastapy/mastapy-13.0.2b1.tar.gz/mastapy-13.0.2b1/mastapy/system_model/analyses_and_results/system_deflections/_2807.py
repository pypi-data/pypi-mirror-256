"""ShaftToMountableComponentConnectionSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2690
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ShaftToMountableComponentConnectionSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2297
    from mastapy.system_model.analyses_and_results.power_flows import _4136


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionSystemDeflection",)


Self = TypeVar("Self", bound="ShaftToMountableComponentConnectionSystemDeflection")


class ShaftToMountableComponentConnectionSystemDeflection(
    _2690.AbstractShaftToMountableComponentConnectionSystemDeflection
):
    """ShaftToMountableComponentConnectionSystemDeflection

    This is a mastapy class.
    """

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_ShaftToMountableComponentConnectionSystemDeflection"
    )

    class _Cast_ShaftToMountableComponentConnectionSystemDeflection:
        """Special nested class for casting ShaftToMountableComponentConnectionSystemDeflection to subclasses."""

        def __init__(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
            parent: "ShaftToMountableComponentConnectionSystemDeflection",
        ):
            self._parent = parent

        @property
        def abstract_shaft_to_mountable_component_connection_system_deflection(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            return self._parent._cast(
                _2690.AbstractShaftToMountableComponentConnectionSystemDeflection
            )

        @property
        def connection_system_deflection(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2729,
            )

            return self._parent._cast(_2729.ConnectionSystemDeflection)

        @property
        def connection_fe_analysis(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.ConnectionFEAnalysis)

        @property
        def connection_static_load_analysis_case(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def coaxial_connection_system_deflection(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2716,
            )

            return self._parent._cast(_2716.CoaxialConnectionSystemDeflection)

        @property
        def cycloidal_disc_central_bearing_connection_system_deflection(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2738,
            )

            return self._parent._cast(
                _2738.CycloidalDiscCentralBearingConnectionSystemDeflection
            )

        @property
        def planetary_connection_system_deflection(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2791,
            )

            return self._parent._cast(_2791.PlanetaryConnectionSystemDeflection)

        @property
        def shaft_to_mountable_component_connection_system_deflection(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
        ) -> "ShaftToMountableComponentConnectionSystemDeflection":
            return self._parent

        def __getattr__(
            self: "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection",
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
        instance_to_wrap: "ShaftToMountableComponentConnectionSystemDeflection.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2297.ShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(
        self: Self,
    ) -> "_4136.ShaftToMountableComponentConnectionPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ShaftToMountableComponentConnectionPowerFlow

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
    ) -> "ShaftToMountableComponentConnectionSystemDeflection._Cast_ShaftToMountableComponentConnectionSystemDeflection":
        return self._Cast_ShaftToMountableComponentConnectionSystemDeflection(self)
