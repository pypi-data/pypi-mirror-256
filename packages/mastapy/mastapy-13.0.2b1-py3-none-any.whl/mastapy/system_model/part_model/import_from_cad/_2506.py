"""MountableComponentFromCAD"""

from __future__ import annotations

from typing import TypeVar

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy.system_model.part_model.import_from_cad import _2497
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "MountableComponentFromCAD"
)


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentFromCAD",)


Self = TypeVar("Self", bound="MountableComponentFromCAD")


class MountableComponentFromCAD(_2497.ComponentFromCAD):
    """MountableComponentFromCAD

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_FROM_CAD
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_MountableComponentFromCAD")

    class _Cast_MountableComponentFromCAD:
        """Special nested class for casting MountableComponentFromCAD to subclasses."""

        def __init__(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
            parent: "MountableComponentFromCAD",
        ):
            self._parent = parent

        @property
        def component_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            return self._parent._cast(_2497.ComponentFromCAD)

        @property
        def clutch_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2496

            return self._parent._cast(_2496.ClutchFromCAD)

        @property
        def concept_bearing_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2498

            return self._parent._cast(_2498.ConceptBearingFromCAD)

        @property
        def connector_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2499

            return self._parent._cast(_2499.ConnectorFromCAD)

        @property
        def cylindrical_gear_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2500

            return self._parent._cast(_2500.CylindricalGearFromCAD)

        @property
        def cylindrical_gear_in_planetary_set_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2501

            return self._parent._cast(_2501.CylindricalGearInPlanetarySetFromCAD)

        @property
        def cylindrical_planet_gear_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2502

            return self._parent._cast(_2502.CylindricalPlanetGearFromCAD)

        @property
        def cylindrical_ring_gear_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2503

            return self._parent._cast(_2503.CylindricalRingGearFromCAD)

        @property
        def cylindrical_sun_gear_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2504

            return self._parent._cast(_2504.CylindricalSunGearFromCAD)

        @property
        def pulley_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2508

            return self._parent._cast(_2508.PulleyFromCAD)

        @property
        def rigid_connector_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2509

            return self._parent._cast(_2509.RigidConnectorFromCAD)

        @property
        def rolling_bearing_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ):
            from mastapy.system_model.part_model.import_from_cad import _2510

            return self._parent._cast(_2510.RollingBearingFromCAD)

        @property
        def mountable_component_from_cad(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD",
        ) -> "MountableComponentFromCAD":
            return self._parent

        def __getattr__(
            self: "MountableComponentFromCAD._Cast_MountableComponentFromCAD", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "MountableComponentFromCAD.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def offset(self: Self) -> "float":
        """float"""
        temp = self.wrapped.Offset

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @enforce_parameter_types
    def offset(self: Self, value: "float"):
        self.wrapped.Offset = float(value) if value is not None else 0.0

    @property
    def cast_to(
        self: Self,
    ) -> "MountableComponentFromCAD._Cast_MountableComponentFromCAD":
        return self._Cast_MountableComponentFromCAD(self)
