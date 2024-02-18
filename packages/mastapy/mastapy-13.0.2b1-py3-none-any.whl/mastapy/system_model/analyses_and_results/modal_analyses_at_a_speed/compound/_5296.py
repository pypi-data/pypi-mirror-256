"""CylindricalGearCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5307,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "CylindricalGearCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2527
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5167,
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearCompoundModalAnalysisAtASpeed",)


Self = TypeVar("Self", bound="CylindricalGearCompoundModalAnalysisAtASpeed")


class CylindricalGearCompoundModalAnalysisAtASpeed(
    _5307.GearCompoundModalAnalysisAtASpeed
):
    """CylindricalGearCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CylindricalGearCompoundModalAnalysisAtASpeed"
    )

    class _Cast_CylindricalGearCompoundModalAnalysisAtASpeed:
        """Special nested class for casting CylindricalGearCompoundModalAnalysisAtASpeed to subclasses."""

        def __init__(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
            parent: "CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            self._parent = parent

        @property
        def gear_compound_modal_analysis_at_a_speed(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            return self._parent._cast(_5307.GearCompoundModalAnalysisAtASpeed)

        @property
        def mountable_component_compound_modal_analysis_at_a_speed(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5326,
            )

            return self._parent._cast(
                _5326.MountableComponentCompoundModalAnalysisAtASpeed
            )

        @property
        def component_compound_modal_analysis_at_a_speed(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5274,
            )

            return self._parent._cast(_5274.ComponentCompoundModalAnalysisAtASpeed)

        @property
        def part_compound_modal_analysis_at_a_speed(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5328,
            )

            return self._parent._cast(_5328.PartCompoundModalAnalysisAtASpeed)

        @property
        def part_compound_analysis(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cylindrical_planet_gear_compound_modal_analysis_at_a_speed(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
                _5299,
            )

            return self._parent._cast(
                _5299.CylindricalPlanetGearCompoundModalAnalysisAtASpeed
            )

        @property
        def cylindrical_gear_compound_modal_analysis_at_a_speed(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
        ) -> "CylindricalGearCompoundModalAnalysisAtASpeed":
            return self._parent

        def __getattr__(
            self: "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed",
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
        instance_to_wrap: "CylindricalGearCompoundModalAnalysisAtASpeed.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2527.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear

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
    ) -> "List[_5167.CylindricalGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.CylindricalGearModalAnalysisAtASpeed]

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
    def planetaries(self: Self) -> "List[CylindricalGearCompoundModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound.CylindricalGearCompoundModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_5167.CylindricalGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.CylindricalGearModalAnalysisAtASpeed]

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
    ) -> "CylindricalGearCompoundModalAnalysisAtASpeed._Cast_CylindricalGearCompoundModalAnalysisAtASpeed":
        return self._Cast_CylindricalGearCompoundModalAnalysisAtASpeed(self)
