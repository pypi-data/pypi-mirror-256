"""ClampedSectionMaterialDatabase"""

from __future__ import annotations

from typing import TypeVar

from mastapy.bolts import _1468
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CLAMPED_SECTION_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Bolts", "ClampedSectionMaterialDatabase"
)


__docformat__ = "restructuredtext en"
__all__ = ("ClampedSectionMaterialDatabase",)


Self = TypeVar("Self", bound="ClampedSectionMaterialDatabase")


class ClampedSectionMaterialDatabase(
    _1468.BoltedJointMaterialDatabase["_1467.BoltedJointMaterial"]
):
    """ClampedSectionMaterialDatabase

    This is a mastapy class.
    """

    TYPE = _CLAMPED_SECTION_MATERIAL_DATABASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ClampedSectionMaterialDatabase")

    class _Cast_ClampedSectionMaterialDatabase:
        """Special nested class for casting ClampedSectionMaterialDatabase to subclasses."""

        def __init__(
            self: "ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase",
            parent: "ClampedSectionMaterialDatabase",
        ):
            self._parent = parent

        @property
        def bolted_joint_material_database(
            self: "ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase",
        ):
            return self._parent._cast(_1468.BoltedJointMaterialDatabase)

        @property
        def named_database(
            self: "ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase",
        ):
            from mastapy.utility.databases import _1830

            return self._parent._cast(_1830.NamedDatabase)

        @property
        def sql_database(
            self: "ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase",
        ):
            pass

            from mastapy.utility.databases import _1833

            return self._parent._cast(_1833.SQLDatabase)

        @property
        def database(
            self: "ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase",
        ):
            pass

            from mastapy.utility.databases import _1826

            return self._parent._cast(_1826.Database)

        @property
        def clamped_section_material_database(
            self: "ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase",
        ) -> "ClampedSectionMaterialDatabase":
            return self._parent

        def __getattr__(
            self: "ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ClampedSectionMaterialDatabase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase":
        return self._Cast_ClampedSectionMaterialDatabase(self)
