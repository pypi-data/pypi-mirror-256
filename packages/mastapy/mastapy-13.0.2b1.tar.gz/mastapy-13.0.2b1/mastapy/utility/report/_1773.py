"""CustomReportNameableItem"""

from __future__ import annotations

from typing import TypeVar

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy.utility.report import _1765
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_NAMEABLE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportNameableItem"
)


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportNameableItem",)


Self = TypeVar("Self", bound="CustomReportNameableItem")


class CustomReportNameableItem(_1765.CustomReportItem):
    """CustomReportNameableItem

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_NAMEABLE_ITEM
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CustomReportNameableItem")

    class _Cast_CustomReportNameableItem:
        """Special nested class for casting CustomReportNameableItem to subclasses."""

        def __init__(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
            parent: "CustomReportNameableItem",
        ):
            self._parent = parent

        @property
        def custom_report_item(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            return self._parent._cast(_1765.CustomReportItem)

        @property
        def shaft_damage_results_table_and_chart(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.shafts import _20

            return self._parent._cast(_20.ShaftDamageResultsTableAndChart)

        @property
        def cylindrical_gear_table_with_mg_charts(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.gears.gear_designs.cylindrical import _1035

            return self._parent._cast(_1035.CylindricalGearTableWithMGCharts)

        @property
        def ad_hoc_custom_table(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1744

            return self._parent._cast(_1744.AdHocCustomTable)

        @property
        def custom_chart(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1752

            return self._parent._cast(_1752.CustomChart)

        @property
        def custom_drawing(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1753

            return self._parent._cast(_1753.CustomDrawing)

        @property
        def custom_graphic(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1754

            return self._parent._cast(_1754.CustomGraphic)

        @property
        def custom_image(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1755

            return self._parent._cast(_1755.CustomImage)

        @property
        def custom_report_cad_drawing(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1757

            return self._parent._cast(_1757.CustomReportCadDrawing)

        @property
        def custom_report_chart(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1758

            return self._parent._cast(_1758.CustomReportChart)

        @property
        def custom_report_definition_item(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1762

            return self._parent._cast(_1762.CustomReportDefinitionItem)

        @property
        def custom_report_html_item(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1764

            return self._parent._cast(_1764.CustomReportHtmlItem)

        @property
        def custom_report_multi_property_item(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1771

            return self._parent._cast(_1771.CustomReportMultiPropertyItem)

        @property
        def custom_report_multi_property_item_base(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1772

            return self._parent._cast(_1772.CustomReportMultiPropertyItemBase)

        @property
        def custom_report_named_item(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1774

            return self._parent._cast(_1774.CustomReportNamedItem)

        @property
        def custom_report_status_item(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1776

            return self._parent._cast(_1776.CustomReportStatusItem)

        @property
        def custom_report_text(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1779

            return self._parent._cast(_1779.CustomReportText)

        @property
        def custom_sub_report(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1781

            return self._parent._cast(_1781.CustomSubReport)

        @property
        def custom_table(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1782

            return self._parent._cast(_1782.CustomTable)

        @property
        def dynamic_custom_report_item(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility.report import _1784

            return self._parent._cast(_1784.DynamicCustomReportItem)

        @property
        def custom_line_chart(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility_gui.charts import _1856

            return self._parent._cast(_1856.CustomLineChart)

        @property
        def custom_table_and_chart(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.utility_gui.charts import _1857

            return self._parent._cast(_1857.CustomTableAndChart)

        @property
        def loaded_ball_element_chart_reporter(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.bearings.bearing_results import _1948

            return self._parent._cast(_1948.LoadedBallElementChartReporter)

        @property
        def loaded_bearing_chart_reporter(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.bearings.bearing_results import _1949

            return self._parent._cast(_1949.LoadedBearingChartReporter)

        @property
        def loaded_bearing_temperature_chart(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.bearings.bearing_results import _1952

            return self._parent._cast(_1952.LoadedBearingTemperatureChart)

        @property
        def loaded_roller_element_chart_reporter(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.bearings.bearing_results import _1960

            return self._parent._cast(_1960.LoadedRollerElementChartReporter)

        @property
        def shaft_system_deflection_sections_report(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.system_model.analyses_and_results.system_deflections.reporting import (
                _2851,
            )

            return self._parent._cast(_2851.ShaftSystemDeflectionSectionsReport)

        @property
        def parametric_study_histogram(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4388,
            )

            return self._parent._cast(_4388.ParametricStudyHistogram)

        @property
        def campbell_diagram_report(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
                _4719,
            )

            return self._parent._cast(_4719.CampbellDiagramReport)

        @property
        def per_mode_results_report(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ):
            from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
                _4723,
            )

            return self._parent._cast(_4723.PerModeResultsReport)

        @property
        def custom_report_nameable_item(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem",
        ) -> "CustomReportNameableItem":
            return self._parent

        def __getattr__(
            self: "CustomReportNameableItem._Cast_CustomReportNameableItem", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CustomReportNameableItem.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self: Self) -> "str":
        """str"""
        temp = self.wrapped.Name

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: Self, value: "str"):
        self.wrapped.Name = str(value) if value is not None else ""

    @property
    def x_position_for_cad(self: Self) -> "float":
        """float"""
        temp = self.wrapped.XPositionForCAD

        if temp is None:
            return 0.0

        return temp

    @x_position_for_cad.setter
    @enforce_parameter_types
    def x_position_for_cad(self: Self, value: "float"):
        self.wrapped.XPositionForCAD = float(value) if value is not None else 0.0

    @property
    def y_position_for_cad(self: Self) -> "float":
        """float"""
        temp = self.wrapped.YPositionForCAD

        if temp is None:
            return 0.0

        return temp

    @y_position_for_cad.setter
    @enforce_parameter_types
    def y_position_for_cad(self: Self, value: "float"):
        self.wrapped.YPositionForCAD = float(value) if value is not None else 0.0

    @property
    def cast_to(
        self: Self,
    ) -> "CustomReportNameableItem._Cast_CustomReportNameableItem":
        return self._Cast_CustomReportNameableItem(self)
