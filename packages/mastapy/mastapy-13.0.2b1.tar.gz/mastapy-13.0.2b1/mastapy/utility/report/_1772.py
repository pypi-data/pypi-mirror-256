"""CustomReportMultiPropertyItemBase"""

from __future__ import annotations

from typing import TypeVar

from mastapy.utility.report import _1773
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM_BASE = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportMultiPropertyItemBase"
)


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportMultiPropertyItemBase",)


Self = TypeVar("Self", bound="CustomReportMultiPropertyItemBase")


class CustomReportMultiPropertyItemBase(_1773.CustomReportNameableItem):
    """CustomReportMultiPropertyItemBase

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM_BASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CustomReportMultiPropertyItemBase")

    class _Cast_CustomReportMultiPropertyItemBase:
        """Special nested class for casting CustomReportMultiPropertyItemBase to subclasses."""

        def __init__(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
            parent: "CustomReportMultiPropertyItemBase",
        ):
            self._parent = parent

        @property
        def custom_report_nameable_item(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            return self._parent._cast(_1773.CustomReportNameableItem)

        @property
        def custom_report_item(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.utility.report import _1765

            return self._parent._cast(_1765.CustomReportItem)

        @property
        def shaft_damage_results_table_and_chart(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.shafts import _20

            return self._parent._cast(_20.ShaftDamageResultsTableAndChart)

        @property
        def cylindrical_gear_table_with_mg_charts(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.gears.gear_designs.cylindrical import _1035

            return self._parent._cast(_1035.CylindricalGearTableWithMGCharts)

        @property
        def custom_report_chart(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.utility.report import _1758

            return self._parent._cast(_1758.CustomReportChart)

        @property
        def custom_report_multi_property_item(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.utility.report import _1771

            return self._parent._cast(_1771.CustomReportMultiPropertyItem)

        @property
        def custom_table(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.utility.report import _1782

            return self._parent._cast(_1782.CustomTable)

        @property
        def custom_line_chart(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.utility_gui.charts import _1856

            return self._parent._cast(_1856.CustomLineChart)

        @property
        def custom_table_and_chart(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.utility_gui.charts import _1857

            return self._parent._cast(_1857.CustomTableAndChart)

        @property
        def loaded_ball_element_chart_reporter(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.bearings.bearing_results import _1948

            return self._parent._cast(_1948.LoadedBallElementChartReporter)

        @property
        def loaded_bearing_temperature_chart(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.bearings.bearing_results import _1952

            return self._parent._cast(_1952.LoadedBearingTemperatureChart)

        @property
        def loaded_roller_element_chart_reporter(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.bearings.bearing_results import _1960

            return self._parent._cast(_1960.LoadedRollerElementChartReporter)

        @property
        def shaft_system_deflection_sections_report(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.reporting import (
                _2851,
            )

            return self._parent._cast(_2851.ShaftSystemDeflectionSectionsReport)

        @property
        def campbell_diagram_report(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
                _4719,
            )

            return self._parent._cast(_4719.CampbellDiagramReport)

        @property
        def per_mode_results_report(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
                _4723,
            )

            return self._parent._cast(_4723.PerModeResultsReport)

        @property
        def custom_report_multi_property_item_base(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
        ) -> "CustomReportMultiPropertyItemBase":
            return self._parent

        def __getattr__(
            self: "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(
        self: Self, instance_to_wrap: "CustomReportMultiPropertyItemBase.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase":
        return self._Cast_CustomReportMultiPropertyItemBase(self)
