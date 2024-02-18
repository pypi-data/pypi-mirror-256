"""ParetoHypoidGearSetOptimisationStrategyDatabase"""

from __future__ import annotations

from typing import TypeVar

from mastapy.gears.gear_set_pareto_optimiser import _923
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PARETO_HYPOID_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser",
    "ParetoHypoidGearSetOptimisationStrategyDatabase",
)


__docformat__ = "restructuredtext en"
__all__ = ("ParetoHypoidGearSetOptimisationStrategyDatabase",)


Self = TypeVar("Self", bound="ParetoHypoidGearSetOptimisationStrategyDatabase")


class ParetoHypoidGearSetOptimisationStrategyDatabase(
    _923.ParetoConicalRatingOptimisationStrategyDatabase
):
    """ParetoHypoidGearSetOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _PARETO_HYPOID_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_ParetoHypoidGearSetOptimisationStrategyDatabase"
    )

    class _Cast_ParetoHypoidGearSetOptimisationStrategyDatabase:
        """Special nested class for casting ParetoHypoidGearSetOptimisationStrategyDatabase to subclasses."""

        def __init__(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
            parent: "ParetoHypoidGearSetOptimisationStrategyDatabase",
        ):
            self._parent = parent

        @property
        def pareto_conical_rating_optimisation_strategy_database(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
        ):
            return self._parent._cast(
                _923.ParetoConicalRatingOptimisationStrategyDatabase
            )

        @property
        def pareto_optimisation_strategy_database(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
        ):
            from mastapy.math_utility.optimisation import _1554

            return self._parent._cast(_1554.ParetoOptimisationStrategyDatabase)

        @property
        def design_space_search_strategy_database(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
        ):
            from mastapy.math_utility.optimisation import _1541

            return self._parent._cast(_1541.DesignSpaceSearchStrategyDatabase)

        @property
        def named_database(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
        ):
            pass

            from mastapy.utility.databases import _1830

            return self._parent._cast(_1830.NamedDatabase)

        @property
        def sql_database(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
        ):
            pass

            from mastapy.utility.databases import _1833

            return self._parent._cast(_1833.SQLDatabase)

        @property
        def database(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
        ):
            pass

            from mastapy.utility.databases import _1826

            return self._parent._cast(_1826.Database)

        @property
        def pareto_hypoid_gear_set_optimisation_strategy_database(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
        ) -> "ParetoHypoidGearSetOptimisationStrategyDatabase":
            return self._parent

        def __getattr__(
            self: "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase",
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
        self: Self,
        instance_to_wrap: "ParetoHypoidGearSetOptimisationStrategyDatabase.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "ParetoHypoidGearSetOptimisationStrategyDatabase._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase":
        return self._Cast_ParetoHypoidGearSetOptimisationStrategyDatabase(self)
