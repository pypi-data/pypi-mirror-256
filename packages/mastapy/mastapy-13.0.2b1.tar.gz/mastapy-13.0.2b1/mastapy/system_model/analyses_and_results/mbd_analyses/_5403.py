"""ClutchMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5420
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CLUTCH_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "ClutchMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2580
    from mastapy.system_model.analyses_and_results.static_loads import _6837
    from mastapy.system_model.analyses_and_results.mbd_analyses import _5401


__docformat__ = "restructuredtext en"
__all__ = ("ClutchMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="ClutchMultibodyDynamicsAnalysis")


class ClutchMultibodyDynamicsAnalysis(_5420.CouplingMultibodyDynamicsAnalysis):
    """ClutchMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ClutchMultibodyDynamicsAnalysis")

    class _Cast_ClutchMultibodyDynamicsAnalysis:
        """Special nested class for casting ClutchMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
            parent: "ClutchMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_multibody_dynamics_analysis(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(_5420.CouplingMultibodyDynamicsAnalysis)

        @property
        def specialised_assembly_multibody_dynamics_analysis(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5491

            return self._parent._cast(
                _5491.SpecialisedAssemblyMultibodyDynamicsAnalysis
            )

        @property
        def abstract_assembly_multibody_dynamics_analysis(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5378

            return self._parent._cast(_5378.AbstractAssemblyMultibodyDynamicsAnalysis)

        @property
        def part_multibody_dynamics_analysis(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5469

            return self._parent._cast(_5469.PartMultibodyDynamicsAnalysis)

        @property
        def part_time_series_load_analysis_case(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7551

            return self._parent._cast(_7551.PartTimeSeriesLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_multibody_dynamics_analysis(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
        ) -> "ClutchMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ClutchMultibodyDynamicsAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2580.Clutch":
        """mastapy.system_model.part_model.couplings.Clutch

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6837.ClutchLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def clutch_connection(
        self: Self,
    ) -> "_5401.ClutchConnectionMultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.ClutchConnectionMultibodyDynamicsAnalysis

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ClutchConnection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "ClutchMultibodyDynamicsAnalysis._Cast_ClutchMultibodyDynamicsAnalysis":
        return self._Cast_ClutchMultibodyDynamicsAnalysis(self)
