"""CouplingHalfDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6358
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "CouplingHalfDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2586


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfDynamicAnalysis",)


Self = TypeVar("Self", bound="CouplingHalfDynamicAnalysis")


class CouplingHalfDynamicAnalysis(_6358.MountableComponentDynamicAnalysis):
    """CouplingHalfDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _COUPLING_HALF_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingHalfDynamicAnalysis")

    class _Cast_CouplingHalfDynamicAnalysis:
        """Special nested class for casting CouplingHalfDynamicAnalysis to subclasses."""

        def __init__(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
            parent: "CouplingHalfDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def mountable_component_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            return self._parent._cast(_6358.MountableComponentDynamicAnalysis)

        @property
        def component_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6304

            return self._parent._cast(_6304.ComponentDynamicAnalysis)

        @property
        def part_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6360

            return self._parent._cast(_6360.PartDynamicAnalysis)

        @property
        def part_fe_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_half_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6302

            return self._parent._cast(_6302.ClutchHalfDynamicAnalysis)

        @property
        def concept_coupling_half_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6307

            return self._parent._cast(_6307.ConceptCouplingHalfDynamicAnalysis)

        @property
        def cvt_pulley_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6321

            return self._parent._cast(_6321.CVTPulleyDynamicAnalysis)

        @property
        def part_to_part_shear_coupling_half_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6363

            return self._parent._cast(_6363.PartToPartShearCouplingHalfDynamicAnalysis)

        @property
        def pulley_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6369

            return self._parent._cast(_6369.PulleyDynamicAnalysis)

        @property
        def rolling_ring_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6374

            return self._parent._cast(_6374.RollingRingDynamicAnalysis)

        @property
        def spring_damper_half_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6385

            return self._parent._cast(_6385.SpringDamperHalfDynamicAnalysis)

        @property
        def synchroniser_half_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6395

            return self._parent._cast(_6395.SynchroniserHalfDynamicAnalysis)

        @property
        def synchroniser_part_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6396

            return self._parent._cast(_6396.SynchroniserPartDynamicAnalysis)

        @property
        def synchroniser_sleeve_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6397

            return self._parent._cast(_6397.SynchroniserSleeveDynamicAnalysis)

        @property
        def torque_converter_pump_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6400

            return self._parent._cast(_6400.TorqueConverterPumpDynamicAnalysis)

        @property
        def torque_converter_turbine_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6401

            return self._parent._cast(_6401.TorqueConverterTurbineDynamicAnalysis)

        @property
        def coupling_half_dynamic_analysis(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
        ) -> "CouplingHalfDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CouplingHalfDynamicAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2586.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CouplingHalfDynamicAnalysis._Cast_CouplingHalfDynamicAnalysis":
        return self._Cast_CouplingHalfDynamicAnalysis(self)
