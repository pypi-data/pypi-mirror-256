"""LoadedNonBarrelRollerBearingResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _2031
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_NON_BARREL_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedNonBarrelRollerBearingResults",
)

if TYPE_CHECKING:
    from mastapy.bearings.bearing_results.rolling import _2074


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonBarrelRollerBearingResults",)


Self = TypeVar("Self", bound="LoadedNonBarrelRollerBearingResults")


class LoadedNonBarrelRollerBearingResults(_2031.LoadedRollerBearingResults):
    """LoadedNonBarrelRollerBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_NON_BARREL_ROLLER_BEARING_RESULTS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_LoadedNonBarrelRollerBearingResults")

    class _Cast_LoadedNonBarrelRollerBearingResults:
        """Special nested class for casting LoadedNonBarrelRollerBearingResults to subclasses."""

        def __init__(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
            parent: "LoadedNonBarrelRollerBearingResults",
        ):
            self._parent = parent

        @property
        def loaded_roller_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            return self._parent._cast(_2031.LoadedRollerBearingResults)

        @property
        def loaded_rolling_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2035

            return self._parent._cast(_2035.LoadedRollingBearingResults)

        @property
        def loaded_detailed_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1956

            return self._parent._cast(_1956.LoadedDetailedBearingResults)

        @property
        def loaded_non_linear_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1959

            return self._parent._cast(_1959.LoadedNonLinearBearingResults)

        @property
        def loaded_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results import _1951

            return self._parent._cast(_1951.LoadedBearingResults)

        @property
        def bearing_load_case_results_lightweight(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings import _1877

            return self._parent._cast(_1877.BearingLoadCaseResultsLightweight)

        @property
        def loaded_axial_thrust_cylindrical_roller_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1996

            return self._parent._cast(
                _1996.LoadedAxialThrustCylindricalRollerBearingResults
            )

        @property
        def loaded_axial_thrust_needle_roller_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _1999

            return self._parent._cast(_1999.LoadedAxialThrustNeedleRollerBearingResults)

        @property
        def loaded_cylindrical_roller_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2011

            return self._parent._cast(_2011.LoadedCylindricalRollerBearingResults)

        @property
        def loaded_needle_roller_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2023

            return self._parent._cast(_2023.LoadedNeedleRollerBearingResults)

        @property
        def loaded_taper_roller_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ):
            from mastapy.bearings.bearing_results.rolling import _2050

            return self._parent._cast(_2050.LoadedTaperRollerBearingResults)

        @property
        def loaded_non_barrel_roller_bearing_results(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
        ) -> "LoadedNonBarrelRollerBearingResults":
            return self._parent

        def __getattr__(
            self: "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
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
        self: Self, instance_to_wrap: "LoadedNonBarrelRollerBearingResults.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def smt_rib_stress(self: Self) -> "_2074.SMTRibStressResults":
        """mastapy.bearings.bearing_results.rolling.SMTRibStressResults

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SMTRibStress

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> (
        "LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults"
    ):
        return self._Cast_LoadedNonBarrelRollerBearingResults(self)
