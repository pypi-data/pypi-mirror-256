"""InterMountableComponentConnectionPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4069
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "InterMountableComponentConnectionPowerFlow",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2283


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionPowerFlow",)


Self = TypeVar("Self", bound="InterMountableComponentConnectionPowerFlow")


class InterMountableComponentConnectionPowerFlow(_4069.ConnectionPowerFlow):
    """InterMountableComponentConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_POWER_FLOW
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_InterMountableComponentConnectionPowerFlow"
    )

    class _Cast_InterMountableComponentConnectionPowerFlow:
        """Special nested class for casting InterMountableComponentConnectionPowerFlow to subclasses."""

        def __init__(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
            parent: "InterMountableComponentConnectionPowerFlow",
        ):
            self._parent = parent

        @property
        def connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            return self._parent._cast(_4069.ConnectionPowerFlow)

        @property
        def connection_static_load_analysis_case(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4038

            return self._parent._cast(_4038.AGMAGleasonConicalGearMeshPowerFlow)

        @property
        def belt_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4043

            return self._parent._cast(_4043.BeltConnectionPowerFlow)

        @property
        def bevel_differential_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4045

            return self._parent._cast(_4045.BevelDifferentialGearMeshPowerFlow)

        @property
        def bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4050

            return self._parent._cast(_4050.BevelGearMeshPowerFlow)

        @property
        def clutch_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4055

            return self._parent._cast(_4055.ClutchConnectionPowerFlow)

        @property
        def concept_coupling_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4060

            return self._parent._cast(_4060.ConceptCouplingConnectionPowerFlow)

        @property
        def concept_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4063

            return self._parent._cast(_4063.ConceptGearMeshPowerFlow)

        @property
        def conical_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4066

            return self._parent._cast(_4066.ConicalGearMeshPowerFlow)

        @property
        def coupling_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4071

            return self._parent._cast(_4071.CouplingConnectionPowerFlow)

        @property
        def cvt_belt_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4074

            return self._parent._cast(_4074.CVTBeltConnectionPowerFlow)

        @property
        def cylindrical_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4082

            return self._parent._cast(_4082.CylindricalGearMeshPowerFlow)

        @property
        def face_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4088

            return self._parent._cast(_4088.FaceGearMeshPowerFlow)

        @property
        def gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4095

            return self._parent._cast(_4095.GearMeshPowerFlow)

        @property
        def hypoid_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4099

            return self._parent._cast(_4099.HypoidGearMeshPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4103

            return self._parent._cast(
                _4103.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4106

            return self._parent._cast(
                _4106.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4109

            return self._parent._cast(
                _4109.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
            )

        @property
        def part_to_part_shear_coupling_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4117

            return self._parent._cast(_4117.PartToPartShearCouplingConnectionPowerFlow)

        @property
        def ring_pins_to_disc_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4129

            return self._parent._cast(_4129.RingPinsToDiscConnectionPowerFlow)

        @property
        def rolling_ring_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4131

            return self._parent._cast(_4131.RollingRingConnectionPowerFlow)

        @property
        def spiral_bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4138

            return self._parent._cast(_4138.SpiralBevelGearMeshPowerFlow)

        @property
        def spring_damper_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4141

            return self._parent._cast(_4141.SpringDamperConnectionPowerFlow)

        @property
        def straight_bevel_diff_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4144

            return self._parent._cast(_4144.StraightBevelDiffGearMeshPowerFlow)

        @property
        def straight_bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4147

            return self._parent._cast(_4147.StraightBevelGearMeshPowerFlow)

        @property
        def torque_converter_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4157

            return self._parent._cast(_4157.TorqueConverterConnectionPowerFlow)

        @property
        def worm_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4163

            return self._parent._cast(_4163.WormGearMeshPowerFlow)

        @property
        def zerol_bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4166

            return self._parent._cast(_4166.ZerolBevelGearMeshPowerFlow)

        @property
        def inter_mountable_component_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "InterMountableComponentConnectionPowerFlow":
            return self._parent

        def __getattr__(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
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
        self: Self, instance_to_wrap: "InterMountableComponentConnectionPowerFlow.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2283.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow":
        return self._Cast_InterMountableComponentConnectionPowerFlow(self)
