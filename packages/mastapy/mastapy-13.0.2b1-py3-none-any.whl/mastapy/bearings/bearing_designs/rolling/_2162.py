"""NeedleRollerBearing"""

from __future__ import annotations

from typing import TypeVar

from mastapy.bearings.bearing_designs.rolling import _2151
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_NEEDLE_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "NeedleRollerBearing"
)


__docformat__ = "restructuredtext en"
__all__ = ("NeedleRollerBearing",)


Self = TypeVar("Self", bound="NeedleRollerBearing")


class NeedleRollerBearing(_2151.CylindricalRollerBearing):
    """NeedleRollerBearing

    This is a mastapy class.
    """

    TYPE = _NEEDLE_ROLLER_BEARING
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_NeedleRollerBearing")

    class _Cast_NeedleRollerBearing:
        """Special nested class for casting NeedleRollerBearing to subclasses."""

        def __init__(
            self: "NeedleRollerBearing._Cast_NeedleRollerBearing",
            parent: "NeedleRollerBearing",
        ):
            self._parent = parent

        @property
        def cylindrical_roller_bearing(
            self: "NeedleRollerBearing._Cast_NeedleRollerBearing",
        ):
            return self._parent._cast(_2151.CylindricalRollerBearing)

        @property
        def non_barrel_roller_bearing(
            self: "NeedleRollerBearing._Cast_NeedleRollerBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2163

            return self._parent._cast(_2163.NonBarrelRollerBearing)

        @property
        def roller_bearing(self: "NeedleRollerBearing._Cast_NeedleRollerBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2164

            return self._parent._cast(_2164.RollerBearing)

        @property
        def rolling_bearing(self: "NeedleRollerBearing._Cast_NeedleRollerBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2167

            return self._parent._cast(_2167.RollingBearing)

        @property
        def detailed_bearing(self: "NeedleRollerBearing._Cast_NeedleRollerBearing"):
            from mastapy.bearings.bearing_designs import _2133

            return self._parent._cast(_2133.DetailedBearing)

        @property
        def non_linear_bearing(self: "NeedleRollerBearing._Cast_NeedleRollerBearing"):
            from mastapy.bearings.bearing_designs import _2136

            return self._parent._cast(_2136.NonLinearBearing)

        @property
        def bearing_design(self: "NeedleRollerBearing._Cast_NeedleRollerBearing"):
            from mastapy.bearings.bearing_designs import _2132

            return self._parent._cast(_2132.BearingDesign)

        @property
        def needle_roller_bearing(
            self: "NeedleRollerBearing._Cast_NeedleRollerBearing",
        ) -> "NeedleRollerBearing":
            return self._parent

        def __getattr__(
            self: "NeedleRollerBearing._Cast_NeedleRollerBearing", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "NeedleRollerBearing.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "NeedleRollerBearing._Cast_NeedleRollerBearing":
        return self._Cast_NeedleRollerBearing(self)
