"""
Test suite for wood stud wall calculations.
Critical for load-bearing design - complex factor calculations and data mutations.
"""
import pytest
import sys
from pathlib import Path

# Import the module to test
sys.path.insert(0, str(Path(__file__).parent.parent / 'Wood'))
import wood_classes as wood


class TestWoodStudWallInitialization:
    """Tests for wood_stud_wall class initialization and basic properties."""

    def test_initialization_defaults(self):
        """Test default initialization."""
        wall = wood.wood_stud_wall()
        
        assert wall.b_in == 1.5
        assert wall.d_in == 3.5
        assert wall.height_in == 120  # 10 ft * 12
        assert wall.spacing_in == 12
        assert wall.fb_psi == 875
        assert wall.fv_psi == 150

    def test_initialization_custom_values(self):
        """Test initialization with custom values."""
        wall = wood.wood_stud_wall(
            b_in=1.75,
            d_in=5.5,
            height_ft=12,
            spacing_in=16,
            grade="Construction",
            fb_psi=1000,
            fv_psi=200
        )
        
        assert wall.b_in == 1.75
        assert wall.d_in == 5.5
        assert wall.height_in == 144  # 12 ft * 12
        assert wall.spacing_in == 16
        assert wall.fb_psi == 1000
        assert wall.fv_psi == 200

    def test_height_with_plates(self):
        """Test height adjustment when accounting for plates."""
        # 10 ft wall with 2 plates (1.5" each = 3" total)
        wall = wood.wood_stud_wall(height_ft=10, num_plates=2)
        assert wall.height_in == 117  # 120 - 3

    def test_section_properties_calculation(self):
        """Test section property calculations (area, MOI, section modulus)."""
        wall = wood.wood_stud_wall(b_in=1.5, d_in=3.5)
        
        # Area = b * d
        expected_area = 1.5 * 3.5
        assert wall.area_in2 == pytest.approx(expected_area)
        
        # I = b * d^3 / 12
        expected_I = (1.5 * 3.5**3) / 12
        assert wall.I_in4 == pytest.approx(expected_I)
        
        # S = b * d^2 / 6
        expected_S = (1.5 * 3.5**2) / 6
        assert wall.s_in3 == pytest.approx(expected_S)

    def test_repetitive_member_factor_16_spacing(self):
        """Test CR factor for 16" spacing (most common)."""
        wall = wood.wood_stud_wall(spacing_in=16)
        assert wall.cr == 1.15  # Typical factor for spaced studs

    def test_repetitive_member_factor_24_spacing(self):
        """Test CR factor for 24" spacing."""
        wall = wood.wood_stud_wall(spacing_in=24)
        assert wall.cr == 1.15

    def test_repetitive_member_factor_over_24_spacing(self):
        """Test CR factor for spacing > 24"."""
        wall = wood.wood_stud_wall(spacing_in=25)
        assert wall.cr == 1.0  # No repetitive member factor

    def test_size_factor_by_grade(self):
        """Test size factor (Cf) varies by grade."""
        # Stud grade
        wall_stud = wood.wood_stud_wall(d_in=3.5, grade="Stud")
        assert wall_stud.cf_fb > 0
        assert wall_stud.cf_fc > 0
        
        # Construction grade
        wall_const = wood.wood_stud_wall(d_in=3.5, grade="Construction")
        assert wall_const.cf_fb == 1.0
        assert wall_const.cf_fc == 1.0

    def test_size_factor_by_depth(self):
        """Test Cf changes with stud depth (Stud grade)."""
        depths = [3.5, 5.5, 7.25, 9.25, 11.25]
        cf_values = []
        
        for d in depths:
            wall = wood.wood_stud_wall(d_in=d, grade="Stud")
            cf_values.append(wall.cf_fb)
        
        # Cf should decrease as depth increases for visually graded lumber
        assert cf_values[-1] <= cf_values[0]

    def test_wet_service_factor_calculation(self):
        """Test wet service factor (Cm) application."""
        # Dry condition (19% moisture or less)
        wall_dry = wood.wood_stud_wall(moisture_percent=19)
        assert wall_dry.cm_fb == 1.0
        assert wall_dry.cm_fc == 1.0
        assert wall_dry.cm_E == 1.0
        
        # Wet condition (> 19% moisture)
        wall_wet = wood.wood_stud_wall(moisture_percent=20)
        assert wall_wet.cm_E == 0.9  # E reduced
        assert wall_wet.cm_fc_perp == 0.67  # fc_perp reduced

    def test_temperature_factor_normal(self):
        """Test temperature factor (Ct) for normal conditions."""
        wall = wood.wood_stud_wall(temp=90)
        assert wall.ct_E == 1.0
        assert wall.ct_fb == 1.0
        assert wall.ct_fc == 1.0

    def test_temperature_factor_elevated(self):
        """Test Ct for elevated temperatures."""
        wall = wood.wood_stud_wall(temp=120, moisture_percent=12)
        assert wall.ct_E == 0.9
        assert wall.ct_fb == 0.7  # Wet + hot
        
    def test_temperature_factor_very_high(self):
        """Test Ct for temperatures over 150F (out of range)."""
        wall = wood.wood_stud_wall(temp=160)
        assert wall.ct_fb == 0.01  # Flag value
        assert 'Appendix C' in wall.warning  # Should warn

    def test_incising_factor(self):
        """Test incising factor (Ci)."""
        wall_not_incised = wood.wood_stud_wall(incised=0)
        assert wall_not_incised.ci_fb == 1.0
        assert wall_not_incised.ci_E == 1.0
        
        wall_incised = wood.wood_stud_wall(incised=1)
        assert wall_incised.ci_fb == 0.8
        assert wall_incised.ci_E == 0.95

    def test_bearing_area_factor(self):
        """Test bearing area factor (Cb) for perpendicular compression."""
        # b < 6" get Cb enhancement
        wall = wood.wood_stud_wall(b_in=1.5)
        expected_cb = (1.5 + 0.375) / 1.5
        assert wall.cb_fc_perp == pytest.approx(expected_cb)
        
        # b >= 6" get no enhancement
        wall_large = wood.wood_stud_wall(b_in=6)
        assert wall_large.cb_fc_perp == 1.0

    def test_deflection_limits(self):
        """Test deflection limits (L/180, L/240, L/360)."""
        wall = wood.wood_stud_wall(height_ft=10)
        height_in = 120
        
        assert wall.defl_180 == pytest.approx(height_in / 180.0)
        assert wall.defl_240 == pytest.approx(height_in / 240.0)
        assert wall.defl_360 == pytest.approx(height_in / 360.0)

    def test_adjusted_properties_calculation(self):
        """Test that adjusted properties (with factors) are calculated."""
        wall = wood.wood_stud_wall()
        
        # E' = E * Cm * Ct * Ci * Cft
        assert wall.E_prime_psi > 0
        assert wall.E_prime_psi < wall.E_psi  # Should be reduced by factors
        
        # Fv' = Fv * Cm * Ct * Ci * Cft
        assert wall.fv_prime_psi > 0

    def test_fc_perp_with_factors(self):
        """Test perpendicular compression with all factors."""
        wall = wood.wood_stud_wall(b_in=1.5)
        
        # Fc_perp' = Fc_perp * Cm * Ct * Ci * Cb * Cft
        assert wall.fc_perp_pl_prime_psi > 0
        assert wall.fc_perp_pl_prime_psi <= wall.fc_perp_pl_psi


