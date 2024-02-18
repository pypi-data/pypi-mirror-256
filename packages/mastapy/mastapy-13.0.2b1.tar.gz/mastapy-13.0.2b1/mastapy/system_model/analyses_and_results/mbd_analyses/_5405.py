"""CoaxialConnectionMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5489
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "CoaxialConnectionMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2271
    from mastapy.system_model.analyses_and_results.static_loads import _6839


__docformat__ = "restructuredtext en"
__all__ = ("CoaxialConnectionMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="CoaxialConnectionMultibodyDynamicsAnalysis")


class CoaxialConnectionMultibodyDynamicsAnalysis(
    _5489.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
):
    """CoaxialConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _COAXIAL_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CoaxialConnectionMultibodyDynamicsAnalysis"
    )

    class _Cast_CoaxialConnectionMultibodyDynamicsAnalysis:
        """Special nested class for casting CoaxialConnectionMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
            parent: "CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def shaft_to_mountable_component_connection_multibody_dynamics_analysis(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(
                _5489.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
            )

        @property
        def abstract_shaft_to_mountable_component_connection_multibody_dynamics_analysis(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5381

            return self._parent._cast(
                _5381.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
            )

        @property
        def connection_multibody_dynamics_analysis(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5416

            return self._parent._cast(_5416.ConnectionMultibodyDynamicsAnalysis)

        @property
        def connection_time_series_load_analysis_case(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.ConnectionTimeSeriesLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cycloidal_disc_central_bearing_connection_multibody_dynamics_analysis(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5425

            return self._parent._cast(
                _5425.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis
            )

        @property
        def coaxial_connection_multibody_dynamics_analysis(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
        ) -> "CoaxialConnectionMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis",
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
        self: Self, instance_to_wrap: "CoaxialConnectionMultibodyDynamicsAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2271.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: Self) -> "_6839.CoaxialConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CoaxialConnectionMultibodyDynamicsAnalysis._Cast_CoaxialConnectionMultibodyDynamicsAnalysis":
        return self._Cast_CoaxialConnectionMultibodyDynamicsAnalysis(self)
