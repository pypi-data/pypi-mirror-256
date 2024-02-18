"""RootAssemblySystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2694
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "RootAssemblySystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2476
    from mastapy.system_model.analyses_and_results.power_flows import _4133
    from mastapy.system_model.analyses_and_results.system_deflections import (
        _2827,
        _2718,
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblySystemDeflection",)


Self = TypeVar("Self", bound="RootAssemblySystemDeflection")


class RootAssemblySystemDeflection(_2694.AssemblySystemDeflection):
    """RootAssemblySystemDeflection

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_RootAssemblySystemDeflection")

    class _Cast_RootAssemblySystemDeflection:
        """Special nested class for casting RootAssemblySystemDeflection to subclasses."""

        def __init__(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
            parent: "RootAssemblySystemDeflection",
        ):
            self._parent = parent

        @property
        def assembly_system_deflection(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            return self._parent._cast(_2694.AssemblySystemDeflection)

        @property
        def abstract_assembly_system_deflection(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2687,
            )

            return self._parent._cast(_2687.AbstractAssemblySystemDeflection)

        @property
        def part_system_deflection(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def root_assembly_system_deflection(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
        ) -> "RootAssemblySystemDeflection":
            return self._parent

        def __getattr__(
            self: "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "RootAssemblySystemDeflection.TYPE"):
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
    def power_flow_results(self: Self) -> "_4133.RootAssemblyPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow

        Note:
            This property is readonly.
        """
        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_inputs(self: Self) -> "_2827.SystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.SystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_deflection_results(
        self: Self,
    ) -> "List[_2718.ConcentricPartGroupCombinationSystemDeflectionResults]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConcentricPartGroupCombinationSystemDeflectionResults]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ShaftDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "RootAssemblySystemDeflection._Cast_RootAssemblySystemDeflection":
        return self._Cast_RootAssemblySystemDeflection(self)
