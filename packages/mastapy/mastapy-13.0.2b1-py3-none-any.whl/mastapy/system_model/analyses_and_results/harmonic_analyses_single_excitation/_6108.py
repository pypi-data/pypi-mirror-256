"""ShaftHubConnectionHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _6046,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2600
    from mastapy.system_model.analyses_and_results.static_loads import _6952


__docformat__ = "restructuredtext en"
__all__ = ("ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",)


Self = TypeVar("Self", bound="ShaftHubConnectionHarmonicAnalysisOfSingleExcitation")


class ShaftHubConnectionHarmonicAnalysisOfSingleExcitation(
    _6046.ConnectorHarmonicAnalysisOfSingleExcitation
):
    """ShaftHubConnectionHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _SHAFT_HUB_CONNECTION_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation"
    )

    class _Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation:
        """Special nested class for casting ShaftHubConnectionHarmonicAnalysisOfSingleExcitation to subclasses."""

        def __init__(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
            parent: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            self._parent = parent

        @property
        def connector_harmonic_analysis_of_single_excitation(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            return self._parent._cast(_6046.ConnectorHarmonicAnalysisOfSingleExcitation)

        @property
        def mountable_component_harmonic_analysis_of_single_excitation(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6089,
            )

            return self._parent._cast(
                _6089.MountableComponentHarmonicAnalysisOfSingleExcitation
            )

        @property
        def component_harmonic_analysis_of_single_excitation(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6035,
            )

            return self._parent._cast(_6035.ComponentHarmonicAnalysisOfSingleExcitation)

        @property
        def part_harmonic_analysis_of_single_excitation(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6091,
            )

            return self._parent._cast(_6091.PartHarmonicAnalysisOfSingleExcitation)

        @property
        def part_static_load_analysis_case(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def shaft_hub_connection_harmonic_analysis_of_single_excitation(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
        ) -> "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation":
            return self._parent

        def __getattr__(
            self: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation",
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
        instance_to_wrap: "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2600.ShaftHubConnection":
        """mastapy.system_model.part_model.couplings.ShaftHubConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6952.ShaftHubConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(
        self: Self,
    ) -> "List[ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "ShaftHubConnectionHarmonicAnalysisOfSingleExcitation._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation":
        return self._Cast_ShaftHubConnectionHarmonicAnalysisOfSingleExcitation(self)
