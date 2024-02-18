"""GearLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Union, Tuple

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6927
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearLoadCase"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2532
    from mastapy.system_model.analyses_and_results.static_loads import _6894


__docformat__ = "restructuredtext en"
__all__ = ("GearLoadCase",)


Self = TypeVar("Self", bound="GearLoadCase")


class GearLoadCase(_6927.MountableComponentLoadCase):
    """GearLoadCase

    This is a mastapy class.
    """

    TYPE = _GEAR_LOAD_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_GearLoadCase")

    class _Cast_GearLoadCase:
        """Special nested class for casting GearLoadCase to subclasses."""

        def __init__(self: "GearLoadCase._Cast_GearLoadCase", parent: "GearLoadCase"):
            self._parent = parent

        @property
        def mountable_component_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            return self._parent._cast(_6927.MountableComponentLoadCase)

        @property
        def component_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6840

            return self._parent._cast(_6840.ComponentLoadCase)

        @property
        def part_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6931

            return self._parent._cast(_6931.PartLoadCase)

        @property
        def part_analysis(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "GearLoadCase._Cast_GearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_load_case(
            self: "GearLoadCase._Cast_GearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6816

            return self._parent._cast(_6816.AGMAGleasonConicalGearLoadCase)

        @property
        def bevel_differential_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6825

            return self._parent._cast(_6825.BevelDifferentialGearLoadCase)

        @property
        def bevel_differential_planet_gear_load_case(
            self: "GearLoadCase._Cast_GearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6828

            return self._parent._cast(_6828.BevelDifferentialPlanetGearLoadCase)

        @property
        def bevel_differential_sun_gear_load_case(
            self: "GearLoadCase._Cast_GearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6829

            return self._parent._cast(_6829.BevelDifferentialSunGearLoadCase)

        @property
        def bevel_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6830

            return self._parent._cast(_6830.BevelGearLoadCase)

        @property
        def concept_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6844

            return self._parent._cast(_6844.ConceptGearLoadCase)

        @property
        def conical_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6847

            return self._parent._cast(_6847.ConicalGearLoadCase)

        @property
        def cylindrical_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6864

            return self._parent._cast(_6864.CylindricalGearLoadCase)

        @property
        def cylindrical_planet_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6869

            return self._parent._cast(_6869.CylindricalPlanetGearLoadCase)

        @property
        def face_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6887

            return self._parent._cast(_6887.FaceGearLoadCase)

        @property
        def hypoid_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6908

            return self._parent._cast(_6908.HypoidGearLoadCase)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_load_case(
            self: "GearLoadCase._Cast_GearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6915

            return self._parent._cast(_6915.KlingelnbergCycloPalloidConicalGearLoadCase)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
            self: "GearLoadCase._Cast_GearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6918

            return self._parent._cast(_6918.KlingelnbergCycloPalloidHypoidGearLoadCase)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
            self: "GearLoadCase._Cast_GearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6921

            return self._parent._cast(
                _6921.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
            )

        @property
        def spiral_bevel_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6956

            return self._parent._cast(_6956.SpiralBevelGearLoadCase)

        @property
        def straight_bevel_diff_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6962

            return self._parent._cast(_6962.StraightBevelDiffGearLoadCase)

        @property
        def straight_bevel_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6965

            return self._parent._cast(_6965.StraightBevelGearLoadCase)

        @property
        def straight_bevel_planet_gear_load_case(
            self: "GearLoadCase._Cast_GearLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6968

            return self._parent._cast(_6968.StraightBevelPlanetGearLoadCase)

        @property
        def straight_bevel_sun_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6969

            return self._parent._cast(_6969.StraightBevelSunGearLoadCase)

        @property
        def worm_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6985

            return self._parent._cast(_6985.WormGearLoadCase)

        @property
        def zerol_bevel_gear_load_case(self: "GearLoadCase._Cast_GearLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6988

            return self._parent._cast(_6988.ZerolBevelGearLoadCase)

        @property
        def gear_load_case(self: "GearLoadCase._Cast_GearLoadCase") -> "GearLoadCase":
            return self._parent

        def __getattr__(self: "GearLoadCase._Cast_GearLoadCase", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "GearLoadCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_temperature(self: Self) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = self.wrapped.GearTemperature

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @gear_temperature.setter
    @enforce_parameter_types
    def gear_temperature(self: Self, value: "Union[float, Tuple[float, bool]]"):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        self.wrapped.GearTemperature = value

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
    def gear_manufacture_errors(self: Self) -> "_6894.GearManufactureError":
        """mastapy.system_model.analyses_and_results.static_loads.GearManufactureError

        Note:
            This property is readonly.
        """
        temp = self.wrapped.GearManufactureErrors

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "GearLoadCase._Cast_GearLoadCase":
        return self._Cast_GearLoadCase(self)
