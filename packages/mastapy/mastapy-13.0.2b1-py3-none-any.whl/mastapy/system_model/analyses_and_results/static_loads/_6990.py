"""ZerolBevelGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6832
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ZerolBevelGearSetLoadCase",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2556
    from mastapy.system_model.analyses_and_results.static_loads import _6988, _6989


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearSetLoadCase",)


Self = TypeVar("Self", bound="ZerolBevelGearSetLoadCase")


class ZerolBevelGearSetLoadCase(_6832.BevelGearSetLoadCase):
    """ZerolBevelGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_SET_LOAD_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ZerolBevelGearSetLoadCase")

    class _Cast_ZerolBevelGearSetLoadCase:
        """Special nested class for casting ZerolBevelGearSetLoadCase to subclasses."""

        def __init__(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
            parent: "ZerolBevelGearSetLoadCase",
        ):
            self._parent = parent

        @property
        def bevel_gear_set_load_case(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            return self._parent._cast(_6832.BevelGearSetLoadCase)

        @property
        def agma_gleason_conical_gear_set_load_case(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6818

            return self._parent._cast(_6818.AGMAGleasonConicalGearSetLoadCase)

        @property
        def conical_gear_set_load_case(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6851

            return self._parent._cast(_6851.ConicalGearSetLoadCase)

        @property
        def gear_set_load_case(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6898

            return self._parent._cast(_6898.GearSetLoadCase)

        @property
        def specialised_assembly_load_case(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6955

            return self._parent._cast(_6955.SpecialisedAssemblyLoadCase)

        @property
        def abstract_assembly_load_case(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6809

            return self._parent._cast(_6809.AbstractAssemblyLoadCase)

        @property
        def part_load_case(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6931

            return self._parent._cast(_6931.PartLoadCase)

        @property
        def part_analysis(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def zerol_bevel_gear_set_load_case(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase",
        ) -> "ZerolBevelGearSetLoadCase":
            return self._parent

        def __getattr__(
            self: "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ZerolBevelGearSetLoadCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2556.ZerolBevelGearSet":
        """mastapy.system_model.part_model.gears.ZerolBevelGearSet

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears(self: Self) -> "List[_6988.ZerolBevelGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_gears_load_case(self: Self) -> "List[_6988.ZerolBevelGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ZerolBevelGearsLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_meshes_load_case(
        self: Self,
    ) -> "List[_6989.ZerolBevelGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ZerolBevelMeshesLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "ZerolBevelGearSetLoadCase._Cast_ZerolBevelGearSetLoadCase":
        return self._Cast_ZerolBevelGearSetLoadCase(self)
