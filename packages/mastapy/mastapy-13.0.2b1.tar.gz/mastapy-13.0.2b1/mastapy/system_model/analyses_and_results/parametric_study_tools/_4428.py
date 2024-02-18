"""StraightBevelSunGearParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4422
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "StraightBevelSunGearParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2552


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearParametricStudyTool",)


Self = TypeVar("Self", bound="StraightBevelSunGearParametricStudyTool")


class StraightBevelSunGearParametricStudyTool(
    _4422.StraightBevelDiffGearParametricStudyTool
):
    """StraightBevelSunGearParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_StraightBevelSunGearParametricStudyTool"
    )

    class _Cast_StraightBevelSunGearParametricStudyTool:
        """Special nested class for casting StraightBevelSunGearParametricStudyTool to subclasses."""

        def __init__(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
            parent: "StraightBevelSunGearParametricStudyTool",
        ):
            self._parent = parent

        @property
        def straight_bevel_diff_gear_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            return self._parent._cast(_4422.StraightBevelDiffGearParametricStudyTool)

        @property
        def bevel_gear_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4315,
            )

            return self._parent._cast(_4315.BevelGearParametricStudyTool)

        @property
        def agma_gleason_conical_gear_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4303,
            )

            return self._parent._cast(_4303.AGMAGleasonConicalGearParametricStudyTool)

        @property
        def conical_gear_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4331,
            )

            return self._parent._cast(_4331.ConicalGearParametricStudyTool)

        @property
        def gear_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4364,
            )

            return self._parent._cast(_4364.GearParametricStudyTool)

        @property
        def mountable_component_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4383,
            )

            return self._parent._cast(_4383.MountableComponentParametricStudyTool)

        @property
        def component_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4323,
            )

            return self._parent._cast(_4323.ComponentParametricStudyTool)

        @property
        def part_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4395,
            )

            return self._parent._cast(_4395.PartParametricStudyTool)

        @property
        def part_analysis_case(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def straight_bevel_sun_gear_parametric_study_tool(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
        ) -> "StraightBevelSunGearParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool",
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
        self: Self, instance_to_wrap: "StraightBevelSunGearParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2552.StraightBevelSunGear":
        """mastapy.system_model.part_model.gears.StraightBevelSunGear

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
    ) -> "StraightBevelSunGearParametricStudyTool._Cast_StraightBevelSunGearParametricStudyTool":
        return self._Cast_StraightBevelSunGearParametricStudyTool(self)
