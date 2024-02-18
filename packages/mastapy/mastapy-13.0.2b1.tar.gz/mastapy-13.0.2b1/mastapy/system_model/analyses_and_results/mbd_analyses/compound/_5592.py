"""GuideDxfModelCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5556
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "GuideDxfModelCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2457
    from mastapy.system_model.analyses_and_results.mbd_analyses import _5443


__docformat__ = "restructuredtext en"
__all__ = ("GuideDxfModelCompoundMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="GuideDxfModelCompoundMultibodyDynamicsAnalysis")


class GuideDxfModelCompoundMultibodyDynamicsAnalysis(
    _5556.ComponentCompoundMultibodyDynamicsAnalysis
):
    """GuideDxfModelCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis"
    )

    class _Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis:
        """Special nested class for casting GuideDxfModelCompoundMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis",
            parent: "GuideDxfModelCompoundMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def component_compound_multibody_dynamics_analysis(
            self: "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(_5556.ComponentCompoundMultibodyDynamicsAnalysis)

        @property
        def part_compound_multibody_dynamics_analysis(
            self: "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
                _5610,
            )

            return self._parent._cast(_5610.PartCompoundMultibodyDynamicsAnalysis)

        @property
        def part_compound_analysis(
            self: "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def guide_dxf_model_compound_multibody_dynamics_analysis(
            self: "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis",
        ) -> "GuideDxfModelCompoundMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis",
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
        instance_to_wrap: "GuideDxfModelCompoundMultibodyDynamicsAnalysis.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2457.GuideDxfModel":
        """mastapy.system_model.part_model.GuideDxfModel

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_5443.GuideDxfModelMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.GuideDxfModelMultibodyDynamicsAnalysis]

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
    def component_analysis_cases(
        self: Self,
    ) -> "List[_5443.GuideDxfModelMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.GuideDxfModelMultibodyDynamicsAnalysis]

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
    def cast_to(
        self: Self,
    ) -> "GuideDxfModelCompoundMultibodyDynamicsAnalysis._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis":
        return self._Cast_GuideDxfModelCompoundMultibodyDynamicsAnalysis(self)
