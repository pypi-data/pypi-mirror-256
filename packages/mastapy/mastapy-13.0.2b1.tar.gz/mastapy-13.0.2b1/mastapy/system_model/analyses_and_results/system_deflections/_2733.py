"""CouplingSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2808
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CouplingSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2585
    from mastapy.system_model.analyses_and_results.power_flows import _4073


__docformat__ = "restructuredtext en"
__all__ = ("CouplingSystemDeflection",)


Self = TypeVar("Self", bound="CouplingSystemDeflection")


class CouplingSystemDeflection(_2808.SpecialisedAssemblySystemDeflection):
    """CouplingSystemDeflection

    This is a mastapy class.
    """

    TYPE = _COUPLING_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingSystemDeflection")

    class _Cast_CouplingSystemDeflection:
        """Special nested class for casting CouplingSystemDeflection to subclasses."""

        def __init__(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
            parent: "CouplingSystemDeflection",
        ):
            self._parent = parent

        @property
        def specialised_assembly_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            return self._parent._cast(_2808.SpecialisedAssemblySystemDeflection)

        @property
        def abstract_assembly_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2687,
            )

            return self._parent._cast(_2687.AbstractAssemblySystemDeflection)

        @property
        def part_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2715,
            )

            return self._parent._cast(_2715.ClutchSystemDeflection)

        @property
        def concept_coupling_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2721,
            )

            return self._parent._cast(_2721.ConceptCouplingSystemDeflection)

        @property
        def part_to_part_shear_coupling_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2790,
            )

            return self._parent._cast(_2790.PartToPartShearCouplingSystemDeflection)

        @property
        def spring_damper_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2814,
            )

            return self._parent._cast(_2814.SpringDamperSystemDeflection)

        @property
        def torque_converter_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2832,
            )

            return self._parent._cast(_2832.TorqueConverterSystemDeflection)

        @property
        def coupling_system_deflection(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection",
        ) -> "CouplingSystemDeflection":
            return self._parent

        def __getattr__(
            self: "CouplingSystemDeflection._Cast_CouplingSystemDeflection", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CouplingSystemDeflection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2585.Coupling":
        """mastapy.system_model.part_model.couplings.Coupling

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: Self) -> "_4073.CouplingPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow

        Note:
            This property is readonly.
        """
        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CouplingSystemDeflection._Cast_CouplingSystemDeflection":
        return self._Cast_CouplingSystemDeflection(self)
