"""NonLinearBearing"""

from __future__ import annotations

from typing import TypeVar

from mastapy.bearings.bearing_designs import _2132
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_NON_LINEAR_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "NonLinearBearing"
)


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearBearing",)


Self = TypeVar("Self", bound="NonLinearBearing")


class NonLinearBearing(_2132.BearingDesign):
    """NonLinearBearing

    This is a mastapy class.
    """

    TYPE = _NON_LINEAR_BEARING
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_NonLinearBearing")

    class _Cast_NonLinearBearing:
        """Special nested class for casting NonLinearBearing to subclasses."""

        def __init__(
            self: "NonLinearBearing._Cast_NonLinearBearing", parent: "NonLinearBearing"
        ):
            self._parent = parent

        @property
        def bearing_design(self: "NonLinearBearing._Cast_NonLinearBearing"):
            return self._parent._cast(_2132.BearingDesign)

        @property
        def detailed_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs import _2133

            return self._parent._cast(_2133.DetailedBearing)

        @property
        def angular_contact_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2137

            return self._parent._cast(_2137.AngularContactBallBearing)

        @property
        def angular_contact_thrust_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2138

            return self._parent._cast(_2138.AngularContactThrustBallBearing)

        @property
        def asymmetric_spherical_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2139

            return self._parent._cast(_2139.AsymmetricSphericalRollerBearing)

        @property
        def axial_thrust_cylindrical_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2140

            return self._parent._cast(_2140.AxialThrustCylindricalRollerBearing)

        @property
        def axial_thrust_needle_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2141

            return self._parent._cast(_2141.AxialThrustNeedleRollerBearing)

        @property
        def ball_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2142

            return self._parent._cast(_2142.BallBearing)

        @property
        def barrel_roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2144

            return self._parent._cast(_2144.BarrelRollerBearing)

        @property
        def crossed_roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2150

            return self._parent._cast(_2150.CrossedRollerBearing)

        @property
        def cylindrical_roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2151

            return self._parent._cast(_2151.CylindricalRollerBearing)

        @property
        def deep_groove_ball_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2152

            return self._parent._cast(_2152.DeepGrooveBallBearing)

        @property
        def four_point_contact_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2156

            return self._parent._cast(_2156.FourPointContactBallBearing)

        @property
        def multi_point_contact_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2161

            return self._parent._cast(_2161.MultiPointContactBallBearing)

        @property
        def needle_roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2162

            return self._parent._cast(_2162.NeedleRollerBearing)

        @property
        def non_barrel_roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2163

            return self._parent._cast(_2163.NonBarrelRollerBearing)

        @property
        def roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2164

            return self._parent._cast(_2164.RollerBearing)

        @property
        def rolling_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2167

            return self._parent._cast(_2167.RollingBearing)

        @property
        def self_aligning_ball_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2168

            return self._parent._cast(_2168.SelfAligningBallBearing)

        @property
        def spherical_roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2171

            return self._parent._cast(_2171.SphericalRollerBearing)

        @property
        def spherical_roller_thrust_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2172

            return self._parent._cast(_2172.SphericalRollerThrustBearing)

        @property
        def taper_roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2173

            return self._parent._cast(_2173.TaperRollerBearing)

        @property
        def three_point_contact_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.rolling import _2174

            return self._parent._cast(_2174.ThreePointContactBallBearing)

        @property
        def thrust_ball_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2175

            return self._parent._cast(_2175.ThrustBallBearing)

        @property
        def toroidal_roller_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.rolling import _2176

            return self._parent._cast(_2176.ToroidalRollerBearing)

        @property
        def pad_fluid_film_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.fluid_film import _2189

            return self._parent._cast(_2189.PadFluidFilmBearing)

        @property
        def plain_grease_filled_journal_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.fluid_film import _2191

            return self._parent._cast(_2191.PlainGreaseFilledJournalBearing)

        @property
        def plain_journal_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.fluid_film import _2193

            return self._parent._cast(_2193.PlainJournalBearing)

        @property
        def plain_oil_fed_journal_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.fluid_film import _2195

            return self._parent._cast(_2195.PlainOilFedJournalBearing)

        @property
        def tilting_pad_journal_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.fluid_film import _2196

            return self._parent._cast(_2196.TiltingPadJournalBearing)

        @property
        def tilting_pad_thrust_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.fluid_film import _2197

            return self._parent._cast(_2197.TiltingPadThrustBearing)

        @property
        def concept_axial_clearance_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.concept import _2199

            return self._parent._cast(_2199.ConceptAxialClearanceBearing)

        @property
        def concept_clearance_bearing(self: "NonLinearBearing._Cast_NonLinearBearing"):
            from mastapy.bearings.bearing_designs.concept import _2200

            return self._parent._cast(_2200.ConceptClearanceBearing)

        @property
        def concept_radial_clearance_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ):
            from mastapy.bearings.bearing_designs.concept import _2201

            return self._parent._cast(_2201.ConceptRadialClearanceBearing)

        @property
        def non_linear_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "NonLinearBearing":
            return self._parent

        def __getattr__(self: "NonLinearBearing._Cast_NonLinearBearing", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "NonLinearBearing.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "NonLinearBearing._Cast_NonLinearBearing":
        return self._Cast_NonLinearBearing(self)
