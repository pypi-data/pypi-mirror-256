"""BeltDriveCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3997
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "BeltDriveCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2578
    from mastapy.system_model.analyses_and_results.stability_analyses import _3775


__docformat__ = "restructuredtext en"
__all__ = ("BeltDriveCompoundStabilityAnalysis",)


Self = TypeVar("Self", bound="BeltDriveCompoundStabilityAnalysis")


class BeltDriveCompoundStabilityAnalysis(
    _3997.SpecialisedAssemblyCompoundStabilityAnalysis
):
    """BeltDriveCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _BELT_DRIVE_COMPOUND_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BeltDriveCompoundStabilityAnalysis")

    class _Cast_BeltDriveCompoundStabilityAnalysis:
        """Special nested class for casting BeltDriveCompoundStabilityAnalysis to subclasses."""

        def __init__(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
            parent: "BeltDriveCompoundStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def specialised_assembly_compound_stability_analysis(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
        ):
            return self._parent._cast(
                _3997.SpecialisedAssemblyCompoundStabilityAnalysis
            )

        @property
        def abstract_assembly_compound_stability_analysis(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3899,
            )

            return self._parent._cast(_3899.AbstractAssemblyCompoundStabilityAnalysis)

        @property
        def part_compound_stability_analysis(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3978,
            )

            return self._parent._cast(_3978.PartCompoundStabilityAnalysis)

        @property
        def part_compound_analysis(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cvt_compound_stability_analysis(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3940,
            )

            return self._parent._cast(_3940.CVTCompoundStabilityAnalysis)

        @property
        def belt_drive_compound_stability_analysis(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
        ) -> "BeltDriveCompoundStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis",
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
        self: Self, instance_to_wrap: "BeltDriveCompoundStabilityAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2578.BeltDrive":
        """mastapy.system_model.part_model.couplings.BeltDrive

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: Self) -> "_2578.BeltDrive":
        """mastapy.system_model.part_model.couplings.BeltDrive

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: Self,
    ) -> "List[_3775.BeltDriveStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.BeltDriveStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(self: Self) -> "List[_3775.BeltDriveStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.BeltDriveStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "BeltDriveCompoundStabilityAnalysis._Cast_BeltDriveCompoundStabilityAnalysis":
        return self._Cast_BeltDriveCompoundStabilityAnalysis(self)
