"""ConnectorCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3976
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "ConnectorCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.stability_analyses import _3801


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorCompoundStabilityAnalysis",)


Self = TypeVar("Self", bound="ConnectorCompoundStabilityAnalysis")


class ConnectorCompoundStabilityAnalysis(
    _3976.MountableComponentCompoundStabilityAnalysis
):
    """ConnectorCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CONNECTOR_COMPOUND_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ConnectorCompoundStabilityAnalysis")

    class _Cast_ConnectorCompoundStabilityAnalysis:
        """Special nested class for casting ConnectorCompoundStabilityAnalysis to subclasses."""

        def __init__(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
            parent: "ConnectorCompoundStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def mountable_component_compound_stability_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            return self._parent._cast(_3976.MountableComponentCompoundStabilityAnalysis)

        @property
        def component_compound_stability_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3924,
            )

            return self._parent._cast(_3924.ComponentCompoundStabilityAnalysis)

        @property
        def part_compound_stability_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3978,
            )

            return self._parent._cast(_3978.PartCompoundStabilityAnalysis)

        @property
        def part_compound_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bearing_compound_stability_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3907,
            )

            return self._parent._cast(_3907.BearingCompoundStabilityAnalysis)

        @property
        def oil_seal_compound_stability_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3977,
            )

            return self._parent._cast(_3977.OilSealCompoundStabilityAnalysis)

        @property
        def shaft_hub_connection_compound_stability_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3995,
            )

            return self._parent._cast(_3995.ShaftHubConnectionCompoundStabilityAnalysis)

        @property
        def connector_compound_stability_analysis(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
        ) -> "ConnectorCompoundStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis",
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
        self: Self, instance_to_wrap: "ConnectorCompoundStabilityAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_3801.ConnectorStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ConnectorStabilityAnalysis]

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
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_3801.ConnectorStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ConnectorStabilityAnalysis]

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
    def cast_to(
        self: Self,
    ) -> "ConnectorCompoundStabilityAnalysis._Cast_ConnectorCompoundStabilityAnalysis":
        return self._Cast_ConnectorCompoundStabilityAnalysis(self)
