"""ConceptGearSetParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4365
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ConceptGearSetParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2524
    from mastapy.system_model.analyses_and_results.static_loads import _6846
    from mastapy.system_model.analyses_and_results.system_deflections import _2723
    from mastapy.system_model.analyses_and_results.parametric_study_tools import (
        _4328,
        _4327,
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearSetParametricStudyTool",)


Self = TypeVar("Self", bound="ConceptGearSetParametricStudyTool")


class ConceptGearSetParametricStudyTool(_4365.GearSetParametricStudyTool):
    """ConceptGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_SET_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ConceptGearSetParametricStudyTool")

    class _Cast_ConceptGearSetParametricStudyTool:
        """Special nested class for casting ConceptGearSetParametricStudyTool to subclasses."""

        def __init__(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
            parent: "ConceptGearSetParametricStudyTool",
        ):
            self._parent = parent

        @property
        def gear_set_parametric_study_tool(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ):
            return self._parent._cast(_4365.GearSetParametricStudyTool)

        @property
        def specialised_assembly_parametric_study_tool(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4414,
            )

            return self._parent._cast(_4414.SpecialisedAssemblyParametricStudyTool)

        @property
        def abstract_assembly_parametric_study_tool(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4298,
            )

            return self._parent._cast(_4298.AbstractAssemblyParametricStudyTool)

        @property
        def part_parametric_study_tool(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4395,
            )

            return self._parent._cast(_4395.PartParametricStudyTool)

        @property
        def part_analysis_case(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def concept_gear_set_parametric_study_tool(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
        ) -> "ConceptGearSetParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool",
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
        self: Self, instance_to_wrap: "ConceptGearSetParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2524.ConceptGearSet":
        """mastapy.system_model.part_model.gears.ConceptGearSet

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6846.ConceptGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_system_deflection_results(
        self: Self,
    ) -> "List[_2723.ConceptGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConceptGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_gears_parametric_study_tool(
        self: Self,
    ) -> "List[_4328.ConceptGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConceptGearsParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_meshes_parametric_study_tool(
        self: Self,
    ) -> "List[_4327.ConceptGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConceptMeshesParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "ConceptGearSetParametricStudyTool._Cast_ConceptGearSetParametricStudyTool":
        return self._Cast_ConceptGearSetParametricStudyTool(self)
