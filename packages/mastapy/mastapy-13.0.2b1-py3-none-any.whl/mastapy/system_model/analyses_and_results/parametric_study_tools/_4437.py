"""UnbalancedMassParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4438
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "UnbalancedMassParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2479
    from mastapy.system_model.analyses_and_results.static_loads import _6983
    from mastapy.system_model.analyses_and_results.system_deflections import _2836


__docformat__ = "restructuredtext en"
__all__ = ("UnbalancedMassParametricStudyTool",)


Self = TypeVar("Self", bound="UnbalancedMassParametricStudyTool")


class UnbalancedMassParametricStudyTool(_4438.VirtualComponentParametricStudyTool):
    """UnbalancedMassParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _UNBALANCED_MASS_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_UnbalancedMassParametricStudyTool")

    class _Cast_UnbalancedMassParametricStudyTool:
        """Special nested class for casting UnbalancedMassParametricStudyTool to subclasses."""

        def __init__(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
            parent: "UnbalancedMassParametricStudyTool",
        ):
            self._parent = parent

        @property
        def virtual_component_parametric_study_tool(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ):
            return self._parent._cast(_4438.VirtualComponentParametricStudyTool)

        @property
        def mountable_component_parametric_study_tool(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4383,
            )

            return self._parent._cast(_4383.MountableComponentParametricStudyTool)

        @property
        def component_parametric_study_tool(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4323,
            )

            return self._parent._cast(_4323.ComponentParametricStudyTool)

        @property
        def part_parametric_study_tool(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4395,
            )

            return self._parent._cast(_4395.PartParametricStudyTool)

        @property
        def part_analysis_case(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def unbalanced_mass_parametric_study_tool(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
        ) -> "UnbalancedMassParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool",
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
        self: Self, instance_to_wrap: "UnbalancedMassParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2479.UnbalancedMass":
        """mastapy.system_model.part_model.UnbalancedMass

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6983.UnbalancedMassLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_system_deflection_results(
        self: Self,
    ) -> "List[_2836.UnbalancedMassSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.UnbalancedMassSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "UnbalancedMassParametricStudyTool._Cast_UnbalancedMassParametricStudyTool":
        return self._Cast_UnbalancedMassParametricStudyTool(self)
