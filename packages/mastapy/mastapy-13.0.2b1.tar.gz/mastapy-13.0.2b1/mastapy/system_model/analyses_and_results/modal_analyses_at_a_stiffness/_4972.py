"""StraightBevelPlanetGearModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _4967,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "StraightBevelPlanetGearModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2551


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelPlanetGearModalAnalysisAtAStiffness",)


Self = TypeVar("Self", bound="StraightBevelPlanetGearModalAnalysisAtAStiffness")


class StraightBevelPlanetGearModalAnalysisAtAStiffness(
    _4967.StraightBevelDiffGearModalAnalysisAtAStiffness
):
    """StraightBevelPlanetGearModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness"
    )

    class _Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness:
        """Special nested class for casting StraightBevelPlanetGearModalAnalysisAtAStiffness to subclasses."""

        def __init__(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
            parent: "StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            self._parent = parent

        @property
        def straight_bevel_diff_gear_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            return self._parent._cast(
                _4967.StraightBevelDiffGearModalAnalysisAtAStiffness
            )

        @property
        def bevel_gear_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4876,
            )

            return self._parent._cast(_4876.BevelGearModalAnalysisAtAStiffness)

        @property
        def agma_gleason_conical_gear_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4864,
            )

            return self._parent._cast(
                _4864.AGMAGleasonConicalGearModalAnalysisAtAStiffness
            )

        @property
        def conical_gear_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4892,
            )

            return self._parent._cast(_4892.ConicalGearModalAnalysisAtAStiffness)

        @property
        def gear_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4919,
            )

            return self._parent._cast(_4919.GearModalAnalysisAtAStiffness)

        @property
        def mountable_component_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4938,
            )

            return self._parent._cast(_4938.MountableComponentModalAnalysisAtAStiffness)

        @property
        def component_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4884,
            )

            return self._parent._cast(_4884.ComponentModalAnalysisAtAStiffness)

        @property
        def part_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4940,
            )

            return self._parent._cast(_4940.PartModalAnalysisAtAStiffness)

        @property
        def part_static_load_analysis_case(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def straight_bevel_planet_gear_modal_analysis_at_a_stiffness(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
        ) -> "StraightBevelPlanetGearModalAnalysisAtAStiffness":
            return self._parent

        def __getattr__(
            self: "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness",
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
        instance_to_wrap: "StraightBevelPlanetGearModalAnalysisAtAStiffness.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2551.StraightBevelPlanetGear":
        """mastapy.system_model.part_model.gears.StraightBevelPlanetGear

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
    ) -> "StraightBevelPlanetGearModalAnalysisAtAStiffness._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness":
        return self._Cast_StraightBevelPlanetGearModalAnalysisAtAStiffness(self)
