"""LoadedAxialThrustCylindricalRollerBearingResults"""

from __future__ import annotations

from typing import TypeVar

from mastapy.bearings.bearing_results.rolling import _2026
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_AXIAL_THRUST_CYLINDRICAL_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedAxialThrustCylindricalRollerBearingResults",
)


__docformat__ = "restructuredtext en"
__all__ = ("LoadedAxialThrustCylindricalRollerBearingResults",)


Self = TypeVar("Self", bound="LoadedAxialThrustCylindricalRollerBearingResults")


class LoadedAxialThrustCylindricalRollerBearingResults(
    _2026.LoadedNonBarrelRollerBearingResults
):
    """LoadedAxialThrustCylindricalRollerBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_AXIAL_THRUST_CYLINDRICAL_ROLLER_BEARING_RESULTS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_LoadedAxialThrustCylindricalRollerBearingResults"
    )

    class _Cast_LoadedAxialThrustCylindricalRollerBearingResults:
        """Special nested class for casting LoadedAxialThrustCylindricalRollerBearingResults to subclasses."""

        def __init__(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
            parent: "LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            self._parent = parent

        @property
        def loaded_non_barrel_roller_bearing_results(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            return self._parent._cast(_2026.LoadedNonBarrelRollerBearingResults)

        @property
        def loaded_roller_bearing_results(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2031

            return self._parent._cast(_2031.LoadedRollerBearingResults)

        @property
        def loaded_rolling_bearing_results(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2035

            return self._parent._cast(_2035.LoadedRollingBearingResults)

        @property
        def loaded_detailed_bearing_results(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1956

            return self._parent._cast(_1956.LoadedDetailedBearingResults)

        @property
        def loaded_non_linear_bearing_results(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1959

            return self._parent._cast(_1959.LoadedNonLinearBearingResults)

        @property
        def loaded_bearing_results(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1951

            return self._parent._cast(_1951.LoadedBearingResults)

        @property
        def bearing_load_case_results_lightweight(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            from mastapy.bearings import _1877

            return self._parent._cast(_1877.BearingLoadCaseResultsLightweight)

        @property
        def loaded_axial_thrust_needle_roller_bearing_results(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1999

            return self._parent._cast(_1999.LoadedAxialThrustNeedleRollerBearingResults)

        @property
        def loaded_axial_thrust_cylindrical_roller_bearing_results(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
        ) -> "LoadedAxialThrustCylindricalRollerBearingResults":
            return self._parent

        def __getattr__(
            self: "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults",
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
        instance_to_wrap: "LoadedAxialThrustCylindricalRollerBearingResults.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "LoadedAxialThrustCylindricalRollerBearingResults._Cast_LoadedAxialThrustCylindricalRollerBearingResults":
        return self._Cast_LoadedAxialThrustCylindricalRollerBearingResults(self)
