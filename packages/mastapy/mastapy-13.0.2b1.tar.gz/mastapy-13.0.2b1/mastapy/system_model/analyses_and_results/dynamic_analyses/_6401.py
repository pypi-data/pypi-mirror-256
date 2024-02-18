"""TorqueConverterTurbineDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6318
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "TorqueConverterTurbineDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2612
    from mastapy.system_model.analyses_and_results.static_loads import _6978


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterTurbineDynamicAnalysis",)


Self = TypeVar("Self", bound="TorqueConverterTurbineDynamicAnalysis")


class TorqueConverterTurbineDynamicAnalysis(_6318.CouplingHalfDynamicAnalysis):
    """TorqueConverterTurbineDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_TURBINE_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_TorqueConverterTurbineDynamicAnalysis"
    )

    class _Cast_TorqueConverterTurbineDynamicAnalysis:
        """Special nested class for casting TorqueConverterTurbineDynamicAnalysis to subclasses."""

        def __init__(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
            parent: "TorqueConverterTurbineDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_half_dynamic_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            return self._parent._cast(_6318.CouplingHalfDynamicAnalysis)

        @property
        def mountable_component_dynamic_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6358

            return self._parent._cast(_6358.MountableComponentDynamicAnalysis)

        @property
        def component_dynamic_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6304

            return self._parent._cast(_6304.ComponentDynamicAnalysis)

        @property
        def part_dynamic_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6360

            return self._parent._cast(_6360.PartDynamicAnalysis)

        @property
        def part_fe_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def torque_converter_turbine_dynamic_analysis(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
        ) -> "TorqueConverterTurbineDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis",
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
        self: Self, instance_to_wrap: "TorqueConverterTurbineDynamicAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2612.TorqueConverterTurbine":
        """mastapy.system_model.part_model.couplings.TorqueConverterTurbine

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6978.TorqueConverterTurbineLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase

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
    ) -> "TorqueConverterTurbineDynamicAnalysis._Cast_TorqueConverterTurbineDynamicAnalysis":
        return self._Cast_TorqueConverterTurbineDynamicAnalysis(self)
