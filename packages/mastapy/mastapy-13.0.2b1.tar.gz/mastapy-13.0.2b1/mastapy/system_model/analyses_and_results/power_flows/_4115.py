"""OilSealPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4070
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "OilSealPowerFlow"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2468
    from mastapy.system_model.analyses_and_results.static_loads import _6929


__docformat__ = "restructuredtext en"
__all__ = ("OilSealPowerFlow",)


Self = TypeVar("Self", bound="OilSealPowerFlow")


class OilSealPowerFlow(_4070.ConnectorPowerFlow):
    """OilSealPowerFlow

    This is a mastapy class.
    """

    TYPE = _OIL_SEAL_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_OilSealPowerFlow")

    class _Cast_OilSealPowerFlow:
        """Special nested class for casting OilSealPowerFlow to subclasses."""

        def __init__(
            self: "OilSealPowerFlow._Cast_OilSealPowerFlow", parent: "OilSealPowerFlow"
        ):
            self._parent = parent

        @property
        def connector_power_flow(self: "OilSealPowerFlow._Cast_OilSealPowerFlow"):
            return self._parent._cast(_4070.ConnectorPowerFlow)

        @property
        def mountable_component_power_flow(
            self: "OilSealPowerFlow._Cast_OilSealPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4114

            return self._parent._cast(_4114.MountableComponentPowerFlow)

        @property
        def component_power_flow(self: "OilSealPowerFlow._Cast_OilSealPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4059

            return self._parent._cast(_4059.ComponentPowerFlow)

        @property
        def part_power_flow(self: "OilSealPowerFlow._Cast_OilSealPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4116

            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "OilSealPowerFlow._Cast_OilSealPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(self: "OilSealPowerFlow._Cast_OilSealPowerFlow"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "OilSealPowerFlow._Cast_OilSealPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "OilSealPowerFlow._Cast_OilSealPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(self: "OilSealPowerFlow._Cast_OilSealPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def oil_seal_power_flow(
            self: "OilSealPowerFlow._Cast_OilSealPowerFlow",
        ) -> "OilSealPowerFlow":
            return self._parent

        def __getattr__(self: "OilSealPowerFlow._Cast_OilSealPowerFlow", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "OilSealPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2468.OilSeal":
        """mastapy.system_model.part_model.OilSeal

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6929.OilSealLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "OilSealPowerFlow._Cast_OilSealPowerFlow":
        return self._Cast_OilSealPowerFlow(self)
