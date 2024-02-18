"""SpecialisedAssemblyParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4298
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "SpecialisedAssemblyParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2478


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyParametricStudyTool",)


Self = TypeVar("Self", bound="SpecialisedAssemblyParametricStudyTool")


class SpecialisedAssemblyParametricStudyTool(_4298.AbstractAssemblyParametricStudyTool):
    """SpecialisedAssemblyParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _SPECIALISED_ASSEMBLY_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_SpecialisedAssemblyParametricStudyTool"
    )

    class _Cast_SpecialisedAssemblyParametricStudyTool:
        """Special nested class for casting SpecialisedAssemblyParametricStudyTool to subclasses."""

        def __init__(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
            parent: "SpecialisedAssemblyParametricStudyTool",
        ):
            self._parent = parent

        @property
        def abstract_assembly_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            return self._parent._cast(_4298.AbstractAssemblyParametricStudyTool)

        @property
        def part_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4395,
            )

            return self._parent._cast(_4395.PartParametricStudyTool)

        @property
        def part_analysis_case(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4304,
            )

            return self._parent._cast(
                _4304.AGMAGleasonConicalGearSetParametricStudyTool
            )

        @property
        def belt_drive_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4308,
            )

            return self._parent._cast(_4308.BeltDriveParametricStudyTool)

        @property
        def bevel_differential_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4311,
            )

            return self._parent._cast(_4311.BevelDifferentialGearSetParametricStudyTool)

        @property
        def bevel_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4316,
            )

            return self._parent._cast(_4316.BevelGearSetParametricStudyTool)

        @property
        def bolted_joint_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4317,
            )

            return self._parent._cast(_4317.BoltedJointParametricStudyTool)

        @property
        def clutch_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4321,
            )

            return self._parent._cast(_4321.ClutchParametricStudyTool)

        @property
        def concept_coupling_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4326,
            )

            return self._parent._cast(_4326.ConceptCouplingParametricStudyTool)

        @property
        def concept_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4329,
            )

            return self._parent._cast(_4329.ConceptGearSetParametricStudyTool)

        @property
        def conical_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4332,
            )

            return self._parent._cast(_4332.ConicalGearSetParametricStudyTool)

        @property
        def coupling_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4337,
            )

            return self._parent._cast(_4337.CouplingParametricStudyTool)

        @property
        def cvt_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4339,
            )

            return self._parent._cast(_4339.CVTParametricStudyTool)

        @property
        def cycloidal_assembly_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4341,
            )

            return self._parent._cast(_4341.CycloidalAssemblyParametricStudyTool)

        @property
        def cylindrical_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4347,
            )

            return self._parent._cast(_4347.CylindricalGearSetParametricStudyTool)

        @property
        def face_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4360,
            )

            return self._parent._cast(_4360.FaceGearSetParametricStudyTool)

        @property
        def flexible_pin_assembly_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4362,
            )

            return self._parent._cast(_4362.FlexiblePinAssemblyParametricStudyTool)

        @property
        def gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4365,
            )

            return self._parent._cast(_4365.GearSetParametricStudyTool)

        @property
        def hypoid_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4369,
            )

            return self._parent._cast(_4369.HypoidGearSetParametricStudyTool)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4373,
            )

            return self._parent._cast(
                _4373.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4376,
            )

            return self._parent._cast(
                _4376.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4379,
            )

            return self._parent._cast(
                _4379.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
            )

        @property
        def part_to_part_shear_coupling_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4398,
            )

            return self._parent._cast(_4398.PartToPartShearCouplingParametricStudyTool)

        @property
        def planetary_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4400,
            )

            return self._parent._cast(_4400.PlanetaryGearSetParametricStudyTool)

        @property
        def rolling_ring_assembly_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4407,
            )

            return self._parent._cast(_4407.RollingRingAssemblyParametricStudyTool)

        @property
        def spiral_bevel_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4417,
            )

            return self._parent._cast(_4417.SpiralBevelGearSetParametricStudyTool)

        @property
        def spring_damper_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4420,
            )

            return self._parent._cast(_4420.SpringDamperParametricStudyTool)

        @property
        def straight_bevel_diff_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4423,
            )

            return self._parent._cast(_4423.StraightBevelDiffGearSetParametricStudyTool)

        @property
        def straight_bevel_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4426,
            )

            return self._parent._cast(_4426.StraightBevelGearSetParametricStudyTool)

        @property
        def synchroniser_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4430,
            )

            return self._parent._cast(_4430.SynchroniserParametricStudyTool)

        @property
        def torque_converter_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4434,
            )

            return self._parent._cast(_4434.TorqueConverterParametricStudyTool)

        @property
        def worm_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4441,
            )

            return self._parent._cast(_4441.WormGearSetParametricStudyTool)

        @property
        def zerol_bevel_gear_set_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4444,
            )

            return self._parent._cast(_4444.ZerolBevelGearSetParametricStudyTool)

        @property
        def specialised_assembly_parametric_study_tool(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
        ) -> "SpecialisedAssemblyParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool",
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
        self: Self, instance_to_wrap: "SpecialisedAssemblyParametricStudyTool.TYPE"
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
    ) -> "SpecialisedAssemblyParametricStudyTool._Cast_SpecialisedAssemblyParametricStudyTool":
        return self._Cast_SpecialisedAssemblyParametricStudyTool(self)
