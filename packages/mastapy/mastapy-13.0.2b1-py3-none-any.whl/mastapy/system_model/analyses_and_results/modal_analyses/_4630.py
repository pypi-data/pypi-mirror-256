"""ExternalCADModelModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4599
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "ExternalCADModelModalAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2454
    from mastapy.system_model.analyses_and_results.static_loads import _6886
    from mastapy.system_model.analyses_and_results.system_deflections import _2754


__docformat__ = "restructuredtext en"
__all__ = ("ExternalCADModelModalAnalysis",)


Self = TypeVar("Self", bound="ExternalCADModelModalAnalysis")


class ExternalCADModelModalAnalysis(_4599.ComponentModalAnalysis):
    """ExternalCADModelModalAnalysis

    This is a mastapy class.
    """

    TYPE = _EXTERNAL_CAD_MODEL_MODAL_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ExternalCADModelModalAnalysis")

    class _Cast_ExternalCADModelModalAnalysis:
        """Special nested class for casting ExternalCADModelModalAnalysis to subclasses."""

        def __init__(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
            parent: "ExternalCADModelModalAnalysis",
        ):
            self._parent = parent

        @property
        def component_modal_analysis(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
        ):
            return self._parent._cast(_4599.ComponentModalAnalysis)

        @property
        def part_modal_analysis(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4664

            return self._parent._cast(_4664.PartModalAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def external_cad_model_modal_analysis(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
        ) -> "ExternalCADModelModalAnalysis":
            return self._parent

        def __getattr__(
            self: "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ExternalCADModelModalAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2454.ExternalCADModel":
        """mastapy.system_model.part_model.ExternalCADModel

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6886.ExternalCADModelLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: Self,
    ) -> "_2754.ExternalCADModelSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ExternalCADModelSystemDeflection

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
    ) -> "ExternalCADModelModalAnalysis._Cast_ExternalCADModelModalAnalysis":
        return self._Cast_ExternalCADModelModalAnalysis(self)
