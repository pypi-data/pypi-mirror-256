"""Connection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal.sentinels import ListWithSelectedItem_None
from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.python_net import python_net_import
from mastapy.system_model import _2205
from mastapy._internal.cast_exception import CastException

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2446
    from mastapy.system_model.connections_and_sockets import _2298


__docformat__ = "restructuredtext en"
__all__ = ("Connection",)


Self = TypeVar("Self", bound="Connection")


class Connection(_2205.DesignEntity):
    """Connection

    This is a mastapy class.
    """

    TYPE = _CONNECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_Connection")

    class _Cast_Connection:
        """Special nested class for casting Connection to subclasses."""

        def __init__(self: "Connection._Cast_Connection", parent: "Connection"):
            self._parent = parent

        @property
        def design_entity(self: "Connection._Cast_Connection"):
            return self._parent._cast(_2205.DesignEntity)

        @property
        def abstract_shaft_to_mountable_component_connection(
            self: "Connection._Cast_Connection",
        ):
            from mastapy.system_model.connections_and_sockets import _2267

            return self._parent._cast(_2267.AbstractShaftToMountableComponentConnection)

        @property
        def belt_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets import _2270

            return self._parent._cast(_2270.BeltConnection)

        @property
        def coaxial_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets import _2271

            return self._parent._cast(_2271.CoaxialConnection)

        @property
        def cvt_belt_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets import _2275

            return self._parent._cast(_2275.CVTBeltConnection)

        @property
        def inter_mountable_component_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets import _2283

            return self._parent._cast(_2283.InterMountableComponentConnection)

        @property
        def planetary_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets import _2289

            return self._parent._cast(_2289.PlanetaryConnection)

        @property
        def rolling_ring_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets import _2294

            return self._parent._cast(_2294.RollingRingConnection)

        @property
        def shaft_to_mountable_component_connection(
            self: "Connection._Cast_Connection",
        ):
            from mastapy.system_model.connections_and_sockets import _2297

            return self._parent._cast(_2297.ShaftToMountableComponentConnection)

        @property
        def agma_gleason_conical_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2301

            return self._parent._cast(_2301.AGMAGleasonConicalGearMesh)

        @property
        def bevel_differential_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2303

            return self._parent._cast(_2303.BevelDifferentialGearMesh)

        @property
        def bevel_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2305

            return self._parent._cast(_2305.BevelGearMesh)

        @property
        def concept_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2307

            return self._parent._cast(_2307.ConceptGearMesh)

        @property
        def conical_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2309

            return self._parent._cast(_2309.ConicalGearMesh)

        @property
        def cylindrical_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2311

            return self._parent._cast(_2311.CylindricalGearMesh)

        @property
        def face_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2313

            return self._parent._cast(_2313.FaceGearMesh)

        @property
        def gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2315

            return self._parent._cast(_2315.GearMesh)

        @property
        def hypoid_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2317

            return self._parent._cast(_2317.HypoidGearMesh)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh(
            self: "Connection._Cast_Connection",
        ):
            from mastapy.system_model.connections_and_sockets.gears import _2320

            return self._parent._cast(_2320.KlingelnbergCycloPalloidConicalGearMesh)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
            self: "Connection._Cast_Connection",
        ):
            from mastapy.system_model.connections_and_sockets.gears import _2321

            return self._parent._cast(_2321.KlingelnbergCycloPalloidHypoidGearMesh)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
            self: "Connection._Cast_Connection",
        ):
            from mastapy.system_model.connections_and_sockets.gears import _2322

            return self._parent._cast(_2322.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        @property
        def spiral_bevel_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2325

            return self._parent._cast(_2325.SpiralBevelGearMesh)

        @property
        def straight_bevel_diff_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2327

            return self._parent._cast(_2327.StraightBevelDiffGearMesh)

        @property
        def straight_bevel_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2329

            return self._parent._cast(_2329.StraightBevelGearMesh)

        @property
        def worm_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2331

            return self._parent._cast(_2331.WormGearMesh)

        @property
        def zerol_bevel_gear_mesh(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.gears import _2333

            return self._parent._cast(_2333.ZerolBevelGearMesh)

        @property
        def cycloidal_disc_central_bearing_connection(
            self: "Connection._Cast_Connection",
        ):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2337

            return self._parent._cast(_2337.CycloidalDiscCentralBearingConnection)

        @property
        def cycloidal_disc_planetary_bearing_connection(
            self: "Connection._Cast_Connection",
        ):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2340

            return self._parent._cast(_2340.CycloidalDiscPlanetaryBearingConnection)

        @property
        def ring_pins_to_disc_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.cycloidal import _2343

            return self._parent._cast(_2343.RingPinsToDiscConnection)

        @property
        def clutch_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.couplings import _2344

            return self._parent._cast(_2344.ClutchConnection)

        @property
        def concept_coupling_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.couplings import _2346

            return self._parent._cast(_2346.ConceptCouplingConnection)

        @property
        def coupling_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.couplings import _2348

            return self._parent._cast(_2348.CouplingConnection)

        @property
        def part_to_part_shear_coupling_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.couplings import _2350

            return self._parent._cast(_2350.PartToPartShearCouplingConnection)

        @property
        def spring_damper_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.couplings import _2352

            return self._parent._cast(_2352.SpringDamperConnection)

        @property
        def torque_converter_connection(self: "Connection._Cast_Connection"):
            from mastapy.system_model.connections_and_sockets.couplings import _2354

            return self._parent._cast(_2354.TorqueConverterConnection)

        @property
        def connection(self: "Connection._Cast_Connection") -> "Connection":
            return self._parent

        def __getattr__(self: "Connection._Cast_Connection", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "Connection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_id(self: Self) -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionID

        if temp is None:
            return ""

        return temp

    @property
    def drawing_position(
        self: Self,
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = self.wrapped.DrawingPosition

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @drawing_position.setter
    @enforce_parameter_types
    def drawing_position(self: Self, value: "str"):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        self.wrapped.DrawingPosition = value

    @property
    def speed_ratio_from_a_to_b(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SpeedRatioFromAToB

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ratio_from_a_to_b(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.TorqueRatioFromAToB

        if temp is None:
            return 0.0

        return temp

    @property
    def unique_name(self: Self) -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = self.wrapped.UniqueName

        if temp is None:
            return ""

        return temp

    @property
    def owner_a(self: Self) -> "_2446.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def owner_b(self: Self) -> "_2446.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def socket_a(self: Self) -> "_2298.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SocketA

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def socket_b(self: Self) -> "_2298.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SocketB

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def other_owner(self: Self, component: "_2446.Component") -> "_2446.Component":
        """mastapy.system_model.part_model.Component

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = self.wrapped.OtherOwner(
            component.wrapped if component else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def other_socket_for_component(
        self: Self, component: "_2446.Component"
    ) -> "_2298.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = self.wrapped.OtherSocket.Overloads[_COMPONENT](
            component.wrapped if component else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def other_socket(self: Self, socket: "_2298.Socket") -> "_2298.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = self.wrapped.OtherSocket.Overloads[_SOCKET](
            socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def socket_for(self: Self, component: "_2446.Component") -> "_2298.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = self.wrapped.SocketFor(component.wrapped if component else None)
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: Self) -> "Connection._Cast_Connection":
        return self._Cast_Connection(self)
