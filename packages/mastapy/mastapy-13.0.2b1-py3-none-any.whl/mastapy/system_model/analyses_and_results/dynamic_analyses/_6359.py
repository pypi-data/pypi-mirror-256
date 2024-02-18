"""OilSealDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6315
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "OilSealDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2468
    from mastapy.system_model.analyses_and_results.static_loads import _6929


__docformat__ = "restructuredtext en"
__all__ = ("OilSealDynamicAnalysis",)


Self = TypeVar("Self", bound="OilSealDynamicAnalysis")


class OilSealDynamicAnalysis(_6315.ConnectorDynamicAnalysis):
    """OilSealDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _OIL_SEAL_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_OilSealDynamicAnalysis")

    class _Cast_OilSealDynamicAnalysis:
        """Special nested class for casting OilSealDynamicAnalysis to subclasses."""

        def __init__(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
            parent: "OilSealDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def connector_dynamic_analysis(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            return self._parent._cast(_6315.ConnectorDynamicAnalysis)

        @property
        def mountable_component_dynamic_analysis(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6358

            return self._parent._cast(_6358.MountableComponentDynamicAnalysis)

        @property
        def component_dynamic_analysis(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6304

            return self._parent._cast(_6304.ComponentDynamicAnalysis)

        @property
        def part_dynamic_analysis(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6360

            return self._parent._cast(_6360.PartDynamicAnalysis)

        @property
        def part_fe_analysis(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def oil_seal_dynamic_analysis(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis",
        ) -> "OilSealDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "OilSealDynamicAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2468.OilSeal":
        """mastapy.system_model.part_model.OilSeal

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6929.OilSealLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "OilSealDynamicAnalysis._Cast_OilSealDynamicAnalysis":
        return self._Cast_OilSealDynamicAnalysis(self)
