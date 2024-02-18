"""PartToPartShearCouplingHalfCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5920
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2591
    from mastapy.system_model.analyses_and_results.harmonic_analyses import _5792


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCouplingHalfCompoundHarmonicAnalysis",)


Self = TypeVar("Self", bound="PartToPartShearCouplingHalfCompoundHarmonicAnalysis")


class PartToPartShearCouplingHalfCompoundHarmonicAnalysis(
    _5920.CouplingHalfCompoundHarmonicAnalysis
):
    """PartToPartShearCouplingHalfCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_HARMONIC_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis"
    )

    class _Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis:
        """Special nested class for casting PartToPartShearCouplingHalfCompoundHarmonicAnalysis to subclasses."""

        def __init__(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
            parent: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_half_compound_harmonic_analysis(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ):
            return self._parent._cast(_5920.CouplingHalfCompoundHarmonicAnalysis)

        @property
        def mountable_component_compound_harmonic_analysis(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5958,
            )

            return self._parent._cast(_5958.MountableComponentCompoundHarmonicAnalysis)

        @property
        def component_compound_harmonic_analysis(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5906,
            )

            return self._parent._cast(_5906.ComponentCompoundHarmonicAnalysis)

        @property
        def part_compound_harmonic_analysis(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
                _5960,
            )

            return self._parent._cast(_5960.PartCompoundHarmonicAnalysis)

        @property
        def part_compound_analysis(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def part_to_part_shear_coupling_half_compound_harmonic_analysis(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
        ) -> "PartToPartShearCouplingHalfCompoundHarmonicAnalysis":
            return self._parent

        def __getattr__(
            self: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis",
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
        self: Self,
        instance_to_wrap: "PartToPartShearCouplingHalfCompoundHarmonicAnalysis.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2591.PartToPartShearCouplingHalf":
        """mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf

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
    ) -> "List[_5792.PartToPartShearCouplingHalfHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.PartToPartShearCouplingHalfHarmonicAnalysis]

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
    def component_analysis_cases(
        self: Self,
    ) -> "List[_5792.PartToPartShearCouplingHalfHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.PartToPartShearCouplingHalfHarmonicAnalysis]

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
    ) -> "PartToPartShearCouplingHalfCompoundHarmonicAnalysis._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis":
        return self._Cast_PartToPartShearCouplingHalfCompoundHarmonicAnalysis(self)
