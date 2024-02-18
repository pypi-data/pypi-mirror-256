"""CylindricalPlanetGearCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7455,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "CylindricalPlanetGearCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
        _7327,
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearCompoundAdvancedSystemDeflection",)


Self = TypeVar("Self", bound="CylindricalPlanetGearCompoundAdvancedSystemDeflection")


class CylindricalPlanetGearCompoundAdvancedSystemDeflection(
    _7455.CylindricalGearCompoundAdvancedSystemDeflection
):
    """CylindricalPlanetGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_PLANET_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection"
    )

    class _Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection:
        """Special nested class for casting CylindricalPlanetGearCompoundAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
            parent: "CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def cylindrical_gear_compound_advanced_system_deflection(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            return self._parent._cast(
                _7455.CylindricalGearCompoundAdvancedSystemDeflection
            )

        @property
        def gear_compound_advanced_system_deflection(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7466,
            )

            return self._parent._cast(_7466.GearCompoundAdvancedSystemDeflection)

        @property
        def mountable_component_compound_advanced_system_deflection(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7485,
            )

            return self._parent._cast(
                _7485.MountableComponentCompoundAdvancedSystemDeflection
            )

        @property
        def component_compound_advanced_system_deflection(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7433,
            )

            return self._parent._cast(_7433.ComponentCompoundAdvancedSystemDeflection)

        @property
        def part_compound_advanced_system_deflection(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
                _7487,
            )

            return self._parent._cast(_7487.PartCompoundAdvancedSystemDeflection)

        @property
        def part_compound_analysis(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cylindrical_planet_gear_compound_advanced_system_deflection(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
        ) -> "CylindricalPlanetGearCompoundAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection",
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
        instance_to_wrap: "CylindricalPlanetGearCompoundAdvancedSystemDeflection.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_7327.CylindricalPlanetGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_7327.CylindricalPlanetGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "CylindricalPlanetGearCompoundAdvancedSystemDeflection._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection":
        return self._Cast_CylindricalPlanetGearCompoundAdvancedSystemDeflection(self)
