"""SpiralBevelGearLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6830
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpiralBevelGearLoadCase"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2545


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearLoadCase",)


Self = TypeVar("Self", bound="SpiralBevelGearLoadCase")


class SpiralBevelGearLoadCase(_6830.BevelGearLoadCase):
    """SpiralBevelGearLoadCase

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_LOAD_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_SpiralBevelGearLoadCase")

    class _Cast_SpiralBevelGearLoadCase:
        """Special nested class for casting SpiralBevelGearLoadCase to subclasses."""

        def __init__(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
            parent: "SpiralBevelGearLoadCase",
        ):
            self._parent = parent

        @property
        def bevel_gear_load_case(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            return self._parent._cast(_6830.BevelGearLoadCase)

        @property
        def agma_gleason_conical_gear_load_case(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6816

            return self._parent._cast(_6816.AGMAGleasonConicalGearLoadCase)

        @property
        def conical_gear_load_case(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6847

            return self._parent._cast(_6847.ConicalGearLoadCase)

        @property
        def gear_load_case(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6893

            return self._parent._cast(_6893.GearLoadCase)

        @property
        def mountable_component_load_case(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6927

            return self._parent._cast(_6927.MountableComponentLoadCase)

        @property
        def component_load_case(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6840

            return self._parent._cast(_6840.ComponentLoadCase)

        @property
        def part_load_case(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6931

            return self._parent._cast(_6931.PartLoadCase)

        @property
        def part_analysis(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def spiral_bevel_gear_load_case(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase",
        ) -> "SpiralBevelGearLoadCase":
            return self._parent

        def __getattr__(
            self: "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "SpiralBevelGearLoadCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2545.SpiralBevelGear":
        """mastapy.system_model.part_model.gears.SpiralBevelGear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase":
        return self._Cast_SpiralBevelGearLoadCase(self)
