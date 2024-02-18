"""TorqueConverterDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6317
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "TorqueConverterDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2609
    from mastapy.system_model.analyses_and_results.static_loads import _6976


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterDynamicAnalysis",)


Self = TypeVar("Self", bound="TorqueConverterDynamicAnalysis")


class TorqueConverterDynamicAnalysis(_6317.CouplingDynamicAnalysis):
    """TorqueConverterDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_TorqueConverterDynamicAnalysis")

    class _Cast_TorqueConverterDynamicAnalysis:
        """Special nested class for casting TorqueConverterDynamicAnalysis to subclasses."""

        def __init__(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
            parent: "TorqueConverterDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_dynamic_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            return self._parent._cast(_6317.CouplingDynamicAnalysis)

        @property
        def specialised_assembly_dynamic_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6379

            return self._parent._cast(_6379.SpecialisedAssemblyDynamicAnalysis)

        @property
        def abstract_assembly_dynamic_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6279

            return self._parent._cast(_6279.AbstractAssemblyDynamicAnalysis)

        @property
        def part_dynamic_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6360

            return self._parent._cast(_6360.PartDynamicAnalysis)

        @property
        def part_fe_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def torque_converter_dynamic_analysis(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
        ) -> "TorqueConverterDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "TorqueConverterDynamicAnalysis.TYPE"):
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
    def cast_to(
        self: Self,
    ) -> "TorqueConverterDynamicAnalysis._Cast_TorqueConverterDynamicAnalysis":
        return self._Cast_TorqueConverterDynamicAnalysis(self)
