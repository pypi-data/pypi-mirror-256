"""ShaftToMountableComponentConnectionAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7275
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "ShaftToMountableComponentConnectionAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2297


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionAdvancedSystemDeflection",)


Self = TypeVar(
    "Self", bound="ShaftToMountableComponentConnectionAdvancedSystemDeflection"
)


class ShaftToMountableComponentConnectionAdvancedSystemDeflection(
    _7275.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection
):
    """ShaftToMountableComponentConnectionAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
    )

    class _Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection:
        """Special nested class for casting ShaftToMountableComponentConnectionAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
            parent: "ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def abstract_shaft_to_mountable_component_connection_advanced_system_deflection(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            return self._parent._cast(
                _7275.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection
            )

        @property
        def connection_advanced_system_deflection(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7310,
            )

            return self._parent._cast(_7310.ConnectionAdvancedSystemDeflection)

        @property
        def connection_static_load_analysis_case(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def coaxial_connection_advanced_system_deflection(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7299,
            )

            return self._parent._cast(_7299.CoaxialConnectionAdvancedSystemDeflection)

        @property
        def cycloidal_disc_central_bearing_connection_advanced_system_deflection(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7321,
            )

            return self._parent._cast(
                _7321.CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection
            )

        @property
        def planetary_connection_advanced_system_deflection(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7361,
            )

            return self._parent._cast(_7361.PlanetaryConnectionAdvancedSystemDeflection)

        @property
        def shaft_to_mountable_component_connection_advanced_system_deflection(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
        ) -> "ShaftToMountableComponentConnectionAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection",
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
        instance_to_wrap: "ShaftToMountableComponentConnectionAdvancedSystemDeflection.TYPE",
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
    def cast_to(
        self: Self,
    ) -> "ShaftToMountableComponentConnectionAdvancedSystemDeflection._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection":
        return self._Cast_ShaftToMountableComponentConnectionAdvancedSystemDeflection(
            self
        )
