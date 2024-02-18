"""CVTPulleyModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4673
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "CVTPulleyModalAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2589
    from mastapy.system_model.analyses_and_results.system_deflections import _2735


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleyModalAnalysis",)


Self = TypeVar("Self", bound="CVTPulleyModalAnalysis")


class CVTPulleyModalAnalysis(_4673.PulleyModalAnalysis):
    """CVTPulleyModalAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_MODAL_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CVTPulleyModalAnalysis")

    class _Cast_CVTPulleyModalAnalysis:
        """Special nested class for casting CVTPulleyModalAnalysis to subclasses."""

        def __init__(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
            parent: "CVTPulleyModalAnalysis",
        ):
            self._parent = parent

        @property
        def pulley_modal_analysis(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            return self._parent._cast(_4673.PulleyModalAnalysis)

        @property
        def coupling_half_modal_analysis(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4613

            return self._parent._cast(_4613.CouplingHalfModalAnalysis)

        @property
        def mountable_component_modal_analysis(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4660

            return self._parent._cast(_4660.MountableComponentModalAnalysis)

        @property
        def component_modal_analysis(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4599

            return self._parent._cast(_4599.ComponentModalAnalysis)

        @property
        def part_modal_analysis(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4664

            return self._parent._cast(_4664.PartModalAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cvt_pulley_modal_analysis(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis",
        ) -> "CVTPulleyModalAnalysis":
            return self._parent

        def __getattr__(
            self: "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CVTPulleyModalAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2589.CVTPulley":
        """mastapy.system_model.part_model.couplings.CVTPulley

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: Self) -> "_2735.CVTPulleySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CVTPulleySystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "CVTPulleyModalAnalysis._Cast_CVTPulleyModalAnalysis":
        return self._Cast_CVTPulleyModalAnalysis(self)
