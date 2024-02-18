"""CustomReportDefinitionItem"""

from __future__ import annotations

from typing import TypeVar

from mastapy.utility.report import _1773
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_DEFINITION_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportDefinitionItem"
)


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportDefinitionItem",)


Self = TypeVar("Self", bound="CustomReportDefinitionItem")


class CustomReportDefinitionItem(_1773.CustomReportNameableItem):
    """CustomReportDefinitionItem

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_DEFINITION_ITEM
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CustomReportDefinitionItem")

    class _Cast_CustomReportDefinitionItem:
        """Special nested class for casting CustomReportDefinitionItem to subclasses."""

        def __init__(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
            parent: "CustomReportDefinitionItem",
        ):
            self._parent = parent

        @property
        def custom_report_nameable_item(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            return self._parent._cast(_1773.CustomReportNameableItem)

        @property
        def custom_report_item(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1765

            return self._parent._cast(_1765.CustomReportItem)

        @property
        def ad_hoc_custom_table(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1744

            return self._parent._cast(_1744.AdHocCustomTable)

        @property
        def custom_chart(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1752

            return self._parent._cast(_1752.CustomChart)

        @property
        def custom_drawing(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1753

            return self._parent._cast(_1753.CustomDrawing)

        @property
        def custom_graphic(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1754

            return self._parent._cast(_1754.CustomGraphic)

        @property
        def custom_image(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1755

            return self._parent._cast(_1755.CustomImage)

        @property
        def custom_report_html_item(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1764

            return self._parent._cast(_1764.CustomReportHtmlItem)

        @property
        def custom_report_status_item(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1776

            return self._parent._cast(_1776.CustomReportStatusItem)

        @property
        def custom_report_text(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1779

            return self._parent._cast(_1779.CustomReportText)

        @property
        def custom_sub_report(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.utility.report import _1781

            return self._parent._cast(_1781.CustomSubReport)

        @property
        def loaded_bearing_chart_reporter(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.bearings.bearing_results import _1949

            return self._parent._cast(_1949.LoadedBearingChartReporter)

        @property
        def parametric_study_histogram(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4388,
            )

            return self._parent._cast(_4388.ParametricStudyHistogram)

        @property
        def custom_report_definition_item(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
        ) -> "CustomReportDefinitionItem":
            return self._parent

        def __getattr__(
            self: "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CustomReportDefinitionItem.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "CustomReportDefinitionItem._Cast_CustomReportDefinitionItem":
        return self._Cast_CustomReportDefinitionItem(self)
