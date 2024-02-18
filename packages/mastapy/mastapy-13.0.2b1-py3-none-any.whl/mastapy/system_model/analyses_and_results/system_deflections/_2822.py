"""StraightBevelSunGearSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2817
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "StraightBevelSunGearSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2552
    from mastapy.system_model.analyses_and_results.power_flows import _4151


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearSystemDeflection",)


Self = TypeVar("Self", bound="StraightBevelSunGearSystemDeflection")


class StraightBevelSunGearSystemDeflection(_2817.StraightBevelDiffGearSystemDeflection):
    """StraightBevelSunGearSystemDeflection

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_StraightBevelSunGearSystemDeflection")

    class _Cast_StraightBevelSunGearSystemDeflection:
        """Special nested class for casting StraightBevelSunGearSystemDeflection to subclasses."""

        def __init__(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
            parent: "StraightBevelSunGearSystemDeflection",
        ):
            self._parent = parent

        @property
        def straight_bevel_diff_gear_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            return self._parent._cast(_2817.StraightBevelDiffGearSystemDeflection)

        @property
        def bevel_gear_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2710,
            )

            return self._parent._cast(_2710.BevelGearSystemDeflection)

        @property
        def agma_gleason_conical_gear_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2693,
            )

            return self._parent._cast(_2693.AGMAGleasonConicalGearSystemDeflection)

        @property
        def conical_gear_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2728,
            )

            return self._parent._cast(_2728.ConicalGearSystemDeflection)

        @property
        def gear_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2763,
            )

            return self._parent._cast(_2763.GearSystemDeflection)

        @property
        def mountable_component_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2784,
            )

            return self._parent._cast(_2784.MountableComponentSystemDeflection)

        @property
        def component_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2717,
            )

            return self._parent._cast(_2717.ComponentSystemDeflection)

        @property
        def part_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def straight_bevel_sun_gear_system_deflection(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
        ) -> "StraightBevelSunGearSystemDeflection":
            return self._parent

        def __getattr__(
            self: "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection",
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
        self: Self, instance_to_wrap: "StraightBevelSunGearSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2552.StraightBevelSunGear":
        """mastapy.system_model.part_model.gears.StraightBevelSunGear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: Self) -> "_4151.StraightBevelSunGearPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow

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
    ) -> "StraightBevelSunGearSystemDeflection._Cast_StraightBevelSunGearSystemDeflection":
        return self._Cast_StraightBevelSunGearSystemDeflection(self)
