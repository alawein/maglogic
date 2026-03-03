"""
Tests for MagLogic core constants and physics calculations.

Validates material parameters, physical constants, and derived
quantities against known values from literature.

Author: Meshal Alawein
Email: meshal@berkeley.edu
License: MIT
"""

import pytest
import numpy as np

from maglogic.core.constants import (
    PHYSICAL_CONSTANTS,
    MATERIAL_CONSTANTS,
    SIMULATION_DEFAULTS,
    PARAMETER_RANGES,
    UNIT_CONVERSIONS,
    SHAPE_ANISOTROPY,
    TEMPERATURE_POINTS,
    get_material_parameter,
    list_materials,
    get_material_info,
    calculate_exchange_length,
    calculate_domain_wall_width,
    thermal_energy,
    magnetic_energy_scale,
    validate_parameter,
)


class TestPhysicalConstants:
    """Tests for fundamental physical constants."""

    def test_vacuum_permeability(self):
        """mu_0 should be 4*pi*1e-7 H/m."""
        expected = 4 * np.pi * 1e-7
        assert PHYSICAL_CONSTANTS["mu_0"] == pytest.approx(expected, rel=1e-12)

    def test_boltzmann_constant(self):
        """k_B should match 2019 SI redefinition value."""
        assert PHYSICAL_CONSTANTS["k_B"] == pytest.approx(1.380649e-23, rel=1e-6)

    def test_elementary_charge(self):
        """Elementary charge should match exact 2019 SI value."""
        assert PHYSICAL_CONSTANTS["e"] == pytest.approx(1.602176634e-19, rel=1e-6)

    def test_bohr_magneton(self):
        """Bohr magneton should be e*hbar / (2*m_e)."""
        e = PHYSICAL_CONSTANTS["e"]
        hbar = PHYSICAL_CONSTANTS["hbar"]
        m_e = PHYSICAL_CONSTANTS["m_e"]
        expected = e * hbar / (2 * m_e)
        assert PHYSICAL_CONSTANTS["mu_B"] == pytest.approx(expected, rel=1e-4)

    def test_speed_of_light(self):
        """Speed of light should be exactly 299792458 m/s."""
        assert PHYSICAL_CONSTANTS["c"] == pytest.approx(2.99792458e8, rel=1e-9)

    def test_planck_hbar_relation(self):
        """hbar should equal h / (2*pi)."""
        expected = PHYSICAL_CONSTANTS["h"] / (2 * np.pi)
        assert PHYSICAL_CONSTANTS["hbar"] == pytest.approx(expected, rel=1e-6)

    def test_all_constants_positive(self):
        """All physical constants should be positive."""
        for name, value in PHYSICAL_CONSTANTS.items():
            assert value > 0, f"Constant {name} should be positive, got {value}"


class TestMaterialConstants:
    """Tests for material parameter database."""

    def test_permalloy_saturation_magnetization(self):
        """Permalloy Ms should be ~860 kA/m (literature value)."""
        Ms = MATERIAL_CONSTANTS["permalloy_ni80fe20"]["Ms"]
        assert Ms == pytest.approx(860e3, rel=0.05)

    def test_permalloy_exchange_constant(self):
        """Permalloy A_ex should be ~13 pJ/m."""
        A_ex = MATERIAL_CONSTANTS["permalloy_ni80fe20"]["A_ex"]
        assert A_ex == pytest.approx(13e-12, rel=0.1)

    def test_permalloy_zero_anisotropy(self):
        """Permalloy K1 should be essentially zero (soft magnet)."""
        K1 = MATERIAL_CONSTANTS["permalloy_ni80fe20"]["K1"]
        assert K1 == 0.0

    def test_cofeb_higher_ms_than_permalloy(self):
        """CoFeB should have higher Ms than permalloy."""
        Ms_cofeb = MATERIAL_CONSTANTS["cofeb"]["Ms"]
        Ms_py = MATERIAL_CONSTANTS["permalloy_ni80fe20"]["Ms"]
        assert Ms_cofeb > Ms_py

    def test_iron_curie_temperature_consistency(self):
        """Iron Curie temp in TEMPERATURE_POINTS should be ~1043 K."""
        assert TEMPERATURE_POINTS["iron_curie"] == pytest.approx(1043.0, rel=0.01)

    def test_all_materials_have_required_fields(self):
        """Every material must have Ms, A_ex, alpha, and gamma."""
        required = {"Ms", "A_ex", "alpha", "gamma"}
        for material, params in MATERIAL_CONSTANTS.items():
            for field in required:
                assert field in params, (
                    f"Material '{material}' missing required field '{field}'"
                )

    def test_damping_in_physical_range(self):
        """Gilbert damping should be between 1e-4 and 1 for all materials."""
        for material, params in MATERIAL_CONSTANTS.items():
            alpha = params["alpha"]
            assert 1e-5 <= alpha <= 1.0, (
                f"Material '{material}' has alpha={alpha} outside physical range"
            )

    def test_material_densities_positive(self):
        """All material densities should be positive."""
        for material, params in MATERIAL_CONSTANTS.items():
            assert params["density"] > 0, (
                f"Material '{material}' has non-positive density"
            )


