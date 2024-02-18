"""PulleyCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3938
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "PulleyCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2592
    from mastapy.system_model.analyses_and_results.stability_analyses import _3855


__docformat__ = "restructuredtext en"
__all__ = ("PulleyCompoundStabilityAnalysis",)


Self = TypeVar("Self", bound="PulleyCompoundStabilityAnalysis")


class PulleyCompoundStabilityAnalysis(_3938.CouplingHalfCompoundStabilityAnalysis):
    """PulleyCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _PULLEY_COMPOUND_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PulleyCompoundStabilityAnalysis")

    class _Cast_PulleyCompoundStabilityAnalysis:
        """Special nested class for casting PulleyCompoundStabilityAnalysis to subclasses."""

        def __init__(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
            parent: "PulleyCompoundStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_half_compound_stability_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ):
            return self._parent._cast(_3938.CouplingHalfCompoundStabilityAnalysis)

        @property
        def mountable_component_compound_stability_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3976,
            )

            return self._parent._cast(_3976.MountableComponentCompoundStabilityAnalysis)

        @property
        def component_compound_stability_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3924,
            )

            return self._parent._cast(_3924.ComponentCompoundStabilityAnalysis)

        @property
        def part_compound_stability_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3978,
            )

            return self._parent._cast(_3978.PartCompoundStabilityAnalysis)

        @property
        def part_compound_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cvt_pulley_compound_stability_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3941,
            )

            return self._parent._cast(_3941.CVTPulleyCompoundStabilityAnalysis)

        @property
        def pulley_compound_stability_analysis(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
        ) -> "PulleyCompoundStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PulleyCompoundStabilityAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2592.Pulley":
        """mastapy.system_model.part_model.couplings.Pulley

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_3855.PulleyStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.PulleyStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(self: Self) -> "List[_3855.PulleyStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.PulleyStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "PulleyCompoundStabilityAnalysis._Cast_PulleyCompoundStabilityAnalysis":
        return self._Cast_PulleyCompoundStabilityAnalysis(self)
