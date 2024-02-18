"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1744 import AdHocCustomTable
    from ._1745 import AxisSettings
    from ._1746 import BlankRow
    from ._1747 import CadPageOrientation
    from ._1748 import CadPageSize
    from ._1749 import CadTableBorderType
    from ._1750 import ChartDefinition
    from ._1751 import SMTChartPointShape
    from ._1752 import CustomChart
    from ._1753 import CustomDrawing
    from ._1754 import CustomGraphic
    from ._1755 import CustomImage
    from ._1756 import CustomReport
    from ._1757 import CustomReportCadDrawing
    from ._1758 import CustomReportChart
    from ._1759 import CustomReportChartItem
    from ._1760 import CustomReportColumn
    from ._1761 import CustomReportColumns
    from ._1762 import CustomReportDefinitionItem
    from ._1763 import CustomReportHorizontalLine
    from ._1764 import CustomReportHtmlItem
    from ._1765 import CustomReportItem
    from ._1766 import CustomReportItemContainer
    from ._1767 import CustomReportItemContainerCollection
    from ._1768 import CustomReportItemContainerCollectionBase
    from ._1769 import CustomReportItemContainerCollectionItem
    from ._1770 import CustomReportKey
    from ._1771 import CustomReportMultiPropertyItem
    from ._1772 import CustomReportMultiPropertyItemBase
    from ._1773 import CustomReportNameableItem
    from ._1774 import CustomReportNamedItem
    from ._1775 import CustomReportPropertyItem
    from ._1776 import CustomReportStatusItem
    from ._1777 import CustomReportTab
    from ._1778 import CustomReportTabs
    from ._1779 import CustomReportText
    from ._1780 import CustomRow
    from ._1781 import CustomSubReport
    from ._1782 import CustomTable
    from ._1783 import DefinitionBooleanCheckOptions
    from ._1784 import DynamicCustomReportItem
    from ._1785 import FontStyle
    from ._1786 import FontWeight
    from ._1787 import HeadingSize
    from ._1788 import SimpleChartDefinition
    from ._1789 import UserTextRow
else:
    import_structure = {
        "_1744": ["AdHocCustomTable"],
        "_1745": ["AxisSettings"],
        "_1746": ["BlankRow"],
        "_1747": ["CadPageOrientation"],
        "_1748": ["CadPageSize"],
        "_1749": ["CadTableBorderType"],
        "_1750": ["ChartDefinition"],
        "_1751": ["SMTChartPointShape"],
        "_1752": ["CustomChart"],
        "_1753": ["CustomDrawing"],
        "_1754": ["CustomGraphic"],
        "_1755": ["CustomImage"],
        "_1756": ["CustomReport"],
        "_1757": ["CustomReportCadDrawing"],
        "_1758": ["CustomReportChart"],
        "_1759": ["CustomReportChartItem"],
        "_1760": ["CustomReportColumn"],
        "_1761": ["CustomReportColumns"],
        "_1762": ["CustomReportDefinitionItem"],
        "_1763": ["CustomReportHorizontalLine"],
        "_1764": ["CustomReportHtmlItem"],
        "_1765": ["CustomReportItem"],
        "_1766": ["CustomReportItemContainer"],
        "_1767": ["CustomReportItemContainerCollection"],
        "_1768": ["CustomReportItemContainerCollectionBase"],
        "_1769": ["CustomReportItemContainerCollectionItem"],
        "_1770": ["CustomReportKey"],
        "_1771": ["CustomReportMultiPropertyItem"],
        "_1772": ["CustomReportMultiPropertyItemBase"],
        "_1773": ["CustomReportNameableItem"],
        "_1774": ["CustomReportNamedItem"],
        "_1775": ["CustomReportPropertyItem"],
        "_1776": ["CustomReportStatusItem"],
        "_1777": ["CustomReportTab"],
        "_1778": ["CustomReportTabs"],
        "_1779": ["CustomReportText"],
        "_1780": ["CustomRow"],
        "_1781": ["CustomSubReport"],
        "_1782": ["CustomTable"],
        "_1783": ["DefinitionBooleanCheckOptions"],
        "_1784": ["DynamicCustomReportItem"],
        "_1785": ["FontStyle"],
        "_1786": ["FontWeight"],
        "_1787": ["HeadingSize"],
        "_1788": ["SimpleChartDefinition"],
        "_1789": ["UserTextRow"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "AdHocCustomTable",
    "AxisSettings",
    "BlankRow",
    "CadPageOrientation",
    "CadPageSize",
    "CadTableBorderType",
    "ChartDefinition",
    "SMTChartPointShape",
    "CustomChart",
    "CustomDrawing",
    "CustomGraphic",
    "CustomImage",
    "CustomReport",
    "CustomReportCadDrawing",
    "CustomReportChart",
    "CustomReportChartItem",
    "CustomReportColumn",
    "CustomReportColumns",
    "CustomReportDefinitionItem",
    "CustomReportHorizontalLine",
    "CustomReportHtmlItem",
    "CustomReportItem",
    "CustomReportItemContainer",
    "CustomReportItemContainerCollection",
    "CustomReportItemContainerCollectionBase",
    "CustomReportItemContainerCollectionItem",
    "CustomReportKey",
    "CustomReportMultiPropertyItem",
    "CustomReportMultiPropertyItemBase",
    "CustomReportNameableItem",
    "CustomReportNamedItem",
    "CustomReportPropertyItem",
    "CustomReportStatusItem",
    "CustomReportTab",
    "CustomReportTabs",
    "CustomReportText",
    "CustomRow",
    "CustomSubReport",
    "CustomTable",
    "DefinitionBooleanCheckOptions",
    "DynamicCustomReportItem",
    "FontStyle",
    "FontWeight",
    "HeadingSize",
    "SimpleChartDefinition",
    "UserTextRow",
)
