"""BoltStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3790
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BOLT_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "BoltStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2444
    from mastapy.system_model.analyses_and_results.static_loads import _6834


__docformat__ = "restructuredtext en"
__all__ = ("BoltStabilityAnalysis",)


Self = TypeVar("Self", bound="BoltStabilityAnalysis")


class BoltStabilityAnalysis(_3790.ComponentStabilityAnalysis):
    """BoltStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _BOLT_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BoltStabilityAnalysis")

    class _Cast_BoltStabilityAnalysis:
        """Special nested class for casting BoltStabilityAnalysis to subclasses."""

        def __init__(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis",
            parent: "BoltStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def component_stability_analysis(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis",
        ):
            return self._parent._cast(_3790.ComponentStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3846,
            )

            return self._parent._cast(_3846.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bolt_stability_analysis(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis",
        ) -> "BoltStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BoltStabilityAnalysis.TYPE"):
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
    def cast_to(self: Self) -> "BoltStabilityAnalysis._Cast_BoltStabilityAnalysis":
        return self._Cast_BoltStabilityAnalysis(self)
