"""CustomReportMultiPropertyItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

from mastapy.utility.report import _1772
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportMultiPropertyItem"
)

if TYPE_CHECKING:
    from mastapy.utility.report import _1775


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportMultiPropertyItem",)


Self = TypeVar("Self", bound="CustomReportMultiPropertyItem")
TItem = TypeVar("TItem", bound="_1775.CustomReportPropertyItem")


class CustomReportMultiPropertyItem(
    _1772.CustomReportMultiPropertyItemBase, Generic[TItem]
):
    """CustomReportMultiPropertyItem

    This is a mastapy class.

    Generic Types:
        TItem
    """

    TYPE = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CustomReportMultiPropertyItem")

    class _Cast_CustomReportMultiPropertyItem:
        """Special nested class for casting CustomReportMultiPropertyItem to subclasses."""

        def __init__(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
            parent: "CustomReportMultiPropertyItem",
        ):
            self._parent = parent

        @property
        def custom_report_multi_property_item_base(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            return self._parent._cast(_1772.CustomReportMultiPropertyItemBase)

        @property
        def custom_report_nameable_item(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.utility.report import _1773

            return self._parent._cast(_1773.CustomReportNameableItem)

        @property
        def custom_report_item(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.utility.report import _1765

            return self._parent._cast(_1765.CustomReportItem)

        @property
        def shaft_damage_results_table_and_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.shafts import _20

            return self._parent._cast(_20.ShaftDamageResultsTableAndChart)

        @property
        def cylindrical_gear_table_with_mg_charts(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.gears.gear_designs.cylindrical import _1035

            return self._parent._cast(_1035.CylindricalGearTableWithMGCharts)

        @property
        def custom_report_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.utility.report import _1758

            return self._parent._cast(_1758.CustomReportChart)

        @property
        def custom_table(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.utility.report import _1782

            return self._parent._cast(_1782.CustomTable)

        @property
        def custom_line_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.utility_gui.charts import _1856

            return self._parent._cast(_1856.CustomLineChart)

        @property
        def custom_table_and_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.utility_gui.charts import _1857

            return self._parent._cast(_1857.CustomTableAndChart)

        @property
        def loaded_ball_element_chart_reporter(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.bearings.bearing_results import _1948

            return self._parent._cast(_1948.LoadedBallElementChartReporter)

        @property
        def loaded_bearing_temperature_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.bearings.bearing_results import _1952

            return self._parent._cast(_1952.LoadedBearingTemperatureChart)

        @property
        def loaded_roller_element_chart_reporter(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.bearings.bearing_results import _1960

            return self._parent._cast(_1960.LoadedRollerElementChartReporter)

        @property
        def shaft_system_deflection_sections_report(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.reporting import (
                _2851,
            )

            return self._parent._cast(_2851.ShaftSystemDeflectionSectionsReport)

        @property
        def campbell_diagram_report(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
                _4719,
            )

            return self._parent._cast(_4719.CampbellDiagramReport)

        @property
        def per_mode_results_report(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
                _4723,
            )

            return self._parent._cast(_4723.PerModeResultsReport)

        @property
        def custom_report_multi_property_item(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "CustomReportMultiPropertyItem":
            return self._parent

        def __getattr__(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CustomReportMultiPropertyItem.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem":
        return self._Cast_CustomReportMultiPropertyItem(self)
