"""ZerolBevelGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2521
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
)

if TYPE_CHECKING:
    from mastapy.gears.gear_designs.zerol_bevel import _952


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGear",)


Self = TypeVar("Self", bound="ZerolBevelGear")


class ZerolBevelGear(_2521.BevelGear):
    """ZerolBevelGear

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ZerolBevelGear")

    class _Cast_ZerolBevelGear:
        """Special nested class for casting ZerolBevelGear to subclasses."""

        def __init__(
            self: "ZerolBevelGear._Cast_ZerolBevelGear", parent: "ZerolBevelGear"
        ):
            self._parent = parent

        @property
        def bevel_gear(self: "ZerolBevelGear._Cast_ZerolBevelGear"):
            return self._parent._cast(_2521.BevelGear)

        @property
        def agma_gleason_conical_gear(self: "ZerolBevelGear._Cast_ZerolBevelGear"):
            from mastapy.system_model.part_model.gears import _2515

            return self._parent._cast(_2515.AGMAGleasonConicalGear)

        @property
        def conical_gear(self: "ZerolBevelGear._Cast_ZerolBevelGear"):
            from mastapy.system_model.part_model.gears import _2525

            return self._parent._cast(_2525.ConicalGear)

        @property
        def gear(self: "ZerolBevelGear._Cast_ZerolBevelGear"):
            from mastapy.system_model.part_model.gears import _2532

            return self._parent._cast(_2532.Gear)

        @property
        def mountable_component(self: "ZerolBevelGear._Cast_ZerolBevelGear"):
            from mastapy.system_model.part_model import _2466

            return self._parent._cast(_2466.MountableComponent)

        @property
        def component(self: "ZerolBevelGear._Cast_ZerolBevelGear"):
            from mastapy.system_model.part_model import _2446

            return self._parent._cast(_2446.Component)

        @property
        def part(self: "ZerolBevelGear._Cast_ZerolBevelGear"):
            from mastapy.system_model.part_model import _2470

            return self._parent._cast(_2470.Part)

        @property
        def design_entity(self: "ZerolBevelGear._Cast_ZerolBevelGear"):
            from mastapy.system_model import _2205

            return self._parent._cast(_2205.DesignEntity)

        @property
        def zerol_bevel_gear(
            self: "ZerolBevelGear._Cast_ZerolBevelGear",
        ) -> "ZerolBevelGear":
            return self._parent

        def __getattr__(self: "ZerolBevelGear._Cast_ZerolBevelGear", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ZerolBevelGear.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_design(self: Self) -> "_952.ZerolBevelGearDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearDesign

        Note:
            This property is readonly.
        """
        temp = self.wrapped.BevelGearDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def zerol_bevel_gear_design(self: Self) -> "_952.ZerolBevelGearDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearDesign

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ZerolBevelGearDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "ZerolBevelGear._Cast_ZerolBevelGear":
        return self._Cast_ZerolBevelGear(self)
