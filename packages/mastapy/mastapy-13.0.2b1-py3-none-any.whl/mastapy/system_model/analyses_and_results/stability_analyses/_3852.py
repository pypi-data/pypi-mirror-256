"""PlanetCarrierStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3844
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "PlanetCarrierStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2471
    from mastapy.system_model.analyses_and_results.static_loads import _6938


__docformat__ = "restructuredtext en"
__all__ = ("PlanetCarrierStabilityAnalysis",)


Self = TypeVar("Self", bound="PlanetCarrierStabilityAnalysis")


class PlanetCarrierStabilityAnalysis(_3844.MountableComponentStabilityAnalysis):
    """PlanetCarrierStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _PLANET_CARRIER_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PlanetCarrierStabilityAnalysis")

    class _Cast_PlanetCarrierStabilityAnalysis:
        """Special nested class for casting PlanetCarrierStabilityAnalysis to subclasses."""

        def __init__(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
            parent: "PlanetCarrierStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def mountable_component_stability_analysis(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ):
            return self._parent._cast(_3844.MountableComponentStabilityAnalysis)

        @property
        def component_stability_analysis(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3790,
            )

            return self._parent._cast(_3790.ComponentStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3846,
            )

            return self._parent._cast(_3846.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def planet_carrier_stability_analysis(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
        ) -> "PlanetCarrierStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PlanetCarrierStabilityAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2471.PlanetCarrier":
        """mastapy.system_model.part_model.PlanetCarrier

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6938.PlanetCarrierLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase

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
    ) -> "PlanetCarrierStabilityAnalysis._Cast_PlanetCarrierStabilityAnalysis":
        return self._Cast_PlanetCarrierStabilityAnalysis(self)
