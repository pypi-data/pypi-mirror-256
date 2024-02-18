"""PartToPartShearCoupling"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2585
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.couplings import _2350


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCoupling",)


Self = TypeVar("Self", bound="PartToPartShearCoupling")


class PartToPartShearCoupling(_2585.Coupling):
    """PartToPartShearCoupling

    This is a mastapy class.
    """

    TYPE = _PART_TO_PART_SHEAR_COUPLING
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PartToPartShearCoupling")

    class _Cast_PartToPartShearCoupling:
        """Special nested class for casting PartToPartShearCoupling to subclasses."""

        def __init__(
            self: "PartToPartShearCoupling._Cast_PartToPartShearCoupling",
            parent: "PartToPartShearCoupling",
        ):
            self._parent = parent

        @property
        def coupling(self: "PartToPartShearCoupling._Cast_PartToPartShearCoupling"):
            return self._parent._cast(_2585.Coupling)

        @property
        def specialised_assembly(
            self: "PartToPartShearCoupling._Cast_PartToPartShearCoupling",
        ):
            from mastapy.system_model.part_model import _2478

            return self._parent._cast(_2478.SpecialisedAssembly)

        @property
        def abstract_assembly(
            self: "PartToPartShearCoupling._Cast_PartToPartShearCoupling",
        ):
            from mastapy.system_model.part_model import _2436

            return self._parent._cast(_2436.AbstractAssembly)

        @property
        def part(self: "PartToPartShearCoupling._Cast_PartToPartShearCoupling"):
            from mastapy.system_model.part_model import _2470

            return self._parent._cast(_2470.Part)

        @property
        def design_entity(
            self: "PartToPartShearCoupling._Cast_PartToPartShearCoupling",
        ):
            from mastapy.system_model import _2205

            return self._parent._cast(_2205.DesignEntity)

        @property
        def part_to_part_shear_coupling(
            self: "PartToPartShearCoupling._Cast_PartToPartShearCoupling",
        ) -> "PartToPartShearCoupling":
            return self._parent

        def __getattr__(
            self: "PartToPartShearCoupling._Cast_PartToPartShearCoupling", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PartToPartShearCoupling.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def part_to_part_shear_coupling_connection(
        self: Self,
    ) -> "_2350.PartToPartShearCouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.PartToPartShearCouplingConnection

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: Self) -> "PartToPartShearCoupling._Cast_PartToPartShearCoupling":
        return self._Cast_PartToPartShearCoupling(self)
