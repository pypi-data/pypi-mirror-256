"""CouplingConnectionParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4370
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "CouplingConnectionParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.couplings import _2348


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionParametricStudyTool",)


Self = TypeVar("Self", bound="CouplingConnectionParametricStudyTool")


class CouplingConnectionParametricStudyTool(
    _4370.InterMountableComponentConnectionParametricStudyTool
):
    """CouplingConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _COUPLING_CONNECTION_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CouplingConnectionParametricStudyTool"
    )

    class _Cast_CouplingConnectionParametricStudyTool:
        """Special nested class for casting CouplingConnectionParametricStudyTool to subclasses."""

        def __init__(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
            parent: "CouplingConnectionParametricStudyTool",
        ):
            self._parent = parent

        @property
        def inter_mountable_component_connection_parametric_study_tool(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            return self._parent._cast(
                _4370.InterMountableComponentConnectionParametricStudyTool
            )

        @property
        def connection_parametric_study_tool(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4333,
            )

            return self._parent._cast(_4333.ConnectionParametricStudyTool)

        @property
        def connection_analysis_case(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_connection_parametric_study_tool(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4319,
            )

            return self._parent._cast(_4319.ClutchConnectionParametricStudyTool)

        @property
        def concept_coupling_connection_parametric_study_tool(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4324,
            )

            return self._parent._cast(
                _4324.ConceptCouplingConnectionParametricStudyTool
            )

        @property
        def part_to_part_shear_coupling_connection_parametric_study_tool(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4396,
            )

            return self._parent._cast(
                _4396.PartToPartShearCouplingConnectionParametricStudyTool
            )

        @property
        def spring_damper_connection_parametric_study_tool(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4418,
            )

            return self._parent._cast(_4418.SpringDamperConnectionParametricStudyTool)

        @property
        def torque_converter_connection_parametric_study_tool(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4433,
            )

            return self._parent._cast(
                _4433.TorqueConverterConnectionParametricStudyTool
            )

        @property
        def coupling_connection_parametric_study_tool(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
        ) -> "CouplingConnectionParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool",
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
        self: Self, instance_to_wrap: "CouplingConnectionParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2348.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CouplingConnectionParametricStudyTool._Cast_CouplingConnectionParametricStudyTool":
        return self._Cast_CouplingConnectionParametricStudyTool(self)
