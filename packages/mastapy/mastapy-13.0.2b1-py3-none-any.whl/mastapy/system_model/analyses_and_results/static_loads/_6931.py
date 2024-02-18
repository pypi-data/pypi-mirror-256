"""PartLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal.sentinels import ListWithSelectedItem_None
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import _6900, _6807
from mastapy.system_model.analyses_and_results import _2659
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PartLoadCase"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2470
    from mastapy.system_model.analyses_and_results.static_loads import _6808
    from mastapy.electric_machines.harmonic_load_data import _1381


__docformat__ = "restructuredtext en"
__all__ = ("PartLoadCase",)


Self = TypeVar("Self", bound="PartLoadCase")


class PartLoadCase(_2659.PartAnalysis):
    """PartLoadCase

    This is a mastapy class.
    """

    TYPE = _PART_LOAD_CASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PartLoadCase")

    class _Cast_PartLoadCase:
        """Special nested class for casting PartLoadCase to subclasses."""

        def __init__(self: "PartLoadCase._Cast_PartLoadCase", parent: "PartLoadCase"):
            self._parent = parent

        @property
        def part_analysis(self: "PartLoadCase._Cast_PartLoadCase"):
            return self._parent._cast(_2659.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results import _2655

            return self._parent._cast(_2655.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntityAnalysis)

        @property
        def abstract_assembly_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6809

            return self._parent._cast(_6809.AbstractAssemblyLoadCase)

        @property
        def abstract_shaft_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6810

            return self._parent._cast(_6810.AbstractShaftLoadCase)

        @property
        def abstract_shaft_or_housing_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6811

            return self._parent._cast(_6811.AbstractShaftOrHousingLoadCase)

        @property
        def agma_gleason_conical_gear_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6816

            return self._parent._cast(_6816.AGMAGleasonConicalGearLoadCase)

        @property
        def agma_gleason_conical_gear_set_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6818

            return self._parent._cast(_6818.AGMAGleasonConicalGearSetLoadCase)

        @property
        def assembly_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6821

            return self._parent._cast(_6821.AssemblyLoadCase)

        @property
        def bearing_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6822

            return self._parent._cast(_6822.BearingLoadCase)

        @property
        def belt_drive_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6824

            return self._parent._cast(_6824.BeltDriveLoadCase)

        @property
        def bevel_differential_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6825

            return self._parent._cast(_6825.BevelDifferentialGearLoadCase)

        @property
        def bevel_differential_gear_set_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6827

            return self._parent._cast(_6827.BevelDifferentialGearSetLoadCase)

        @property
        def bevel_differential_planet_gear_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6828

            return self._parent._cast(_6828.BevelDifferentialPlanetGearLoadCase)

        @property
        def bevel_differential_sun_gear_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6829

            return self._parent._cast(_6829.BevelDifferentialSunGearLoadCase)

        @property
        def bevel_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6830

            return self._parent._cast(_6830.BevelGearLoadCase)

        @property
        def bevel_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6832

            return self._parent._cast(_6832.BevelGearSetLoadCase)

        @property
        def bolted_joint_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6833

            return self._parent._cast(_6833.BoltedJointLoadCase)

        @property
        def bolt_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6834

            return self._parent._cast(_6834.BoltLoadCase)

        @property
        def clutch_half_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6836

            return self._parent._cast(_6836.ClutchHalfLoadCase)

        @property
        def clutch_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6837

            return self._parent._cast(_6837.ClutchLoadCase)

        @property
        def component_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6840

            return self._parent._cast(_6840.ComponentLoadCase)

        @property
        def concept_coupling_half_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6842

            return self._parent._cast(_6842.ConceptCouplingHalfLoadCase)

        @property
        def concept_coupling_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6843

            return self._parent._cast(_6843.ConceptCouplingLoadCase)

        @property
        def concept_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6844

            return self._parent._cast(_6844.ConceptGearLoadCase)

        @property
        def concept_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6846

            return self._parent._cast(_6846.ConceptGearSetLoadCase)

        @property
        def conical_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6847

            return self._parent._cast(_6847.ConicalGearLoadCase)

        @property
        def conical_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6851

            return self._parent._cast(_6851.ConicalGearSetLoadCase)

        @property
        def connector_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6853

            return self._parent._cast(_6853.ConnectorLoadCase)

        @property
        def coupling_half_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6855

            return self._parent._cast(_6855.CouplingHalfLoadCase)

        @property
        def coupling_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6856

            return self._parent._cast(_6856.CouplingLoadCase)

        @property
        def cvt_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6858

            return self._parent._cast(_6858.CVTLoadCase)

        @property
        def cvt_pulley_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6859

            return self._parent._cast(_6859.CVTPulleyLoadCase)

        @property
        def cycloidal_assembly_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6860

            return self._parent._cast(_6860.CycloidalAssemblyLoadCase)

        @property
        def cycloidal_disc_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6862

            return self._parent._cast(_6862.CycloidalDiscLoadCase)

        @property
        def cylindrical_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6864

            return self._parent._cast(_6864.CylindricalGearLoadCase)

        @property
        def cylindrical_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6868

            return self._parent._cast(_6868.CylindricalGearSetLoadCase)

        @property
        def cylindrical_planet_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6869

            return self._parent._cast(_6869.CylindricalPlanetGearLoadCase)

        @property
        def datum_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6872

            return self._parent._cast(_6872.DatumLoadCase)

        @property
        def external_cad_model_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6886

            return self._parent._cast(_6886.ExternalCADModelLoadCase)

        @property
        def face_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6887

            return self._parent._cast(_6887.FaceGearLoadCase)

        @property
        def face_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6889

            return self._parent._cast(_6889.FaceGearSetLoadCase)

        @property
        def fe_part_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6890

            return self._parent._cast(_6890.FEPartLoadCase)

        @property
        def flexible_pin_assembly_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6891

            return self._parent._cast(_6891.FlexiblePinAssemblyLoadCase)

        @property
        def gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6893

            return self._parent._cast(_6893.GearLoadCase)

        @property
        def gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6898

            return self._parent._cast(_6898.GearSetLoadCase)

        @property
        def guide_dxf_model_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6899

            return self._parent._cast(_6899.GuideDxfModelLoadCase)

        @property
        def hypoid_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6908

            return self._parent._cast(_6908.HypoidGearLoadCase)

        @property
        def hypoid_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6910

            return self._parent._cast(_6910.HypoidGearSetLoadCase)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6915

            return self._parent._cast(_6915.KlingelnbergCycloPalloidConicalGearLoadCase)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6917

            return self._parent._cast(
                _6917.KlingelnbergCycloPalloidConicalGearSetLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6918

            return self._parent._cast(_6918.KlingelnbergCycloPalloidHypoidGearLoadCase)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6920

            return self._parent._cast(
                _6920.KlingelnbergCycloPalloidHypoidGearSetLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6921

            return self._parent._cast(
                _6921.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6923

            return self._parent._cast(
                _6923.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
            )

        @property
        def mass_disc_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6924

            return self._parent._cast(_6924.MassDiscLoadCase)

        @property
        def measurement_component_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6925

            return self._parent._cast(_6925.MeasurementComponentLoadCase)

        @property
        def mountable_component_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6927

            return self._parent._cast(_6927.MountableComponentLoadCase)

        @property
        def oil_seal_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6929

            return self._parent._cast(_6929.OilSealLoadCase)

        @property
        def part_to_part_shear_coupling_half_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6933

            return self._parent._cast(_6933.PartToPartShearCouplingHalfLoadCase)

        @property
        def part_to_part_shear_coupling_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6934

            return self._parent._cast(_6934.PartToPartShearCouplingLoadCase)

        @property
        def planetary_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6936

            return self._parent._cast(_6936.PlanetaryGearSetLoadCase)

        @property
        def planet_carrier_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6938

            return self._parent._cast(_6938.PlanetCarrierLoadCase)

        @property
        def point_load_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6941

            return self._parent._cast(_6941.PointLoadLoadCase)

        @property
        def power_load_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6942

            return self._parent._cast(_6942.PowerLoadLoadCase)

        @property
        def pulley_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6943

            return self._parent._cast(_6943.PulleyLoadCase)

        @property
        def ring_pins_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6946

            return self._parent._cast(_6946.RingPinsLoadCase)

        @property
        def rolling_ring_assembly_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6948

            return self._parent._cast(_6948.RollingRingAssemblyLoadCase)

        @property
        def rolling_ring_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6950

            return self._parent._cast(_6950.RollingRingLoadCase)

        @property
        def root_assembly_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6951

            return self._parent._cast(_6951.RootAssemblyLoadCase)

        @property
        def shaft_hub_connection_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6952

            return self._parent._cast(_6952.ShaftHubConnectionLoadCase)

        @property
        def shaft_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6953

            return self._parent._cast(_6953.ShaftLoadCase)

        @property
        def specialised_assembly_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6955

            return self._parent._cast(_6955.SpecialisedAssemblyLoadCase)

        @property
        def spiral_bevel_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6956

            return self._parent._cast(_6956.SpiralBevelGearLoadCase)

        @property
        def spiral_bevel_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6958

            return self._parent._cast(_6958.SpiralBevelGearSetLoadCase)

        @property
        def spring_damper_half_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6960

            return self._parent._cast(_6960.SpringDamperHalfLoadCase)

        @property
        def spring_damper_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6961

            return self._parent._cast(_6961.SpringDamperLoadCase)

        @property
        def straight_bevel_diff_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6962

            return self._parent._cast(_6962.StraightBevelDiffGearLoadCase)

        @property
        def straight_bevel_diff_gear_set_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6964

            return self._parent._cast(_6964.StraightBevelDiffGearSetLoadCase)

        @property
        def straight_bevel_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6965

            return self._parent._cast(_6965.StraightBevelGearLoadCase)

        @property
        def straight_bevel_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6967

            return self._parent._cast(_6967.StraightBevelGearSetLoadCase)

        @property
        def straight_bevel_planet_gear_load_case(
            self: "PartLoadCase._Cast_PartLoadCase",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6968

            return self._parent._cast(_6968.StraightBevelPlanetGearLoadCase)

        @property
        def straight_bevel_sun_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6969

            return self._parent._cast(_6969.StraightBevelSunGearLoadCase)

        @property
        def synchroniser_half_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6970

            return self._parent._cast(_6970.SynchroniserHalfLoadCase)

        @property
        def synchroniser_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6971

            return self._parent._cast(_6971.SynchroniserLoadCase)

        @property
        def synchroniser_part_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6972

            return self._parent._cast(_6972.SynchroniserPartLoadCase)

        @property
        def synchroniser_sleeve_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6973

            return self._parent._cast(_6973.SynchroniserSleeveLoadCase)

        @property
        def torque_converter_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6976

            return self._parent._cast(_6976.TorqueConverterLoadCase)

        @property
        def torque_converter_pump_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6977

            return self._parent._cast(_6977.TorqueConverterPumpLoadCase)

        @property
        def torque_converter_turbine_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6978

            return self._parent._cast(_6978.TorqueConverterTurbineLoadCase)

        @property
        def unbalanced_mass_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6983

            return self._parent._cast(_6983.UnbalancedMassLoadCase)

        @property
        def virtual_component_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6984

            return self._parent._cast(_6984.VirtualComponentLoadCase)

        @property
        def worm_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6985

            return self._parent._cast(_6985.WormGearLoadCase)

        @property
        def worm_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6987

            return self._parent._cast(_6987.WormGearSetLoadCase)

        @property
        def zerol_bevel_gear_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6988

            return self._parent._cast(_6988.ZerolBevelGearLoadCase)

        @property
        def zerol_bevel_gear_set_load_case(self: "PartLoadCase._Cast_PartLoadCase"):
            from mastapy.system_model.analyses_and_results.static_loads import _6990

            return self._parent._cast(_6990.ZerolBevelGearSetLoadCase)

        @property
        def part_load_case(self: "PartLoadCase._Cast_PartLoadCase") -> "PartLoadCase":
            return self._parent

        def __getattr__(self: "PartLoadCase._Cast_PartLoadCase", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PartLoadCase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def excitation_data_is_up_to_date(self: Self) -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ExcitationDataIsUpToDate

        if temp is None:
            return False

        return temp

    @property
    def harmonic_excitation_type(
        self: Self,
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.HarmonicExcitationType]"""
        temp = self.wrapped.HarmonicExcitationType

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @harmonic_excitation_type.setter
    @enforce_parameter_types
    def harmonic_excitation_type(self: Self, value: "_6900.HarmonicExcitationType"):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.HarmonicExcitationType = value

    @property
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: Self,
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = (
            self.wrapped.LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up.setter
    @enforce_parameter_types
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: Self, value: "_6807.StaticLoadCase"
    ):
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        self.wrapped.LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp = (
            value
        )

    @property
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: Self,
    ) -> "bool":
        """bool"""
        temp = (
            self.wrapped.UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp
        )

        if temp is None:
            return False

        return temp

    @use_this_load_case_for_advanced_system_deflection_current_load_case_set_up.setter
    @enforce_parameter_types
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: Self, value: "bool"
    ):
        self.wrapped.UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp = (
            bool(value) if value is not None else False
        )

    @property
    def component_design(self: Self) -> "_2470.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def static_load_case(self: Self) -> "_6807.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.StaticLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def time_series_load_case(self: Self) -> "_6808.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.TimeSeriesLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def clear_user_specified_excitation_data_for_this_load_case(self: Self):
        """Method does not return."""
        self.wrapped.ClearUserSpecifiedExcitationDataForThisLoadCase()

    def get_harmonic_load_data_for_import(self: Self) -> "_1381.HarmonicLoadDataBase":
        """mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataBase"""
        method_result = self.wrapped.GetHarmonicLoadDataForImport()
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: Self) -> "PartLoadCase._Cast_PartLoadCase":
        return self._Cast_PartLoadCase(self)
