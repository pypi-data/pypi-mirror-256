"""CVTPulleyStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3855
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "CVTPulleyStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2589


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleyStabilityAnalysis",)


Self = TypeVar("Self", bound="CVTPulleyStabilityAnalysis")


class CVTPulleyStabilityAnalysis(_3855.PulleyStabilityAnalysis):
    """CVTPulleyStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CVTPulleyStabilityAnalysis")

    class _Cast_CVTPulleyStabilityAnalysis:
        """Special nested class for casting CVTPulleyStabilityAnalysis to subclasses."""

        def __init__(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
            parent: "CVTPulleyStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def pulley_stability_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            return self._parent._cast(_3855.PulleyStabilityAnalysis)

        @property
        def coupling_half_stability_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3803,
            )

            return self._parent._cast(_3803.CouplingHalfStabilityAnalysis)

        @property
        def mountable_component_stability_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3844,
            )

            return self._parent._cast(_3844.MountableComponentStabilityAnalysis)

        @property
        def component_stability_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3790,
            )

            return self._parent._cast(_3790.ComponentStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3846,
            )

            return self._parent._cast(_3846.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cvt_pulley_stability_analysis(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
        ) -> "CVTPulleyStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CVTPulleyStabilityAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2589.CVTPulley":
        """mastapy.system_model.part_model.couplings.CVTPulley

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CVTPulleyStabilityAnalysis._Cast_CVTPulleyStabilityAnalysis":
        return self._Cast_CVTPulleyStabilityAnalysis(self)
