"""BevelDifferentialSunGearCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2864
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "BevelDifferentialSunGearCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.system_deflections import _2707


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialSunGearCompoundSystemDeflection",)


Self = TypeVar("Self", bound="BevelDifferentialSunGearCompoundSystemDeflection")


class BevelDifferentialSunGearCompoundSystemDeflection(
    _2864.BevelDifferentialGearCompoundSystemDeflection
):
    """BevelDifferentialSunGearCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_BevelDifferentialSunGearCompoundSystemDeflection"
    )

    class _Cast_BevelDifferentialSunGearCompoundSystemDeflection:
        """Special nested class for casting BevelDifferentialSunGearCompoundSystemDeflection to subclasses."""

        def __init__(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
            parent: "BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            self._parent = parent

        @property
        def bevel_differential_gear_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            return self._parent._cast(
                _2864.BevelDifferentialGearCompoundSystemDeflection
            )

        @property
        def bevel_gear_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2869,
            )

            return self._parent._cast(_2869.BevelGearCompoundSystemDeflection)

        @property
        def agma_gleason_conical_gear_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2857,
            )

            return self._parent._cast(
                _2857.AGMAGleasonConicalGearCompoundSystemDeflection
            )

        @property
        def conical_gear_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2885,
            )

            return self._parent._cast(_2885.ConicalGearCompoundSystemDeflection)

        @property
        def gear_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2912,
            )

            return self._parent._cast(_2912.GearCompoundSystemDeflection)

        @property
        def mountable_component_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2931,
            )

            return self._parent._cast(_2931.MountableComponentCompoundSystemDeflection)

        @property
        def component_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2878,
            )

            return self._parent._cast(_2878.ComponentCompoundSystemDeflection)

        @property
        def part_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2933,
            )

            return self._parent._cast(_2933.PartCompoundSystemDeflection)

        @property
        def part_compound_analysis(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bevel_differential_sun_gear_compound_system_deflection(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
        ) -> "BevelDifferentialSunGearCompoundSystemDeflection":
            return self._parent

        def __getattr__(
            self: "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection",
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
        instance_to_wrap: "BevelDifferentialSunGearCompoundSystemDeflection.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_2707.BevelDifferentialSunGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialSunGearSystemDeflection]

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
    ) -> "List[_2707.BevelDifferentialSunGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialSunGearSystemDeflection]

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
    ) -> "BevelDifferentialSunGearCompoundSystemDeflection._Cast_BevelDifferentialSunGearCompoundSystemDeflection":
        return self._Cast_BevelDifferentialSunGearCompoundSystemDeflection(self)
