"""CylindricalPlanetGearModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4623
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "CylindricalPlanetGearModalAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2529
    from mastapy.system_model.analyses_and_results.system_deflections import _2752


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearModalAnalysis",)


Self = TypeVar("Self", bound="CylindricalPlanetGearModalAnalysis")


class CylindricalPlanetGearModalAnalysis(_4623.CylindricalGearModalAnalysis):
    """CylindricalPlanetGearModalAnalysis

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_PLANET_GEAR_MODAL_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CylindricalPlanetGearModalAnalysis")

    class _Cast_CylindricalPlanetGearModalAnalysis:
        """Special nested class for casting CylindricalPlanetGearModalAnalysis to subclasses."""

        def __init__(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
            parent: "CylindricalPlanetGearModalAnalysis",
        ):
            self._parent = parent

        @property
        def cylindrical_gear_modal_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            return self._parent._cast(_4623.CylindricalGearModalAnalysis)

        @property
        def gear_modal_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4638

            return self._parent._cast(_4638.GearModalAnalysis)

        @property
        def mountable_component_modal_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4660

            return self._parent._cast(_4660.MountableComponentModalAnalysis)

        @property
        def component_modal_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4599

            return self._parent._cast(_4599.ComponentModalAnalysis)

        @property
        def part_modal_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4664

            return self._parent._cast(_4664.PartModalAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2659

            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def cylindrical_planet_gear_modal_analysis(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
        ) -> "CylindricalPlanetGearModalAnalysis":
            return self._parent

        def __getattr__(
            self: "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis",
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
        self: Self, instance_to_wrap: "CylindricalPlanetGearModalAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2529.CylindricalPlanetGear":
        """mastapy.system_model.part_model.gears.CylindricalPlanetGear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: Self,
    ) -> "_2752.CylindricalPlanetGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalPlanetGearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CylindricalPlanetGearModalAnalysis._Cast_CylindricalPlanetGearModalAnalysis":
        return self._Cast_CylindricalPlanetGearModalAnalysis(self)
