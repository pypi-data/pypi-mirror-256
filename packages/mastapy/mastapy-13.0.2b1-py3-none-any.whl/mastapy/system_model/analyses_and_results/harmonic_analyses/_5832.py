"""SynchroniserSleeveHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5831
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "SynchroniserSleeveHarmonicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2608
    from mastapy.system_model.analyses_and_results.static_loads import _6973
    from mastapy.system_model.analyses_and_results.system_deflections import _2825


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserSleeveHarmonicAnalysis",)


Self = TypeVar("Self", bound="SynchroniserSleeveHarmonicAnalysis")


class SynchroniserSleeveHarmonicAnalysis(_5831.SynchroniserPartHarmonicAnalysis):
    """SynchroniserSleeveHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_SLEEVE_HARMONIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_SynchroniserSleeveHarmonicAnalysis")

    class _Cast_SynchroniserSleeveHarmonicAnalysis:
        """Special nested class for casting SynchroniserSleeveHarmonicAnalysis to subclasses."""

        def __init__(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
            parent: "SynchroniserSleeveHarmonicAnalysis",
        ):
            self._parent = parent

        @property
        def synchroniser_part_harmonic_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            return self._parent._cast(_5831.SynchroniserPartHarmonicAnalysis)

        @property
        def coupling_half_harmonic_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5720,
            )

            return self._parent._cast(_5720.CouplingHalfHarmonicAnalysis)

        @property
        def mountable_component_harmonic_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5788,
            )

            return self._parent._cast(_5788.MountableComponentHarmonicAnalysis)

        @property
        def component_harmonic_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5707,
            )

            return self._parent._cast(_5707.ComponentHarmonicAnalysis)

        @property
        def part_harmonic_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5790,
            )

            return self._parent._cast(_5790.PartHarmonicAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def synchroniser_sleeve_harmonic_analysis(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
        ) -> "SynchroniserSleeveHarmonicAnalysis":
            return self._parent

        def __getattr__(
            self: "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis",
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
        self: Self, instance_to_wrap: "SynchroniserSleeveHarmonicAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2608.SynchroniserSleeve":
        """mastapy.system_model.part_model.couplings.SynchroniserSleeve

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6973.SynchroniserSleeveLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: Self,
    ) -> "_2825.SynchroniserSleeveSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.SynchroniserSleeveSystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "SynchroniserSleeveHarmonicAnalysis._Cast_SynchroniserSleeveHarmonicAnalysis":
        return self._Cast_SynchroniserSleeveHarmonicAnalysis(self)
