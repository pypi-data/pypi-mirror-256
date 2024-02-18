"""AxialThrustCylindricalRollerBearing"""

from __future__ import annotations

from typing import TypeVar

from mastapy.bearings.bearing_designs.rolling import _2163
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_AXIAL_THRUST_CYLINDRICAL_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling",
    "AxialThrustCylindricalRollerBearing",
)


__docformat__ = "restructuredtext en"
__all__ = ("AxialThrustCylindricalRollerBearing",)


Self = TypeVar("Self", bound="AxialThrustCylindricalRollerBearing")


class AxialThrustCylindricalRollerBearing(_2163.NonBarrelRollerBearing):
    """AxialThrustCylindricalRollerBearing

    This is a mastapy class.
    """

    TYPE = _AXIAL_THRUST_CYLINDRICAL_ROLLER_BEARING
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_AxialThrustCylindricalRollerBearing")

    class _Cast_AxialThrustCylindricalRollerBearing:
        """Special nested class for casting AxialThrustCylindricalRollerBearing to subclasses."""

        def __init__(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
            parent: "AxialThrustCylindricalRollerBearing",
        ):
            self._parent = parent

        @property
        def non_barrel_roller_bearing(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
        ):
            return self._parent._cast(_2163.NonBarrelRollerBearing)

        @property
        def roller_bearing(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2164

            return self._parent._cast(_2164.RollerBearing)

        @property
        def rolling_bearing(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2167

            return self._parent._cast(_2167.RollingBearing)

        @property
        def detailed_bearing(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
        ):
            from mastapy.bearings.bearing_designs import _2133

            return self._parent._cast(_2133.DetailedBearing)

        @property
        def non_linear_bearing(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
        ):
            from mastapy.bearings.bearing_designs import _2136

            return self._parent._cast(_2136.NonLinearBearing)

        @property
        def bearing_design(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
        ):
            from mastapy.bearings.bearing_designs import _2132

            return self._parent._cast(_2132.BearingDesign)

        @property
        def axial_thrust_needle_roller_bearing(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2141

            return self._parent._cast(_2141.AxialThrustNeedleRollerBearing)

        @property
        def axial_thrust_cylindrical_roller_bearing(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
        ) -> "AxialThrustCylindricalRollerBearing":
            return self._parent

        def __getattr__(
            self: "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing",
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
        self: Self, instance_to_wrap: "AxialThrustCylindricalRollerBearing.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> (
        "AxialThrustCylindricalRollerBearing._Cast_AxialThrustCylindricalRollerBearing"
    ):
        return self._Cast_AxialThrustCylindricalRollerBearing(self)
