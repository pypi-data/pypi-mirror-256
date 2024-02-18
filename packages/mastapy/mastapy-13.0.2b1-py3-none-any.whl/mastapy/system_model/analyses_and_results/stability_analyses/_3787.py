"""ClutchHalfStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3803
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "ClutchHalfStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2581
    from mastapy.system_model.analyses_and_results.static_loads import _6836


__docformat__ = "restructuredtext en"
__all__ = ("ClutchHalfStabilityAnalysis",)


Self = TypeVar("Self", bound="ClutchHalfStabilityAnalysis")


class ClutchHalfStabilityAnalysis(_3803.CouplingHalfStabilityAnalysis):
    """ClutchHalfStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_HALF_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ClutchHalfStabilityAnalysis")

    class _Cast_ClutchHalfStabilityAnalysis:
        """Special nested class for casting ClutchHalfStabilityAnalysis to subclasses."""

        def __init__(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
            parent: "ClutchHalfStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_half_stability_analysis(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            return self._parent._cast(_3803.CouplingHalfStabilityAnalysis)

        @property
        def mountable_component_stability_analysis(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3844,
            )

            return self._parent._cast(_3844.MountableComponentStabilityAnalysis)

        @property
        def component_stability_analysis(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3790,
            )

            return self._parent._cast(_3790.ComponentStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3846,
            )

            return self._parent._cast(_3846.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_half_stability_analysis(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
        ) -> "ClutchHalfStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ClutchHalfStabilityAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2581.ClutchHalf":
        """mastapy.system_model.part_model.couplings.ClutchHalf

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6836.ClutchHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase

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
    ) -> "ClutchHalfStabilityAnalysis._Cast_ClutchHalfStabilityAnalysis":
        return self._Cast_ClutchHalfStabilityAnalysis(self)
