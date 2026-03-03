"""
Tests for MagLogic input validation utilities.

Covers numeric validation, material parameter checks, simulation parameter
validation, geometry validation, and numerical stability analysis.

Author: Meshal Alawein
Email: meshal@berkeley.edu
License: MIT
"""

import pytest
import numpy as np
import warnings

from maglogic.core.validators import (
    ValidationError,
    ValidationWarning,
    validate_input,
    validate_material_parameter,
    validate_simulation_parameters,
    validate_geometry,
    validate_field_profile,
    check_numerical_stability,
    validate_simulation_config,
)


class TestValidateInput:
    """Tests for the validate_input function."""

    # --- Valid inputs ---

    def test_valid_scalar(self):
        """Should accept a valid scalar within range."""
        result = validate_input(5.0, "test_param", min_val=0, max_val=10)
        assert result == pytest.approx(5.0)

    def test_valid_positive(self):
        """Should accept positive value when positive=True."""
        result = validate_input(1e-9, "cell_size", positive=True)
        assert result == pytest.approx(1e-9)

    def test_valid_integer(self):
        """Should accept integer value when integer=True."""
        result = validate_input(5, "count", integer=True)
        assert result == 5

    def test_valid_array(self):
        """Should accept a valid numpy array."""
        arr = np.array([1.0, 2.0, 3.0])
        result = validate_input(arr, "test_array", min_val=0, max_val=5)
        np.testing.assert_array_almost_equal(result, arr)

    def test_returns_float_for_scalar(self):
        """Should return float type for scalar input."""
        result = validate_input(5, "test", min_val=0, max_val=10)
        assert isinstance(result, float)

    def test_returns_int_for_integer_flag(self):
        """Should return int type when integer=True."""
        result = validate_input(5, "test", integer=True)
        assert isinstance(result, int)

    # --- Invalid inputs ---

    def test_nan_raises(self):
        """NaN should raise ValidationError when finite=True (default)."""
        with pytest.raises(ValidationError, match="finite"):
            validate_input(float("nan"), "param")

    def test_inf_raises(self):
        """Infinity should raise ValidationError when finite=True."""
        with pytest.raises(ValidationError, match="finite"):
            validate_input(float("inf"), "param")

    def test_negative_inf_raises(self):
        """Negative infinity should raise ValidationError."""
        with pytest.raises(ValidationError, match="finite"):
            validate_input(float("-inf"), "param")

    def test_below_minimum_raises(self):
        """Value below min_val should raise ValidationError."""
        with pytest.raises(ValidationError, match=">="):
            validate_input(-1.0, "param", min_val=0.0)

    def test_above_maximum_raises(self):
        """Value above max_val should raise ValidationError."""
        with pytest.raises(ValidationError, match="<="):
            validate_input(100.0, "param", max_val=10.0)

    def test_non_positive_raises(self):
        """Zero should raise ValidationError when positive=True."""
        with pytest.raises(ValidationError, match="positive"):
            validate_input(0.0, "param", positive=True)

    def test_negative_raises_when_positive_required(self):
        """Negative value should raise when positive=True."""
        with pytest.raises(ValidationError, match="positive"):
            validate_input(-1.0, "damping", positive=True)

    def test_float_raises_when_integer_required(self):
        """Non-integer float should raise when integer=True."""
        with pytest.raises(ValidationError, match="integer"):
            validate_input(5.5, "count", integer=True)

    def test_array_with_nan_raises(self):
        """Array containing NaN should raise ValidationError."""
        arr = np.array([1.0, np.nan, 3.0])
        with pytest.raises(ValidationError, match="finite"):
            validate_input(arr, "test_array")

    def test_array_element_below_min(self):
        """Array with element below min should raise."""
        arr = np.array([1.0, 2.0, -1.0])
        with pytest.raises(ValidationError, match=">="):
            validate_input(arr, "test_array", min_val=0.0)

    # --- Edge cases ---

    def test_exact_boundary_min(self):
        """Value exactly at min should be accepted."""
        result = validate_input(0.0, "param", min_val=0.0)
        assert result == pytest.approx(0.0)

    def test_exact_boundary_max(self):
        """Value exactly at max should be accepted."""
        result = validate_input(10.0, "param", max_val=10.0)
        assert result == pytest.approx(10.0)

    def test_no_constraints(self):
        """Should pass with no constraints specified."""
        result = validate_input(42.0, "param")
        assert result == pytest.approx(42.0)

    def test_finite_false_allows_inf(self):
        """Should allow infinity when finite=False."""
        result = validate_input(float("inf"), "param", finite=False)
        assert result == float("inf")


