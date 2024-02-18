"""RootAssemblyStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3772
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "RootAssemblyStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2476
    from mastapy.system_model.analyses_and_results.stability_analyses import _3872


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyStabilityAnalysis",)


Self = TypeVar("Self", bound="RootAssemblyStabilityAnalysis")


class RootAssemblyStabilityAnalysis(_3772.AssemblyStabilityAnalysis):
    """RootAssemblyStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_RootAssemblyStabilityAnalysis")

    class _Cast_RootAssemblyStabilityAnalysis:
        """Special nested class for casting RootAssemblyStabilityAnalysis to subclasses."""

        def __init__(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
            parent: "RootAssemblyStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def assembly_stability_analysis(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ):
            return self._parent._cast(_3772.AssemblyStabilityAnalysis)

        @property
        def abstract_assembly_stability_analysis(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3765,
            )

            return self._parent._cast(_3765.AbstractAssemblyStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3846,
            )

            return self._parent._cast(_3846.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def root_assembly_stability_analysis(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
        ) -> "RootAssemblyStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "RootAssemblyStabilityAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2476.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stability_analysis_inputs(self: Self) -> "_3872.StabilityAnalysis":
        """mastapy.system_model.analyses_and_results.stability_analyses.StabilityAnalysis

        Note:
            This property is readonly.
        """
        temp = self.wrapped.StabilityAnalysisInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "RootAssemblyStabilityAnalysis._Cast_RootAssemblyStabilityAnalysis":
        return self._Cast_RootAssemblyStabilityAnalysis(self)
