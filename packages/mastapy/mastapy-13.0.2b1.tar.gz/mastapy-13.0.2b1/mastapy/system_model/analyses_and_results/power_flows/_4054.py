"""BoltPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4059
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BOLT_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "BoltPowerFlow"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2444
    from mastapy.system_model.analyses_and_results.static_loads import _6834


__docformat__ = "restructuredtext en"
__all__ = ("BoltPowerFlow",)


Self = TypeVar("Self", bound="BoltPowerFlow")


class BoltPowerFlow(_4059.ComponentPowerFlow):
    """BoltPowerFlow

    This is a mastapy class.
    """

    TYPE = _BOLT_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BoltPowerFlow")

    class _Cast_BoltPowerFlow:
        """Special nested class for casting BoltPowerFlow to subclasses."""

        def __init__(
            self: "BoltPowerFlow._Cast_BoltPowerFlow", parent: "BoltPowerFlow"
        ):
            self._parent = parent

        @property
        def component_power_flow(self: "BoltPowerFlow._Cast_BoltPowerFlow"):
            return self._parent._cast(_4059.ComponentPowerFlow)

        @property
        def part_power_flow(self: "BoltPowerFlow._Cast_BoltPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4116

            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(self: "BoltPowerFlow._Cast_BoltPowerFlow"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(self: "BoltPowerFlow._Cast_BoltPowerFlow"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "BoltPowerFlow._Cast_BoltPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BoltPowerFlow._Cast_BoltPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(self: "BoltPowerFlow._Cast_BoltPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bolt_power_flow(
            self: "BoltPowerFlow._Cast_BoltPowerFlow",
        ) -> "BoltPowerFlow":
            return self._parent

        def __getattr__(self: "BoltPowerFlow._Cast_BoltPowerFlow", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BoltPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2444.Bolt":
        """mastapy.system_model.part_model.Bolt

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6834.BoltLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "BoltPowerFlow._Cast_BoltPowerFlow":
        return self._Cast_BoltPowerFlow(self)
