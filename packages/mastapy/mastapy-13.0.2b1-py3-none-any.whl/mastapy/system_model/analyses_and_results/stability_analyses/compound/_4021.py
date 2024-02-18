"""VirtualComponentCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3976
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "VirtualComponentCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.stability_analyses import _3892


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundStabilityAnalysis",)


Self = TypeVar("Self", bound="VirtualComponentCompoundStabilityAnalysis")


class VirtualComponentCompoundStabilityAnalysis(
    _3976.MountableComponentCompoundStabilityAnalysis
):
    """VirtualComponentCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_STABILITY_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_VirtualComponentCompoundStabilityAnalysis"
    )

    class _Cast_VirtualComponentCompoundStabilityAnalysis:
        """Special nested class for casting VirtualComponentCompoundStabilityAnalysis to subclasses."""

        def __init__(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
            parent: "VirtualComponentCompoundStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def mountable_component_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            return self._parent._cast(_3976.MountableComponentCompoundStabilityAnalysis)

        @property
        def component_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3924,
            )

            return self._parent._cast(_3924.ComponentCompoundStabilityAnalysis)

        @property
        def part_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3978,
            )

            return self._parent._cast(_3978.PartCompoundStabilityAnalysis)

        @property
        def part_compound_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def mass_disc_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3974,
            )

            return self._parent._cast(_3974.MassDiscCompoundStabilityAnalysis)

        @property
        def measurement_component_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3975,
            )

            return self._parent._cast(
                _3975.MeasurementComponentCompoundStabilityAnalysis
            )

        @property
        def point_load_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3985,
            )

            return self._parent._cast(_3985.PointLoadCompoundStabilityAnalysis)

        @property
        def power_load_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3986,
            )

            return self._parent._cast(_3986.PowerLoadCompoundStabilityAnalysis)

        @property
        def unbalanced_mass_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4020,
            )

            return self._parent._cast(_4020.UnbalancedMassCompoundStabilityAnalysis)

        @property
        def virtual_component_compound_stability_analysis(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
        ) -> "VirtualComponentCompoundStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis",
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
        self: Self, instance_to_wrap: "VirtualComponentCompoundStabilityAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_3892.VirtualComponentStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.VirtualComponentStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_3892.VirtualComponentStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.VirtualComponentStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "VirtualComponentCompoundStabilityAnalysis._Cast_VirtualComponentCompoundStabilityAnalysis":
        return self._Cast_VirtualComponentCompoundStabilityAnalysis(self)
