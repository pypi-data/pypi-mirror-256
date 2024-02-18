"""ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5381
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
        "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
    )
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2297


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",)


Self = TypeVar(
    "Self", bound="ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis"
)


class ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis(
    _5381.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
):
    """ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
    )

    class _Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis:
        """Special nested class for casting ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
            parent: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def abstract_shaft_to_mountable_component_connection_multibody_dynamics_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(
                _5381.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
            )

        @property
        def connection_multibody_dynamics_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5416

            return self._parent._cast(_5416.ConnectionMultibodyDynamicsAnalysis)

        @property
        def connection_time_series_load_analysis_case(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.ConnectionTimeSeriesLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def coaxial_connection_multibody_dynamics_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5405

            return self._parent._cast(_5405.CoaxialConnectionMultibodyDynamicsAnalysis)

        @property
        def cycloidal_disc_central_bearing_connection_multibody_dynamics_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5425

            return self._parent._cast(
                _5425.CycloidalDiscCentralBearingConnectionMultibodyDynamicsAnalysis
            )

        @property
        def planetary_connection_multibody_dynamics_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5473

            return self._parent._cast(
                _5473.PlanetaryConnectionMultibodyDynamicsAnalysis
            )

        @property
        def shaft_to_mountable_component_connection_multibody_dynamics_analysis(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
        ) -> "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis",
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
        instance_to_wrap: "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2297.ShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis":
        return self._Cast_ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis(
            self
        )