class TestValidateMaterialParameter:
    """Tests for validate_material_parameter."""

    def test_valid_permalloy_ms(self):
        """Should accept typical permalloy Ms value."""
        result = validate_material_parameter("permalloy_ni80fe20", "Ms", 860e3)
        assert result == pytest.approx(860e3)

    def test_valid_alpha(self):
        """Should accept valid damping parameter."""
        result = validate_material_parameter("permalloy_ni80fe20", "alpha", 0.01)
        assert result == pytest.approx(0.01)

    def test_ms_out_of_range_raises(self):
        """Ms outside physical range should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_material_parameter("permalloy_ni80fe20", "Ms", -100)

    def test_warning_for_unusual_value(self):
        """Should warn when value differs significantly from typical."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            validate_material_parameter("permalloy_ni80fe20", "Ms", 10e3)
            validation_warnings = [
                x for x in w if issubclass(x.category, ValidationWarning)
            ]
            assert len(validation_warnings) > 0

    def test_unknown_parameter_generic_validation(self):
        """Unknown parameter should still get finite check."""
        result = validate_material_parameter("permalloy_ni80fe20", "custom_param", 1.0)
        assert result == pytest.approx(1.0)

    def test_unknown_parameter_nan_raises(self):
        """Unknown parameter with NaN should raise."""
        with pytest.raises(ValidationError):
            validate_material_parameter("permalloy_ni80fe20", "custom_param", float("nan"))

    def test_unknown_material_still_validates_range(self):
        """Should validate range even for unknown material."""
        result = validate_material_parameter("unknown_material", "Ms", 500e3)
        assert result == pytest.approx(500e3)


