"""DynamicAnalysis"""

from __future__ import annotations

from typing import TypeVar

from mastapy.system_model.analyses_and_results.analysis_cases import _7546
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses", "DynamicAnalysis"
)


__docformat__ = "restructuredtext en"
__all__ = ("DynamicAnalysis",)


Self = TypeVar("Self", bound="DynamicAnalysis")


class DynamicAnalysis(_7546.FEAnalysis):
    """DynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _DYNAMIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_DynamicAnalysis")

    class _Cast_DynamicAnalysis:
        """Special nested class for casting DynamicAnalysis to subclasses."""

        def __init__(
            self: "DynamicAnalysis._Cast_DynamicAnalysis", parent: "DynamicAnalysis"
        ):
            self._parent = parent

        @property
        def fe_analysis(self: "DynamicAnalysis._Cast_DynamicAnalysis"):
            return self._parent._cast(_7546.FEAnalysis)

        @property
        def static_load_analysis_case(self: "DynamicAnalysis._Cast_DynamicAnalysis"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7552

            return self._parent._cast(_7552.StaticLoadAnalysisCase)

        @property
        def analysis_case(self: "DynamicAnalysis._Cast_DynamicAnalysis"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7537

            return self._parent._cast(_7537.AnalysisCase)

        @property
        def context(self: "DynamicAnalysis._Cast_DynamicAnalysis"):
            from mastapy.system_model.analyses_and_results import _2652

            return self._parent._cast(_2652.Context)

        @property
        def dynamic_model_for_steady_state_synchronous_response(
            self: "DynamicAnalysis._Cast_DynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3037,
            )

            return self._parent._cast(
                _3037.DynamicModelForSteadyStateSynchronousResponse
            )

        @property
        def dynamic_model_for_stability_analysis(
            self: "DynamicAnalysis._Cast_DynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3818,
            )

            return self._parent._cast(_3818.DynamicModelForStabilityAnalysis)

        @property
        def dynamic_model_for_modal_analysis(
            self: "DynamicAnalysis._Cast_DynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4627

            return self._parent._cast(_4627.DynamicModelForModalAnalysis)

        @property
        def dynamic_model_at_a_stiffness(self: "DynamicAnalysis._Cast_DynamicAnalysis"):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4911,
            )

            return self._parent._cast(_4911.DynamicModelAtAStiffness)

        @property
        def dynamic_model_for_harmonic_analysis(
            self: "DynamicAnalysis._Cast_DynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5734,
            )

            return self._parent._cast(_5734.DynamicModelForHarmonicAnalysis)

        @property
        def dynamic_analysis(
            self: "DynamicAnalysis._Cast_DynamicAnalysis",
        ) -> "DynamicAnalysis":
            return self._parent

        def __getattr__(self: "DynamicAnalysis._Cast_DynamicAnalysis", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "DynamicAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "DynamicAnalysis._Cast_DynamicAnalysis":
        return self._Cast_DynamicAnalysis(self)
