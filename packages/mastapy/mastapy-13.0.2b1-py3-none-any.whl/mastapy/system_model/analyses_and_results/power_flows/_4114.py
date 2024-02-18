"""MountableComponentPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4059
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "MountableComponentPowerFlow",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2466


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentPowerFlow",)


Self = TypeVar("Self", bound="MountableComponentPowerFlow")


class MountableComponentPowerFlow(_4059.ComponentPowerFlow):
    """MountableComponentPowerFlow

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_MountableComponentPowerFlow")

    class _Cast_MountableComponentPowerFlow:
        """Special nested class for casting MountableComponentPowerFlow to subclasses."""

        def __init__(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
            parent: "MountableComponentPowerFlow",
        ):
            self._parent = parent

        @property
        def component_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            return self._parent._cast(_4059.ComponentPowerFlow)

        @property
        def part_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4116

            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4039

            return self._parent._cast(_4039.AGMAGleasonConicalGearPowerFlow)

        @property
        def bearing_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4042

            return self._parent._cast(_4042.BearingPowerFlow)

        @property
        def bevel_differential_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4046

            return self._parent._cast(_4046.BevelDifferentialGearPowerFlow)

        @property
        def bevel_differential_planet_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4048

            return self._parent._cast(_4048.BevelDifferentialPlanetGearPowerFlow)

        @property
        def bevel_differential_sun_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4049

            return self._parent._cast(_4049.BevelDifferentialSunGearPowerFlow)

        @property
        def bevel_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4051

            return self._parent._cast(_4051.BevelGearPowerFlow)

        @property
        def clutch_half_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4056

            return self._parent._cast(_4056.ClutchHalfPowerFlow)

        @property
        def concept_coupling_half_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4061

            return self._parent._cast(_4061.ConceptCouplingHalfPowerFlow)

        @property
        def concept_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4064

            return self._parent._cast(_4064.ConceptGearPowerFlow)

        @property
        def conical_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4067

            return self._parent._cast(_4067.ConicalGearPowerFlow)

        @property
        def connector_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4070

            return self._parent._cast(_4070.ConnectorPowerFlow)

        @property
        def coupling_half_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4072

            return self._parent._cast(_4072.CouplingHalfPowerFlow)

        @property
        def cvt_pulley_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4076

            return self._parent._cast(_4076.CVTPulleyPowerFlow)

        @property
        def cylindrical_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4083

            return self._parent._cast(_4083.CylindricalGearPowerFlow)

        @property
        def cylindrical_planet_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4085

            return self._parent._cast(_4085.CylindricalPlanetGearPowerFlow)

        @property
        def face_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4089

            return self._parent._cast(_4089.FaceGearPowerFlow)

        @property
        def gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4096

            return self._parent._cast(_4096.GearPowerFlow)

        @property
        def hypoid_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4100

            return self._parent._cast(_4100.HypoidGearPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4104

            return self._parent._cast(
                _4104.KlingelnbergCycloPalloidConicalGearPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4107

            return self._parent._cast(_4107.KlingelnbergCycloPalloidHypoidGearPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4110

            return self._parent._cast(
                _4110.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
            )

        @property
        def mass_disc_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4112

            return self._parent._cast(_4112.MassDiscPowerFlow)

        @property
        def measurement_component_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4113

            return self._parent._cast(_4113.MeasurementComponentPowerFlow)

        @property
        def oil_seal_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4115

            return self._parent._cast(_4115.OilSealPowerFlow)

        @property
        def part_to_part_shear_coupling_half_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4118

            return self._parent._cast(_4118.PartToPartShearCouplingHalfPowerFlow)

        @property
        def planet_carrier_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4122

            return self._parent._cast(_4122.PlanetCarrierPowerFlow)

        @property
        def point_load_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4123

            return self._parent._cast(_4123.PointLoadPowerFlow)

        @property
        def power_load_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4126

            return self._parent._cast(_4126.PowerLoadPowerFlow)

        @property
        def pulley_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4127

            return self._parent._cast(_4127.PulleyPowerFlow)

        @property
        def ring_pins_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4128

            return self._parent._cast(_4128.RingPinsPowerFlow)

        @property
        def rolling_ring_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4132

            return self._parent._cast(_4132.RollingRingPowerFlow)

        @property
        def shaft_hub_connection_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4134

            return self._parent._cast(_4134.ShaftHubConnectionPowerFlow)

        @property
        def spiral_bevel_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4139

            return self._parent._cast(_4139.SpiralBevelGearPowerFlow)

        @property
        def spring_damper_half_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4142

            return self._parent._cast(_4142.SpringDamperHalfPowerFlow)

        @property
        def straight_bevel_diff_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4145

            return self._parent._cast(_4145.StraightBevelDiffGearPowerFlow)

        @property
        def straight_bevel_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4148

            return self._parent._cast(_4148.StraightBevelGearPowerFlow)

        @property
        def straight_bevel_planet_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4150

            return self._parent._cast(_4150.StraightBevelPlanetGearPowerFlow)

        @property
        def straight_bevel_sun_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4151

            return self._parent._cast(_4151.StraightBevelSunGearPowerFlow)

        @property
        def synchroniser_half_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4152

            return self._parent._cast(_4152.SynchroniserHalfPowerFlow)

        @property
        def synchroniser_part_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4153

            return self._parent._cast(_4153.SynchroniserPartPowerFlow)

        @property
        def synchroniser_sleeve_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4155

            return self._parent._cast(_4155.SynchroniserSleevePowerFlow)

        @property
        def torque_converter_pump_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4159

            return self._parent._cast(_4159.TorqueConverterPumpPowerFlow)

        @property
        def torque_converter_turbine_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4160

            return self._parent._cast(_4160.TorqueConverterTurbinePowerFlow)

        @property
        def unbalanced_mass_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4161

            return self._parent._cast(_4161.UnbalancedMassPowerFlow)

        @property
        def virtual_component_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4162

            return self._parent._cast(_4162.VirtualComponentPowerFlow)

        @property
        def worm_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4164

            return self._parent._cast(_4164.WormGearPowerFlow)

        @property
        def zerol_bevel_gear_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4167

            return self._parent._cast(_4167.ZerolBevelGearPowerFlow)

        @property
        def mountable_component_power_flow(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
        ) -> "MountableComponentPowerFlow":
            return self._parent

        def __getattr__(
            self: "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "MountableComponentPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2466.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "MountableComponentPowerFlow._Cast_MountableComponentPowerFlow":
        return self._Cast_MountableComponentPowerFlow(self)
