"""KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3834
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2541
    from mastapy.system_model.analyses_and_results.static_loads import _6920
    from mastapy.system_model.analyses_and_results.stability_analyses import (
        _3838,
        _3836,
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",)


Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis")


class KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis(
    _3834.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
):
    """KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_STABILITY_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
    )

    class _Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis:
        """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis to subclasses."""

        def __init__(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
            parent: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_stability_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            return self._parent._cast(
                _3834.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
            )

        @property
        def conical_gear_set_stability_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3798,
            )

            return self._parent._cast(_3798.ConicalGearSetStabilityAnalysis)

        @property
        def gear_set_stability_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3826,
            )

            return self._parent._cast(_3826.GearSetStabilityAnalysis)

        @property
        def specialised_assembly_stability_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3865,
            )

            return self._parent._cast(_3865.SpecialisedAssemblyStabilityAnalysis)

        @property
        def abstract_assembly_stability_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3765,
            )

            return self._parent._cast(_3765.AbstractAssemblyStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3846,
            )

            return self._parent._cast(_3846.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_stability_analysis(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
        ) -> "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis",
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
        instance_to_wrap: "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2541.KlingelnbergCycloPalloidHypoidGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(
        self: Self,
    ) -> "_6920.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_stability_analysis(
        self: Self,
    ) -> "List[_3838.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearsStabilityAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_stability_analysis(
        self: Self,
    ) -> "List[_3836.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.KlingelnbergCycloPalloidHypoidMeshesStabilityAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis":
        return self._Cast_KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis(self)
