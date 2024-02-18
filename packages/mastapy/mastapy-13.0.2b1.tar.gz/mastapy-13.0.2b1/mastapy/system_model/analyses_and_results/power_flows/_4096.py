"""GearPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4114
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_GEAR_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "GearPowerFlow"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2532


__docformat__ = "restructuredtext en"
__all__ = ("GearPowerFlow",)


Self = TypeVar("Self", bound="GearPowerFlow")


class GearPowerFlow(_4114.MountableComponentPowerFlow):
    """GearPowerFlow

    This is a mastapy class.
    """

    TYPE = _GEAR_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_GearPowerFlow")

    class _Cast_GearPowerFlow:
        """Special nested class for casting GearPowerFlow to subclasses."""

        def __init__(
            self: "GearPowerFlow._Cast_GearPowerFlow", parent: "GearPowerFlow"
        ):
            self._parent = parent

        @property
        def mountable_component_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            return self._parent._cast(_4114.MountableComponentPowerFlow)

        @property
        def component_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4059

            return self._parent._cast(_4059.ComponentPowerFlow)

        @property
        def part_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4116

            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4039

            return self._parent._cast(_4039.AGMAGleasonConicalGearPowerFlow)

        @property
        def bevel_differential_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4046

            return self._parent._cast(_4046.BevelDifferentialGearPowerFlow)

        @property
        def bevel_differential_planet_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4048

            return self._parent._cast(_4048.BevelDifferentialPlanetGearPowerFlow)

        @property
        def bevel_differential_sun_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4049

            return self._parent._cast(_4049.BevelDifferentialSunGearPowerFlow)

        @property
        def bevel_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4051

            return self._parent._cast(_4051.BevelGearPowerFlow)

        @property
        def concept_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4064

            return self._parent._cast(_4064.ConceptGearPowerFlow)

        @property
        def conical_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4067

            return self._parent._cast(_4067.ConicalGearPowerFlow)

        @property
        def cylindrical_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4083

            return self._parent._cast(_4083.CylindricalGearPowerFlow)

        @property
        def cylindrical_planet_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4085

            return self._parent._cast(_4085.CylindricalPlanetGearPowerFlow)

        @property
        def face_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4089

            return self._parent._cast(_4089.FaceGearPowerFlow)

        @property
        def hypoid_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4100

            return self._parent._cast(_4100.HypoidGearPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4104

            return self._parent._cast(
                _4104.KlingelnbergCycloPalloidConicalGearPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4107

            return self._parent._cast(_4107.KlingelnbergCycloPalloidHypoidGearPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4110

            return self._parent._cast(
                _4110.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
            )

        @property
        def spiral_bevel_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4139

            return self._parent._cast(_4139.SpiralBevelGearPowerFlow)

        @property
        def straight_bevel_diff_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4145

            return self._parent._cast(_4145.StraightBevelDiffGearPowerFlow)

        @property
        def straight_bevel_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4148

            return self._parent._cast(_4148.StraightBevelGearPowerFlow)

        @property
        def straight_bevel_planet_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4150

            return self._parent._cast(_4150.StraightBevelPlanetGearPowerFlow)

        @property
        def straight_bevel_sun_gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4151

            return self._parent._cast(_4151.StraightBevelSunGearPowerFlow)

        @property
        def worm_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4164

            return self._parent._cast(_4164.WormGearPowerFlow)

        @property
        def zerol_bevel_gear_power_flow(self: "GearPowerFlow._Cast_GearPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4167

            return self._parent._cast(_4167.ZerolBevelGearPowerFlow)

        @property
        def gear_power_flow(
            self: "GearPowerFlow._Cast_GearPowerFlow",
        ) -> "GearPowerFlow":
            return self._parent

        def __getattr__(self: "GearPowerFlow._Cast_GearPowerFlow", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "GearPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_loaded(self: Self) -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = self.wrapped.IsLoaded

        if temp is None:
            return False

        return temp

    @property
    def component_design(self: Self) -> "_2532.Gear":
        """mastapy.system_model.part_model.gears.Gear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "GearPowerFlow._Cast_GearPowerFlow":
        return self._Cast_GearPowerFlow(self)
