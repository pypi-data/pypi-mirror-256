"""CouplingConnectionCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5946
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "CouplingConnectionCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.harmonic_analyses import _5719


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundHarmonicAnalysis",)


Self = TypeVar("Self", bound="CouplingConnectionCompoundHarmonicAnalysis")


class CouplingConnectionCompoundHarmonicAnalysis(
    _5946.InterMountableComponentConnectionCompoundHarmonicAnalysis
):
    """CouplingConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _COUPLING_CONNECTION_COMPOUND_HARMONIC_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CouplingConnectionCompoundHarmonicAnalysis"
    )

    class _Cast_CouplingConnectionCompoundHarmonicAnalysis:
        """Special nested class for casting CouplingConnectionCompoundHarmonicAnalysis to subclasses."""

        def __init__(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
            parent: "CouplingConnectionCompoundHarmonicAnalysis",
        ):
            self._parent = parent

        @property
        def inter_mountable_component_connection_compound_harmonic_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            return self._parent._cast(
                _5946.InterMountableComponentConnectionCompoundHarmonicAnalysis
            )

        @property
        def connection_compound_harmonic_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5916,
            )

            return self._parent._cast(_5916.ConnectionCompoundHarmonicAnalysis)

        @property
        def connection_compound_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7541

            return self._parent._cast(_7541.ConnectionCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_connection_compound_harmonic_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5903,
            )

            return self._parent._cast(_5903.ClutchConnectionCompoundHarmonicAnalysis)

        @property
        def concept_coupling_connection_compound_harmonic_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5908,
            )

            return self._parent._cast(
                _5908.ConceptCouplingConnectionCompoundHarmonicAnalysis
            )

        @property
        def part_to_part_shear_coupling_connection_compound_harmonic_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5962,
            )

            return self._parent._cast(
                _5962.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis
            )

        @property
        def spring_damper_connection_compound_harmonic_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5984,
            )

            return self._parent._cast(
                _5984.SpringDamperConnectionCompoundHarmonicAnalysis
            )

        @property
        def torque_converter_connection_compound_harmonic_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5999,
            )

            return self._parent._cast(
                _5999.TorqueConverterConnectionCompoundHarmonicAnalysis
            )

        @property
        def coupling_connection_compound_harmonic_analysis(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
        ) -> "CouplingConnectionCompoundHarmonicAnalysis":
            return self._parent

        def __getattr__(
            self: "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
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
        self: Self, instance_to_wrap: "CouplingConnectionCompoundHarmonicAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(
        self: Self,
    ) -> "List[_5719.CouplingConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.CouplingConnectionHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: Self,
    ) -> "List[_5719.CouplingConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.CouplingConnectionHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis":
        return self._Cast_CouplingConnectionCompoundHarmonicAnalysis(self)
