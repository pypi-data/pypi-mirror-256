"""PlanetCarrierMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5466
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "PlanetCarrierMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2471
    from mastapy.system_model.analyses_and_results.static_loads import _6938


__docformat__ = "restructuredtext en"
__all__ = ("PlanetCarrierMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="PlanetCarrierMultibodyDynamicsAnalysis")


class PlanetCarrierMultibodyDynamicsAnalysis(
    _5466.MountableComponentMultibodyDynamicsAnalysis
):
    """PlanetCarrierMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _PLANET_CARRIER_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_PlanetCarrierMultibodyDynamicsAnalysis"
    )

    class _Cast_PlanetCarrierMultibodyDynamicsAnalysis:
        """Special nested class for casting PlanetCarrierMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
            parent: "PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def mountable_component_multibody_dynamics_analysis(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(_5466.MountableComponentMultibodyDynamicsAnalysis)

        @property
        def component_multibody_dynamics_analysis(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5406

            return self._parent._cast(_5406.ComponentMultibodyDynamicsAnalysis)

        @property
        def part_multibody_dynamics_analysis(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5469

            return self._parent._cast(_5469.PartMultibodyDynamicsAnalysis)

        @property
        def part_time_series_load_analysis_case(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7551

            return self._parent._cast(_7551.PartTimeSeriesLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def planet_carrier_multibody_dynamics_analysis(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
        ) -> "PlanetCarrierMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis",
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
        self: Self, instance_to_wrap: "PlanetCarrierMultibodyDynamicsAnalysis.TYPE"
    ):
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
    ) -> "PlanetCarrierMultibodyDynamicsAnalysis._Cast_PlanetCarrierMultibodyDynamicsAnalysis":
        return self._Cast_PlanetCarrierMultibodyDynamicsAnalysis(self)
