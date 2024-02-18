"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter


if TYPE_CHECKING:
    from ._1614 import Acceleration
    from ._1615 import Angle
    from ._1616 import AnglePerUnitTemperature
    from ._1617 import AngleSmall
    from ._1618 import AngleVerySmall
    from ._1619 import AngularAcceleration
    from ._1620 import AngularCompliance
    from ._1621 import AngularJerk
    from ._1622 import AngularStiffness
    from ._1623 import AngularVelocity
    from ._1624 import Area
    from ._1625 import AreaSmall
    from ._1626 import CarbonEmissionFactor
    from ._1627 import CurrentDensity
    from ._1628 import CurrentPerLength
    from ._1629 import Cycles
    from ._1630 import Damage
    from ._1631 import DamageRate
    from ._1632 import DataSize
    from ._1633 import Decibel
    from ._1634 import Density
    from ._1635 import ElectricalResistance
    from ._1636 import ElectricalResistivity
    from ._1637 import ElectricCurrent
    from ._1638 import Energy
    from ._1639 import EnergyPerUnitArea
    from ._1640 import EnergyPerUnitAreaSmall
    from ._1641 import EnergySmall
    from ._1642 import Enum
    from ._1643 import FlowRate
    from ._1644 import Force
    from ._1645 import ForcePerUnitLength
    from ._1646 import ForcePerUnitPressure
    from ._1647 import ForcePerUnitTemperature
    from ._1648 import FractionMeasurementBase
    from ._1649 import FractionPerTemperature
    from ._1650 import Frequency
    from ._1651 import FuelConsumptionEngine
    from ._1652 import FuelEfficiencyVehicle
    from ._1653 import Gradient
    from ._1654 import HeatConductivity
    from ._1655 import HeatTransfer
    from ._1656 import HeatTransferCoefficientForPlasticGearTooth
    from ._1657 import HeatTransferResistance
    from ._1658 import Impulse
    from ._1659 import Index
    from ._1660 import Inductance
    from ._1661 import Integer
    from ._1662 import InverseShortLength
    from ._1663 import InverseShortTime
    from ._1664 import Jerk
    from ._1665 import KinematicViscosity
    from ._1666 import LengthLong
    from ._1667 import LengthMedium
    from ._1668 import LengthPerUnitTemperature
    from ._1669 import LengthShort
    from ._1670 import LengthToTheFourth
    from ._1671 import LengthVeryLong
    from ._1672 import LengthVeryShort
    from ._1673 import LengthVeryShortPerLengthShort
    from ._1674 import LinearAngularDamping
    from ._1675 import LinearAngularStiffnessCrossTerm
    from ._1676 import LinearDamping
    from ._1677 import LinearFlexibility
    from ._1678 import LinearStiffness
    from ._1679 import MagneticFieldStrength
    from ._1680 import MagneticFlux
    from ._1681 import MagneticFluxDensity
    from ._1682 import MagneticVectorPotential
    from ._1683 import MagnetomotiveForce
    from ._1684 import Mass
    from ._1685 import MassPerUnitLength
    from ._1686 import MassPerUnitTime
    from ._1687 import MomentOfInertia
    from ._1688 import MomentOfInertiaPerUnitLength
    from ._1689 import MomentPerUnitPressure
    from ._1690 import Number
    from ._1691 import Percentage
    from ._1692 import Power
    from ._1693 import PowerPerSmallArea
    from ._1694 import PowerPerUnitTime
    from ._1695 import PowerSmall
    from ._1696 import PowerSmallPerArea
    from ._1697 import PowerSmallPerMass
    from ._1698 import PowerSmallPerUnitAreaPerUnitTime
    from ._1699 import PowerSmallPerUnitTime
    from ._1700 import PowerSmallPerVolume
    from ._1701 import Pressure
    from ._1702 import PressurePerUnitTime
    from ._1703 import PressureVelocityProduct
    from ._1704 import PressureViscosityCoefficient
    from ._1705 import Price
    from ._1706 import PricePerUnitMass
    from ._1707 import QuadraticAngularDamping
    from ._1708 import QuadraticDrag
    from ._1709 import RescaledMeasurement
    from ._1710 import Rotatum
    from ._1711 import SafetyFactor
    from ._1712 import SpecificAcousticImpedance
    from ._1713 import SpecificHeat
    from ._1714 import SquareRootOfUnitForcePerUnitArea
    from ._1715 import StiffnessPerUnitFaceWidth
    from ._1716 import Stress
    from ._1717 import Temperature
    from ._1718 import TemperatureDifference
    from ._1719 import TemperaturePerUnitTime
    from ._1720 import Text
    from ._1721 import ThermalContactCoefficient
    from ._1722 import ThermalExpansionCoefficient
    from ._1723 import ThermoElasticFactor
    from ._1724 import Time
    from ._1725 import TimeShort
    from ._1726 import TimeVeryShort
    from ._1727 import Torque
    from ._1728 import TorqueConverterInverseK
    from ._1729 import TorqueConverterK
    from ._1730 import TorquePerCurrent
    from ._1731 import TorquePerSquareRootOfPower
    from ._1732 import TorquePerUnitTemperature
    from ._1733 import Velocity
    from ._1734 import VelocitySmall
    from ._1735 import Viscosity
    from ._1736 import Voltage
    from ._1737 import VoltagePerAngularVelocity
    from ._1738 import Volume
    from ._1739 import WearCoefficient
    from ._1740 import Yank
