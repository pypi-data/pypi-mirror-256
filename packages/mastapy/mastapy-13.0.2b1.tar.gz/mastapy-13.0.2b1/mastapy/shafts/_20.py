"""ShaftDamageResultsTableAndChart"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor, conversion
from mastapy.utility.report import _1758
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SHAFT_DAMAGE_RESULTS_TABLE_AND_CHART = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftDamageResultsTableAndChart"
)

if TYPE_CHECKING:
    from mastapy.utility.enums import _1822


__docformat__ = "restructuredtext en"
__all__ = ("ShaftDamageResultsTableAndChart",)


Self = TypeVar("Self", bound="ShaftDamageResultsTableAndChart")


class ShaftDamageResultsTableAndChart(_1758.CustomReportChart):
    """ShaftDamageResultsTableAndChart

    This is a mastapy class.
    """

    TYPE = _SHAFT_DAMAGE_RESULTS_TABLE_AND_CHART
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ShaftDamageResultsTableAndChart")

    class _Cast_ShaftDamageResultsTableAndChart:
        """Special nested class for casting ShaftDamageResultsTableAndChart to subclasses."""

        def __init__(
            self: "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
            parent: "ShaftDamageResultsTableAndChart",
        ):
            self._parent = parent

        @property
        def custom_report_chart(
            self: "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
        ):
            return self._parent._cast(_1758.CustomReportChart)

        @property
        def custom_report_multi_property_item(
            self: "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
        ):
            pass

            from mastapy.utility.report import _1771

            return self._parent._cast(_1771.CustomReportMultiPropertyItem)

        @property
        def custom_report_multi_property_item_base(
            self: "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
        ):
            from mastapy.utility.report import _1772

            return self._parent._cast(_1772.CustomReportMultiPropertyItemBase)

        @property
        def custom_report_nameable_item(
            self: "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
        ):
            from mastapy.utility.report import _1773

            return self._parent._cast(_1773.CustomReportNameableItem)

        @property
        def custom_report_item(
            self: "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
        ):
            from mastapy.utility.report import _1765

            return self._parent._cast(_1765.CustomReportItem)

        @property
        def shaft_damage_results_table_and_chart(
            self: "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
        ) -> "ShaftDamageResultsTableAndChart":
            return self._parent

        def __getattr__(
            self: "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ShaftDamageResultsTableAndChart.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def display(self: Self) -> "_1822.TableAndChartOptions":
        """mastapy.utility.enums.TableAndChartOptions"""
        temp = self.wrapped.Display

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Enums.TableAndChartOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy.utility.enums._1822", "TableAndChartOptions"
        )(value)

    @display.setter
    @enforce_parameter_types
    def display(self: Self, value: "_1822.TableAndChartOptions"):
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Enums.TableAndChartOptions"
        )
        self.wrapped.Display = value

    @property
    def cast_to(
        self: Self,
    ) -> "ShaftDamageResultsTableAndChart._Cast_ShaftDamageResultsTableAndChart":
        return self._Cast_ShaftDamageResultsTableAndChart(self)