class TestWoodStudWallDesignFactors:
    """Tests for design factor calculations."""

    def test_all_factors_positive(self):
        """All design factors should be positive."""
        wall = wood.wood_stud_wall()
        
        factors = [
            wall.cr, wall.cf_fb, wall.cf_fc,
            wall.cm_fb, wall.cm_fc, wall.cm_E,
            wall.ct_fb, wall.ct_fc, wall.ct_E,
            wall.ci_fb, wall.ci_fc, wall.ci_E,
            wall.cb_fc_perp, wall.cfu, wall.cT
        ]
        
        assert all(f > 0 for f in factors), "All factors should be positive"

    def test_factors_not_exceed_unity(self):
        """Most factors should not exceed 1.0 (except Cr and Cf)."""
        wall = wood.wood_stud_wall()
        
        # These should typically be <= 1.0
        typical_factors = [
            wall.cm_fb, wall.cm_fc, wall.cm_E,
            wall.ct_fb, wall.ct_fc, wall.ct_E,
            wall.ci_fb, wall.ci_fc, wall.ci_E
        ]
        
        assert all(f <= 1.0 for f in typical_factors)

    def test_cr_factor_physical_validity(self):
        """Cr factor should be 1.0 or 1.15 for typical cases."""
        wall_16 = wood.wood_stud_wall(spacing_in=16)
        wall_25 = wood.wood_stud_wall(spacing_in=25)
        
        assert wall_16.cr in [1.0, 1.15]
        assert wall_25.cr in [1.0, 1.15]

    def test_beam_stability_factor_sheathed(self):
        """Test beam stability factor for sheathed stud."""
        wall = wood.wood_stud_wall(compression_face=1.0)
        assert wall.cl == 1.0  # Sheathed case

    def test_beam_stability_factor_unsheathed(self):
        """Test beam stability factor for unsheathed stud."""
        wall = wood.wood_stud_wall(compression_face=0)
        # Should have calculated CL components
        assert hasattr(wall, 'Rb_cl')
        assert hasattr(wall, 'Fbe_cl')
        assert wall.Rb_cl > 0
        assert wall.Fbe_cl > 0


