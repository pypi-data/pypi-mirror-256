"""KlingelnbergCycloPalloidConicalGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6851
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearSetLoadCase",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2539


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSetLoadCase",)


Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearSetLoadCase")


class KlingelnbergCycloPalloidConicalGearSetLoadCase(_6851.ConicalGearSetLoadCase):
    """KlingelnbergCycloPalloidConicalGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_LOAD_CASE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase"
    )

    class _Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase:
        """Special nested class for casting KlingelnbergCycloPalloidConicalGearSetLoadCase to subclasses."""

        def __init__(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
            parent: "KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            self._parent = parent

        @property
        def conical_gear_set_load_case(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            return self._parent._cast(_6851.ConicalGearSetLoadCase)

        @property
        def gear_set_load_case(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6898

            return self._parent._cast(_6898.GearSetLoadCase)

        @property
        def specialised_assembly_load_case(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6955

            return self._parent._cast(_6955.SpecialisedAssemblyLoadCase)

        @property
        def abstract_assembly_load_case(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6809

            return self._parent._cast(_6809.AbstractAssemblyLoadCase)

        @property
        def part_load_case(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6931

            return self._parent._cast(_6931.PartLoadCase)

        @property
        def part_analysis(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6920

            return self._parent._cast(
                _6920.KlingelnbergCycloPalloidHypoidGearSetLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6923

            return self._parent._cast(
                _6923.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
        ) -> "KlingelnbergCycloPalloidConicalGearSetLoadCase":
            return self._parent

        def __getattr__(
            self: "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(
        self: Self,
        instance_to_wrap: "KlingelnbergCycloPalloidConicalGearSetLoadCase.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2539.KlingelnbergCycloPalloidConicalGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "KlingelnbergCycloPalloidConicalGearSetLoadCase._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase":
        return self._Cast_KlingelnbergCycloPalloidConicalGearSetLoadCase(self)
