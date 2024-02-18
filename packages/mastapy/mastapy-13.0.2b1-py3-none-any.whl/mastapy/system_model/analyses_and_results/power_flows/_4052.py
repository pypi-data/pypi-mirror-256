"""BevelGearSetPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4040
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "BevelGearSetPowerFlow"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2522


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetPowerFlow",)


Self = TypeVar("Self", bound="BevelGearSetPowerFlow")


class BevelGearSetPowerFlow(_4040.AGMAGleasonConicalGearSetPowerFlow):
    """BevelGearSetPowerFlow

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_SET_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BevelGearSetPowerFlow")

    class _Cast_BevelGearSetPowerFlow:
        """Special nested class for casting BevelGearSetPowerFlow to subclasses."""

        def __init__(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
            parent: "BevelGearSetPowerFlow",
        ):
            self._parent = parent

        @property
        def agma_gleason_conical_gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            return self._parent._cast(_4040.AGMAGleasonConicalGearSetPowerFlow)

        @property
        def conical_gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4068

            return self._parent._cast(_4068.ConicalGearSetPowerFlow)

        @property
        def gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4097

            return self._parent._cast(_4097.GearSetPowerFlow)

        @property
        def specialised_assembly_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4137

            return self._parent._cast(_4137.SpecialisedAssemblyPowerFlow)

        @property
        def abstract_assembly_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4034

            return self._parent._cast(_4034.AbstractAssemblyPowerFlow)

        @property
        def part_power_flow(self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4116

            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4047

            return self._parent._cast(_4047.BevelDifferentialGearSetPowerFlow)

        @property
        def spiral_bevel_gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4140

            return self._parent._cast(_4140.SpiralBevelGearSetPowerFlow)

        @property
        def straight_bevel_diff_gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4146

            return self._parent._cast(_4146.StraightBevelDiffGearSetPowerFlow)

        @property
        def straight_bevel_gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4149

            return self._parent._cast(_4149.StraightBevelGearSetPowerFlow)

        @property
        def zerol_bevel_gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4168

            return self._parent._cast(_4168.ZerolBevelGearSetPowerFlow)

        @property
        def bevel_gear_set_power_flow(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow",
        ) -> "BevelGearSetPowerFlow":
            return self._parent

        def __getattr__(
            self: "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BevelGearSetPowerFlow.TYPE"):
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
    def cast_to(self: Self) -> "BevelGearSetPowerFlow._Cast_BevelGearSetPowerFlow":
        return self._Cast_BevelGearSetPowerFlow(self)
