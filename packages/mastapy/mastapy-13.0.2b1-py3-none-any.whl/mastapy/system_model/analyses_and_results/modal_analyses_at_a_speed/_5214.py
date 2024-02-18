"""RootAssemblyModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5126
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "RootAssemblyModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2476
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5196,
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyModalAnalysisAtASpeed",)


Self = TypeVar("Self", bound="RootAssemblyModalAnalysisAtASpeed")


class RootAssemblyModalAnalysisAtASpeed(_5126.AssemblyModalAnalysisAtASpeed):
    """RootAssemblyModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_RootAssemblyModalAnalysisAtASpeed")

    class _Cast_RootAssemblyModalAnalysisAtASpeed:
        """Special nested class for casting RootAssemblyModalAnalysisAtASpeed to subclasses."""

        def __init__(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
            parent: "RootAssemblyModalAnalysisAtASpeed",
        ):
            self._parent = parent

        @property
        def assembly_modal_analysis_at_a_speed(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ):
            return self._parent._cast(_5126.AssemblyModalAnalysisAtASpeed)

        @property
        def abstract_assembly_modal_analysis_at_a_speed(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5119,
            )

            return self._parent._cast(_5119.AbstractAssemblyModalAnalysisAtASpeed)

        @property
        def part_modal_analysis_at_a_speed(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5199,
            )

            return self._parent._cast(_5199.PartModalAnalysisAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def root_assembly_modal_analysis_at_a_speed(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
        ) -> "RootAssemblyModalAnalysisAtASpeed":
            return self._parent

        def __getattr__(
            self: "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed",
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
        self: Self, instance_to_wrap: "RootAssemblyModalAnalysisAtASpeed.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2476.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def modal_analysis_at_a_speed_inputs(self: Self) -> "_5196.ModalAnalysisAtASpeed":
        """mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ModalAnalysisAtASpeed

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ModalAnalysisAtASpeedInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "RootAssemblyModalAnalysisAtASpeed._Cast_RootAssemblyModalAnalysisAtASpeed":
        return self._Cast_RootAssemblyModalAnalysisAtASpeed(self)
