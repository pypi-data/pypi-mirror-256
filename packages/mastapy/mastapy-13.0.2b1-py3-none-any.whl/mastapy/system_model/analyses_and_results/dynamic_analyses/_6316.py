"""CouplingConnectionDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6346
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "CouplingConnectionDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.couplings import _2348


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionDynamicAnalysis",)


Self = TypeVar("Self", bound="CouplingConnectionDynamicAnalysis")


class CouplingConnectionDynamicAnalysis(
    _6346.InterMountableComponentConnectionDynamicAnalysis
):
    """CouplingConnectionDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _COUPLING_CONNECTION_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingConnectionDynamicAnalysis")

    class _Cast_CouplingConnectionDynamicAnalysis:
        """Special nested class for casting CouplingConnectionDynamicAnalysis to subclasses."""

        def __init__(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
            parent: "CouplingConnectionDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def inter_mountable_component_connection_dynamic_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            return self._parent._cast(
                _6346.InterMountableComponentConnectionDynamicAnalysis
            )

        @property
        def connection_dynamic_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6314

            return self._parent._cast(_6314.ConnectionDynamicAnalysis)

        @property
        def connection_fe_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.ConnectionFEAnalysis)

        @property
        def connection_static_load_analysis_case(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_connection_dynamic_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6300

            return self._parent._cast(_6300.ClutchConnectionDynamicAnalysis)

        @property
        def concept_coupling_connection_dynamic_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6305

            return self._parent._cast(_6305.ConceptCouplingConnectionDynamicAnalysis)

        @property
        def part_to_part_shear_coupling_connection_dynamic_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6361

            return self._parent._cast(
                _6361.PartToPartShearCouplingConnectionDynamicAnalysis
            )

        @property
        def spring_damper_connection_dynamic_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6383

            return self._parent._cast(_6383.SpringDamperConnectionDynamicAnalysis)

        @property
        def torque_converter_connection_dynamic_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6398

            return self._parent._cast(_6398.TorqueConverterConnectionDynamicAnalysis)

        @property
        def coupling_connection_dynamic_analysis(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
        ) -> "CouplingConnectionDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
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
        self: Self, instance_to_wrap: "CouplingConnectionDynamicAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2348.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis":
        return self._Cast_CouplingConnectionDynamicAnalysis(self)
