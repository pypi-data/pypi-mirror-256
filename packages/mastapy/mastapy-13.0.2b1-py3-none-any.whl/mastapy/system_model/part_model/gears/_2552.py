"""StraightBevelSunGear"""

from __future__ import annotations

from typing import TypeVar

from mastapy.system_model.part_model.gears import _2547
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
)


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGear",)


Self = TypeVar("Self", bound="StraightBevelSunGear")


class StraightBevelSunGear(_2547.StraightBevelDiffGear):
    """StraightBevelSunGear

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_StraightBevelSunGear")

    class _Cast_StraightBevelSunGear:
        """Special nested class for casting StraightBevelSunGear to subclasses."""

        def __init__(
            self: "StraightBevelSunGear._Cast_StraightBevelSunGear",
            parent: "StraightBevelSunGear",
        ):
            self._parent = parent

        @property
        def straight_bevel_diff_gear(
            self: "StraightBevelSunGear._Cast_StraightBevelSunGear",
        ):
            return self._parent._cast(_2547.StraightBevelDiffGear)

        @property
        def bevel_gear(self: "StraightBevelSunGear._Cast_StraightBevelSunGear"):
            from mastapy.system_model.part_model.gears import _2521

            return self._parent._cast(_2521.BevelGear)

        @property
        def agma_gleason_conical_gear(
            self: "StraightBevelSunGear._Cast_StraightBevelSunGear",
        ):
            from mastapy.system_model.part_model.gears import _2515

            return self._parent._cast(_2515.AGMAGleasonConicalGear)

        @property
        def conical_gear(self: "StraightBevelSunGear._Cast_StraightBevelSunGear"):
            from mastapy.system_model.part_model.gears import _2525

            return self._parent._cast(_2525.ConicalGear)

        @property
        def gear(self: "StraightBevelSunGear._Cast_StraightBevelSunGear"):
            from mastapy.system_model.part_model.gears import _2532

            return self._parent._cast(_2532.Gear)

        @property
        def mountable_component(
            self: "StraightBevelSunGear._Cast_StraightBevelSunGear",
        ):
            from mastapy.system_model.part_model import _2466

            return self._parent._cast(_2466.MountableComponent)

        @property
        def component(self: "StraightBevelSunGear._Cast_StraightBevelSunGear"):
            from mastapy.system_model.part_model import _2446

            return self._parent._cast(_2446.Component)

        @property
        def part(self: "StraightBevelSunGear._Cast_StraightBevelSunGear"):
            from mastapy.system_model.part_model import _2470

            return self._parent._cast(_2470.Part)

        @property
        def design_entity(self: "StraightBevelSunGear._Cast_StraightBevelSunGear"):
            from mastapy.system_model import _2205

            return self._parent._cast(_2205.DesignEntity)

        @property
        def straight_bevel_sun_gear(
            self: "StraightBevelSunGear._Cast_StraightBevelSunGear",
        ) -> "StraightBevelSunGear":
            return self._parent

        def __getattr__(
            self: "StraightBevelSunGear._Cast_StraightBevelSunGear", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "StraightBevelSunGear.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "StraightBevelSunGear._Cast_StraightBevelSunGear":
        return self._Cast_StraightBevelSunGear(self)
