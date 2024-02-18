"""BoltMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5406
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BOLT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "BoltMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2444
    from mastapy.system_model.analyses_and_results.static_loads import _6834


__docformat__ = "restructuredtext en"
__all__ = ("BoltMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="BoltMultibodyDynamicsAnalysis")


class BoltMultibodyDynamicsAnalysis(_5406.ComponentMultibodyDynamicsAnalysis):
    """BoltMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _BOLT_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BoltMultibodyDynamicsAnalysis")

    class _Cast_BoltMultibodyDynamicsAnalysis:
        """Special nested class for casting BoltMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
            parent: "BoltMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def component_multibody_dynamics_analysis(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(_5406.ComponentMultibodyDynamicsAnalysis)

        @property
        def part_multibody_dynamics_analysis(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5469

            return self._parent._cast(_5469.PartMultibodyDynamicsAnalysis)

        @property
        def part_time_series_load_analysis_case(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7551

            return self._parent._cast(_7551.PartTimeSeriesLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bolt_multibody_dynamics_analysis(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
        ) -> "BoltMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BoltMultibodyDynamicsAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2444.Bolt":
        """mastapy.system_model.part_model.Bolt

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6834.BoltLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase

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
    ) -> "BoltMultibodyDynamicsAnalysis._Cast_BoltMultibodyDynamicsAnalysis":
        return self._Cast_BoltMultibodyDynamicsAnalysis(self)
