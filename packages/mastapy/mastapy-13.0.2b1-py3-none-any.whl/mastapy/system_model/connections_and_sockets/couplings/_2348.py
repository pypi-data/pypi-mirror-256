"""CouplingConnection"""

from __future__ import annotations

from typing import TypeVar

from mastapy.system_model.connections_and_sockets import _2283
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnection",)


Self = TypeVar("Self", bound="CouplingConnection")


class CouplingConnection(_2283.InterMountableComponentConnection):
    """CouplingConnection

    This is a mastapy class.
    """

    TYPE = _COUPLING_CONNECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingConnection")

    class _Cast_CouplingConnection:
        """Special nested class for casting CouplingConnection to subclasses."""

        def __init__(
            self: "CouplingConnection._Cast_CouplingConnection",
            parent: "CouplingConnection",
        ):
            self._parent = parent

        @property
        def inter_mountable_component_connection(
            self: "CouplingConnection._Cast_CouplingConnection",
        ):
            return self._parent._cast(_2283.InterMountableComponentConnection)

        @property
        def connection(self: "CouplingConnection._Cast_CouplingConnection"):
            from mastapy.system_model.connections_and_sockets import _2274

            return self._parent._cast(_2274.Connection)

        @property
        def design_entity(self: "CouplingConnection._Cast_CouplingConnection"):
            from mastapy.system_model import _2205

            return self._parent._cast(_2205.DesignEntity)

        @property
        def clutch_connection(self: "CouplingConnection._Cast_CouplingConnection"):
            from mastapy.system_model.connections_and_sockets.couplings import _2344

            return self._parent._cast(_2344.ClutchConnection)

        @property
        def concept_coupling_connection(
            self: "CouplingConnection._Cast_CouplingConnection",
        ):
            from mastapy.system_model.connections_and_sockets.couplings import _2346

            return self._parent._cast(_2346.ConceptCouplingConnection)

        @property
        def part_to_part_shear_coupling_connection(
            self: "CouplingConnection._Cast_CouplingConnection",
        ):
            from mastapy.system_model.connections_and_sockets.couplings import _2350

            return self._parent._cast(_2350.PartToPartShearCouplingConnection)

        @property
        def spring_damper_connection(
            self: "CouplingConnection._Cast_CouplingConnection",
        ):
            from mastapy.system_model.connections_and_sockets.couplings import _2352

            return self._parent._cast(_2352.SpringDamperConnection)

        @property
        def torque_converter_connection(
            self: "CouplingConnection._Cast_CouplingConnection",
        ):
            from mastapy.system_model.connections_and_sockets.couplings import _2354

            return self._parent._cast(_2354.TorqueConverterConnection)

        @property
        def coupling_connection(
            self: "CouplingConnection._Cast_CouplingConnection",
        ) -> "CouplingConnection":
            return self._parent

        def __getattr__(self: "CouplingConnection._Cast_CouplingConnection", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CouplingConnection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "CouplingConnection._Cast_CouplingConnection":
        return self._Cast_CouplingConnection(self)
