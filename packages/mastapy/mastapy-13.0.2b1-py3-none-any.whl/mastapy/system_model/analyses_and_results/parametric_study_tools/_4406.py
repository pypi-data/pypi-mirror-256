"""RingPinsToDiscConnectionParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4370
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "RingPinsToDiscConnectionParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.cycloidal import _2343
    from mastapy.system_model.analyses_and_results.static_loads import _6947
    from mastapy.system_model.analyses_and_results.system_deflections import _2797


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsToDiscConnectionParametricStudyTool",)


Self = TypeVar("Self", bound="RingPinsToDiscConnectionParametricStudyTool")


class RingPinsToDiscConnectionParametricStudyTool(
    _4370.InterMountableComponentConnectionParametricStudyTool
):
    """RingPinsToDiscConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _RING_PINS_TO_DISC_CONNECTION_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_RingPinsToDiscConnectionParametricStudyTool"
    )

    class _Cast_RingPinsToDiscConnectionParametricStudyTool:
        """Special nested class for casting RingPinsToDiscConnectionParametricStudyTool to subclasses."""

        def __init__(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
            parent: "RingPinsToDiscConnectionParametricStudyTool",
        ):
            self._parent = parent

        @property
        def inter_mountable_component_connection_parametric_study_tool(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
        ):
            return self._parent._cast(
                _4370.InterMountableComponentConnectionParametricStudyTool
            )

        @property
        def connection_parametric_study_tool(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4333,
            )

            return self._parent._cast(_4333.ConnectionParametricStudyTool)

        @property
        def connection_analysis_case(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def ring_pins_to_disc_connection_parametric_study_tool(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
        ) -> "RingPinsToDiscConnectionParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool",
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
        self: Self, instance_to_wrap: "RingPinsToDiscConnectionParametricStudyTool.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2343.RingPinsToDiscConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: Self) -> "_6947.RingPinsToDiscConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase

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
    ) -> "List[_2797.RingPinsToDiscConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.RingPinsToDiscConnectionSystemDeflection]

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
    ) -> "RingPinsToDiscConnectionParametricStudyTool._Cast_RingPinsToDiscConnectionParametricStudyTool":
        return self._Cast_RingPinsToDiscConnectionParametricStudyTool(self)
