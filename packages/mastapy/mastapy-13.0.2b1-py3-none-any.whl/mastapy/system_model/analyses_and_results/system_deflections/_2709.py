"""BevelGearSetSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2692
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "BevelGearSetSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2522
    from mastapy.system_model.analyses_and_results.power_flows import _4052


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetSystemDeflection",)


Self = TypeVar("Self", bound="BevelGearSetSystemDeflection")


class BevelGearSetSystemDeflection(_2692.AGMAGleasonConicalGearSetSystemDeflection):
    """BevelGearSetSystemDeflection

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_SET_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BevelGearSetSystemDeflection")

    class _Cast_BevelGearSetSystemDeflection:
        """Special nested class for casting BevelGearSetSystemDeflection to subclasses."""

        def __init__(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
            parent: "BevelGearSetSystemDeflection",
        ):
            self._parent = parent

        @property
        def agma_gleason_conical_gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            return self._parent._cast(_2692.AGMAGleasonConicalGearSetSystemDeflection)

        @property
        def conical_gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2727,
            )

            return self._parent._cast(_2727.ConicalGearSetSystemDeflection)

        @property
        def gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2762,
            )

            return self._parent._cast(_2762.GearSetSystemDeflection)

        @property
        def specialised_assembly_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2808,
            )

            return self._parent._cast(_2808.SpecialisedAssemblySystemDeflection)

        @property
        def abstract_assembly_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2687,
            )

            return self._parent._cast(_2687.AbstractAssemblySystemDeflection)

        @property
        def part_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2704,
            )

            return self._parent._cast(_2704.BevelDifferentialGearSetSystemDeflection)

        @property
        def spiral_bevel_gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2810,
            )

            return self._parent._cast(_2810.SpiralBevelGearSetSystemDeflection)

        @property
        def straight_bevel_diff_gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2816,
            )

            return self._parent._cast(_2816.StraightBevelDiffGearSetSystemDeflection)

        @property
        def straight_bevel_gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2819,
            )

            return self._parent._cast(_2819.StraightBevelGearSetSystemDeflection)

        @property
        def zerol_bevel_gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2842,
            )

            return self._parent._cast(_2842.ZerolBevelGearSetSystemDeflection)

        @property
        def bevel_gear_set_system_deflection(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
        ) -> "BevelGearSetSystemDeflection":
            return self._parent

        def __getattr__(
            self: "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BevelGearSetSystemDeflection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2522.BevelGearSet":
        """mastapy.system_model.part_model.gears.BevelGearSet

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: Self) -> "_4052.BevelGearSetPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow

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
    ) -> "BevelGearSetSystemDeflection._Cast_BevelGearSetSystemDeflection":
        return self._Cast_BevelGearSetSystemDeflection(self)
