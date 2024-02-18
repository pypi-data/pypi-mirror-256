"""PlanetaryConnectionCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2952
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "PlanetaryConnectionCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2289
    from mastapy.system_model.analyses_and_results.system_deflections import _2791


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryConnectionCompoundSystemDeflection",)


Self = TypeVar("Self", bound="PlanetaryConnectionCompoundSystemDeflection")


class PlanetaryConnectionCompoundSystemDeflection(
    _2952.ShaftToMountableComponentConnectionCompoundSystemDeflection
):
    """PlanetaryConnectionCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _PLANETARY_CONNECTION_COMPOUND_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_PlanetaryConnectionCompoundSystemDeflection"
    )

    class _Cast_PlanetaryConnectionCompoundSystemDeflection:
        """Special nested class for casting PlanetaryConnectionCompoundSystemDeflection to subclasses."""

        def __init__(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
            parent: "PlanetaryConnectionCompoundSystemDeflection",
        ):
            self._parent = parent

        @property
        def shaft_to_mountable_component_connection_compound_system_deflection(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
        ):
            return self._parent._cast(
                _2952.ShaftToMountableComponentConnectionCompoundSystemDeflection
            )

        @property
        def abstract_shaft_to_mountable_component_connection_compound_system_deflection(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2856,
            )

            return self._parent._cast(
                _2856.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection
            )

        @property
        def connection_compound_system_deflection(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2888,
            )

            return self._parent._cast(_2888.ConnectionCompoundSystemDeflection)

        @property
        def connection_compound_analysis(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7541

            return self._parent._cast(_7541.ConnectionCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def planetary_connection_compound_system_deflection(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
        ) -> "PlanetaryConnectionCompoundSystemDeflection":
            return self._parent

        def __getattr__(
            self: "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection",
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
        self: Self, instance_to_wrap: "PlanetaryConnectionCompoundSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2289.PlanetaryConnection":
        """mastapy.system_model.connections_and_sockets.PlanetaryConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: Self) -> "_2289.PlanetaryConnection":
        """mastapy.system_model.connections_and_sockets.PlanetaryConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: Self,
    ) -> "List[_2791.PlanetaryConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.PlanetaryConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases(
        self: Self,
    ) -> "List[_2791.PlanetaryConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.PlanetaryConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "PlanetaryConnectionCompoundSystemDeflection._Cast_PlanetaryConnectionCompoundSystemDeflection":
        return self._Cast_PlanetaryConnectionCompoundSystemDeflection(self)
