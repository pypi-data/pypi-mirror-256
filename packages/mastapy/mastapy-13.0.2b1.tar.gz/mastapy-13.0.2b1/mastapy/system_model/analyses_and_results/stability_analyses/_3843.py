"""MeasurementComponentStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3892
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "MeasurementComponentStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2465
    from mastapy.system_model.analyses_and_results.static_loads import _6925


__docformat__ = "restructuredtext en"
__all__ = ("MeasurementComponentStabilityAnalysis",)


Self = TypeVar("Self", bound="MeasurementComponentStabilityAnalysis")


class MeasurementComponentStabilityAnalysis(_3892.VirtualComponentStabilityAnalysis):
    """MeasurementComponentStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _MEASUREMENT_COMPONENT_STABILITY_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_MeasurementComponentStabilityAnalysis"
    )

    class _Cast_MeasurementComponentStabilityAnalysis:
        """Special nested class for casting MeasurementComponentStabilityAnalysis to subclasses."""

        def __init__(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
            parent: "MeasurementComponentStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def virtual_component_stability_analysis(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            return self._parent._cast(_3892.VirtualComponentStabilityAnalysis)

        @property
        def mountable_component_stability_analysis(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3844,
            )

            return self._parent._cast(_3844.MountableComponentStabilityAnalysis)

        @property
        def component_stability_analysis(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3790,
            )

            return self._parent._cast(_3790.ComponentStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3846,
            )

            return self._parent._cast(_3846.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def measurement_component_stability_analysis(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
        ) -> "MeasurementComponentStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis",
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
        self: Self, instance_to_wrap: "MeasurementComponentStabilityAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2465.MeasurementComponent":
        """mastapy.system_model.part_model.MeasurementComponent

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6925.MeasurementComponentLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase

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
    ) -> "MeasurementComponentStabilityAnalysis._Cast_MeasurementComponentStabilityAnalysis":
        return self._Cast_MeasurementComponentStabilityAnalysis(self)
