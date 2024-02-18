"""ClutchHalfSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2732
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ClutchHalfSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2581
    from mastapy.system_model.analyses_and_results.static_loads import _6836
    from mastapy.system_model.analyses_and_results.power_flows import _4056


__docformat__ = "restructuredtext en"
__all__ = ("ClutchHalfSystemDeflection",)


Self = TypeVar("Self", bound="ClutchHalfSystemDeflection")


class ClutchHalfSystemDeflection(_2732.CouplingHalfSystemDeflection):
    """ClutchHalfSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CLUTCH_HALF_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ClutchHalfSystemDeflection")

    class _Cast_ClutchHalfSystemDeflection:
        """Special nested class for casting ClutchHalfSystemDeflection to subclasses."""

        def __init__(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
            parent: "ClutchHalfSystemDeflection",
        ):
            self._parent = parent

        @property
        def coupling_half_system_deflection(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            return self._parent._cast(_2732.CouplingHalfSystemDeflection)

        @property
        def mountable_component_system_deflection(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2784,
            )

            return self._parent._cast(_2784.MountableComponentSystemDeflection)

        @property
        def component_system_deflection(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2717,
            )

            return self._parent._cast(_2717.ComponentSystemDeflection)

        @property
        def part_system_deflection(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_half_system_deflection(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
        ) -> "ClutchHalfSystemDeflection":
            return self._parent

        def __getattr__(
            self: "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ClutchHalfSystemDeflection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2581.ClutchHalf":
        """mastapy.system_model.part_model.couplings.ClutchHalf

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6836.ClutchHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: Self) -> "_4056.ClutchHalfPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ClutchHalfPowerFlow

        Note:
            This property is readonly.
        """
        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "ClutchHalfSystemDeflection._Cast_ClutchHalfSystemDeflection":
        return self._Cast_ClutchHalfSystemDeflection(self)
