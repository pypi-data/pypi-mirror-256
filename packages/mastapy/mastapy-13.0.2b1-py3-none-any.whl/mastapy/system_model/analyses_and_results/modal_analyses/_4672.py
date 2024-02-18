"""PowerLoadModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4708
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "PowerLoadModalAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2474
    from mastapy.system_model.analyses_and_results.static_loads import _6942
    from mastapy.system_model.analyses_and_results.system_deflections import _2794


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadModalAnalysis",)


Self = TypeVar("Self", bound="PowerLoadModalAnalysis")


class PowerLoadModalAnalysis(_4708.VirtualComponentModalAnalysis):
    """PowerLoadModalAnalysis

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_MODAL_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PowerLoadModalAnalysis")

    class _Cast_PowerLoadModalAnalysis:
        """Special nested class for casting PowerLoadModalAnalysis to subclasses."""

        def __init__(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
            parent: "PowerLoadModalAnalysis",
        ):
            self._parent = parent

        @property
        def virtual_component_modal_analysis(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ):
            return self._parent._cast(_4708.VirtualComponentModalAnalysis)

        @property
        def mountable_component_modal_analysis(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4660

            return self._parent._cast(_4660.MountableComponentModalAnalysis)

        @property
        def component_modal_analysis(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4599

            return self._parent._cast(_4599.ComponentModalAnalysis)

        @property
        def part_modal_analysis(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4664

            return self._parent._cast(_4664.PartModalAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def power_load_modal_analysis(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis",
        ) -> "PowerLoadModalAnalysis":
            return self._parent

        def __getattr__(
            self: "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PowerLoadModalAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2474.PowerLoad":
        """mastapy.system_model.part_model.PowerLoad

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6942.PowerLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: Self) -> "_2794.PowerLoadSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.PowerLoadSystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "PowerLoadModalAnalysis._Cast_PowerLoadModalAnalysis":
        return self._Cast_PowerLoadModalAnalysis(self)