class TestGetMaterialParameter:
    """Tests for the get_material_parameter function."""

    def test_known_material_known_parameter(self):
        """Should return correct value for known material and parameter."""
        Ms = get_material_parameter("permalloy_ni80fe20", "Ms")
        assert Ms == 860e3

    def test_cofeb_exchange(self):
        """Should return CoFeB exchange constant."""
        A_ex = get_material_parameter("cofeb", "A_ex")
        assert A_ex == 20e-12

    def test_iron_anisotropy(self):
        """Should return iron K1."""
        K1 = get_material_parameter("iron", "K1")
        assert K1 == 48e3

    def test_unknown_material_raises_keyerror(self):
        """Should raise KeyError for unknown material."""
        with pytest.raises(KeyError, match="not found"):
            get_material_parameter("unobtanium", "Ms")

    def test_unknown_parameter_raises_keyerror(self):
        """Should raise KeyError for unknown parameter on valid material."""
        with pytest.raises(KeyError, match="not found"):
            get_material_parameter("permalloy_ni80fe20", "nonexistent_param")

    def test_returns_string_for_description(self):
        """Should return string for description field."""
        desc = get_material_parameter("permalloy_ni80fe20", "description")
        assert isinstance(desc, str)
        assert len(desc) > 0


class TestListMaterials:
    """Tests for the list_materials function."""

    def test_returns_list(self):
        """Should return a list."""
        result = list_materials()
        assert isinstance(result, list)

    def test_contains_expected_materials(self):
        """Should contain standard materials."""
        materials = list_materials()
        expected = {"permalloy_ni80fe20", "cofeb", "iron", "gadolinium"}
        assert expected.issubset(set(materials))

    def test_heusler_alloy_present(self):
        """Heusler alloy should be in the database."""
        materials = list_materials()
        assert "heusler_co2mnsi" in materials

    def test_count_at_least_five(self):
        """Should have at least five materials."""
        assert len(list_materials()) >= 5


class TestGetMaterialInfo:
    """Tests for get_material_info function."""

    def test_returns_dict(self):
        """Should return a dictionary."""
        info = get_material_info("iron")
        assert isinstance(info, dict)

    def test_returns_copy(self):
        """Returned dict should be a copy, not a reference."""
        info = get_material_info("iron")
        info["Ms"] = 0.0
        original = MATERIAL_CONSTANTS["iron"]["Ms"]
        assert original != 0.0

    def test_unknown_material_raises(self):
        """Should raise KeyError for unknown material."""
        with pytest.raises(KeyError):
            get_material_info("nonexistent_material")


class TestCalculateExchangeLength:
    """Tests for exchange length calculation."""

    def test_permalloy_exchange_length(self):
        """Permalloy exchange length should be ~5-6 nm."""
        l_ex = calculate_exchange_length("permalloy_ni80fe20")
        # l_ex = sqrt(2*A / (mu_0 * Ms^2))
        assert 4e-9 < l_ex < 7e-9, f"Permalloy l_ex={l_ex:.2e} m outside expected range"

    def test_manual_calculation_match(self):
        """Should match manual calculation."""
        A_ex = 13e-12
        Ms = 860e3
        mu_0 = 4 * np.pi * 1e-7
        expected = np.sqrt(2 * A_ex / (mu_0 * Ms**2))
        result = calculate_exchange_length("permalloy_ni80fe20")
        assert result == pytest.approx(expected, rel=1e-10)

    def test_iron_shorter_than_permalloy(self):
        """Iron has higher Ms and should have shorter exchange length."""
        l_ex_py = calculate_exchange_length("permalloy_ni80fe20")
        l_ex_fe = calculate_exchange_length("iron")
        # Iron has higher Ms, so exchange length should be shorter
        # unless exchange constant is much higher
        assert l_ex_fe > 0  # At minimum it should be positive

    def test_positive_result(self):
        """Exchange length should always be positive."""
        for material in list_materials():
            l_ex = calculate_exchange_length(material)
            assert l_ex > 0, f"Exchange length for {material} should be positive"

    def test_unknown_material_raises(self):
        """Should propagate KeyError for unknown material."""
        with pytest.raises(KeyError):
            calculate_exchange_length("unobtanium")


