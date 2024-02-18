"""LoadedRollerBearingResults"""

from __future__ import annotations

from typing import TypeVar

from mastapy.bearings.bearing_results.rolling import _2035
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollerBearingResults"
)


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollerBearingResults",)


Self = TypeVar("Self", bound="LoadedRollerBearingResults")


class LoadedRollerBearingResults(_2035.LoadedRollingBearingResults):
    """LoadedRollerBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_ROLLER_BEARING_RESULTS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_LoadedRollerBearingResults")

    class _Cast_LoadedRollerBearingResults:
        """Special nested class for casting LoadedRollerBearingResults to subclasses."""

        def __init__(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
            parent: "LoadedRollerBearingResults",
        ):
            self._parent = parent

        @property
        def loaded_rolling_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            return self._parent._cast(_2035.LoadedRollingBearingResults)

        @property
        def loaded_detailed_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1956

            return self._parent._cast(_1956.LoadedDetailedBearingResults)

        @property
        def loaded_non_linear_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1959

            return self._parent._cast(_1959.LoadedNonLinearBearingResults)

        @property
        def loaded_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1951

            return self._parent._cast(_1951.LoadedBearingResults)

        @property
        def bearing_load_case_results_lightweight(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings import _1877

            return self._parent._cast(_1877.BearingLoadCaseResultsLightweight)

        @property
        def loaded_asymmetric_spherical_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1991

            return self._parent._cast(
                _1991.LoadedAsymmetricSphericalRollerBearingResults
            )

        @property
        def loaded_axial_thrust_cylindrical_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1996

            return self._parent._cast(
                _1996.LoadedAxialThrustCylindricalRollerBearingResults
            )

        @property
        def loaded_axial_thrust_needle_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1999

            return self._parent._cast(_1999.LoadedAxialThrustNeedleRollerBearingResults)

        @property
        def loaded_crossed_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2007

            return self._parent._cast(_2007.LoadedCrossedRollerBearingResults)

        @property
        def loaded_cylindrical_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2011

            return self._parent._cast(_2011.LoadedCylindricalRollerBearingResults)

        @property
        def loaded_needle_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2023

            return self._parent._cast(_2023.LoadedNeedleRollerBearingResults)

        @property
        def loaded_non_barrel_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2026

            return self._parent._cast(_2026.LoadedNonBarrelRollerBearingResults)

        @property
        def loaded_spherical_roller_radial_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2042

            return self._parent._cast(_2042.LoadedSphericalRollerRadialBearingResults)

        @property
        def loaded_spherical_roller_thrust_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2045

            return self._parent._cast(_2045.LoadedSphericalRollerThrustBearingResults)

        @property
        def loaded_taper_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2050

            return self._parent._cast(_2050.LoadedTaperRollerBearingResults)

        @property
        def loaded_toroidal_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2059

            return self._parent._cast(_2059.LoadedToroidalRollerBearingResults)

        @property
        def loaded_roller_bearing_results(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
        ) -> "LoadedRollerBearingResults":
            return self._parent

        def __getattr__(
            self: "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "LoadedRollerBearingResults.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def element_angular_velocity(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ElementAngularVelocity

        if temp is None:
            return 0.0

        return temp

    @property
    def element_centrifugal_force(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ElementCentrifugalForce

        if temp is None:
            return 0.0

        return temp

    @property
    def element_surface_velocity(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ElementSurfaceVelocity

        if temp is None:
            return 0.0

        return temp

    @property
    def hertzian_contact_width_inner(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.HertzianContactWidthInner

        if temp is None:
            return 0.0

        return temp

    @property
    def hertzian_contact_width_outer(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.HertzianContactWidthOuter

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_shear_stress_inner(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MaximumShearStressInner

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_shear_stress_outer(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.MaximumShearStressOuter

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(
        self: Self,
    ) -> "LoadedRollerBearingResults._Cast_LoadedRollerBearingResults":
        return self._Cast_LoadedRollerBearingResults(self)
