"""PulleyPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4072
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PULLEY_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "PulleyPowerFlow"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2592
    from mastapy.system_model.analyses_and_results.static_loads import _6943


__docformat__ = "restructuredtext en"
__all__ = ("PulleyPowerFlow",)


Self = TypeVar("Self", bound="PulleyPowerFlow")


class PulleyPowerFlow(_4072.CouplingHalfPowerFlow):
    """PulleyPowerFlow

    This is a mastapy class.
    """

    TYPE = _PULLEY_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PulleyPowerFlow")

    class _Cast_PulleyPowerFlow:
        """Special nested class for casting PulleyPowerFlow to subclasses."""

        def __init__(
            self: "PulleyPowerFlow._Cast_PulleyPowerFlow", parent: "PulleyPowerFlow"
        ):
            self._parent = parent

        @property
        def coupling_half_power_flow(self: "PulleyPowerFlow._Cast_PulleyPowerFlow"):
            return self._parent._cast(_4072.CouplingHalfPowerFlow)

        @property
        def mountable_component_power_flow(
            self: "PulleyPowerFlow._Cast_PulleyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4114

            return self._parent._cast(_4114.MountableComponentPowerFlow)

        @property
        def component_power_flow(self: "PulleyPowerFlow._Cast_PulleyPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4059

            return self._parent._cast(_4059.ComponentPowerFlow)

        @property
        def part_power_flow(self: "PulleyPowerFlow._Cast_PulleyPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4116

            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "PulleyPowerFlow._Cast_PulleyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(self: "PulleyPowerFlow._Cast_PulleyPowerFlow"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "PulleyPowerFlow._Cast_PulleyPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PulleyPowerFlow._Cast_PulleyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(self: "PulleyPowerFlow._Cast_PulleyPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cvt_pulley_power_flow(self: "PulleyPowerFlow._Cast_PulleyPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4076

            return self._parent._cast(_4076.CVTPulleyPowerFlow)

        @property
        def pulley_power_flow(
            self: "PulleyPowerFlow._Cast_PulleyPowerFlow",
        ) -> "PulleyPowerFlow":
            return self._parent

        def __getattr__(self: "PulleyPowerFlow._Cast_PulleyPowerFlow", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PulleyPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2592.Pulley":
        """mastapy.system_model.part_model.couplings.Pulley

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6943.PulleyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "PulleyPowerFlow._Cast_PulleyPowerFlow":
        return self._Cast_PulleyPowerFlow(self)
