"""CouplingHalfLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6927
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingHalfLoadCase"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2586


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfLoadCase",)


Self = TypeVar("Self", bound="CouplingHalfLoadCase")


class CouplingHalfLoadCase(_6927.MountableComponentLoadCase):
    """CouplingHalfLoadCase

    This is a mastapy class.
    """

    TYPE = _COUPLING_HALF_LOAD_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingHalfLoadCase")

    class _Cast_CouplingHalfLoadCase:
        """Special nested class for casting CouplingHalfLoadCase to subclasses."""

        def __init__(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
            parent: "CouplingHalfLoadCase",
        ):
            self._parent = parent

        @property
        def mountable_component_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            return self._parent._cast(_6927.MountableComponentLoadCase)

        @property
        def component_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6840

            return self._parent._cast(_6840.ComponentLoadCase)

        @property
        def part_load_case(self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6931

            return self._parent._cast(_6931.PartLoadCase)

        @property
        def part_analysis(self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_half_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6836

            return self._parent._cast(_6836.ClutchHalfLoadCase)

        @property
        def concept_coupling_half_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6842

            return self._parent._cast(_6842.ConceptCouplingHalfLoadCase)

        @property
        def cvt_pulley_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6859

            return self._parent._cast(_6859.CVTPulleyLoadCase)

        @property
        def part_to_part_shear_coupling_half_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6933

            return self._parent._cast(_6933.PartToPartShearCouplingHalfLoadCase)

        @property
        def pulley_load_case(self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6943

            return self._parent._cast(_6943.PulleyLoadCase)

        @property
        def rolling_ring_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6950

            return self._parent._cast(_6950.RollingRingLoadCase)

        @property
        def spring_damper_half_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6960

            return self._parent._cast(_6960.SpringDamperHalfLoadCase)

        @property
        def synchroniser_half_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6970

            return self._parent._cast(_6970.SynchroniserHalfLoadCase)

        @property
        def synchroniser_part_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6972

            return self._parent._cast(_6972.SynchroniserPartLoadCase)

        @property
        def synchroniser_sleeve_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6973

            return self._parent._cast(_6973.SynchroniserSleeveLoadCase)

        @property
        def torque_converter_pump_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6977

            return self._parent._cast(_6977.TorqueConverterPumpLoadCase)

        @property
        def torque_converter_turbine_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6978

            return self._parent._cast(_6978.TorqueConverterTurbineLoadCase)

        @property
        def coupling_half_load_case(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase",
        ) -> "CouplingHalfLoadCase":
            return self._parent

        def __getattr__(
            self: "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CouplingHalfLoadCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2586.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "CouplingHalfLoadCase._Cast_CouplingHalfLoadCase":
        return self._Cast_CouplingHalfLoadCase(self)