class TestValidateSimulationParameters:
    """Tests for validate_simulation_parameters."""

    @pytest.fixture
    def valid_params(self):
        """Minimum valid simulation parameter set."""
        return {
            "Ms": 860e3,
            "A_ex": 13e-12,
            "alpha": 0.01,
        }

    def test_valid_minimal_params(self, valid_params):
        """Should accept minimal valid parameter set."""
        result = validate_simulation_parameters(valid_params)
        assert result["Ms"] == pytest.approx(860e3)
        assert result["A_ex"] == pytest.approx(13e-12)
        assert result["alpha"] == pytest.approx(0.01)

    def test_valid_full_params(self, valid_params):
        """Should accept complete parameter set."""
        valid_params.update({
            "gamma": 2.21e5,
            "K1": 0.0,
            "temperature": 293.15,
            "cell_size": 2e-9,
            "time_step": 1e-12,
        })
        result = validate_simulation_parameters(valid_params)
        assert "Ms" in result
        assert "gamma" in result
        assert "temperature" in result

    def test_missing_ms_raises(self):
        """Missing required Ms should raise ValidationError."""
        with pytest.raises(ValidationError, match="Ms"):
            validate_simulation_parameters({"A_ex": 13e-12, "alpha": 0.01})

    def test_missing_exchange_raises(self):
        """Missing required A_ex should raise ValidationError."""
        with pytest.raises(ValidationError, match="A_ex"):
            validate_simulation_parameters({"Ms": 860e3, "alpha": 0.01})

    def test_missing_alpha_raises(self):
        """Missing required alpha should raise ValidationError."""
        with pytest.raises(ValidationError, match="alpha"):
            validate_simulation_parameters({"Ms": 860e3, "A_ex": 13e-12})

    def test_invalid_ms_raises(self):
        """Invalid Ms value should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_simulation_parameters(
                {"Ms": -100, "A_ex": 13e-12, "alpha": 0.01}
            )

    def test_invalid_cell_size_raises(self):
        """Cell size outside range should raise."""
        with pytest.raises(ValidationError):
            validate_simulation_parameters(
                {"Ms": 860e3, "A_ex": 13e-12, "alpha": 0.01, "cell_size": 1e-1}
            )

    def test_negative_temperature_raises(self):
        """Negative temperature should raise."""
        with pytest.raises(ValidationError):
            validate_simulation_parameters(
                {"Ms": 860e3, "A_ex": 13e-12, "alpha": 0.01, "temperature": -10.0}
            )

    def test_k1_negative_accepted(self):
        """Negative K1 is physically valid (easy-plane anisotropy)."""
        params = {"Ms": 860e3, "A_ex": 13e-12, "alpha": 0.01, "K1": -500e3}
        result = validate_simulation_parameters(params)
        assert result["K1"] == pytest.approx(-500e3)

    def test_cell_size_warning_for_large_cell(self, valid_params):
        """Should warn when cell size is too large relative to exchange length."""
        valid_params["cell_size"] = 100e-9  # Very large cell
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            validate_simulation_parameters(valid_params)
            # Check for any validation warning
            relevant = [x for x in w if issubclass(x.category, ValidationWarning)]
            assert len(relevant) > 0

    def test_unknown_extra_params_validated(self, valid_params):
        """Extra unknown parameters should still get finite check."""
        valid_params["custom_param"] = 42.0
        result = validate_simulation_parameters(valid_params)
        assert result["custom_param"] == pytest.approx(42.0)


class TestValidateGeometry:
    """Tests for geometry validation."""

    def test_valid_triangle(self):
        """Should accept valid triangle geometry."""
        geo = {"shape": "triangle", "edge_length": 100e-9}
        result = validate_geometry(geo)
        assert result["shape"] == "triangle"
        assert result["edge_length"] == pytest.approx(100e-9)

    def test_valid_circle(self):
        """Should accept valid circle/disk geometry."""
        geo = {"shape": "circle", "radius": 50e-9}
        result = validate_geometry(geo)
        assert result["shape"] == "circle"
        assert result["radius"] == pytest.approx(50e-9)

    def test_valid_rectangle(self):
        """Should accept valid rectangle geometry."""
        geo = {"shape": "rectangle", "width": 100e-9, "height": 50e-9}
        result = validate_geometry(geo)
        assert result["shape"] == "rectangle"
        assert result["width"] == pytest.approx(100e-9)

    def test_valid_ellipse(self):
        """Should accept valid ellipse geometry."""
        geo = {"shape": "ellipse", "semi_major": 100e-9, "semi_minor": 50e-9}
        result = validate_geometry(geo)
        assert result["semi_major"] == pytest.approx(100e-9)

    def test_missing_shape_raises(self):
        """Missing shape key should raise ValidationError."""
        with pytest.raises(ValidationError, match="shape"):
            validate_geometry({"edge_length": 100e-9})

    def test_triangle_missing_edge_length_raises(self):
        """Triangle without edge_length should raise."""
        with pytest.raises(ValidationError, match="edge_length"):
            validate_geometry({"shape": "triangle"})

    def test_circle_missing_radius_raises(self):
        """Circle without radius should raise."""
        with pytest.raises(ValidationError, match="radius"):
            validate_geometry({"shape": "circle"})

    def test_rectangle_missing_height_raises(self):
        """Rectangle without height should raise."""
        with pytest.raises(ValidationError):
            validate_geometry({"shape": "rectangle", "width": 100e-9})

    def test_ellipse_missing_semi_minor_raises(self):
        """Ellipse without semi_minor should raise."""
        with pytest.raises(ValidationError):
            validate_geometry({"shape": "ellipse", "semi_major": 100e-9})

    def test_negative_edge_length_raises(self):
        """Negative edge length should raise."""
        with pytest.raises(ValidationError):
            validate_geometry({"shape": "triangle", "edge_length": -100e-9})

    def test_zero_radius_raises(self):
        """Zero radius should raise (positive required)."""
        with pytest.raises(ValidationError):
            validate_geometry({"shape": "circle", "radius": 0.0})

    def test_optional_thickness(self):
        """Should accept optional thickness parameter."""
        geo = {"shape": "triangle", "edge_length": 100e-9, "thickness": 10e-9}
        result = validate_geometry(geo)
        assert result["thickness"] == pytest.approx(10e-9)

    def test_position_3d_vector(self):
        """Position should be accepted as 3D vector."""
        geo = {"shape": "circle", "radius": 50e-9, "position": [0, 0, 0]}
        result = validate_geometry(geo)
        np.testing.assert_array_equal(result["position"], [0, 0, 0])

    def test_position_wrong_dimension_raises(self):
        """2D position should raise ValidationError."""
        with pytest.raises(ValidationError, match="3D"):
            validate_geometry({"shape": "circle", "radius": 50e-9, "position": [0, 0]})

    def test_shape_case_insensitive(self):
        """Shape name should be case-insensitive."""
        geo = {"shape": "Triangle", "edge_length": 100e-9}
        result = validate_geometry(geo)
        assert result["shape"] == "triangle"

    def test_edge_length_too_large_raises(self):
        """Edge length above max should raise."""
        with pytest.raises(ValidationError):
            validate_geometry({"shape": "triangle", "edge_length": 1.0})  # 1 meter


class TestCheckNumericalStability:
    """Tests for numerical stability checking."""

    def test_stable_parameters_no_warnings(self):
        """Stable parameters should produce no warnings.

        CFL condition: dt < dx / (gamma * Ms)
        With dx=2e-9, gamma=2.21e5, Ms=860e3:
        dt_max ≈ 2e-9 / (2.21e5 * 860e3) ≈ 1.05e-20 s
        So dt must be below ~1e-20 to avoid the CFL warning.
        """
        params = {
            "time_step": 1e-21,
            "cell_size": 2e-9,
            "gamma": 2.21e5,
            "Ms": 860e3,
            "alpha": 0.01,
        }
        warnings_list = check_numerical_stability(params)
        assert len(warnings_list) == 0

    def test_large_timestep_cfl_warning(self):
        """Time step violating CFL should produce warning."""
        params = {
            "time_step": 1e-9,  # Very large
            "cell_size": 2e-9,
            "gamma": 2.21e5,
            "Ms": 860e3,
            "alpha": 0.01,
        }
        warnings_list = check_numerical_stability(params)
        assert any("CFL" in w for w in warnings_list)

    def test_high_damping_warning(self):
        """Very high damping should produce warning."""
        params = {"alpha": 0.5}
        warnings_list = check_numerical_stability(params)
        assert any("high damping" in w.lower() for w in warnings_list)

    def test_low_damping_warning(self):
        """Very low damping should produce warning."""
        params = {"alpha": 1e-5}
        warnings_list = check_numerical_stability(params)
        assert any("low damping" in w.lower() for w in warnings_list)

    def test_partial_params_no_crash(self):
        """Should not crash with incomplete parameter set."""
        warnings_list = check_numerical_stability({"Ms": 860e3})
        assert isinstance(warnings_list, list)

    def test_empty_params(self):
        """Empty parameter dict should return empty warnings list."""
        warnings_list = check_numerical_stability({})
        assert warnings_list == []

    def test_moderate_damping_no_damping_warning(self):
        """Moderate damping (e.g., 0.01) should not trigger warning."""
        params = {"alpha": 0.01}
        warnings_list = check_numerical_stability(params)
        damping_warnings = [w for w in warnings_list if "damping" in w.lower()]
        assert len(damping_warnings) == 0


class TestValidateFieldProfile:
    """Tests for field profile validation."""

    def test_valid_uniform_field(self):
        """Should accept valid uniform field."""
        field = {
            "type": "uniform",
            "direction": [1.0, 0.0, 0.0],
            "amplitude": 1e5,
        }
        result = validate_field_profile(field)
        assert result["type"] == "uniform"
        assert result["amplitude"] == pytest.approx(1e5)

    def test_uniform_direction_normalized(self):
        """Uniform field direction should be normalized."""
        field = {
            "type": "uniform",
            "direction": [3.0, 4.0, 0.0],
            "amplitude": 1e5,
        }
        result = validate_field_profile(field)
        norm = np.linalg.norm(result["direction"])
        assert norm == pytest.approx(1.0, rel=1e-10)

    def test_missing_type_raises(self):
        """Missing field type should raise."""
        with pytest.raises(ValidationError, match="type"):
            validate_field_profile({"direction": [1, 0, 0], "amplitude": 1e5})

    def test_zero_direction_raises(self):
        """Zero direction vector should raise."""
        with pytest.raises(ValidationError, match="zero"):
            validate_field_profile(
                {"type": "uniform", "direction": [0, 0, 0], "amplitude": 1e5}
            )

    def test_uniform_missing_amplitude_raises(self):
        """Uniform field without amplitude should raise."""
        with pytest.raises(ValidationError):
            validate_field_profile({"type": "uniform", "direction": [1, 0, 0]})

    def test_time_varying_valid(self):
        """Should accept valid time-varying field."""
        field = {
            "type": "time_varying",
            "amplitude": 1e5,
            "frequency": 1e9,
            "phase": 0.0,
        }
        result = validate_field_profile(field)
        assert result["frequency"] == pytest.approx(1e9)


class TestValidationErrorType:
    """Test that ValidationError is a proper exception."""

    def test_is_valueerror_subclass(self):
        """ValidationError should be a subclass of ValueError."""
        assert issubclass(ValidationError, ValueError)

    def test_can_be_raised_and_caught(self):
        """Should be raisable and catchable."""
        with pytest.raises(ValidationError):
            raise ValidationError("test error")

    def test_message_preserved(self):
        """Error message should be preserved."""
        try:
            raise ValidationError("specific error message")
        except ValidationError as e:
            assert "specific error message" in str(e)


class TestValidateSimulationConfig:
    """Tests for complete simulation config validation."""

    def test_valid_config_with_material(self):
        """Should accept config with material section."""
        config = {
            "material": {"Ms": 860e3, "A_ex": 13e-12, "alpha": 0.01}
        }
        result = validate_simulation_config(config)
        assert "material" in result

    def test_valid_config_with_geometry(self):
        """Should accept config with geometry section."""
        config = {
            "geometry": {"shape": "triangle", "edge_length": 100e-9}
        }
        result = validate_simulation_config(config)
        assert "geometry" in result

    def test_empty_config(self):
        """Empty config should return empty validated config."""
        result = validate_simulation_config({})
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__])
