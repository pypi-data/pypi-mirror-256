"""AGMAGleasonConicalGearSet"""

from __future__ import annotations

from typing import TypeVar

from mastapy.system_model.part_model.gears import _2526
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSet",)


Self = TypeVar("Self", bound="AGMAGleasonConicalGearSet")


class AGMAGleasonConicalGearSet(_2526.ConicalGearSet):
    """AGMAGleasonConicalGearSet

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_AGMAGleasonConicalGearSet")

    class _Cast_AGMAGleasonConicalGearSet:
        """Special nested class for casting AGMAGleasonConicalGearSet to subclasses."""

        def __init__(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
            parent: "AGMAGleasonConicalGearSet",
        ):
            self._parent = parent

        @property
        def conical_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            return self._parent._cast(_2526.ConicalGearSet)

        @property
        def gear_set(self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet"):
            from mastapy.system_model.part_model.gears import _2534

            return self._parent._cast(_2534.GearSet)

        @property
        def specialised_assembly(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model import _2478

            return self._parent._cast(_2478.SpecialisedAssembly)

        @property
        def abstract_assembly(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model import _2436

            return self._parent._cast(_2436.AbstractAssembly)

        @property
        def part(self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet"):
            from mastapy.system_model.part_model import _2470

            return self._parent._cast(_2470.Part)

        @property
        def design_entity(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model import _2205

            return self._parent._cast(_2205.DesignEntity)

        @property
        def bevel_differential_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model.gears import _2518

            return self._parent._cast(_2518.BevelDifferentialGearSet)

        @property
        def bevel_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model.gears import _2522

            return self._parent._cast(_2522.BevelGearSet)

        @property
        def hypoid_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model.gears import _2537

            return self._parent._cast(_2537.HypoidGearSet)

        @property
        def spiral_bevel_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model.gears import _2546

            return self._parent._cast(_2546.SpiralBevelGearSet)

        @property
        def straight_bevel_diff_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model.gears import _2548

            return self._parent._cast(_2548.StraightBevelDiffGearSet)

        @property
        def straight_bevel_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model.gears import _2550

            return self._parent._cast(_2550.StraightBevelGearSet)

        @property
        def zerol_bevel_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ):
            from mastapy.system_model.part_model.gears import _2556

            return self._parent._cast(_2556.ZerolBevelGearSet)

        @property
        def agma_gleason_conical_gear_set(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet",
        ) -> "AGMAGleasonConicalGearSet":
            return self._parent

        def __getattr__(
            self: "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "AGMAGleasonConicalGearSet.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet":
        return self._Cast_AGMAGleasonConicalGearSet(self)
