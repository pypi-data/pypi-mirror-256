"""RootAssemblyCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2860
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "RootAssemblyCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.system_deflections.compound import (
        _2905,
    )
    from mastapy.system_model.analyses_and_results.power_flows.compound import _4263
    from mastapy.system_model.analyses_and_results.system_deflections import _2802
    from mastapy.system_model.fe import _2409
    from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1099
    from mastapy.utility_gui.charts import _1869


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyCompoundSystemDeflection",)


Self = TypeVar("Self", bound="RootAssemblyCompoundSystemDeflection")


class RootAssemblyCompoundSystemDeflection(_2860.AssemblyCompoundSystemDeflection):
    """RootAssemblyCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_RootAssemblyCompoundSystemDeflection")

    class _Cast_RootAssemblyCompoundSystemDeflection:
        """Special nested class for casting RootAssemblyCompoundSystemDeflection to subclasses."""

        def __init__(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
            parent: "RootAssemblyCompoundSystemDeflection",
        ):
            self._parent = parent

        @property
        def assembly_compound_system_deflection(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
        ):
            return self._parent._cast(_2860.AssemblyCompoundSystemDeflection)

        @property
        def abstract_assembly_compound_system_deflection(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2853,
            )

            return self._parent._cast(_2853.AbstractAssemblyCompoundSystemDeflection)

        @property
        def part_compound_system_deflection(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2933,
            )

            return self._parent._cast(_2933.PartCompoundSystemDeflection)

        @property
        def part_compound_analysis(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def root_assembly_compound_system_deflection(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
        ) -> "RootAssemblyCompoundSystemDeflection":
            return self._parent

        def __getattr__(
            self: "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection",
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
        self: Self, instance_to_wrap: "RootAssemblyCompoundSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_efficiency_results(self: Self) -> "_2905.DutyCycleEfficiencyResults":
        """mastapy.system_model.analyses_and_results.system_deflections.compound.DutyCycleEfficiencyResults

        Note:
            This property is readonly.
        """
        temp = self.wrapped.DutyCycleEfficiencyResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def root_assembly_compound_power_flow(
        self: Self,
    ) -> "_4263.RootAssemblyCompoundPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.compound.RootAssemblyCompoundPowerFlow

        Note:
            This property is readonly.
        """
        temp = self.wrapped.RootAssemblyCompoundPowerFlow

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: Self,
    ) -> "List[_2802.RootAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection]

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
    def bearing_race_f_es(self: Self) -> "List[_2409.RaceBearingFESystemDeflection]":
        """List[mastapy.system_model.fe.RaceBearingFESystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.BearingRaceFEs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: Self,
    ) -> "List[_2802.RootAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection]

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

    @enforce_parameter_types
    def peak_to_peak_transmission_error_chart(
        self: Self,
        mesh_duty_cycles: "List[_1099.CylindricalGearMeshMicroGeometryDutyCycle]",
        header: "str",
        x_axis_title: "str",
        y_axis_title: "str",
    ) -> "_1869.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Args:
            mesh_duty_cycles (List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMeshMicroGeometryDutyCycle])
            header (str)
            x_axis_title (str)
            y_axis_title (str)
        """
        mesh_duty_cycles = conversion.mp_to_pn_objects_in_dotnet_list(mesh_duty_cycles)
        header = str(header)
        x_axis_title = str(x_axis_title)
        y_axis_title = str(y_axis_title)
        method_result = self.wrapped.PeakToPeakTransmissionErrorChart(
            mesh_duty_cycles,
            header if header else "",
            x_axis_title if x_axis_title else "",
            y_axis_title if y_axis_title else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(
        self: Self,
    ) -> "RootAssemblyCompoundSystemDeflection._Cast_RootAssemblyCompoundSystemDeflection":
        return self._Cast_RootAssemblyCompoundSystemDeflection(self)
