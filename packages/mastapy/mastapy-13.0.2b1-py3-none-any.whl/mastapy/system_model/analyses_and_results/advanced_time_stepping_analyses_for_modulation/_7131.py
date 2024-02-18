"""TorqueConverterAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7050,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2609
    from mastapy.system_model.analyses_and_results.static_loads import _6976
    from mastapy.system_model.analyses_and_results.system_deflections import _2832


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterAdvancedTimeSteppingAnalysisForModulation",)


Self = TypeVar("Self", bound="TorqueConverterAdvancedTimeSteppingAnalysisForModulation")


class TorqueConverterAdvancedTimeSteppingAnalysisForModulation(
    _7050.CouplingAdvancedTimeSteppingAnalysisForModulation
):
    """TorqueConverterAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
    )

    class _Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation:
        """Special nested class for casting TorqueConverterAdvancedTimeSteppingAnalysisForModulation to subclasses."""

        def __init__(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
            parent: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            self._parent = parent

        @property
        def coupling_advanced_time_stepping_analysis_for_modulation(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            return self._parent._cast(
                _7050.CouplingAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def specialised_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7112,
            )

            return self._parent._cast(
                _7112.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def abstract_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7008,
            )

            return self._parent._cast(
                _7008.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_advanced_time_stepping_analysis_for_modulation(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7093,
            )

            return self._parent._cast(
                _7093.PartAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_static_load_analysis_case(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def torque_converter_advanced_time_stepping_analysis_for_modulation(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
        ) -> "TorqueConverterAdvancedTimeSteppingAnalysisForModulation":
            return self._parent

        def __getattr__(
            self: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation",
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
        instance_to_wrap: "TorqueConverterAdvancedTimeSteppingAnalysisForModulation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2609.TorqueConverter":
        """mastapy.system_model.part_model.couplings.TorqueConverter

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6976.TorqueConverterLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: Self,
    ) -> "_2832.TorqueConverterSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterSystemDeflection

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
    ) -> "TorqueConverterAdvancedTimeSteppingAnalysisForModulation._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation":
        return self._Cast_TorqueConverterAdvancedTimeSteppingAnalysisForModulation(self)
