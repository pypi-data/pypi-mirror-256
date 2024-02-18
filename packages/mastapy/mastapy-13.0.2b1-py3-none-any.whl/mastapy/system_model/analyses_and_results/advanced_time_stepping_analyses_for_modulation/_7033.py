"""BoltedJointAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7112,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "BoltedJointAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2445
    from mastapy.system_model.analyses_and_results.static_loads import _6833
    from mastapy.system_model.analyses_and_results.system_deflections import _2711


__docformat__ = "restructuredtext en"
__all__ = ("BoltedJointAdvancedTimeSteppingAnalysisForModulation",)


Self = TypeVar("Self", bound="BoltedJointAdvancedTimeSteppingAnalysisForModulation")


class BoltedJointAdvancedTimeSteppingAnalysisForModulation(
    _7112.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
):
    """BoltedJointAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _BOLTED_JOINT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation"
    )

    class _Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation:
        """Special nested class for casting BoltedJointAdvancedTimeSteppingAnalysisForModulation to subclasses."""

        def __init__(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
            parent: "BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            self._parent = parent

        @property
        def specialised_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            return self._parent._cast(
                _7112.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def abstract_assembly_advanced_time_stepping_analysis_for_modulation(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7008,
            )

            return self._parent._cast(
                _7008.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_advanced_time_stepping_analysis_for_modulation(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7093,
            )

            return self._parent._cast(
                _7093.PartAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_static_load_analysis_case(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def bolted_joint_advanced_time_stepping_analysis_for_modulation(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
        ) -> "BoltedJointAdvancedTimeSteppingAnalysisForModulation":
            return self._parent

        def __getattr__(
            self: "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation",
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
        instance_to_wrap: "BoltedJointAdvancedTimeSteppingAnalysisForModulation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2445.BoltedJoint":
        """mastapy.system_model.part_model.BoltedJoint

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6833.BoltedJointLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: Self) -> "_2711.BoltedJointSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.BoltedJointSystemDeflection

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
    ) -> "BoltedJointAdvancedTimeSteppingAnalysisForModulation._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation":
        return self._Cast_BoltedJointAdvancedTimeSteppingAnalysisForModulation(self)
