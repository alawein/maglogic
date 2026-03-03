"""
Tests for MagLogic magnetization analysis module.

Tests the MagnetizationAnalyzer class methods with synthetic data,
focusing on energy calculations, spatial statistics, and domain analysis.

Author: Meshal Alawein
Email: meshal@berkeley.edu
License: MIT
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock

from maglogic.core.constants import PHYSICAL_CONSTANTS


class TestMagnetizationAnalyzerInit:
    """Tests for MagnetizationAnalyzer initialization."""

    def test_default_initialization(self):
        """Should initialize with default permalloy parameters."""
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            analyzer = MagnetizationAnalyzer()
            assert analyzer.material_params is not None
            assert "Ms" in analyzer.material_params
            assert "A" in analyzer.material_params
            assert "alpha" in analyzer.material_params

    def test_default_ms_value(self):
        """Default Ms should be permalloy value (~860 kA/m)."""
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            analyzer = MagnetizationAnalyzer()
            assert analyzer.material_params["Ms"] == pytest.approx(8.6e5, rel=0.01)

    def test_custom_material_params(self):
        """Should accept custom material parameters."""
        custom = {"Ms": 1.6e6, "A": 2.0e-11, "K1": 1000, "alpha": 0.004}
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            analyzer = MagnetizationAnalyzer(material_params=custom)
            assert analyzer.material_params["Ms"] == 1.6e6
            assert analyzer.material_params["A"] == 2.0e-11

    def test_parsers_initialized(self):
        """Should initialize OOMMF and MuMax3 parsers."""
        with patch("maglogic.analysis.magnetization.OOMMFParser") as mock_oommf, \
             patch("maglogic.analysis.magnetization.MuMax3Parser") as mock_mumax:
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            analyzer = MagnetizationAnalyzer()
            mock_oommf.assert_called_once_with(verbose=False)
            mock_mumax.assert_called_once_with(verbose=False)


class TestCalculateEnergyDensities:
    """Tests for energy density calculations with synthetic data."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer with mocked parsers."""
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            return MagnetizationAnalyzer()

    @pytest.fixture
    def uniform_x_magnetization(self):
        """Uniform magnetization along x-axis (10x10 grid)."""
        size = 10
        mx = np.ones((size, size))
        my = np.zeros((size, size))
        mz = np.zeros((size, size))
        return {"mx": mx, "my": my, "mz": mz}

    @pytest.fixture
    def uniform_z_magnetization(self):
        """Uniform magnetization along z-axis (10x10 grid)."""
        size = 10
        mx = np.zeros((size, size))
        my = np.zeros((size, size))
        mz = np.ones((size, size))
        return {"mx": mx, "my": my, "mz": mz}

    @pytest.fixture
    def coordinates_10x10(self):
        """10x10 coordinate grid with 1 nm spacing."""
        size = 10
        spacing = 1e-9
        x = np.linspace(0, (size - 1) * spacing, size)
        y = np.linspace(0, (size - 1) * spacing, size)
        X, Y = np.meshgrid(x, y, indexing="ij")
        return {"x": X, "y": Y, "z": np.zeros_like(X)}

    def test_returns_all_energy_components(self, analyzer, uniform_x_magnetization, coordinates_10x10):
        """Should return exchange, demag, anisotropy, and total energy."""
        result = analyzer.calculate_energy_densities(
            uniform_x_magnetization, coordinates_10x10
        )
        expected_keys = [
            "exchange_energy",
            "demagnetization_energy",
            "anisotropy_energy",
            "total_energy",
        ]
        for key in expected_keys:
            assert key in result, f"Missing energy component: {key}"

    def test_energy_component_structure(self, analyzer, uniform_x_magnetization, coordinates_10x10):
        """Each energy component should have density, total, and average."""
        result = analyzer.calculate_energy_densities(
            uniform_x_magnetization, coordinates_10x10
        )
        for component in ["exchange_energy", "demagnetization_energy", "anisotropy_energy"]:
            energy = result[component]
            assert "density" in energy
            assert "total" in energy
            assert "average" in energy

    def test_uniform_exchange_energy_zero(self, analyzer, uniform_x_magnetization, coordinates_10x10):
        """Uniform magnetization should have zero exchange energy (no gradients)."""
        result = analyzer.calculate_energy_densities(
            uniform_x_magnetization, coordinates_10x10
        )
        # Interior points should have zero exchange (no gradient)
        # Edge effects from np.gradient may produce small values
        exchange_avg = result["exchange_energy"]["average"]
        assert exchange_avg == pytest.approx(0.0, abs=1e-20)

    def test_demag_energy_z_vs_x(self, analyzer, uniform_x_magnetization, uniform_z_magnetization, coordinates_10x10):
        """Thin film with mz=1 should have higher demag energy than mx=1."""
        # For thin film: Nx=0, Ny=0, Nz=1
        # E_demag(mz=1) = 0.5 * mu0 * Ms^2 * 1.0
        # E_demag(mx=1) = 0.5 * mu0 * Ms^2 * 0.0 = 0
        result_x = analyzer.calculate_energy_densities(
            uniform_x_magnetization, coordinates_10x10
        )
        result_z = analyzer.calculate_energy_densities(
            uniform_z_magnetization, coordinates_10x10
        )
        demag_x = result_x["demagnetization_energy"]["total"]
        demag_z = result_z["demagnetization_energy"]["total"]
        assert demag_z > demag_x

    def test_anisotropy_energy_with_zero_k1(self, analyzer, uniform_x_magnetization, coordinates_10x10):
        """Permalloy has K1=0, so anisotropy energy should be zero."""
        assert analyzer.material_params["K1"] == 0.0
        result = analyzer.calculate_energy_densities(
            uniform_x_magnetization, coordinates_10x10
        )
        aniso_total = result["anisotropy_energy"]["total"]
        assert aniso_total == pytest.approx(0.0, abs=1e-30)

    def test_energy_density_shape(self, analyzer, uniform_x_magnetization, coordinates_10x10):
        """Energy density arrays should match input shape."""
        result = analyzer.calculate_energy_densities(
            uniform_x_magnetization, coordinates_10x10
        )
        expected_shape = (10, 10)
        assert result["exchange_energy"]["density"].shape == expected_shape
        assert result["total_energy"]["density"].shape == expected_shape

    def test_total_is_sum_of_components(self, analyzer, uniform_x_magnetization, coordinates_10x10):
        """Total energy should equal sum of all components."""
        result = analyzer.calculate_energy_densities(
            uniform_x_magnetization, coordinates_10x10
        )
        total = result["total_energy"]["total"]
        component_sum = (
            result["exchange_energy"]["total"]
            + result["demagnetization_energy"]["total"]
            + result["anisotropy_energy"]["total"]
        )
        assert total == pytest.approx(component_sum, rel=1e-10)

    def test_finite_energy_values(self, analyzer, uniform_x_magnetization, coordinates_10x10):
        """All energy values should be finite."""
        result = analyzer.calculate_energy_densities(
            uniform_x_magnetization, coordinates_10x10
        )
        for component in result.values():
            assert np.isfinite(component["total"])
            assert np.isfinite(component["average"])
            assert np.all(np.isfinite(component["density"]))


