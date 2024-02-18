"""BearingPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4070
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEARING_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "BearingPowerFlow"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2441
    from mastapy.system_model.analyses_and_results.static_loads import _6822
    from mastapy.bearings.bearing_results.rolling import _2073


__docformat__ = "restructuredtext en"
__all__ = ("BearingPowerFlow",)


Self = TypeVar("Self", bound="BearingPowerFlow")


class BearingPowerFlow(_4070.ConnectorPowerFlow):
    """BearingPowerFlow

    This is a mastapy class.
    """

    TYPE = _BEARING_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BearingPowerFlow")

    class _Cast_BearingPowerFlow:
        """Special nested class for casting BearingPowerFlow to subclasses."""

        def __init__(
            self: "BearingPowerFlow._Cast_BearingPowerFlow", parent: "BearingPowerFlow"
        ):
            self._parent = parent

        @property
        def connector_power_flow(self: "BearingPowerFlow._Cast_BearingPowerFlow"):
            return self._parent._cast(_4070.ConnectorPowerFlow)

        @property
        def mountable_component_power_flow(
            self: "BearingPowerFlow._Cast_BearingPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4114

            return self._parent._cast(_4114.MountableComponentPowerFlow)

        @property
        def component_power_flow(self: "BearingPowerFlow._Cast_BearingPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4059

            return self._parent._cast(_4059.ComponentPowerFlow)

        @property
        def part_power_flow(self: "BearingPowerFlow._Cast_BearingPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4116

            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "BearingPowerFlow._Cast_BearingPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(self: "BearingPowerFlow._Cast_BearingPowerFlow"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "BearingPowerFlow._Cast_BearingPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BearingPowerFlow._Cast_BearingPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(self: "BearingPowerFlow._Cast_BearingPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bearing_power_flow(
            self: "BearingPowerFlow._Cast_BearingPowerFlow",
        ) -> "BearingPowerFlow":
            return self._parent

        def __getattr__(self: "BearingPowerFlow._Cast_BearingPowerFlow", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BearingPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2441.Bearing":
        """mastapy.system_model.part_model.Bearing

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6822.BearingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rolling_bearing_speed_results(self: Self) -> "_2073.RollingBearingSpeedResults":
        """mastapy.bearings.bearing_results.rolling.RollingBearingSpeedResults

        Note:
            This property is readonly.
        """
        temp = self.wrapped.RollingBearingSpeedResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "BearingPowerFlow._Cast_BearingPowerFlow":
        return self._Cast_BearingPowerFlow(self)
