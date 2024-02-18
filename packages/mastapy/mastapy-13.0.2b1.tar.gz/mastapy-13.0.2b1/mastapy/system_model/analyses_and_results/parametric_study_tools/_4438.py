"""VirtualComponentParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4383
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "VirtualComponentParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2481


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentParametricStudyTool",)


Self = TypeVar("Self", bound="VirtualComponentParametricStudyTool")


class VirtualComponentParametricStudyTool(_4383.MountableComponentParametricStudyTool):
    """VirtualComponentParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_COMPONENT_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_VirtualComponentParametricStudyTool")

    class _Cast_VirtualComponentParametricStudyTool:
        """Special nested class for casting VirtualComponentParametricStudyTool to subclasses."""

        def __init__(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
            parent: "VirtualComponentParametricStudyTool",
        ):
            self._parent = parent

        @property
        def mountable_component_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            return self._parent._cast(_4383.MountableComponentParametricStudyTool)

        @property
        def component_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4323,
            )

            return self._parent._cast(_4323.ComponentParametricStudyTool)

        @property
        def part_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4395,
            )

            return self._parent._cast(_4395.PartParametricStudyTool)

        @property
        def part_analysis_case(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def mass_disc_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4380,
            )

            return self._parent._cast(_4380.MassDiscParametricStudyTool)

        @property
        def measurement_component_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4381,
            )

            return self._parent._cast(_4381.MeasurementComponentParametricStudyTool)

        @property
        def point_load_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4402,
            )

            return self._parent._cast(_4402.PointLoadParametricStudyTool)

        @property
        def power_load_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4403,
            )

            return self._parent._cast(_4403.PowerLoadParametricStudyTool)

        @property
        def unbalanced_mass_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4437,
            )

            return self._parent._cast(_4437.UnbalancedMassParametricStudyTool)

        @property
        def virtual_component_parametric_study_tool(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
        ) -> "VirtualComponentParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool",
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
        self: Self, instance_to_wrap: "VirtualComponentParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2481.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

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
    ) -> (
        "VirtualComponentParametricStudyTool._Cast_VirtualComponentParametricStudyTool"
    ):
        return self._Cast_VirtualComponentParametricStudyTool(self)
