"""CylindricalSocket"""

from __future__ import annotations

from typing import TypeVar

from mastapy.system_model.connections_and_sockets import _2298
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


Self = TypeVar("Self", bound="CylindricalSocket")


class CylindricalSocket(_2298.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_SOCKET
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CylindricalSocket")

    class _Cast_CylindricalSocket:
        """Special nested class for casting CylindricalSocket to subclasses."""

        def __init__(
            self: "CylindricalSocket._Cast_CylindricalSocket",
            parent: "CylindricalSocket",
        ):
            self._parent = parent

        @property
        def socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            return self._parent._cast(_2298.Socket)

        @property
        def bearing_inner_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2268

            return self._parent._cast(_2268.BearingInnerSocket)

        @property
        def bearing_outer_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2269

            return self._parent._cast(_2269.BearingOuterSocket)

        @property
        def cvt_pulley_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2276

            return self._parent._cast(_2276.CVTPulleySocket)

        @property
        def inner_shaft_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2281

            return self._parent._cast(_2281.InnerShaftSocket)

        @property
        def inner_shaft_socket_base(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2282

            return self._parent._cast(_2282.InnerShaftSocketBase)

        @property
        def mountable_component_inner_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets import _2284

            return self._parent._cast(_2284.MountableComponentInnerSocket)

        @property
        def mountable_component_outer_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets import _2285

            return self._parent._cast(_2285.MountableComponentOuterSocket)

        @property
        def mountable_component_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets import _2286

            return self._parent._cast(_2286.MountableComponentSocket)

        @property
        def outer_shaft_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2287

            return self._parent._cast(_2287.OuterShaftSocket)

        @property
        def outer_shaft_socket_base(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2288

            return self._parent._cast(_2288.OuterShaftSocketBase)

        @property
        def planetary_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2290

            return self._parent._cast(_2290.PlanetarySocket)

        @property
        def planetary_socket_base(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2291

            return self._parent._cast(_2291.PlanetarySocketBase)

        @property
        def pulley_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2292

            return self._parent._cast(_2292.PulleySocket)

        @property
        def rolling_ring_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2295

            return self._parent._cast(_2295.RollingRingSocket)

        @property
        def shaft_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets import _2296

            return self._parent._cast(_2296.ShaftSocket)

        @property
        def cylindrical_gear_teeth_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.gears import _2312

            return self._parent._cast(_2312.CylindricalGearTeethSocket)

        @property
        def cycloidal_disc_axial_left_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2335

            return self._parent._cast(_2335.CycloidalDiscAxialLeftSocket)

        @property
        def cycloidal_disc_axial_right_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2336

            return self._parent._cast(_2336.CycloidalDiscAxialRightSocket)

        @property
        def cycloidal_disc_inner_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2338

            return self._parent._cast(_2338.CycloidalDiscInnerSocket)

        @property
        def cycloidal_disc_outer_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2339

            return self._parent._cast(_2339.CycloidalDiscOuterSocket)

        @property
        def cycloidal_disc_planetary_bearing_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2341

            return self._parent._cast(_2341.CycloidalDiscPlanetaryBearingSocket)

        @property
        def ring_pins_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2342

            return self._parent._cast(_2342.RingPinsSocket)

        @property
        def clutch_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets.couplings import _2345

            return self._parent._cast(_2345.ClutchSocket)

        @property
        def concept_coupling_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets.couplings import _2347

            return self._parent._cast(_2347.ConceptCouplingSocket)

        @property
        def coupling_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets.couplings import _2349

            return self._parent._cast(_2349.CouplingSocket)

        @property
        def part_to_part_shear_coupling_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.couplings import _2351

            return self._parent._cast(_2351.PartToPartShearCouplingSocket)

        @property
        def spring_damper_socket(self: "CylindricalSocket._Cast_CylindricalSocket"):
            from mastapy.system_model.connections_and_sockets.couplings import _2353

            return self._parent._cast(_2353.SpringDamperSocket)

        @property
        def torque_converter_pump_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.couplings import _2355

            return self._parent._cast(_2355.TorqueConverterPumpSocket)

        @property
        def torque_converter_turbine_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ):
            from mastapy.system_model.connections_and_sockets.couplings import _2356

            return self._parent._cast(_2356.TorqueConverterTurbineSocket)

        @property
        def cylindrical_socket(
            self: "CylindricalSocket._Cast_CylindricalSocket",
        ) -> "CylindricalSocket":
            return self._parent

        def __getattr__(self: "CylindricalSocket._Cast_CylindricalSocket", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CylindricalSocket.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "CylindricalSocket._Cast_CylindricalSocket":
        return self._Cast_CylindricalSocket(self)
