"""CouplingHalfSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2784
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CouplingHalfSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2586
    from mastapy.system_model.analyses_and_results.power_flows import _4072


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfSystemDeflection",)


Self = TypeVar("Self", bound="CouplingHalfSystemDeflection")


class CouplingHalfSystemDeflection(_2784.MountableComponentSystemDeflection):
    """CouplingHalfSystemDeflection

    This is a mastapy class.
    """

    TYPE = _COUPLING_HALF_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingHalfSystemDeflection")

    class _Cast_CouplingHalfSystemDeflection:
        """Special nested class for casting CouplingHalfSystemDeflection to subclasses."""

        def __init__(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
            parent: "CouplingHalfSystemDeflection",
        ):
            self._parent = parent

        @property
        def mountable_component_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            return self._parent._cast(_2784.MountableComponentSystemDeflection)

        @property
        def component_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2717,
            )

            return self._parent._cast(_2717.ComponentSystemDeflection)

        @property
        def part_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2787,
            )

            return self._parent._cast(_2787.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7549

            return self._parent._cast(_7549.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def clutch_half_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2714,
            )

            return self._parent._cast(_2714.ClutchHalfSystemDeflection)

        @property
        def concept_coupling_half_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2720,
            )

            return self._parent._cast(_2720.ConceptCouplingHalfSystemDeflection)

        @property
        def cvt_pulley_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2735,
            )

            return self._parent._cast(_2735.CVTPulleySystemDeflection)

        @property
        def part_to_part_shear_coupling_half_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2789,
            )

            return self._parent._cast(_2789.PartToPartShearCouplingHalfSystemDeflection)

        @property
        def pulley_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2795,
            )

            return self._parent._cast(_2795.PulleySystemDeflection)

        @property
        def rolling_ring_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2801,
            )

            return self._parent._cast(_2801.RollingRingSystemDeflection)

        @property
        def spring_damper_half_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2813,
            )

            return self._parent._cast(_2813.SpringDamperHalfSystemDeflection)

        @property
        def synchroniser_half_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2823,
            )

            return self._parent._cast(_2823.SynchroniserHalfSystemDeflection)

        @property
        def synchroniser_part_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2824,
            )

            return self._parent._cast(_2824.SynchroniserPartSystemDeflection)

        @property
        def synchroniser_sleeve_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2825,
            )

            return self._parent._cast(_2825.SynchroniserSleeveSystemDeflection)

        @property
        def torque_converter_pump_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2831,
            )

            return self._parent._cast(_2831.TorqueConverterPumpSystemDeflection)

        @property
        def torque_converter_turbine_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2833,
            )

            return self._parent._cast(_2833.TorqueConverterTurbineSystemDeflection)

        @property
        def coupling_half_system_deflection(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
        ) -> "CouplingHalfSystemDeflection":
            return self._parent

        def __getattr__(
            self: "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CouplingHalfSystemDeflection.TYPE"):
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
    def power_flow_results(self: Self) -> "_4072.CouplingHalfPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.CouplingHalfPowerFlow

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
    ) -> "CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection":
        return self._Cast_CouplingHalfSystemDeflection(self)