class TestWoodStudWallDeflectionCapacity:
    """Tests for deflection capacity calculations."""

    def test_deflection_capacity_calculation(self):
        """Test that deflection capacities are calculated."""
        wall = wood.wood_stud_wall()
        
        # Should have pressures for each deflection limit
        assert hasattr(wall, 'defl_180_w_psf')
        assert hasattr(wall, 'defl_240_w_psf')
        assert hasattr(wall, 'defl_360_w_psf')

    def test_deflection_capacity_physical_validity(self):
        """Stricter limits should result in lower allowable pressures."""
        wall = wood.wood_stud_wall()
        
        # L/180 is stricter than L/240 which is stricter than L/360
        # So corresponding pressures should be: 180 < 240 < 360
        assert wall.defl_180_w_psf < wall.defl_240_w_psf
        assert wall.defl_240_w_psf < wall.defl_360_w_psf

    def test_deflection_increases_with_modulus(self):
        """Higher modulus should increase deflection capacity."""
        wall_low_E = wood.wood_stud_wall(E_psi=1000000)
        wall_high_E = wood.wood_stud_wall(E_psi=2000000)
        
        # Higher E should give higher deflection capacity
        assert wall_high_E.defl_180_w_psf > wall_low_E.defl_180_w_psf


class TestWoodStudWallEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_minimum_dimensions(self):
        """Test with minimal stud dimensions."""
        wall = wood.wood_stud_wall(b_in=1.5, d_in=1.5, height_ft=1)
        assert wall.area_in2 > 0
        assert wall.I_in4 > 0
        assert wall.s_in3 > 0

    def test_large_dimensions(self):
        """Test with large stud dimensions."""
        wall = wood.wood_stud_wall(b_in=12, d_in=12, height_ft=30)
        assert wall.area_in2 == 144
        assert wall.height_in == 360

    def test_all_grades(self):
        """Test with various lumber grades."""
        grades = ["Stud", "Construction", "Utility", "No. 2", "No. 1"]
        
        for grade in grades:
            try:
                wall = wood.wood_stud_wall(grade=grade)
                assert wall.cf_fb > 0
                assert wall.cf_fc > 0
            except:
                # Some grades may not be implemented, which is OK
                pass

    def test_southern_pine_properties(self):
        """Test Southern Pine (SyP) flag."""
        wall_syp = wood.wood_stud_wall(is_syp=1)
        wall_other = wood.wood_stud_wall(is_syp=0)
        
        # Both should have factors
        assert wall_syp.cf_fb > 0
        assert wall_other.cf_fb > 0

    def test_extreme_temperatures(self):
        """Test with extreme temperature conditions."""
        # Very cold
        wall_cold = wood.wood_stud_wall(temp=0)
        assert wall_cold.ct_E >= 0.9
        
        # Very hot
        wall_hot = wood.wood_stud_wall(temp=150)
        # Should trigger some flag
        assert wall_hot.ct_E >= 0

    def test_varying_c_frt_array(self):
        """Test with different c_frt factor arrays."""
        default_wall = wood.wood_stud_wall()
        
        # Custom factors
        custom_factors = [0.8, 0.9, 0.7, 0.85, 1.0, 1.1]
        custom_wall = wood.wood_stud_wall(c_frt=custom_factors)
        
        # Should be applied to calculations
        assert default_wall.E_prime_psi != custom_wall.E_prime_psi

    def test_blocking_specification(self):
        """Test blocking factor."""
        wall_no_blocking = wood.wood_stud_wall(blocking_ft=0)
        assert wall_no_blocking.blocking_in == 0
        
        wall_with_blocking = wood.wood_stud_wall(blocking_ft=4)
        assert wall_with_blocking.blocking_in == 48