class TestSpatialStatistics:
    """Tests for spatial statistics calculation."""

    @pytest.fixture
    def analyzer(self):
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            return MagnetizationAnalyzer()

    @pytest.fixture
    def uniform_mag(self):
        """Uniform magnetization along x for 10x10 grid."""
        size = 10
        return {
            "mx": np.ones((size, size)),
            "my": np.zeros((size, size)),
            "mz": np.zeros((size, size)),
            "magnitude": np.ones((size, size)),
        }

    @pytest.fixture
    def random_mag(self):
        """Random magnetization for statistics testing."""
        rng = np.random.RandomState(42)
        size = 20
        mx = rng.uniform(-1, 1, (size, size))
        my = rng.uniform(-1, 1, (size, size))
        mz = rng.uniform(-1, 1, (size, size))
        mag = np.sqrt(mx**2 + my**2 + mz**2)
        return {
            "mx": mx / mag,
            "my": my / mag,
            "mz": mz / mag,
            "magnitude": np.ones((size, size)),
        }

    def test_returns_expected_keys(self, analyzer, uniform_mag):
        """Should return all expected statistics sections."""
        result = analyzer.spatial_statistics(uniform_mag)
        assert "field_statistics" in result
        assert "correlations" in result
        assert "gradients" in result
        assert "uniformity_index" in result
        assert "coherence_length" in result

    def test_field_statistics_structure(self, analyzer, uniform_mag):
        """Field statistics should contain mean, std, min, max, etc."""
        result = analyzer.spatial_statistics(uniform_mag)
        stats = result["field_statistics"]
        for comp in ["mx_stats", "my_stats", "mz_stats", "magnitude_stats"]:
            assert comp in stats
            s = stats[comp]
            assert "mean" in s
            assert "std" in s
            assert "min" in s
            assert "max" in s
            assert "rms" in s

    def test_uniform_mx_mean_is_one(self, analyzer, uniform_mag):
        """Uniform mx=1 should have mean=1."""
        result = analyzer.spatial_statistics(uniform_mag)
        mx_mean = result["field_statistics"]["mx_stats"]["mean"]
        assert mx_mean == pytest.approx(1.0, rel=1e-10)

    def test_uniform_mx_std_is_zero(self, analyzer, uniform_mag):
        """Uniform mx should have std=0."""
        result = analyzer.spatial_statistics(uniform_mag)
        mx_std = result["field_statistics"]["mx_stats"]["std"]
        assert mx_std == pytest.approx(0.0, abs=1e-15)

    def test_uniform_uniformity_index_is_one(self, analyzer, uniform_mag):
        """Uniform magnitude should give uniformity index of 1."""
        result = analyzer.spatial_statistics(uniform_mag)
        assert result["uniformity_index"] == pytest.approx(1.0, rel=1e-10)

    def test_correlations_in_valid_range(self, analyzer, random_mag):
        """Correlation coefficients should be in [-1, 1]."""
        result = analyzer.spatial_statistics(random_mag)
        for key, value in result["correlations"].items():
            assert -1.0 <= value <= 1.0, (
                f"Correlation {key}={value} outside [-1, 1]"
            )

    def test_gradients_nonnegative_rms(self, analyzer, random_mag):
        """Gradient RMS values should be non-negative."""
        result = analyzer.spatial_statistics(random_mag)
        for key, grad_stats in result["gradients"].items():
            if isinstance(grad_stats, dict) and "rms" in grad_stats:
                assert grad_stats["rms"] >= 0

    def test_coherence_length_positive(self, analyzer, random_mag):
        """Coherence length should be positive."""
        result = analyzer.spatial_statistics(random_mag)
        assert result["coherence_length"] > 0

    def test_random_mag_has_nonzero_std(self, analyzer, random_mag):
        """Random magnetization should have nonzero standard deviation."""
        result = analyzer.spatial_statistics(random_mag)
        mx_std = result["field_statistics"]["mx_stats"]["std"]
        assert mx_std > 0


