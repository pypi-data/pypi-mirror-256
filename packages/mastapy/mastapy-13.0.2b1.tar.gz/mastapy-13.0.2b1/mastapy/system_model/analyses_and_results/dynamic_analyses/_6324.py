"""CycloidalDiscDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6280
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "CycloidalDiscDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.cycloidal import _2571
    from mastapy.system_model.analyses_and_results.static_loads import _6862


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscDynamicAnalysis",)


Self = TypeVar("Self", bound="CycloidalDiscDynamicAnalysis")


class CycloidalDiscDynamicAnalysis(_6280.AbstractShaftDynamicAnalysis):
    """CycloidalDiscDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CycloidalDiscDynamicAnalysis")

    class _Cast_CycloidalDiscDynamicAnalysis:
        """Special nested class for casting CycloidalDiscDynamicAnalysis to subclasses."""

        def __init__(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
            parent: "CycloidalDiscDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def abstract_shaft_dynamic_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            return self._parent._cast(_6280.AbstractShaftDynamicAnalysis)

        @property
        def abstract_shaft_or_housing_dynamic_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6281

            return self._parent._cast(_6281.AbstractShaftOrHousingDynamicAnalysis)

        @property
        def component_dynamic_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6304

            return self._parent._cast(_6304.ComponentDynamicAnalysis)

        @property
        def part_dynamic_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6360

            return self._parent._cast(_6360.PartDynamicAnalysis)

        @property
        def part_fe_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cycloidal_disc_dynamic_analysis(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
        ) -> "CycloidalDiscDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CycloidalDiscDynamicAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2571.CycloidalDisc":
        """mastapy.system_model.part_model.cycloidal.CycloidalDisc

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6862.CycloidalDiscLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CycloidalDiscDynamicAnalysis._Cast_CycloidalDiscDynamicAnalysis":
        return self._Cast_CycloidalDiscDynamicAnalysis(self)
