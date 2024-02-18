"""VirtualComponentCompoundParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4522,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "VirtualComponentCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.parametric_study_tools import _4438


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundParametricStudyTool",)


Self = TypeVar("Self", bound="VirtualComponentCompoundParametricStudyTool")


class VirtualComponentCompoundParametricStudyTool(
    _4522.MountableComponentCompoundParametricStudyTool
):
    """VirtualComponentCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_VirtualComponentCompoundParametricStudyTool"
    )

    class _Cast_VirtualComponentCompoundParametricStudyTool:
        """Special nested class for casting VirtualComponentCompoundParametricStudyTool to subclasses."""

        def __init__(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
            parent: "VirtualComponentCompoundParametricStudyTool",
        ):
            self._parent = parent

        @property
        def mountable_component_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            return self._parent._cast(
                _4522.MountableComponentCompoundParametricStudyTool
            )

        @property
        def component_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4470,
            )

            return self._parent._cast(_4470.ComponentCompoundParametricStudyTool)

        @property
        def part_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4524,
            )

            return self._parent._cast(_4524.PartCompoundParametricStudyTool)

        @property
        def part_compound_analysis(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def mass_disc_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4520,
            )

            return self._parent._cast(_4520.MassDiscCompoundParametricStudyTool)

        @property
        def measurement_component_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4521,
            )

            return self._parent._cast(
                _4521.MeasurementComponentCompoundParametricStudyTool
            )

        @property
        def point_load_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4531,
            )

            return self._parent._cast(_4531.PointLoadCompoundParametricStudyTool)

        @property
        def power_load_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4532,
            )

            return self._parent._cast(_4532.PowerLoadCompoundParametricStudyTool)

        @property
        def unbalanced_mass_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4566,
            )

            return self._parent._cast(_4566.UnbalancedMassCompoundParametricStudyTool)

        @property
        def virtual_component_compound_parametric_study_tool(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
        ) -> "VirtualComponentCompoundParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
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
        self: Self, instance_to_wrap: "VirtualComponentCompoundParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_4438.VirtualComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_4438.VirtualComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool":
        return self._Cast_VirtualComponentCompoundParametricStudyTool(self)
