"""PlanetaryConnectionMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5489
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "PlanetaryConnectionMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2289
    from mastapy.system_model.analyses_and_results.static_loads import _6935


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryConnectionMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="PlanetaryConnectionMultibodyDynamicsAnalysis")


class PlanetaryConnectionMultibodyDynamicsAnalysis(
    _5489.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
):
    """PlanetaryConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _PLANETARY_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_PlanetaryConnectionMultibodyDynamicsAnalysis"
    )

    class _Cast_PlanetaryConnectionMultibodyDynamicsAnalysis:
        """Special nested class for casting PlanetaryConnectionMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
            parent: "PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def shaft_to_mountable_component_connection_multibody_dynamics_analysis(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(
                _5489.ShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
            )

        @property
        def abstract_shaft_to_mountable_component_connection_multibody_dynamics_analysis(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5381

            return self._parent._cast(
                _5381.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis
            )

        @property
        def connection_multibody_dynamics_analysis(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5416

            return self._parent._cast(_5416.ConnectionMultibodyDynamicsAnalysis)

        @property
        def connection_time_series_load_analysis_case(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.ConnectionTimeSeriesLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def planetary_connection_multibody_dynamics_analysis(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
        ) -> "PlanetaryConnectionMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis",
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
        instance_to_wrap: "PlanetaryConnectionMultibodyDynamicsAnalysis.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2289.PlanetaryConnection":
        """mastapy.system_model.connections_and_sockets.PlanetaryConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: Self) -> "_6935.PlanetaryConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase

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
    ) -> "PlanetaryConnectionMultibodyDynamicsAnalysis._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis":
        return self._Cast_PlanetaryConnectionMultibodyDynamicsAnalysis(self)
