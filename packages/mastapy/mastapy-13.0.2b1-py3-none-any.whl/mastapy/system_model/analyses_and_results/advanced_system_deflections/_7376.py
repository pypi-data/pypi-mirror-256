"""SpecialisedAssemblyAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7272
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "SpecialisedAssemblyAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2478


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyAdvancedSystemDeflection",)


Self = TypeVar("Self", bound="SpecialisedAssemblyAdvancedSystemDeflection")


class SpecialisedAssemblyAdvancedSystemDeflection(
    _7272.AbstractAssemblyAdvancedSystemDeflection
):
    """SpecialisedAssemblyAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _SPECIALISED_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_SpecialisedAssemblyAdvancedSystemDeflection"
    )

    class _Cast_SpecialisedAssemblyAdvancedSystemDeflection:
        """Special nested class for casting SpecialisedAssemblyAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
            parent: "SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def abstract_assembly_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            return self._parent._cast(_7272.AbstractAssemblyAdvancedSystemDeflection)

        @property
        def part_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7357,
            )

            return self._parent._cast(_7357.PartAdvancedSystemDeflection)

        @property
        def part_static_load_analysis_case(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7281,
            )

            return self._parent._cast(
                _7281.AGMAGleasonConicalGearSetAdvancedSystemDeflection
            )

        @property
        def belt_drive_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7285,
            )

            return self._parent._cast(_7285.BeltDriveAdvancedSystemDeflection)

        @property
        def bevel_differential_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7288,
            )

            return self._parent._cast(
                _7288.BevelDifferentialGearSetAdvancedSystemDeflection
            )

        @property
        def bevel_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7293,
            )

            return self._parent._cast(_7293.BevelGearSetAdvancedSystemDeflection)

        @property
        def bolted_joint_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7295,
            )

            return self._parent._cast(_7295.BoltedJointAdvancedSystemDeflection)

        @property
        def clutch_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7296,
            )

            return self._parent._cast(_7296.ClutchAdvancedSystemDeflection)

        @property
        def concept_coupling_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7301,
            )

            return self._parent._cast(_7301.ConceptCouplingAdvancedSystemDeflection)

        @property
        def concept_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7306,
            )

            return self._parent._cast(_7306.ConceptGearSetAdvancedSystemDeflection)

        @property
        def conical_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7309,
            )

            return self._parent._cast(_7309.ConicalGearSetAdvancedSystemDeflection)

        @property
        def coupling_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7313,
            )

            return self._parent._cast(_7313.CouplingAdvancedSystemDeflection)

        @property
        def cvt_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7316,
            )

            return self._parent._cast(_7316.CVTAdvancedSystemDeflection)

        @property
        def cycloidal_assembly_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7319,
            )

            return self._parent._cast(_7319.CycloidalAssemblyAdvancedSystemDeflection)

        @property
        def cylindrical_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7325,
            )

            return self._parent._cast(_7325.CylindricalGearSetAdvancedSystemDeflection)

        @property
        def face_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7332,
            )

            return self._parent._cast(_7332.FaceGearSetAdvancedSystemDeflection)

        @property
        def flexible_pin_assembly_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7334,
            )

            return self._parent._cast(_7334.FlexiblePinAssemblyAdvancedSystemDeflection)

        @property
        def gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7337,
            )

            return self._parent._cast(_7337.GearSetAdvancedSystemDeflection)

        @property
        def hypoid_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7341,
            )

            return self._parent._cast(_7341.HypoidGearSetAdvancedSystemDeflection)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7345,
            )

            return self._parent._cast(
                _7345.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7348,
            )

            return self._parent._cast(
                _7348.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7351,
            )

            return self._parent._cast(
                _7351.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
            )

        @property
        def part_to_part_shear_coupling_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7358,
            )

            return self._parent._cast(
                _7358.PartToPartShearCouplingAdvancedSystemDeflection
            )

        @property
        def planetary_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7362,
            )

            return self._parent._cast(_7362.PlanetaryGearSetAdvancedSystemDeflection)

        @property
        def rolling_ring_assembly_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7370,
            )

            return self._parent._cast(_7370.RollingRingAssemblyAdvancedSystemDeflection)

        @property
        def spiral_bevel_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7379,
            )

            return self._parent._cast(_7379.SpiralBevelGearSetAdvancedSystemDeflection)

        @property
        def spring_damper_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7380,
            )

            return self._parent._cast(_7380.SpringDamperAdvancedSystemDeflection)

        @property
        def straight_bevel_diff_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7385,
            )

            return self._parent._cast(
                _7385.StraightBevelDiffGearSetAdvancedSystemDeflection
            )

        @property
        def straight_bevel_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7388,
            )

            return self._parent._cast(
                _7388.StraightBevelGearSetAdvancedSystemDeflection
            )

        @property
        def synchroniser_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7391,
            )

            return self._parent._cast(_7391.SynchroniserAdvancedSystemDeflection)

        @property
        def torque_converter_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7395,
            )

            return self._parent._cast(_7395.TorqueConverterAdvancedSystemDeflection)

        @property
        def worm_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7404,
            )

            return self._parent._cast(_7404.WormGearSetAdvancedSystemDeflection)

        @property
        def zerol_bevel_gear_set_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7407,
            )

            return self._parent._cast(_7407.ZerolBevelGearSetAdvancedSystemDeflection)

        @property
        def specialised_assembly_advanced_system_deflection(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
        ) -> "SpecialisedAssemblyAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection",
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
        self: Self, instance_to_wrap: "SpecialisedAssemblyAdvancedSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2478.SpecialisedAssembly":
        """mastapy.system_model.part_model.SpecialisedAssembly

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
    ) -> "SpecialisedAssemblyAdvancedSystemDeflection._Cast_SpecialisedAssemblyAdvancedSystemDeflection":
        return self._Cast_SpecialisedAssemblyAdvancedSystemDeflection(self)
