"""HypoidGearSetModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4580
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "HypoidGearSetModalAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2537
    from mastapy.system_model.analyses_and_results.static_loads import _6910
    from mastapy.system_model.analyses_and_results.system_deflections import _2766
    from mastapy.system_model.analyses_and_results.modal_analyses import _4642, _4641


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearSetModalAnalysis",)


Self = TypeVar("Self", bound="HypoidGearSetModalAnalysis")


class HypoidGearSetModalAnalysis(_4580.AGMAGleasonConicalGearSetModalAnalysis):
    """HypoidGearSetModalAnalysis

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_SET_MODAL_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_HypoidGearSetModalAnalysis")

    class _Cast_HypoidGearSetModalAnalysis:
        """Special nested class for casting HypoidGearSetModalAnalysis to subclasses."""

        def __init__(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
            parent: "HypoidGearSetModalAnalysis",
        ):
            self._parent = parent

        @property
        def agma_gleason_conical_gear_set_modal_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            return self._parent._cast(_4580.AGMAGleasonConicalGearSetModalAnalysis)

        @property
        def conical_gear_set_modal_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4608

            return self._parent._cast(_4608.ConicalGearSetModalAnalysis)

        @property
        def gear_set_modal_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4639

            return self._parent._cast(_4639.GearSetModalAnalysis)

        @property
        def specialised_assembly_modal_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4684

            return self._parent._cast(_4684.SpecialisedAssemblyModalAnalysis)

        @property
        def abstract_assembly_modal_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4574

            return self._parent._cast(_4574.AbstractAssemblyModalAnalysis)

        @property
        def part_modal_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4664

            return self._parent._cast(_4664.PartModalAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def hypoid_gear_set_modal_analysis(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
        ) -> "HypoidGearSetModalAnalysis":
            return self._parent

        def __getattr__(
            self: "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "HypoidGearSetModalAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2537.HypoidGearSet":
        """mastapy.system_model.part_model.gears.HypoidGearSet

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6910.HypoidGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: Self) -> "_2766.HypoidGearSetSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.HypoidGearSetSystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def hypoid_gears_modal_analysis(
        self: Self,
    ) -> "List[_4642.HypoidGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.HypoidGearsModalAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_meshes_modal_analysis(
        self: Self,
    ) -> "List[_4641.HypoidGearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearMeshModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.HypoidMeshesModalAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "HypoidGearSetModalAnalysis._Cast_HypoidGearSetModalAnalysis":
        return self._Cast_HypoidGearSetModalAnalysis(self)
