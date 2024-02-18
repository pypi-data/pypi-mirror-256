"""CylindricalPlanetGearAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7323
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "CylindricalPlanetGearAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2529


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearAdvancedSystemDeflection",)


Self = TypeVar("Self", bound="CylindricalPlanetGearAdvancedSystemDeflection")


class CylindricalPlanetGearAdvancedSystemDeflection(
    _7323.CylindricalGearAdvancedSystemDeflection
):
    """CylindricalPlanetGearAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_PLANET_GEAR_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CylindricalPlanetGearAdvancedSystemDeflection"
    )

    class _Cast_CylindricalPlanetGearAdvancedSystemDeflection:
        """Special nested class for casting CylindricalPlanetGearAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
            parent: "CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def cylindrical_gear_advanced_system_deflection(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            return self._parent._cast(_7323.CylindricalGearAdvancedSystemDeflection)

        @property
        def gear_advanced_system_deflection(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7335,
            )

            return self._parent._cast(_7335.GearAdvancedSystemDeflection)

        @property
        def mountable_component_advanced_system_deflection(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7355,
            )

            return self._parent._cast(_7355.MountableComponentAdvancedSystemDeflection)

        @property
        def component_advanced_system_deflection(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7300,
            )

            return self._parent._cast(_7300.ComponentAdvancedSystemDeflection)

        @property
        def part_advanced_system_deflection(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7357,
            )

            return self._parent._cast(_7357.PartAdvancedSystemDeflection)

        @property
        def part_static_load_analysis_case(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cylindrical_planet_gear_advanced_system_deflection(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
        ) -> "CylindricalPlanetGearAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection",
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
        instance_to_wrap: "CylindricalPlanetGearAdvancedSystemDeflection.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2529.CylindricalPlanetGear":
        """mastapy.system_model.part_model.gears.CylindricalPlanetGear

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
    ) -> "CylindricalPlanetGearAdvancedSystemDeflection._Cast_CylindricalPlanetGearAdvancedSystemDeflection":
        return self._Cast_CylindricalPlanetGearAdvancedSystemDeflection(self)
