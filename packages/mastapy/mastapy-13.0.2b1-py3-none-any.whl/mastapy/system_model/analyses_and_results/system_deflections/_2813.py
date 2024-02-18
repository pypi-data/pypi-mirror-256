"""SpringDamperHalfSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2732
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "SpringDamperHalfSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2603
    from mastapy.system_model.analyses_and_results.static_loads import _6960
    from mastapy.system_model.analyses_and_results.power_flows import _4142


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperHalfSystemDeflection",)


Self = TypeVar("Self", bound="SpringDamperHalfSystemDeflection")


class SpringDamperHalfSystemDeflection(_2732.CouplingHalfSystemDeflection):
    """SpringDamperHalfSystemDeflection

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_HALF_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_SpringDamperHalfSystemDeflection")

    class _Cast_SpringDamperHalfSystemDeflection:
        """Special nested class for casting SpringDamperHalfSystemDeflection to subclasses."""

        def __init__(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
            parent: "SpringDamperHalfSystemDeflection",
        ):
            self._parent = parent

        @property
        def coupling_half_system_deflection(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            return self._parent._cast(_2732.CouplingHalfSystemDeflection)

        @property
        def mountable_component_system_deflection(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2784,
            )

            return self._parent._cast(_2784.MountableComponentSystemDeflection)

        @property
        def component_system_deflection(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2717,
            )

            return self._parent._cast(_2717.ComponentSystemDeflection)

        @property
        def part_system_deflection(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def spring_damper_half_system_deflection(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
        ) -> "SpringDamperHalfSystemDeflection":
            return self._parent

        def __getattr__(
            self: "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "SpringDamperHalfSystemDeflection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2603.SpringDamperHalf":
        """mastapy.system_model.part_model.couplings.SpringDamperHalf

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6960.SpringDamperHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: Self) -> "_4142.SpringDamperHalfPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.SpringDamperHalfPowerFlow

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
    ) -> "SpringDamperHalfSystemDeflection._Cast_SpringDamperHalfSystemDeflection":
        return self._Cast_SpringDamperHalfSystemDeflection(self)
