"""AbstractAssemblyPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4116
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "AbstractAssemblyPowerFlow",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2436


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyPowerFlow",)


Self = TypeVar("Self", bound="AbstractAssemblyPowerFlow")


class AbstractAssemblyPowerFlow(_4116.PartPowerFlow):
    """AbstractAssemblyPowerFlow

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_ASSEMBLY_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_AbstractAssemblyPowerFlow")

    class _Cast_AbstractAssemblyPowerFlow:
        """Special nested class for casting AbstractAssemblyPowerFlow to subclasses."""

        def __init__(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
            parent: "AbstractAssemblyPowerFlow",
        ):
            self._parent = parent

        @property
        def part_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            return self._parent._cast(_4116.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4040

            return self._parent._cast(_4040.AGMAGleasonConicalGearSetPowerFlow)

        @property
        def assembly_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4041

            return self._parent._cast(_4041.AssemblyPowerFlow)

        @property
        def belt_drive_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4044

            return self._parent._cast(_4044.BeltDrivePowerFlow)

        @property
        def bevel_differential_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4047

            return self._parent._cast(_4047.BevelDifferentialGearSetPowerFlow)

        @property
        def bevel_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4052

            return self._parent._cast(_4052.BevelGearSetPowerFlow)

        @property
        def bolted_joint_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4053

            return self._parent._cast(_4053.BoltedJointPowerFlow)

        @property
        def clutch_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4057

            return self._parent._cast(_4057.ClutchPowerFlow)

        @property
        def concept_coupling_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4062

            return self._parent._cast(_4062.ConceptCouplingPowerFlow)

        @property
        def concept_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4065

            return self._parent._cast(_4065.ConceptGearSetPowerFlow)

        @property
        def conical_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4068

            return self._parent._cast(_4068.ConicalGearSetPowerFlow)

        @property
        def coupling_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4073

            return self._parent._cast(_4073.CouplingPowerFlow)

        @property
        def cvt_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4075

            return self._parent._cast(_4075.CVTPowerFlow)

        @property
        def cycloidal_assembly_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4077

            return self._parent._cast(_4077.CycloidalAssemblyPowerFlow)

        @property
        def cylindrical_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4084

            return self._parent._cast(_4084.CylindricalGearSetPowerFlow)

        @property
        def face_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4090

            return self._parent._cast(_4090.FaceGearSetPowerFlow)

        @property
        def flexible_pin_assembly_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4094

            return self._parent._cast(_4094.FlexiblePinAssemblyPowerFlow)

        @property
        def gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4097

            return self._parent._cast(_4097.GearSetPowerFlow)

        @property
        def hypoid_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4101

            return self._parent._cast(_4101.HypoidGearSetPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4105

            return self._parent._cast(
                _4105.KlingelnbergCycloPalloidConicalGearSetPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4108

            return self._parent._cast(
                _4108.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4111

            return self._parent._cast(
                _4111.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
            )

        @property
        def part_to_part_shear_coupling_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4119

            return self._parent._cast(_4119.PartToPartShearCouplingPowerFlow)

        @property
        def planetary_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4121

            return self._parent._cast(_4121.PlanetaryGearSetPowerFlow)

        @property
        def rolling_ring_assembly_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4130

            return self._parent._cast(_4130.RollingRingAssemblyPowerFlow)

        @property
        def root_assembly_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4133

            return self._parent._cast(_4133.RootAssemblyPowerFlow)

        @property
        def specialised_assembly_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4137

            return self._parent._cast(_4137.SpecialisedAssemblyPowerFlow)

        @property
        def spiral_bevel_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4140

            return self._parent._cast(_4140.SpiralBevelGearSetPowerFlow)

        @property
        def spring_damper_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4143

            return self._parent._cast(_4143.SpringDamperPowerFlow)

        @property
        def straight_bevel_diff_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4146

            return self._parent._cast(_4146.StraightBevelDiffGearSetPowerFlow)

        @property
        def straight_bevel_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4149

            return self._parent._cast(_4149.StraightBevelGearSetPowerFlow)

        @property
        def synchroniser_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4154

            return self._parent._cast(_4154.SynchroniserPowerFlow)

        @property
        def torque_converter_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4158

            return self._parent._cast(_4158.TorqueConverterPowerFlow)

        @property
        def worm_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4165

            return self._parent._cast(_4165.WormGearSetPowerFlow)

        @property
        def zerol_bevel_gear_set_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ):
            from mastapy.system_model.analyses_and_results.power_flows import _4168

            return self._parent._cast(_4168.ZerolBevelGearSetPowerFlow)

        @property
        def abstract_assembly_power_flow(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow",
        ) -> "AbstractAssemblyPowerFlow":
            return self._parent

        def __getattr__(
            self: "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "AbstractAssemblyPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2436.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: Self) -> "_2436.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow":
        return self._Cast_AbstractAssemblyPowerFlow(self)
