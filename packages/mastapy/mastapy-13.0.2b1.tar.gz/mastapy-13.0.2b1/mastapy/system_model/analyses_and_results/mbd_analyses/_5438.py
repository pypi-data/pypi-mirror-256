"""FlexiblePinAssemblyMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5491
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "FlexiblePinAssemblyMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2456
    from mastapy.system_model.analyses_and_results.static_loads import _6891


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAssemblyMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="FlexiblePinAssemblyMultibodyDynamicsAnalysis")


class FlexiblePinAssemblyMultibodyDynamicsAnalysis(
    _5491.SpecialisedAssemblyMultibodyDynamicsAnalysis
):
    """FlexiblePinAssemblyMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis"
    )

    class _Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis:
        """Special nested class for casting FlexiblePinAssemblyMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
            parent: "FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def specialised_assembly_multibody_dynamics_analysis(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            return self._parent._cast(
                _5491.SpecialisedAssemblyMultibodyDynamicsAnalysis
            )

        @property
        def abstract_assembly_multibody_dynamics_analysis(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5378

            return self._parent._cast(_5378.AbstractAssemblyMultibodyDynamicsAnalysis)

        @property
        def part_multibody_dynamics_analysis(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5469

            return self._parent._cast(_5469.PartMultibodyDynamicsAnalysis)

        @property
        def part_time_series_load_analysis_case(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7551

            return self._parent._cast(_7551.PartTimeSeriesLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def flexible_pin_assembly_multibody_dynamics_analysis(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
        ) -> "FlexiblePinAssemblyMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis",
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
        instance_to_wrap: "FlexiblePinAssemblyMultibodyDynamicsAnalysis.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2456.FlexiblePinAssembly":
        """mastapy.system_model.part_model.FlexiblePinAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6891.FlexiblePinAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "FlexiblePinAssemblyMultibodyDynamicsAnalysis._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis":
        return self._Cast_FlexiblePinAssemblyMultibodyDynamicsAnalysis(self)