class TestAnalyzeDomains:
    """Tests for domain analysis."""

    @pytest.fixture
    def analyzer(self):
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            return MagnetizationAnalyzer()

    @pytest.fixture
    def two_domain_mag(self):
        """Magnetization with two clear domains (left=+x, right=-x)."""
        size = 20
        mx = np.ones((size, size))
        mx[:, size // 2:] = -1.0
        my = np.zeros((size, size))
        mz = np.zeros((size, size))
        theta = np.arccos(np.clip(mz, -1, 1))
        phi = np.arctan2(my, mx)
        return {
            "mx": mx, "my": my, "mz": mz,
            "theta": theta, "phi": phi,
            "magnitude": np.ones((size, size)),
        }

    @pytest.fixture
    def coordinates_20x20(self):
        size = 20
        spacing = 1e-9
        x = np.linspace(0, (size - 1) * spacing, size)
        y = np.linspace(0, (size - 1) * spacing, size)
        X, Y = np.meshgrid(x, y, indexing="ij")
        return {"x": X, "y": Y, "z": np.zeros_like(X)}

    def test_returns_expected_keys(self, analyzer, two_domain_mag, coordinates_20x20):
        """Should return all expected domain analysis keys."""
        result = analyzer.analyze_domains(two_domain_mag, coordinates_20x20)
        assert "num_domains" in result
        assert "domain_labels" in result
        assert "domain_walls" in result
        assert "domain_statistics" in result
        assert "average_domain_size" in result
        assert "domain_wall_density" in result

    def test_domain_labels_shape(self, analyzer, two_domain_mag, coordinates_20x20):
        """Domain labels should match input shape."""
        result = analyzer.analyze_domains(two_domain_mag, coordinates_20x20)
        assert result["domain_labels"].shape == (20, 20)

    def test_domain_walls_boolean(self, analyzer, two_domain_mag, coordinates_20x20):
        """Domain walls should be boolean array."""
        result = analyzer.analyze_domains(two_domain_mag, coordinates_20x20)
        assert result["domain_walls"].dtype == bool

    def test_domain_wall_density_bounded(self, analyzer, two_domain_mag, coordinates_20x20):
        """Domain wall density should be between 0 and 1."""
        result = analyzer.analyze_domains(two_domain_mag, coordinates_20x20)
        assert 0 <= result["domain_wall_density"] <= 1

    def test_num_domains_nonnegative(self, analyzer, two_domain_mag, coordinates_20x20):
        """Number of domains should be non-negative."""
        result = analyzer.analyze_domains(two_domain_mag, coordinates_20x20)
        assert result["num_domains"] >= 0


class TestAnalyzeTopology:
    """Tests for topological analysis."""

    @pytest.fixture
    def analyzer(self):
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            return MagnetizationAnalyzer()

    @pytest.fixture
    def vortex_mag(self):
        """Vortex magnetization pattern (21x21 grid)."""
        size = 21
        center = size // 2
        mx = np.zeros((size, size))
        my = np.zeros((size, size))
        mz = np.zeros((size, size))

        for i in range(size):
            for j in range(size):
                x = j - center
                y = i - center
                r = np.sqrt(x**2 + y**2)
                if r > 0:
                    mx[i, j] = -y / (r + 1)
                    my[i, j] = x / (r + 1)
                    mz[i, j] = np.exp(-r / 3)
                else:
                    mx[i, j] = 0
                    my[i, j] = 0
                    mz[i, j] = 1

        mag = np.sqrt(mx**2 + my**2 + mz**2)
        mag = np.where(mag > 0, mag, 1)
        return {"mx": mx / mag, "my": my / mag, "mz": mz / mag}

    def test_returns_expected_keys(self, analyzer, vortex_mag):
        """Should return vortices, charges, skyrmions, etc."""
        result = analyzer.analyze_topology(vortex_mag)
        assert "vortices" in result
        assert "total_topological_charge" in result
        assert "topological_charge_density" in result
        assert "skyrmions" in result
        assert "num_topological_defects" in result

    def test_topological_charge_finite(self, analyzer, vortex_mag):
        """Total topological charge should be finite."""
        result = analyzer.analyze_topology(vortex_mag)
        assert np.isfinite(result["total_topological_charge"])

    def test_charge_density_shape(self, analyzer, vortex_mag):
        """Topological charge density should be 2D array."""
        result = analyzer.analyze_topology(vortex_mag)
        charge = result["topological_charge_density"]
        assert charge.ndim == 2

    def test_vortex_detection_structure(self, analyzer, vortex_mag):
        """Vortex detection should return positions and charges lists."""
        result = analyzer.analyze_topology(vortex_mag)
        vortices = result["vortices"]
        assert "positions" in vortices
        assert "charges" in vortices
        assert len(vortices["positions"]) == len(vortices["charges"])

    def test_1d_data_no_vortices(self, analyzer):
        """1D data should return empty vortex list."""
        mag = {"mx": np.ones(10), "my": np.zeros(10), "mz": np.zeros(10)}
        result = analyzer.analyze_topology(mag)
        assert result["vortices"]["positions"] == []


class TestFieldStatistics:
    """Tests for the _calculate_field_statistics helper."""

    @pytest.fixture
    def analyzer(self):
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            return MagnetizationAnalyzer()

    def test_known_array(self, analyzer):
        """Test statistics on an array with known values."""
        field = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        stats = analyzer._calculate_field_statistics(field)
        assert stats["mean"] == pytest.approx(3.0)
        assert stats["min"] == pytest.approx(1.0)
        assert stats["max"] == pytest.approx(5.0)
        assert stats["median"] == pytest.approx(3.0)
        assert stats["rms"] == pytest.approx(np.sqrt(np.mean(field**2)))

    def test_constant_array(self, analyzer):
        """Constant array should have std=0."""
        field = np.full(10, 7.0)
        stats = analyzer._calculate_field_statistics(field)
        assert stats["mean"] == pytest.approx(7.0)
        assert stats["std"] == pytest.approx(0.0)


class TestUniformityIndex:
    """Tests for uniformity index calculation."""

    @pytest.fixture
    def analyzer(self):
        with patch("maglogic.analysis.magnetization.OOMMFParser"), \
             patch("maglogic.analysis.magnetization.MuMax3Parser"):
            from maglogic.analysis.magnetization import MagnetizationAnalyzer
            return MagnetizationAnalyzer()

    def test_perfectly_uniform(self, analyzer):
        """Perfectly uniform field should give index 1.0."""
        magnitude = np.ones((10, 10))
        idx = analyzer._calculate_uniformity_index(magnitude)
        assert idx == pytest.approx(1.0, rel=1e-10)

    def test_zero_field(self, analyzer):
        """Zero field should give index 0.0."""
        magnitude = np.zeros((10, 10))
        idx = analyzer._calculate_uniformity_index(magnitude)
        assert idx == 0.0

    def test_nonuniform_less_than_one(self, analyzer):
        """Non-uniform field should give index < 1."""
        rng = np.random.RandomState(42)
        magnitude = rng.uniform(0.5, 1.5, (10, 10))
        idx = analyzer._calculate_uniformity_index(magnitude)
        assert idx < 1.0


if __name__ == "__main__":
    pytest.main([__file__])