else:
    import_structure = {
        "_1614": ["Acceleration"],
        "_1615": ["Angle"],
        "_1616": ["AnglePerUnitTemperature"],
        "_1617": ["AngleSmall"],
        "_1618": ["AngleVerySmall"],
        "_1619": ["AngularAcceleration"],
        "_1620": ["AngularCompliance"],
        "_1621": ["AngularJerk"],
        "_1622": ["AngularStiffness"],
        "_1623": ["AngularVelocity"],
        "_1624": ["Area"],
        "_1625": ["AreaSmall"],
        "_1626": ["CarbonEmissionFactor"],
        "_1627": ["CurrentDensity"],
        "_1628": ["CurrentPerLength"],
        "_1629": ["Cycles"],
        "_1630": ["Damage"],
        "_1631": ["DamageRate"],
        "_1632": ["DataSize"],
        "_1633": ["Decibel"],
        "_1634": ["Density"],
        "_1635": ["ElectricalResistance"],
        "_1636": ["ElectricalResistivity"],
        "_1637": ["ElectricCurrent"],
        "_1638": ["Energy"],
        "_1639": ["EnergyPerUnitArea"],
        "_1640": ["EnergyPerUnitAreaSmall"],
        "_1641": ["EnergySmall"],
        "_1642": ["Enum"],
        "_1643": ["FlowRate"],
        "_1644": ["Force"],
        "_1645": ["ForcePerUnitLength"],
        "_1646": ["ForcePerUnitPressure"],
        "_1647": ["ForcePerUnitTemperature"],
        "_1648": ["FractionMeasurementBase"],
        "_1649": ["FractionPerTemperature"],
        "_1650": ["Frequency"],
        "_1651": ["FuelConsumptionEngine"],
        "_1652": ["FuelEfficiencyVehicle"],
        "_1653": ["Gradient"],
        "_1654": ["HeatConductivity"],
        "_1655": ["HeatTransfer"],
        "_1656": ["HeatTransferCoefficientForPlasticGearTooth"],
        "_1657": ["HeatTransferResistance"],
        "_1658": ["Impulse"],
        "_1659": ["Index"],
        "_1660": ["Inductance"],
        "_1661": ["Integer"],
        "_1662": ["InverseShortLength"],
        "_1663": ["InverseShortTime"],
        "_1664": ["Jerk"],
        "_1665": ["KinematicViscosity"],
        "_1666": ["LengthLong"],
        "_1667": ["LengthMedium"],
        "_1668": ["LengthPerUnitTemperature"],
        "_1669": ["LengthShort"],
        "_1670": ["LengthToTheFourth"],
        "_1671": ["LengthVeryLong"],
        "_1672": ["LengthVeryShort"],
        "_1673": ["LengthVeryShortPerLengthShort"],
        "_1674": ["LinearAngularDamping"],
        "_1675": ["LinearAngularStiffnessCrossTerm"],
        "_1676": ["LinearDamping"],
        "_1677": ["LinearFlexibility"],
        "_1678": ["LinearStiffness"],
        "_1679": ["MagneticFieldStrength"],
        "_1680": ["MagneticFlux"],
        "_1681": ["MagneticFluxDensity"],
        "_1682": ["MagneticVectorPotential"],
        "_1683": ["MagnetomotiveForce"],
        "_1684": ["Mass"],
        "_1685": ["MassPerUnitLength"],
        "_1686": ["MassPerUnitTime"],
        "_1687": ["MomentOfInertia"],
        "_1688": ["MomentOfInertiaPerUnitLength"],
        "_1689": ["MomentPerUnitPressure"],
        "_1690": ["Number"],
        "_1691": ["Percentage"],
        "_1692": ["Power"],
        "_1693": ["PowerPerSmallArea"],
        "_1694": ["PowerPerUnitTime"],
        "_1695": ["PowerSmall"],
        "_1696": ["PowerSmallPerArea"],
        "_1697": ["PowerSmallPerMass"],
        "_1698": ["PowerSmallPerUnitAreaPerUnitTime"],
        "_1699": ["PowerSmallPerUnitTime"],
        "_1700": ["PowerSmallPerVolume"],
        "_1701": ["Pressure"],
        "_1702": ["PressurePerUnitTime"],
        "_1703": ["PressureVelocityProduct"],
        "_1704": ["PressureViscosityCoefficient"],
        "_1705": ["Price"],
        "_1706": ["PricePerUnitMass"],
        "_1707": ["QuadraticAngularDamping"],
        "_1708": ["QuadraticDrag"],
        "_1709": ["RescaledMeasurement"],
        "_1710": ["Rotatum"],
        "_1711": ["SafetyFactor"],
        "_1712": ["SpecificAcousticImpedance"],
        "_1713": ["SpecificHeat"],
        "_1714": ["SquareRootOfUnitForcePerUnitArea"],
        "_1715": ["StiffnessPerUnitFaceWidth"],
        "_1716": ["Stress"],
        "_1717": ["Temperature"],
        "_1718": ["TemperatureDifference"],
        "_1719": ["TemperaturePerUnitTime"],
        "_1720": ["Text"],
        "_1721": ["ThermalContactCoefficient"],
        "_1722": ["ThermalExpansionCoefficient"],
        "_1723": ["ThermoElasticFactor"],
        "_1724": ["Time"],
        "_1725": ["TimeShort"],
        "_1726": ["TimeVeryShort"],
        "_1727": ["Torque"],
        "_1728": ["TorqueConverterInverseK"],
        "_1729": ["TorqueConverterK"],
        "_1730": ["TorquePerCurrent"],
        "_1731": ["TorquePerSquareRootOfPower"],
        "_1732": ["TorquePerUnitTemperature"],
        "_1733": ["Velocity"],
        "_1734": ["VelocitySmall"],
        "_1735": ["Viscosity"],
        "_1736": ["Voltage"],
        "_1737": ["VoltagePerAngularVelocity"],
        "_1738": ["Volume"],
        "_1739": ["WearCoefficient"],
        "_1740": ["Yank"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Acceleration",
    "Angle",
    "AnglePerUnitTemperature",
    "AngleSmall",
    "AngleVerySmall",
    "AngularAcceleration",
    "AngularCompliance",
    "AngularJerk",
    "AngularStiffness",
    "AngularVelocity",
    "Area",
    "AreaSmall",
    "CarbonEmissionFactor",
    "CurrentDensity",
    "CurrentPerLength",
    "Cycles",
    "Damage",
    "DamageRate",
    "DataSize",
    "Decibel",
    "Density",
    "ElectricalResistance",
    "ElectricalResistivity",
    "ElectricCurrent",
    "Energy",
    "EnergyPerUnitArea",
    "EnergyPerUnitAreaSmall",
    "EnergySmall",
    "Enum",
    "FlowRate",
    "Force",
    "ForcePerUnitLength",
    "ForcePerUnitPressure",
    "ForcePerUnitTemperature",
    "FractionMeasurementBase",
    "FractionPerTemperature",
    "Frequency",
    "FuelConsumptionEngine",
    "FuelEfficiencyVehicle",
    "Gradient",
    "HeatConductivity",
    "HeatTransfer",
    "HeatTransferCoefficientForPlasticGearTooth",
    "HeatTransferResistance",
    "Impulse",
    "Index",
    "Inductance",
    "Integer",
    "InverseShortLength",
    "InverseShortTime",
    "Jerk",
    "KinematicViscosity",
    "LengthLong",
    "LengthMedium",
    "LengthPerUnitTemperature",
    "LengthShort",
    "LengthToTheFourth",
    "LengthVeryLong",
    "LengthVeryShort",
    "LengthVeryShortPerLengthShort",
    "LinearAngularDamping",
    "LinearAngularStiffnessCrossTerm",
    "LinearDamping",
    "LinearFlexibility",
    "LinearStiffness",
    "MagneticFieldStrength",
    "MagneticFlux",
    "MagneticFluxDensity",
    "MagneticVectorPotential",
    "MagnetomotiveForce",
    "Mass",
    "MassPerUnitLength",
    "MassPerUnitTime",
    "MomentOfInertia",
    "MomentOfInertiaPerUnitLength",
    "MomentPerUnitPressure",
    "Number",
    "Percentage",
    "Power",
    "PowerPerSmallArea",
    "PowerPerUnitTime",
    "PowerSmall",
    "PowerSmallPerArea",
    "PowerSmallPerMass",
    "PowerSmallPerUnitAreaPerUnitTime",
    "PowerSmallPerUnitTime",
    "PowerSmallPerVolume",
    "Pressure",
    "PressurePerUnitTime",
    "PressureVelocityProduct",
    "PressureViscosityCoefficient",
    "Price",
    "PricePerUnitMass",
    "QuadraticAngularDamping",
    "QuadraticDrag",
    "RescaledMeasurement",
    "Rotatum",
    "SafetyFactor",
    "SpecificAcousticImpedance",
    "SpecificHeat",
    "SquareRootOfUnitForcePerUnitArea",
    "StiffnessPerUnitFaceWidth",
    "Stress",
    "Temperature",
    "TemperatureDifference",
    "TemperaturePerUnitTime",
    "Text",
    "ThermalContactCoefficient",
    "ThermalExpansionCoefficient",
    "ThermoElasticFactor",
    "Time",
    "TimeShort",
    "TimeVeryShort",
    "Torque",
    "TorqueConverterInverseK",
    "TorqueConverterK",
    "TorquePerCurrent",
    "TorquePerSquareRootOfPower",
    "TorquePerUnitTemperature",
    "Velocity",
    "VelocitySmall",
    "Viscosity",
    "Voltage",
    "VoltagePerAngularVelocity",
    "Volume",
    "WearCoefficient",
    "Yank",
)
