"""SpringDamper"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2585
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.couplings import _2352


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamper",)


Self = TypeVar("Self", bound="SpringDamper")


class SpringDamper(_2585.Coupling):
    """SpringDamper

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_SpringDamper")

    class _Cast_SpringDamper:
        """Special nested class for casting SpringDamper to subclasses."""

        def __init__(self: "SpringDamper._Cast_SpringDamper", parent: "SpringDamper"):
            self._parent = parent

        @property
        def coupling(self: "SpringDamper._Cast_SpringDamper"):
            return self._parent._cast(_2585.Coupling)

        @property
        def specialised_assembly(self: "SpringDamper._Cast_SpringDamper"):
            from mastapy.system_model.part_model import _2478

            return self._parent._cast(_2478.SpecialisedAssembly)

        @property
        def abstract_assembly(self: "SpringDamper._Cast_SpringDamper"):
            from mastapy.system_model.part_model import _2436

            return self._parent._cast(_2436.AbstractAssembly)

        @property
        def part(self: "SpringDamper._Cast_SpringDamper"):
            from mastapy.system_model.part_model import _2470

            return self._parent._cast(_2470.Part)

        @property
        def design_entity(self: "SpringDamper._Cast_SpringDamper"):
            from mastapy.system_model import _2205

            return self._parent._cast(_2205.DesignEntity)

        @property
        def spring_damper(self: "SpringDamper._Cast_SpringDamper") -> "SpringDamper":
            return self._parent

        def __getattr__(self: "SpringDamper._Cast_SpringDamper", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "SpringDamper.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection(self: Self) -> "_2352.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Connection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "SpringDamper._Cast_SpringDamper":
        return self._Cast_SpringDamper(self)
