"""BoltedJointMaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.utility.databases import _1830
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Bolts", "BoltedJointMaterialDatabase"
)

if TYPE_CHECKING:
    from mastapy.bolts import _1467


__docformat__ = "restructuredtext en"
__all__ = ("BoltedJointMaterialDatabase",)


Self = TypeVar("Self", bound="BoltedJointMaterialDatabase")
T = TypeVar("T", bound="_1467.BoltedJointMaterial")


class BoltedJointMaterialDatabase(_1830.NamedDatabase[T]):
    """BoltedJointMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _BOLTED_JOINT_MATERIAL_DATABASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BoltedJointMaterialDatabase")

    class _Cast_BoltedJointMaterialDatabase:
        """Special nested class for casting BoltedJointMaterialDatabase to subclasses."""

        def __init__(
            self: "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
            parent: "BoltedJointMaterialDatabase",
        ):
            self._parent = parent

        @property
        def named_database(
            self: "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
        ):
            return self._parent._cast(_1830.NamedDatabase)

        @property
        def sql_database(
            self: "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
        ):
            pass

            from mastapy.utility.databases import _1833

            return self._parent._cast(_1833.SQLDatabase)

        @property
        def database(
            self: "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
        ):
            pass

            from mastapy.utility.databases import _1826

            return self._parent._cast(_1826.Database)

        @property
        def bolt_material_database(
            self: "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
        ):
            from mastapy.bolts import _1472

            return self._parent._cast(_1472.BoltMaterialDatabase)

        @property
        def clamped_section_material_database(
            self: "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
        ):
            from mastapy.bolts import _1477

            return self._parent._cast(_1477.ClampedSectionMaterialDatabase)

        @property
        def bolted_joint_material_database(
            self: "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
        ) -> "BoltedJointMaterialDatabase":
            return self._parent

        def __getattr__(
            self: "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BoltedJointMaterialDatabase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "BoltedJointMaterialDatabase._Cast_BoltedJointMaterialDatabase":
        return self._Cast_BoltedJointMaterialDatabase(self)
