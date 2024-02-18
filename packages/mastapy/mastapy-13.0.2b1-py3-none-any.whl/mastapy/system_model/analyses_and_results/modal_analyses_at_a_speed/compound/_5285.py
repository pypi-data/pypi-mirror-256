"""ConnectorCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5326,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "ConnectorCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5155,
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorCompoundModalAnalysisAtASpeed",)


Self = TypeVar("Self", bound="ConnectorCompoundModalAnalysisAtASpeed")


class ConnectorCompoundModalAnalysisAtASpeed(
    _5326.MountableComponentCompoundModalAnalysisAtASpeed
):
    """ConnectorCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _CONNECTOR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_ConnectorCompoundModalAnalysisAtASpeed"
    )

    class _Cast_ConnectorCompoundModalAnalysisAtASpeed:
        """Special nested class for casting ConnectorCompoundModalAnalysisAtASpeed to subclasses."""

        def __init__(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
            parent: "ConnectorCompoundModalAnalysisAtASpeed",
        ):
            self._parent = parent

        @property
        def mountable_component_compound_modal_analysis_at_a_speed(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            return self._parent._cast(
                _5326.MountableComponentCompoundModalAnalysisAtASpeed
            )

        @property
        def component_compound_modal_analysis_at_a_speed(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5274,
            )

            return self._parent._cast(_5274.ComponentCompoundModalAnalysisAtASpeed)

        @property
        def part_compound_modal_analysis_at_a_speed(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5328,
            )

            return self._parent._cast(_5328.PartCompoundModalAnalysisAtASpeed)

        @property
        def part_compound_analysis(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bearing_compound_modal_analysis_at_a_speed(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5257,
            )

            return self._parent._cast(_5257.BearingCompoundModalAnalysisAtASpeed)

        @property
        def oil_seal_compound_modal_analysis_at_a_speed(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5327,
            )

            return self._parent._cast(_5327.OilSealCompoundModalAnalysisAtASpeed)

        @property
        def shaft_hub_connection_compound_modal_analysis_at_a_speed(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5345,
            )

            return self._parent._cast(
                _5345.ShaftHubConnectionCompoundModalAnalysisAtASpeed
            )

        @property
        def connector_compound_modal_analysis_at_a_speed(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
        ) -> "ConnectorCompoundModalAnalysisAtASpeed":
            return self._parent

        def __getattr__(
            self: "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed",
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
        self: Self, instance_to_wrap: "ConnectorCompoundModalAnalysisAtASpeed.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_5155.ConnectorModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ConnectorModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_5155.ConnectorModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ConnectorModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "ConnectorCompoundModalAnalysisAtASpeed._Cast_ConnectorCompoundModalAnalysisAtASpeed":
        return self._Cast_ConnectorCompoundModalAnalysisAtASpeed(self)