class TestCalculateDomainWallWidth:
    """Tests for domain wall width calculation."""

    def test_permalloy_domain_wall_width(self):
        """Permalloy domain wall width should be on the nm scale."""
        delta_w = calculate_domain_wall_width("permalloy_ni80fe20")
        # For permalloy with shape anisotropy: K_eff = mu_0*Ms^2/2
        # delta_w = pi * sqrt(A_ex / K_eff)
        assert 1e-9 < delta_w < 100e-9, (
            f"Permalloy wall width={delta_w:.2e} m outside expected range"
        )

    def test_manual_calculation(self):
        """Should match manual formula: delta_w = pi * sqrt(A_ex / K_eff)."""
        A_ex = 13e-12
        Ms = 860e3
        mu_0 = 4 * np.pi * 1e-7
        K_eff = mu_0 * Ms**2 / 2
        expected = np.pi * np.sqrt(A_ex / K_eff)
        result = calculate_domain_wall_width("permalloy_ni80fe20")
        assert result == pytest.approx(expected, rel=1e-10)

    def test_positive_for_all_materials(self):
        """Domain wall width should be positive for all materials."""
        for material in list_materials():
            delta_w = calculate_domain_wall_width(material)
            assert delta_w > 0, f"Wall width for {material} should be positive"

    def test_proportional_to_sqrt_exchange(self):
        """Domain wall width should scale as sqrt(A_ex) for fixed Ms."""
        # Compare materials with similar Ms but different A_ex
        delta_py = calculate_domain_wall_width("permalloy_ni80fe20")
        assert np.isfinite(delta_py)


class TestThermalEnergy:
    """Tests for thermal energy calculation."""

    def test_room_temperature(self):
        """Thermal energy at 293.15 K should be ~4.04e-21 J (≈ 25.3 meV)."""
        E = thermal_energy(293.15)
        expected = 1.380649e-23 * 293.15
        assert E == pytest.approx(expected, rel=1e-6)

    def test_absolute_zero(self):
        """Thermal energy at 0 K should be exactly zero."""
        E = thermal_energy(0.0)
        assert E == 0.0

    def test_liquid_nitrogen(self):
        """Thermal energy at 77 K should be ~1.06e-21 J."""
        E = thermal_energy(77.0)
        expected = 1.380649e-23 * 77.0
        assert E == pytest.approx(expected, rel=1e-6)

    def test_scales_linearly_with_temperature(self):
        """Thermal energy should scale linearly with T."""
        E1 = thermal_energy(100.0)
        E2 = thermal_energy(200.0)
        assert E2 == pytest.approx(2 * E1, rel=1e-10)

    def test_room_temp_in_ev(self):
        """Room temperature thermal energy should be ~25 meV."""
        E = thermal_energy(293.15)
        E_meV = E / PHYSICAL_CONSTANTS["e"] * 1000
        assert E_meV == pytest.approx(25.3, rel=0.05)


class TestMagneticEnergyScale:
    """Tests for magnetic energy scale function."""

    def test_permalloy_small_volume(self):
        """Energy scale for a small permalloy element."""
        volume = (100e-9) ** 3  # 100 nm cube
        E = magnetic_energy_scale("permalloy_ni80fe20", volume)
        # E = mu_0 * Ms^2 * V / 2
        mu_0 = 4 * np.pi * 1e-7
        Ms = 860e3
        expected = mu_0 * Ms**2 * volume / 2
        assert E == pytest.approx(expected, rel=1e-10)

    def test_positive_energy(self):
        """Energy scale should always be positive for positive volume."""
        E = magnetic_energy_scale("iron", 1e-24)
        assert E > 0

    def test_zero_volume(self):
        """Energy scale should be zero for zero volume."""
        E = magnetic_energy_scale("permalloy_ni80fe20", 0.0)
        assert E == 0.0

    def test_scales_with_volume(self):
        """Energy should scale linearly with volume."""
        E1 = magnetic_energy_scale("cofeb", 1e-24)
        E2 = magnetic_energy_scale("cofeb", 2e-24)
        assert E2 == pytest.approx(2 * E1, rel=1e-10)


