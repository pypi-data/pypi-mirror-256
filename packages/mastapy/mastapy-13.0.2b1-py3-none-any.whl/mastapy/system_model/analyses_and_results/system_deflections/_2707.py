"""BevelDifferentialSunGearSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2705
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "BevelDifferentialSunGearSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2520
    from mastapy.system_model.analyses_and_results.power_flows import _4049


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialSunGearSystemDeflection",)


Self = TypeVar("Self", bound="BevelDifferentialSunGearSystemDeflection")


class BevelDifferentialSunGearSystemDeflection(
    _2705.BevelDifferentialGearSystemDeflection
):
    """BevelDifferentialSunGearSystemDeflection

    This is a mastapy class.
    """

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_BevelDifferentialSunGearSystemDeflection"
    )

    class _Cast_BevelDifferentialSunGearSystemDeflection:
        """Special nested class for casting BevelDifferentialSunGearSystemDeflection to subclasses."""

        def __init__(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
            parent: "BevelDifferentialSunGearSystemDeflection",
        ):
            self._parent = parent

        @property
        def bevel_differential_gear_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            return self._parent._cast(_2705.BevelDifferentialGearSystemDeflection)

        @property
        def bevel_gear_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2710,
            )

            return self._parent._cast(_2710.BevelGearSystemDeflection)

        @property
        def agma_gleason_conical_gear_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2693,
            )

            return self._parent._cast(_2693.AGMAGleasonConicalGearSystemDeflection)

        @property
        def conical_gear_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2728,
            )

            return self._parent._cast(_2728.ConicalGearSystemDeflection)

        @property
        def gear_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2763,
            )

            return self._parent._cast(_2763.GearSystemDeflection)

        @property
        def mountable_component_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2784,
            )

            return self._parent._cast(_2784.MountableComponentSystemDeflection)

        @property
        def component_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2717,
            )

            return self._parent._cast(_2717.ComponentSystemDeflection)

        @property
        def part_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bevel_differential_sun_gear_system_deflection(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
        ) -> "BevelDifferentialSunGearSystemDeflection":
            return self._parent

        def __getattr__(
            self: "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection",
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
        self: Self, instance_to_wrap: "BevelDifferentialSunGearSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2520.BevelDifferentialSunGear":
        """mastapy.system_model.part_model.gears.BevelDifferentialSunGear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: Self) -> "_4049.BevelDifferentialSunGearPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialSunGearPowerFlow

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
    ) -> "BevelDifferentialSunGearSystemDeflection._Cast_BevelDifferentialSunGearSystemDeflection":
        return self._Cast_BevelDifferentialSunGearSystemDeflection(self)
