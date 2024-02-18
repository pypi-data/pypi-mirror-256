"""AGMAGleasonConicalGear"""

from __future__ import annotations

from typing import TypeVar

from mastapy.system_model.part_model.gears import _2525
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGear",)


Self = TypeVar("Self", bound="AGMAGleasonConicalGear")


class AGMAGleasonConicalGear(_2525.ConicalGear):
    """AGMAGleasonConicalGear

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_AGMAGleasonConicalGear")

    class _Cast_AGMAGleasonConicalGear:
        """Special nested class for casting AGMAGleasonConicalGear to subclasses."""

        def __init__(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
            parent: "AGMAGleasonConicalGear",
        ):
            self._parent = parent

        @property
        def conical_gear(self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"):
            return self._parent._cast(_2525.ConicalGear)

        @property
        def gear(self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"):
            from mastapy.system_model.part_model.gears import _2532

            return self._parent._cast(_2532.Gear)

        @property
        def mountable_component(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model import _2466

            return self._parent._cast(_2466.MountableComponent)

        @property
        def component(self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"):
            from mastapy.system_model.part_model import _2446

            return self._parent._cast(_2446.Component)

        @property
        def part(self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"):
            from mastapy.system_model.part_model import _2470

            return self._parent._cast(_2470.Part)

        @property
        def design_entity(self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"):
            from mastapy.system_model import _2205

            return self._parent._cast(_2205.DesignEntity)

        @property
        def bevel_differential_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2517

            return self._parent._cast(_2517.BevelDifferentialGear)

        @property
        def bevel_differential_planet_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2519

            return self._parent._cast(_2519.BevelDifferentialPlanetGear)

        @property
        def bevel_differential_sun_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2520

            return self._parent._cast(_2520.BevelDifferentialSunGear)

        @property
        def bevel_gear(self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"):
            from mastapy.system_model.part_model.gears import _2521

            return self._parent._cast(_2521.BevelGear)

        @property
        def hypoid_gear(self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"):
            from mastapy.system_model.part_model.gears import _2536

            return self._parent._cast(_2536.HypoidGear)

        @property
        def spiral_bevel_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2545

            return self._parent._cast(_2545.SpiralBevelGear)

        @property
        def straight_bevel_diff_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2547

            return self._parent._cast(_2547.StraightBevelDiffGear)

        @property
        def straight_bevel_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2549

            return self._parent._cast(_2549.StraightBevelGear)

        @property
        def straight_bevel_planet_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2551

            return self._parent._cast(_2551.StraightBevelPlanetGear)

        @property
        def straight_bevel_sun_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2552

            return self._parent._cast(_2552.StraightBevelSunGear)

        @property
        def zerol_bevel_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ):
            from mastapy.system_model.part_model.gears import _2555

            return self._parent._cast(_2555.ZerolBevelGear)

        @property
        def agma_gleason_conical_gear(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear",
        ) -> "AGMAGleasonConicalGear":
            return self._parent

        def __getattr__(
            self: "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "AGMAGleasonConicalGear.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear":
        return self._Cast_AGMAGleasonConicalGear(self)
