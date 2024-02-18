"""BoltModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5144
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BOLT_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "BoltModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2444
    from mastapy.system_model.analyses_and_results.static_loads import _6834


__docformat__ = "restructuredtext en"
__all__ = ("BoltModalAnalysisAtASpeed",)


Self = TypeVar("Self", bound="BoltModalAnalysisAtASpeed")


class BoltModalAnalysisAtASpeed(_5144.ComponentModalAnalysisAtASpeed):
    """BoltModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _BOLT_MODAL_ANALYSIS_AT_A_SPEED
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BoltModalAnalysisAtASpeed")

    class _Cast_BoltModalAnalysisAtASpeed:
        """Special nested class for casting BoltModalAnalysisAtASpeed to subclasses."""

        def __init__(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
            parent: "BoltModalAnalysisAtASpeed",
        ):
            self._parent = parent

        @property
        def component_modal_analysis_at_a_speed(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
        ):
            return self._parent._cast(_5144.ComponentModalAnalysisAtASpeed)

        @property
        def part_modal_analysis_at_a_speed(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5199,
            )

            return self._parent._cast(_5199.PartModalAnalysisAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bolt_modal_analysis_at_a_speed(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed",
        ) -> "BoltModalAnalysisAtASpeed":
            return self._parent

        def __getattr__(
            self: "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BoltModalAnalysisAtASpeed.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2444.Bolt":
        """mastapy.system_model.part_model.Bolt

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6834.BoltLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "BoltModalAnalysisAtASpeed._Cast_BoltModalAnalysisAtASpeed":
        return self._Cast_BoltModalAnalysisAtASpeed(self)
