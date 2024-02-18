"""PointLoadAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7136,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "PointLoadAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2473
    from mastapy.system_model.analyses_and_results.static_loads import _6941
    from mastapy.system_model.analyses_and_results.system_deflections import _2793


__docformat__ = "restructuredtext en"
__all__ = ("PointLoadAdvancedTimeSteppingAnalysisForModulation",)


Self = TypeVar("Self", bound="PointLoadAdvancedTimeSteppingAnalysisForModulation")


class PointLoadAdvancedTimeSteppingAnalysisForModulation(
    _7136.VirtualComponentAdvancedTimeSteppingAnalysisForModulation
):
    """PointLoadAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation"
    )

    class _Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation:
        """Special nested class for casting PointLoadAdvancedTimeSteppingAnalysisForModulation to subclasses."""

        def __init__(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
            parent: "PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            self._parent = parent

        @property
        def virtual_component_advanced_time_stepping_analysis_for_modulation(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            return self._parent._cast(
                _7136.VirtualComponentAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def mountable_component_advanced_time_stepping_analysis_for_modulation(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7091,
            )

            return self._parent._cast(
                _7091.MountableComponentAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def component_advanced_time_stepping_analysis_for_modulation(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7038,
            )

            return self._parent._cast(
                _7038.ComponentAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_advanced_time_stepping_analysis_for_modulation(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7093,
            )

            return self._parent._cast(
                _7093.PartAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def part_static_load_analysis_case(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def point_load_advanced_time_stepping_analysis_for_modulation(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
        ) -> "PointLoadAdvancedTimeSteppingAnalysisForModulation":
            return self._parent

        def __getattr__(
            self: "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation",
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
        instance_to_wrap: "PointLoadAdvancedTimeSteppingAnalysisForModulation.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2473.PointLoad":
        """mastapy.system_model.part_model.PointLoad

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6941.PointLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: Self) -> "_2793.PointLoadSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.PointLoadSystemDeflection

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
    ) -> "PointLoadAdvancedTimeSteppingAnalysisForModulation._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation":
        return self._Cast_PointLoadAdvancedTimeSteppingAnalysisForModulation(self)
