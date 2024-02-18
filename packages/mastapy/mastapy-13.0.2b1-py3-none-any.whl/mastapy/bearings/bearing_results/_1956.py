"""LoadedDetailedBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor
from mastapy.bearings.bearing_results import _1959
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_DETAILED_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedDetailedBearingResults"
)

if TYPE_CHECKING:
    from mastapy.materials import _267


__docformat__ = "restructuredtext en"
__all__ = ("LoadedDetailedBearingResults",)


Self = TypeVar("Self", bound="LoadedDetailedBearingResults")


class LoadedDetailedBearingResults(_1959.LoadedNonLinearBearingResults):
    """LoadedDetailedBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_DETAILED_BEARING_RESULTS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_LoadedDetailedBearingResults")

    class _Cast_LoadedDetailedBearingResults:
        """Special nested class for casting LoadedDetailedBearingResults to subclasses."""

        def __init__(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
            parent: "LoadedDetailedBearingResults",
        ):
            self._parent = parent

        @property
        def loaded_non_linear_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            return self._parent._cast(_1959.LoadedNonLinearBearingResults)

        @property
        def loaded_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1951

            return self._parent._cast(_1951.LoadedBearingResults)

        @property
        def bearing_load_case_results_lightweight(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings import _1877

            return self._parent._cast(_1877.BearingLoadCaseResultsLightweight)

        @property
        def loaded_angular_contact_ball_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1985

            return self._parent._cast(_1985.LoadedAngularContactBallBearingResults)

        @property
        def loaded_angular_contact_thrust_ball_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1988

            return self._parent._cast(
                _1988.LoadedAngularContactThrustBallBearingResults
            )

        @property
        def loaded_asymmetric_spherical_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1991

            return self._parent._cast(
                _1991.LoadedAsymmetricSphericalRollerBearingResults
            )

        @property
        def loaded_axial_thrust_cylindrical_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1996

            return self._parent._cast(
                _1996.LoadedAxialThrustCylindricalRollerBearingResults
            )

        @property
        def loaded_axial_thrust_needle_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1999

            return self._parent._cast(_1999.LoadedAxialThrustNeedleRollerBearingResults)

        @property
        def loaded_ball_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2004

            return self._parent._cast(_2004.LoadedBallBearingResults)

        @property
        def loaded_crossed_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2007

            return self._parent._cast(_2007.LoadedCrossedRollerBearingResults)

        @property
        def loaded_cylindrical_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2011

            return self._parent._cast(_2011.LoadedCylindricalRollerBearingResults)

        @property
        def loaded_deep_groove_ball_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2014

            return self._parent._cast(_2014.LoadedDeepGrooveBallBearingResults)

        @property
        def loaded_four_point_contact_ball_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2019

            return self._parent._cast(_2019.LoadedFourPointContactBallBearingResults)

        @property
        def loaded_needle_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2023

            return self._parent._cast(_2023.LoadedNeedleRollerBearingResults)

        @property
        def loaded_non_barrel_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2026

            return self._parent._cast(_2026.LoadedNonBarrelRollerBearingResults)

        @property
        def loaded_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2031

            return self._parent._cast(_2031.LoadedRollerBearingResults)

        @property
        def loaded_rolling_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2035

            return self._parent._cast(_2035.LoadedRollingBearingResults)

        @property
        def loaded_self_aligning_ball_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2038

            return self._parent._cast(_2038.LoadedSelfAligningBallBearingResults)

        @property
        def loaded_spherical_roller_radial_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2042

            return self._parent._cast(_2042.LoadedSphericalRollerRadialBearingResults)

        @property
        def loaded_spherical_roller_thrust_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2045

            return self._parent._cast(_2045.LoadedSphericalRollerThrustBearingResults)

        @property
        def loaded_taper_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2050

            return self._parent._cast(_2050.LoadedTaperRollerBearingResults)

        @property
        def loaded_three_point_contact_ball_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2053

            return self._parent._cast(_2053.LoadedThreePointContactBallBearingResults)

        @property
        def loaded_thrust_ball_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2056

            return self._parent._cast(_2056.LoadedThrustBallBearingResults)

        @property
        def loaded_toroidal_roller_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2059

            return self._parent._cast(_2059.LoadedToroidalRollerBearingResults)

        @property
        def loaded_fluid_film_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.fluid_film import _2121

            return self._parent._cast(_2121.LoadedFluidFilmBearingResults)

        @property
        def loaded_grease_filled_journal_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.fluid_film import _2122

            return self._parent._cast(_2122.LoadedGreaseFilledJournalBearingResults)

        @property
        def loaded_pad_fluid_film_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.fluid_film import _2123

            return self._parent._cast(_2123.LoadedPadFluidFilmBearingResults)

        @property
        def loaded_plain_journal_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.fluid_film import _2124

            return self._parent._cast(_2124.LoadedPlainJournalBearingResults)

        @property
        def loaded_plain_oil_fed_journal_bearing(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.fluid_film import _2126

            return self._parent._cast(_2126.LoadedPlainOilFedJournalBearing)

        @property
        def loaded_tilting_pad_journal_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.fluid_film import _2129

            return self._parent._cast(_2129.LoadedTiltingPadJournalBearingResults)

        @property
        def loaded_tilting_pad_thrust_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ):
            from mastapy.bearings.bearing_results.fluid_film import _2130

            return self._parent._cast(_2130.LoadedTiltingPadThrustBearingResults)

        @property
        def loaded_detailed_bearing_results(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
        ) -> "LoadedDetailedBearingResults":
            return self._parent

        def __getattr__(
            self: "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "LoadedDetailedBearingResults.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lubricant_flow_rate(self: Self) -> "float":
        """float"""
        temp = self.wrapped.LubricantFlowRate

        if temp is None:
            return 0.0

        return temp

    @lubricant_flow_rate.setter
    @enforce_parameter_types
    def lubricant_flow_rate(self: Self, value: "float"):
        self.wrapped.LubricantFlowRate = float(value) if value is not None else 0.0

    @property
    def oil_sump_temperature(self: Self) -> "float":
        """float"""
        temp = self.wrapped.OilSumpTemperature

        if temp is None:
            return 0.0

        return temp

    @oil_sump_temperature.setter
    @enforce_parameter_types
    def oil_sump_temperature(self: Self, value: "float"):
        self.wrapped.OilSumpTemperature = float(value) if value is not None else 0.0

    @property
    def operating_air_temperature(self: Self) -> "float":
        """float"""
        temp = self.wrapped.OperatingAirTemperature

        if temp is None:
            return 0.0

        return temp

    @operating_air_temperature.setter
    @enforce_parameter_types
    def operating_air_temperature(self: Self, value: "float"):
        self.wrapped.OperatingAirTemperature = (
            float(value) if value is not None else 0.0
        )

    @property
    def temperature_when_assembled(self: Self) -> "float":
        """float"""
        temp = self.wrapped.TemperatureWhenAssembled

        if temp is None:
            return 0.0

        return temp

    @temperature_when_assembled.setter
    @enforce_parameter_types
    def temperature_when_assembled(self: Self, value: "float"):
        self.wrapped.TemperatureWhenAssembled = (
            float(value) if value is not None else 0.0
        )

    @property
    def lubrication(self: Self) -> "_267.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Lubrication

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "LoadedDetailedBearingResults._Cast_LoadedDetailedBearingResults":
        return self._Cast_LoadedDetailedBearingResults(self)
