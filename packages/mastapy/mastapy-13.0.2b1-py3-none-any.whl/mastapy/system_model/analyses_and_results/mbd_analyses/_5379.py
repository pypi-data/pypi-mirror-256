"""AbstractShaftMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5380
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "AbstractShaftMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2437


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="AbstractShaftMultibodyDynamicsAnalysis")


class AbstractShaftMultibodyDynamicsAnalysis(
    _5380.AbstractShaftOrHousingMultibodyDynamicsAnalysis
):
    """AbstractShaftMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_SHAFT_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_AbstractShaftMultibodyDynamicsAnalysis"
    )

    class _Cast_AbstractShaftMultibodyDynamicsAnalysis:
        """Special nested class for casting AbstractShaftMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
            parent: "AbstractShaftMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def abstract_shaft_or_housing_multibody_dynamics_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(
                _5380.AbstractShaftOrHousingMultibodyDynamicsAnalysis
            )

        @property
        def component_multibody_dynamics_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5406

            return self._parent._cast(_5406.ComponentMultibodyDynamicsAnalysis)

        @property
        def part_multibody_dynamics_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5469

            return self._parent._cast(_5469.PartMultibodyDynamicsAnalysis)

        @property
        def part_time_series_load_analysis_case(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7551

            return self._parent._cast(_7551.PartTimeSeriesLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cycloidal_disc_multibody_dynamics_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5426

            return self._parent._cast(_5426.CycloidalDiscMultibodyDynamicsAnalysis)

        @property
        def shaft_multibody_dynamics_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5488

            return self._parent._cast(_5488.ShaftMultibodyDynamicsAnalysis)

        @property
        def abstract_shaft_multibody_dynamics_analysis(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
        ) -> "AbstractShaftMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
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
        self: Self, instance_to_wrap: "AbstractShaftMultibodyDynamicsAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2437.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis":
        return self._Cast_AbstractShaftMultibodyDynamicsAnalysis(self)
