"""CoaxialConnectionHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5810
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "CoaxialConnectionHarmonicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2271
    from mastapy.system_model.analyses_and_results.static_loads import _6839
    from mastapy.system_model.analyses_and_results.system_deflections import _2716


__docformat__ = "restructuredtext en"
__all__ = ("CoaxialConnectionHarmonicAnalysis",)


Self = TypeVar("Self", bound="CoaxialConnectionHarmonicAnalysis")


class CoaxialConnectionHarmonicAnalysis(
    _5810.ShaftToMountableComponentConnectionHarmonicAnalysis
):
    """CoaxialConnectionHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _COAXIAL_CONNECTION_HARMONIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CoaxialConnectionHarmonicAnalysis")

    class _Cast_CoaxialConnectionHarmonicAnalysis:
        """Special nested class for casting CoaxialConnectionHarmonicAnalysis to subclasses."""

        def __init__(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
            parent: "CoaxialConnectionHarmonicAnalysis",
        ):
            self._parent = parent

        @property
        def shaft_to_mountable_component_connection_harmonic_analysis(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            return self._parent._cast(
                _5810.ShaftToMountableComponentConnectionHarmonicAnalysis
            )

        @property
        def abstract_shaft_to_mountable_component_connection_harmonic_analysis(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5684,
            )

            return self._parent._cast(
                _5684.AbstractShaftToMountableComponentConnectionHarmonicAnalysis
            )

        @property
        def connection_harmonic_analysis(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5717,
            )

            return self._parent._cast(_5717.ConnectionHarmonicAnalysis)

        @property
        def connection_static_load_analysis_case(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cycloidal_disc_central_bearing_connection_harmonic_analysis(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5726,
            )

            return self._parent._cast(
                _5726.CycloidalDiscCentralBearingConnectionHarmonicAnalysis
            )

        @property
        def coaxial_connection_harmonic_analysis(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
        ) -> "CoaxialConnectionHarmonicAnalysis":
            return self._parent

        def __getattr__(
            self: "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis",
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
        self: Self, instance_to_wrap: "CoaxialConnectionHarmonicAnalysis.TYPE"
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
    def system_deflection_results(
        self: Self,
    ) -> "_2716.CoaxialConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CoaxialConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CoaxialConnectionHarmonicAnalysis._Cast_CoaxialConnectionHarmonicAnalysis":
        return self._Cast_CoaxialConnectionHarmonicAnalysis(self)
