"""CVTAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7023,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CVT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "CVTAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2588
    from mastapy.system_model.analyses_and_results.system_deflections import _2736


__docformat__ = "restructuredtext en"
__all__ = ("CVTAdvancedTimeSteppingAnalysisForModulation",)


Self = TypeVar("Self", bound="CVTAdvancedTimeSteppingAnalysisForModulation")


class CVTAdvancedTimeSteppingAnalysisForModulation(
    _7023.BeltDriveAdvancedTimeSteppingAnalysisForModulation
):
    """CVTAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _CVT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CVTAdvancedTimeSteppingAnalysisForModulation"
    )

    class _Cast_CVTAdvancedTimeSteppingAnalysisForModulation:
        """Special nested class for casting CVTAdvancedTimeSteppingAnalysisForModulation to subclasses."""

        def __init__(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
            parent: "CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            self._parent = parent

        @property
        def belt_drive_advanced_time_stepping_analysis_for_modulation(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            return self._parent._cast(
                _7023.BeltDriveAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def specialised_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7112,
            )

            return self._parent._cast(
                _7112.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def abstract_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7008,
            )

            return self._parent._cast(
                _7008.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_advanced_time_stepping_analysis_for_modulation(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7093,
            )

            return self._parent._cast(
                _7093.PartAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_static_load_analysis_case(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cvt_advanced_time_stepping_analysis_for_modulation(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
        ) -> "CVTAdvancedTimeSteppingAnalysisForModulation":
            return self._parent

        def __getattr__(
            self: "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation",
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
        instance_to_wrap: "CVTAdvancedTimeSteppingAnalysisForModulation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2588.CVT":
        """mastapy.system_model.part_model.couplings.CVT

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: Self) -> "_2736.CVTSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CVTSystemDeflection

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
    ) -> "CVTAdvancedTimeSteppingAnalysisForModulation._Cast_CVTAdvancedTimeSteppingAnalysisForModulation":
        return self._Cast_CVTAdvancedTimeSteppingAnalysisForModulation(self)
