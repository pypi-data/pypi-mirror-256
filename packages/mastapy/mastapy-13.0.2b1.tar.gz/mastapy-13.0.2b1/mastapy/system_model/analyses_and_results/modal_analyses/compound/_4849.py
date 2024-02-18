"""TorqueConverterPumpCompoundModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4769
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "TorqueConverterPumpCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2610
    from mastapy.system_model.analyses_and_results.modal_analyses import _4705


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterPumpCompoundModalAnalysis",)


Self = TypeVar("Self", bound="TorqueConverterPumpCompoundModalAnalysis")


class TorqueConverterPumpCompoundModalAnalysis(_4769.CouplingHalfCompoundModalAnalysis):
    """TorqueConverterPumpCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_MODAL_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_TorqueConverterPumpCompoundModalAnalysis"
    )

    class _Cast_TorqueConverterPumpCompoundModalAnalysis:
        """Special nested class for casting TorqueConverterPumpCompoundModalAnalysis to subclasses."""

        def __init__(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
            parent: "TorqueConverterPumpCompoundModalAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_half_compound_modal_analysis(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
        ):
            return self._parent._cast(_4769.CouplingHalfCompoundModalAnalysis)

        @property
        def mountable_component_compound_modal_analysis(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4807,
            )

            return self._parent._cast(_4807.MountableComponentCompoundModalAnalysis)

        @property
        def component_compound_modal_analysis(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4755,
            )

            return self._parent._cast(_4755.ComponentCompoundModalAnalysis)

        @property
        def part_compound_modal_analysis(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4809,
            )

            return self._parent._cast(_4809.PartCompoundModalAnalysis)

        @property
        def part_compound_analysis(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def torque_converter_pump_compound_modal_analysis(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
        ) -> "TorqueConverterPumpCompoundModalAnalysis":
            return self._parent

        def __getattr__(
            self: "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis",
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
        self: Self, instance_to_wrap: "TorqueConverterPumpCompoundModalAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2610.TorqueConverterPump":
        """mastapy.system_model.part_model.couplings.TorqueConverterPump

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_4705.TorqueConverterPumpModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterPumpModalAnalysis]

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
    def component_analysis_cases(
        self: Self,
    ) -> "List[_4705.TorqueConverterPumpModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterPumpModalAnalysis]

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
    def cast_to(
        self: Self,
    ) -> "TorqueConverterPumpCompoundModalAnalysis._Cast_TorqueConverterPumpCompoundModalAnalysis":
        return self._Cast_TorqueConverterPumpCompoundModalAnalysis(self)
