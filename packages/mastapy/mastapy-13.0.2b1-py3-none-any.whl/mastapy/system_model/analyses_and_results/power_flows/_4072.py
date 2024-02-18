"""CouplingHalfPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4114
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "CouplingHalfPowerFlow"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2586


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfPowerFlow",)


Self = TypeVar("Self", bound="CouplingHalfPowerFlow")


class CouplingHalfPowerFlow(_4114.MountableComponentPowerFlow):
    """CouplingHalfPowerFlow

    This is a mastapy class.
    """

    TYPE = _COUPLING_HALF_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingHalfPowerFlow")

    class _Cast_CouplingHalfPowerFlow:
        """Special nested class for casting CouplingHalfPowerFlow to subclasses."""

        def __init__(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
            parent: "CouplingHalfPowerFlow",
        ):
            self._parent = parent

        @property
        def mountable_component_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            return self._parent._cast(_4114.MountableComponentPowerFlow)

        @property
        def component_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4059

            return self._parent._cast(_4059.ComponentPowerFlow)

        @property
        def part_power_flow(self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow"):
            from mastapy.system_model.analyses_and_results.power_flows import _4116

            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_half_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4056

            return self._parent._cast(_4056.ClutchHalfPowerFlow)

        @property
        def concept_coupling_half_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4061

            return self._parent._cast(_4061.ConceptCouplingHalfPowerFlow)

        @property
        def cvt_pulley_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4076

            return self._parent._cast(_4076.CVTPulleyPowerFlow)

        @property
        def part_to_part_shear_coupling_half_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4118

            return self._parent._cast(_4118.PartToPartShearCouplingHalfPowerFlow)

        @property
        def pulley_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4127

            return self._parent._cast(_4127.PulleyPowerFlow)

        @property
        def rolling_ring_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4132

            return self._parent._cast(_4132.RollingRingPowerFlow)

        @property
        def spring_damper_half_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4142

            return self._parent._cast(_4142.SpringDamperHalfPowerFlow)

        @property
        def synchroniser_half_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4152

            return self._parent._cast(_4152.SynchroniserHalfPowerFlow)

        @property
        def synchroniser_part_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4153

            return self._parent._cast(_4153.SynchroniserPartPowerFlow)

        @property
        def synchroniser_sleeve_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4155

            return self._parent._cast(_4155.SynchroniserSleevePowerFlow)

        @property
        def torque_converter_pump_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4159

            return self._parent._cast(_4159.TorqueConverterPumpPowerFlow)

        @property
        def torque_converter_turbine_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4160

            return self._parent._cast(_4160.TorqueConverterTurbinePowerFlow)

        @property
        def coupling_half_power_flow(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow",
        ) -> "CouplingHalfPowerFlow":
            return self._parent

        def __getattr__(
            self: "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CouplingHalfPowerFlow.TYPE"):
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
    def cast_to(self: Self) -> "CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow":
        return self._Cast_CouplingHalfPowerFlow(self)