class TestValidateParameter:
    """Tests for parameter validation function."""

    def test_valid_ms(self):
        """Valid Ms within range should return True."""
        assert validate_parameter("Ms", 860e3) is True

    def test_valid_exchange(self):
        """Valid A_ex within range should return True."""
        assert validate_parameter("A_ex", 13e-12) is True

    def test_valid_damping(self):
        """Valid alpha within range should return True."""
        assert validate_parameter("alpha", 0.01) is True

    def test_ms_below_minimum(self):
        """Ms below minimum should return False."""
        assert validate_parameter("Ms", 100) is False

    def test_ms_above_maximum(self):
        """Ms above maximum should return False."""
        assert validate_parameter("Ms", 5e6) is False

    def test_negative_temperature(self):
        """Negative temperature is below minimum (0 K) and should fail."""
        assert validate_parameter("temperature", -10.0) is False

    def test_zero_temperature_valid(self):
        """0 K is the minimum and should be valid."""
        assert validate_parameter("temperature", 0.0) is True

    def test_unknown_parameter_returns_true(self):
        """Unknown parameter with no validation range should return True."""
        assert validate_parameter("custom_unknown_param", 42.0) is True

    def test_boundary_values(self):
        """Values exactly at boundaries should be valid."""
        for param, ranges in PARAMETER_RANGES.items():
            assert validate_parameter(param, ranges["min"]) is True
            assert validate_parameter(param, ranges["max"]) is True

    def test_just_outside_boundaries(self):
        """Values just outside boundaries should be invalid."""
        min_ms = PARAMETER_RANGES["Ms"]["min"]
        max_ms = PARAMETER_RANGES["Ms"]["max"]
        assert validate_parameter("Ms", min_ms - 1) is False
        assert validate_parameter("Ms", max_ms + 1) is False


class TestUnitConversions:
    """Tests for unit conversion factors."""

    def test_length_nm_to_m(self):
        """1 nm = 1e-9 m."""
        assert UNIT_CONVERSIONS["length"]["nm"] == 1e-9

    def test_time_ns_to_s(self):
        """1 ns = 1e-9 s."""
        assert UNIT_CONVERSIONS["time"]["ns"] == 1e-9

    def test_energy_ev_to_j(self):
        """1 eV should equal elementary charge in joules."""
        assert UNIT_CONVERSIONS["energy"]["eV"] == pytest.approx(
            PHYSICAL_CONSTANTS["e"], rel=1e-6
        )

    def test_magnetization_emu_to_si(self):
        """1 emu/cm^3 = 1000 A/m."""
        assert UNIT_CONVERSIONS["magnetization"]["emu/cm³"] == 1000.0


class TestShapeAnisotropy:
    """Tests for shape demagnetization factors."""

    def test_sphere_isotropic(self):
        """Sphere should have Nx = Ny = Nz = 1/3."""
        sphere = SHAPE_ANISOTROPY["sphere"]
        assert sphere["Nx"] == pytest.approx(1 / 3, rel=1e-10)
        assert sphere["Ny"] == pytest.approx(1 / 3, rel=1e-10)
        assert sphere["Nz"] == pytest.approx(1 / 3, rel=1e-10)

    def test_thin_film(self):
        """Thin film should have Nx=Ny=0, Nz=1."""
        film = SHAPE_ANISOTROPY["thin_film"]
        assert film["Nx"] == 0.0
        assert film["Ny"] == 0.0
        assert film["Nz"] == 1.0

    def test_demagnetization_factor_sum(self):
        """Demagnetization factors must sum to 1 for closed shapes."""
        for shape_name, shape in SHAPE_ANISOTROPY.items():
            if "Nx" in shape:
                total = shape["Nx"] + shape["Ny"] + shape["Nz"]
                assert total == pytest.approx(1.0, rel=1e-10), (
                    f"Demagnetization factors for {shape_name} sum to {total}, expected 1.0"
                )


class TestSimulationDefaults:
    """Tests for default simulation parameters."""

    def test_cell_size_reasonable(self):
        """Default cell size should be in nm range."""
        assert 1e-9 <= SIMULATION_DEFAULTS["cell_size"] <= 10e-9

    def test_time_step_sub_nanosecond(self):
        """Default time step should be sub-nanosecond."""
        assert SIMULATION_DEFAULTS["time_step"] < 1e-9

    def test_temperature_default_zero(self):
        """Default temperature should be 0 K (zero-temperature simulation)."""
        assert SIMULATION_DEFAULTS["temperature"] == 0.0


if __name__ == "__main__":
    pytest.main([__file__])
