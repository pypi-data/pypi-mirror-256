"""PointLoadModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _4983,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "PointLoadModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2473
    from mastapy.system_model.analyses_and_results.static_loads import _6941


__docformat__ = "restructuredtext en"
__all__ = ("PointLoadModalAnalysisAtAStiffness",)


Self = TypeVar("Self", bound="PointLoadModalAnalysisAtAStiffness")


class PointLoadModalAnalysisAtAStiffness(
    _4983.VirtualComponentModalAnalysisAtAStiffness
):
    """PointLoadModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_MODAL_ANALYSIS_AT_A_STIFFNESS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PointLoadModalAnalysisAtAStiffness")

    class _Cast_PointLoadModalAnalysisAtAStiffness:
        """Special nested class for casting PointLoadModalAnalysisAtAStiffness to subclasses."""

        def __init__(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
            parent: "PointLoadModalAnalysisAtAStiffness",
        ):
            self._parent = parent

        @property
        def virtual_component_modal_analysis_at_a_stiffness(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            return self._parent._cast(_4983.VirtualComponentModalAnalysisAtAStiffness)

        @property
        def mountable_component_modal_analysis_at_a_stiffness(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4938,
            )

            return self._parent._cast(_4938.MountableComponentModalAnalysisAtAStiffness)

        @property
        def component_modal_analysis_at_a_stiffness(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4884,
            )

            return self._parent._cast(_4884.ComponentModalAnalysisAtAStiffness)

        @property
        def part_modal_analysis_at_a_stiffness(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4940,
            )

            return self._parent._cast(_4940.PartModalAnalysisAtAStiffness)

        @property
        def part_static_load_analysis_case(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def point_load_modal_analysis_at_a_stiffness(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
        ) -> "PointLoadModalAnalysisAtAStiffness":
            return self._parent

        def __getattr__(
            self: "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness",
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
        self: Self, instance_to_wrap: "PointLoadModalAnalysisAtAStiffness.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2473.PointLoad":
        """mastapy.system_model.part_model.PointLoad

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6941.PointLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase

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
    ) -> "PointLoadModalAnalysisAtAStiffness._Cast_PointLoadModalAnalysisAtAStiffness":
        return self._Cast_PointLoadModalAnalysisAtAStiffness(self)
