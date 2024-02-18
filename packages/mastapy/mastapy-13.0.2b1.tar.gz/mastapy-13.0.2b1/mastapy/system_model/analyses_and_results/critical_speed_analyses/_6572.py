"""ConceptCouplingCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6583
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "ConceptCouplingCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2583
    from mastapy.system_model.analyses_and_results.static_loads import _6843


__docformat__ = "restructuredtext en"
__all__ = ("ConceptCouplingCriticalSpeedAnalysis",)


Self = TypeVar("Self", bound="ConceptCouplingCriticalSpeedAnalysis")


class ConceptCouplingCriticalSpeedAnalysis(_6583.CouplingCriticalSpeedAnalysis):
    """ConceptCouplingCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_CRITICAL_SPEED_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ConceptCouplingCriticalSpeedAnalysis")

    class _Cast_ConceptCouplingCriticalSpeedAnalysis:
        """Special nested class for casting ConceptCouplingCriticalSpeedAnalysis to subclasses."""

        def __init__(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
            parent: "ConceptCouplingCriticalSpeedAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_critical_speed_analysis(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            return self._parent._cast(_6583.CouplingCriticalSpeedAnalysis)

        @property
        def specialised_assembly_critical_speed_analysis(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.critical_speed_analyses import (
                _6646,
            )

            return self._parent._cast(_6646.SpecialisedAssemblyCriticalSpeedAnalysis)

        @property
        def abstract_assembly_critical_speed_analysis(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.critical_speed_analyses import (
                _6545,
            )

            return self._parent._cast(_6545.AbstractAssemblyCriticalSpeedAnalysis)

        @property
        def part_critical_speed_analysis(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.critical_speed_analyses import (
                _6627,
            )

            return self._parent._cast(_6627.PartCriticalSpeedAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def concept_coupling_critical_speed_analysis(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
        ) -> "ConceptCouplingCriticalSpeedAnalysis":
            return self._parent

        def __getattr__(
            self: "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis",
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
        self: Self, instance_to_wrap: "ConceptCouplingCriticalSpeedAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2583.ConceptCoupling":
        """mastapy.system_model.part_model.couplings.ConceptCoupling

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6843.ConceptCouplingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "ConceptCouplingCriticalSpeedAnalysis._Cast_ConceptCouplingCriticalSpeedAnalysis":
        return self._Cast_ConceptCouplingCriticalSpeedAnalysis(self)
