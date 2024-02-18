"""PowerLoadSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2837
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "PowerLoadSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2474
    from mastapy.system_model.analyses_and_results.static_loads import _6942
    from mastapy.system_model.analyses_and_results.power_flows import _4126
    from mastapy.system_model.analyses_and_results.system_deflections import _2835


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadSystemDeflection",)


Self = TypeVar("Self", bound="PowerLoadSystemDeflection")


class PowerLoadSystemDeflection(_2837.VirtualComponentSystemDeflection):
    """PowerLoadSystemDeflection

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PowerLoadSystemDeflection")

    class _Cast_PowerLoadSystemDeflection:
        """Special nested class for casting PowerLoadSystemDeflection to subclasses."""

        def __init__(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
            parent: "PowerLoadSystemDeflection",
        ):
            self._parent = parent

        @property
        def virtual_component_system_deflection(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            return self._parent._cast(_2837.VirtualComponentSystemDeflection)

        @property
        def mountable_component_system_deflection(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2784,
            )

            return self._parent._cast(_2784.MountableComponentSystemDeflection)

        @property
        def component_system_deflection(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2717,
            )

            return self._parent._cast(_2717.ComponentSystemDeflection)

        @property
        def part_system_deflection(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def power_load_system_deflection(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection",
        ) -> "PowerLoadSystemDeflection":
            return self._parent

        def __getattr__(
            self: "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PowerLoadSystemDeflection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def power(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Power

        if temp is None:
            return 0.0

        return temp

    @property
    def torque(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Torque

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: Self) -> "_2474.PowerLoad":
        """mastapy.system_model.part_model.PowerLoad

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6942.PowerLoadLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: Self) -> "_4126.PowerLoadPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.PowerLoadPowerFlow

        Note:
            This property is readonly.
        """
        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def transmission_error_to_other_power_loads(
        self: Self,
    ) -> "List[_2835.TransmissionErrorResult]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.TransmissionErrorResult]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.TransmissionErrorToOtherPowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "PowerLoadSystemDeflection._Cast_PowerLoadSystemDeflection":
        return self._Cast_PowerLoadSystemDeflection(self)