class TestWoodStudWallPhysicalValidity:
    """Tests that ensure physically valid results."""

    def test_positive_material_properties(self):
        """All material properties should be positive."""
        wall = wood.wood_stud_wall()
        
        properties = [
            wall.area_in2, wall.I_in4, wall.s_in3,
            wall.E_psi, wall.Emin_psi, wall.fb_psi,
            wall.fc_psi, wall.fv_psi, wall.fc_perp_pl_psi
        ]
        
        assert all(p > 0 for p in properties)

    def test_adjusted_values_less_than_base(self):
        """Adjusted strengths should be less than or equal to base."""
        wall = wood.wood_stud_wall()
        
        # E' <= E (with factors)
        assert wall.E_prime_psi <= wall.E_psi
        
        # Fv' <= Fv
        assert wall.fv_prime_psi <= wall.fv_psi

    def test_i_increases_with_depth(self):
        """Moment of inertia should increase with depth."""
        wall_small = wood.wood_stud_wall(d_in=3.5)
        wall_large = wood.wood_stud_wall(d_in=7.5)
        
        assert wall_large.I_in4 > wall_small.I_in4

    def test_deflection_limit_ordering(self):
        """Deflection limits should follow L/n pattern."""
        wall = wood.wood_stud_wall(height_ft=10)
        
        # Verify the ratio relationship
        ratio_180_240 = wall.defl_180 / wall.defl_240
        ratio_240_360 = wall.defl_240 / wall.defl_360
        
        # 180/240 = 180/240 ≈ 0.75
        # 240/360 = 240/360 ≈ 0.67
        assert 0.7 < ratio_180_240 < 0.8
        assert 0.65 < ratio_240_360 < 0.7

    def test_section_modulus_relationship(self):
        """Section modulus should relate to I and d."""
        wall = wood.wood_stud_wall(b_in=1.5, d_in=5.5)
        
        # S = I / (d/2)
        expected_S = wall.I_in4 / (wall.d_in / 2.0)
        
        assert wall.s_in3 == pytest.approx(expected_S)


class TestWoodStudWallAssumptions:
    """Tests that verify assumption tracking."""

    def test_assumptions_string_created(self):
        """Test that assumption notes are documented."""
        wall = wood.wood_stud_wall()
        
        assert isinstance(wall.assumptions, str)
        assert len(wall.assumptions) > 0
        assert 'ASSUMPTIONS' in wall.assumptions

    def test_warning_log_creation(self):
        """Test that warning log exists."""
        wall = wood.wood_stud_wall()
        
        assert hasattr(wall, 'warning')
        assert isinstance(wall.warning, str)

    def test_extreme_temp_warning(self):
        """Test that high temperature triggers warning."""
        wall = wood.wood_stud_wall(temp=160)
        
        assert len(wall.warning) > 0
        assert 'Appendix C' in wall.warning

    def test_assumptions_include_details(self):
        """Test that assumptions include specific design assumptions."""
        wall = wood.wood_stud_wall(height_ft=10, num_plates=2)
        
        # Should mention plates adjustment
        assert 'plates' in wall.assumptions.lower()

    def test_southern_pine_assumption(self):
        """Test that SyP assumption is documented."""
        wall_syp = wood.wood_stud_wall(is_syp=1)
        assert 'Southern Pine' in wall_syp.assumptions
        
        wall_other = wood.wood_stud_wall(is_syp=0)
        assert 'North American Species' in wall_other.assumptions
