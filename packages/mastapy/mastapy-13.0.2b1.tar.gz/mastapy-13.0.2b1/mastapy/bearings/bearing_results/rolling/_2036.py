"""LoadedRollingBearingRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from PIL.Image import Image

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLING_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollingBearingRow"
)

if TYPE_CHECKING:
    from mastapy.utility_gui.charts import _1869
    from mastapy.bearings.bearing_results.rolling import (
        _2035,
        _1975,
        _2016,
        _2034,
        _2070,
        _2075,
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollingBearingRow",)


Self = TypeVar("Self", bound="LoadedRollingBearingRow")


class LoadedRollingBearingRow(_0.APIBase):
    """LoadedRollingBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_ROLLING_BEARING_ROW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_LoadedRollingBearingRow")

    class _Cast_LoadedRollingBearingRow:
        """Special nested class for casting LoadedRollingBearingRow to subclasses."""

        def __init__(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
            parent: "LoadedRollingBearingRow",
        ):
            self._parent = parent

        @property
        def loaded_angular_contact_ball_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _1986

            return self._parent._cast(_1986.LoadedAngularContactBallBearingRow)

        @property
        def loaded_angular_contact_thrust_ball_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _1989

            return self._parent._cast(_1989.LoadedAngularContactThrustBallBearingRow)

        @property
        def loaded_asymmetric_spherical_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _1992

            return self._parent._cast(_1992.LoadedAsymmetricSphericalRollerBearingRow)

        @property
        def loaded_axial_thrust_cylindrical_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _1997

            return self._parent._cast(
                _1997.LoadedAxialThrustCylindricalRollerBearingRow
            )

        @property
        def loaded_axial_thrust_needle_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2000

            return self._parent._cast(_2000.LoadedAxialThrustNeedleRollerBearingRow)

        @property
        def loaded_ball_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2005

            return self._parent._cast(_2005.LoadedBallBearingRow)

        @property
        def loaded_crossed_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2008

            return self._parent._cast(_2008.LoadedCrossedRollerBearingRow)

        @property
        def loaded_cylindrical_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2012

            return self._parent._cast(_2012.LoadedCylindricalRollerBearingRow)

        @property
        def loaded_deep_groove_ball_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2015

            return self._parent._cast(_2015.LoadedDeepGrooveBallBearingRow)

        @property
        def loaded_four_point_contact_ball_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2020

            return self._parent._cast(_2020.LoadedFourPointContactBallBearingRow)

        @property
        def loaded_needle_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2024

            return self._parent._cast(_2024.LoadedNeedleRollerBearingRow)

        @property
        def loaded_non_barrel_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2027

            return self._parent._cast(_2027.LoadedNonBarrelRollerBearingRow)

        @property
        def loaded_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2032

            return self._parent._cast(_2032.LoadedRollerBearingRow)

        @property
        def loaded_self_aligning_ball_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2039

            return self._parent._cast(_2039.LoadedSelfAligningBallBearingRow)

        @property
        def loaded_spherical_roller_radial_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2043

            return self._parent._cast(_2043.LoadedSphericalRollerRadialBearingRow)

        @property
        def loaded_spherical_roller_thrust_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2046

            return self._parent._cast(_2046.LoadedSphericalRollerThrustBearingRow)

        @property
        def loaded_taper_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2051

            return self._parent._cast(_2051.LoadedTaperRollerBearingRow)

        @property
        def loaded_three_point_contact_ball_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2054

            return self._parent._cast(_2054.LoadedThreePointContactBallBearingRow)

        @property
        def loaded_thrust_ball_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2057

            return self._parent._cast(_2057.LoadedThrustBallBearingRow)

        @property
        def loaded_toroidal_roller_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ):
            from mastapy.bearings.bearing_results.rolling import _2060

            return self._parent._cast(_2060.LoadedToroidalRollerBearingRow)

        @property
        def loaded_rolling_bearing_row(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow",
        ) -> "LoadedRollingBearingRow":
            return self._parent

        def __getattr__(
            self: "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "LoadedRollingBearingRow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def dynamic_equivalent_reference_load(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.DynamicEquivalentReferenceLoad

        if temp is None:
            return 0.0

        return temp

    @property
    def life_modification_factor_for_systems_approach(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.LifeModificationFactorForSystemsApproach

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_element_normal_stress(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MaximumElementNormalStress

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_element_normal_stress_inner(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MaximumElementNormalStressInner

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_element_normal_stress_outer(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MaximumElementNormalStressOuter

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_normal_load_inner(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MaximumNormalLoadInner

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_normal_load_outer(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MaximumNormalLoadOuter

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_contact_stress_chart_inner(self: Self) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalContactStressChartInner

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def normal_contact_stress_chart_left(self: Self) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalContactStressChartLeft

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def normal_contact_stress_chart_outer(self: Self) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalContactStressChartOuter

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def normal_contact_stress_chart_right(self: Self) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalContactStressChartRight

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def row_id(self: Self) -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = self.wrapped.RowID

        if temp is None:
            return ""

        return temp

    @property
    def subsurface_shear_stress_chart_inner(self: Self) -> "_1869.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SubsurfaceShearStressChartInner

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def subsurface_shear_stress_chart_outer(self: Self) -> "_1869.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SubsurfaceShearStressChartOuter

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def loaded_bearing(self: Self) -> "_2035.LoadedRollingBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedRollingBearingResults

        Note:
            This property is readonly.
        """
        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def maximum_operating_internal_clearance(self: Self) -> "_1975.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MaximumOperatingInternalClearance

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def minimum_operating_internal_clearance(self: Self) -> "_1975.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MinimumOperatingInternalClearance

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def elements(self: Self) -> "List[_2016.LoadedElement]":
        """List[mastapy.bearings.bearing_results.rolling.LoadedElement]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Elements

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def race_results(self: Self) -> "List[_2034.LoadedRollingBearingRaceResults]":
        """List[mastapy.bearings.bearing_results.rolling.LoadedRollingBearingRaceResults]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.RaceResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def ring_force_and_displacement_results(
        self: Self,
    ) -> "List[_2070.RingForceAndDisplacement]":
        """List[mastapy.bearings.bearing_results.rolling.RingForceAndDisplacement]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.RingForceAndDisplacementResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def subsurface_shear_stress_for_most_heavily_loaded_element_inner(
        self: Self,
    ) -> "List[_2075.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SubsurfaceShearStressForMostHeavilyLoadedElementInner

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def subsurface_shear_stress_for_most_heavily_loaded_element_outer(
        self: Self,
    ) -> "List[_2075.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SubsurfaceShearStressForMostHeavilyLoadedElementOuter

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def report_names(self: Self) -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: Self, file_path: "str"):
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else "")

    def get_default_report_with_encoded_images(self: Self) -> "str":
        """str"""
        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: Self, file_path: "str"):
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else "")

    @enforce_parameter_types
    def output_active_report_as_text_to(self: Self, file_path: "str"):
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else "")

    def get_active_report_with_encoded_images(self: Self) -> "str":
        """str"""
        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    @enforce_parameter_types
    def output_named_report_to(self: Self, report_name: "str", file_path: "str"):
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(
            report_name if report_name else "", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: Self, report_name: "str", file_path: "str"
    ):
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(
            report_name if report_name else "", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: Self, report_name: "str", file_path: "str"
    ):
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(
            report_name if report_name else "", file_path if file_path else ""
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: Self, report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(
            report_name if report_name else ""
        )
        return method_result

    @property
    def cast_to(self: Self) -> "LoadedRollingBearingRow._Cast_LoadedRollingBearingRow":
        return self._Cast_LoadedRollingBearingRow(self)
