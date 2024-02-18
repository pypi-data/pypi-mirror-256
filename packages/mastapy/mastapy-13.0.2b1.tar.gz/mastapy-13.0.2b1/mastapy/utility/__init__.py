"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1579 import Command
    from ._1580 import AnalysisRunInformation
    from ._1581 import DispatcherHelper
    from ._1582 import EnvironmentSummary
    from ._1583 import ExternalFullFEFileOption
    from ._1584 import FileHistory
    from ._1585 import FileHistoryItem
    from ._1586 import FolderMonitor
    from ._1588 import IndependentReportablePropertiesBase
    from ._1589 import InputNamePrompter
    from ._1590 import IntegerRange
    from ._1591 import LoadCaseOverrideOption
    from ._1592 import MethodOutcome
    from ._1593 import MethodOutcomeWithResult
    from ._1594 import MKLVersion
    from ._1595 import NumberFormatInfoSummary
    from ._1596 import PerMachineSettings
    from ._1597 import PersistentSingleton
    from ._1598 import ProgramSettings
    from ._1599 import PushbulletSettings
    from ._1600 import RoundingMethods
    from ._1601 import SelectableFolder
    from ._1602 import SystemDirectory
    from ._1603 import SystemDirectoryPopulator
else:
    import_structure = {
        "_1579": ["Command"],
        "_1580": ["AnalysisRunInformation"],
        "_1581": ["DispatcherHelper"],
        "_1582": ["EnvironmentSummary"],
        "_1583": ["ExternalFullFEFileOption"],
        "_1584": ["FileHistory"],
        "_1585": ["FileHistoryItem"],
        "_1586": ["FolderMonitor"],
        "_1588": ["IndependentReportablePropertiesBase"],
        "_1589": ["InputNamePrompter"],
        "_1590": ["IntegerRange"],
        "_1591": ["LoadCaseOverrideOption"],
        "_1592": ["MethodOutcome"],
        "_1593": ["MethodOutcomeWithResult"],
        "_1594": ["MKLVersion"],
        "_1595": ["NumberFormatInfoSummary"],
        "_1596": ["PerMachineSettings"],
        "_1597": ["PersistentSingleton"],
        "_1598": ["ProgramSettings"],
        "_1599": ["PushbulletSettings"],
        "_1600": ["RoundingMethods"],
        "_1601": ["SelectableFolder"],
        "_1602": ["SystemDirectory"],
        "_1603": ["SystemDirectoryPopulator"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Command",
    "AnalysisRunInformation",
    "DispatcherHelper",
    "EnvironmentSummary",
    "ExternalFullFEFileOption",
    "FileHistory",
    "FileHistoryItem",
    "FolderMonitor",
    "IndependentReportablePropertiesBase",
    "InputNamePrompter",
    "IntegerRange",
    "LoadCaseOverrideOption",
    "MethodOutcome",
    "MethodOutcomeWithResult",
    "MKLVersion",
    "NumberFormatInfoSummary",
    "PerMachineSettings",
    "PersistentSingleton",
    "ProgramSettings",
    "PushbulletSettings",
    "RoundingMethods",
    "SelectableFolder",
    "SystemDirectory",
    "SystemDirectoryPopulator",
)
