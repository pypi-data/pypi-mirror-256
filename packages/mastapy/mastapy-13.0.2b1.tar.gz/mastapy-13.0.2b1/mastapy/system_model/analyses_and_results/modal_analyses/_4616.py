"""CVTModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4584
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CVT_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses", "CVTModalAnalysis"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2588
    from mastapy.system_model.analyses_and_results.system_deflections import _2736


__docformat__ = "restructuredtext en"
__all__ = ("CVTModalAnalysis",)


Self = TypeVar("Self", bound="CVTModalAnalysis")


class CVTModalAnalysis(_4584.BeltDriveModalAnalysis):
    """CVTModalAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_MODAL_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CVTModalAnalysis")

    class _Cast_CVTModalAnalysis:
        """Special nested class for casting CVTModalAnalysis to subclasses."""

        def __init__(
            self: "CVTModalAnalysis._Cast_CVTModalAnalysis", parent: "CVTModalAnalysis"
        ):
            self._parent = parent

        @property
        def belt_drive_modal_analysis(self: "CVTModalAnalysis._Cast_CVTModalAnalysis"):
            return self._parent._cast(_4584.BeltDriveModalAnalysis)

        @property
        def specialised_assembly_modal_analysis(
            self: "CVTModalAnalysis._Cast_CVTModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4684

            return self._parent._cast(_4684.SpecialisedAssemblyModalAnalysis)

        @property
        def abstract_assembly_modal_analysis(
            self: "CVTModalAnalysis._Cast_CVTModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4574

            return self._parent._cast(_4574.AbstractAssemblyModalAnalysis)

        @property
        def part_modal_analysis(self: "CVTModalAnalysis._Cast_CVTModalAnalysis"):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4664

            return self._parent._cast(_4664.PartModalAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CVTModalAnalysis._Cast_CVTModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(self: "CVTModalAnalysis._Cast_CVTModalAnalysis"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(self: "CVTModalAnalysis._Cast_CVTModalAnalysis"):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CVTModalAnalysis._Cast_CVTModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(self: "CVTModalAnalysis._Cast_CVTModalAnalysis"):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cvt_modal_analysis(
            self: "CVTModalAnalysis._Cast_CVTModalAnalysis",
        ) -> "CVTModalAnalysis":
            return self._parent

        def __getattr__(self: "CVTModalAnalysis._Cast_CVTModalAnalysis", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CVTModalAnalysis.TYPE"):
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
    def cast_to(self: Self) -> "CVTModalAnalysis._Cast_CVTModalAnalysis":
        return self._Cast_CVTModalAnalysis(self)
