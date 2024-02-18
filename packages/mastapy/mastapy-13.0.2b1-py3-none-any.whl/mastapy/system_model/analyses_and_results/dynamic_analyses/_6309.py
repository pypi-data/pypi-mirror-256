"""ConceptGearMeshDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6340
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "ConceptGearMeshDynamicAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.gears import _2307
    from mastapy.system_model.analyses_and_results.static_loads import _6845


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearMeshDynamicAnalysis",)


Self = TypeVar("Self", bound="ConceptGearMeshDynamicAnalysis")


class ConceptGearMeshDynamicAnalysis(_6340.GearMeshDynamicAnalysis):
    """ConceptGearMeshDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_MESH_DYNAMIC_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ConceptGearMeshDynamicAnalysis")

    class _Cast_ConceptGearMeshDynamicAnalysis:
        """Special nested class for casting ConceptGearMeshDynamicAnalysis to subclasses."""

        def __init__(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
            parent: "ConceptGearMeshDynamicAnalysis",
        ):
            self._parent = parent

        @property
        def gear_mesh_dynamic_analysis(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            return self._parent._cast(_6340.GearMeshDynamicAnalysis)

        @property
        def inter_mountable_component_connection_dynamic_analysis(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6346

            return self._parent._cast(
                _6346.InterMountableComponentConnectionDynamicAnalysis
            )

        @property
        def connection_dynamic_analysis(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6314

            return self._parent._cast(_6314.ConnectionDynamicAnalysis)

        @property
        def connection_fe_analysis(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.ConnectionFEAnalysis)

        @property
        def connection_static_load_analysis_case(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def concept_gear_mesh_dynamic_analysis(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
        ) -> "ConceptGearMeshDynamicAnalysis":
            return self._parent

        def __getattr__(
            self: "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ConceptGearMeshDynamicAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2307.ConceptGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: Self) -> "_6845.ConceptGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "ConceptGearMeshDynamicAnalysis._Cast_ConceptGearMeshDynamicAnalysis":
        return self._Cast_ConceptGearMeshDynamicAnalysis(self)
