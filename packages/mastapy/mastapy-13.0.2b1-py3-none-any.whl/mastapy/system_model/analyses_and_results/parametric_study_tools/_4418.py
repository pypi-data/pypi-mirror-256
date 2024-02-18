"""SpringDamperConnectionParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4335
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "SpringDamperConnectionParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.couplings import _2352
    from mastapy.system_model.analyses_and_results.static_loads import _6959
    from mastapy.system_model.analyses_and_results.system_deflections import _2812


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperConnectionParametricStudyTool",)


Self = TypeVar("Self", bound="SpringDamperConnectionParametricStudyTool")


class SpringDamperConnectionParametricStudyTool(
    _4335.CouplingConnectionParametricStudyTool
):
    """SpringDamperConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_CONNECTION_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_SpringDamperConnectionParametricStudyTool"
    )

    class _Cast_SpringDamperConnectionParametricStudyTool:
        """Special nested class for casting SpringDamperConnectionParametricStudyTool to subclasses."""

        def __init__(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
            parent: "SpringDamperConnectionParametricStudyTool",
        ):
            self._parent = parent

        @property
        def coupling_connection_parametric_study_tool(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
        ):
            return self._parent._cast(_4335.CouplingConnectionParametricStudyTool)

        @property
        def inter_mountable_component_connection_parametric_study_tool(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4370,
            )

            return self._parent._cast(
                _4370.InterMountableComponentConnectionParametricStudyTool
            )

        @property
        def connection_parametric_study_tool(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4333,
            )

            return self._parent._cast(_4333.ConnectionParametricStudyTool)

        @property
        def connection_analysis_case(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def spring_damper_connection_parametric_study_tool(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
        ) -> "SpringDamperConnectionParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool",
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
        self: Self, instance_to_wrap: "SpringDamperConnectionParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2352.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: Self) -> "_6959.SpringDamperConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_system_deflection_results(
        self: Self,
    ) -> "List[_2812.SpringDamperConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.SpringDamperConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "SpringDamperConnectionParametricStudyTool._Cast_SpringDamperConnectionParametricStudyTool":
        return self._Cast_SpringDamperConnectionParametricStudyTool(self)
