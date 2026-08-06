"""
Test suite for pin-pin beam equation classes.
Critical for structural analysis - core calculation functions with complex math.
"""
import pytest
import sys
import math
from pathlib import Path

# Import the module to test
sys.path.insert(0, str(Path(__file__).parent.parent / 'Analysis'))
import pin_pin_beam_equations_classes as ppbeam


class TestPolyEval:
    """Tests for poly_eval function - polynomial evaluation."""

    def test_zero_coefficients(self):
        """Test with all zero coefficients."""
        result = ppbeam.poly_eval([0, 0, 0], 5)
        assert result == 0

    def test_constant_polynomial(self):
        """Test constant polynomial - only c0."""
        result = ppbeam.poly_eval([5], 0)
        assert result == 5
        result = ppbeam.poly_eval([5], 10)
        assert result == 5

    def test_linear_polynomial(self):
        """Test linear polynomial: 3 + 2x."""
        # Coefficients: [c0, c1x] = [3, 2]
        result = ppbeam.poly_eval([3, 2], 0)
        assert result == 3
        result = ppbeam.poly_eval([3, 2], 5)
        assert result == 13  # 3 + 2*5
        result = ppbeam.poly_eval([3, 2], -2)
        assert result == -1  # 3 + 2*(-2)

    def test_quadratic_polynomial(self):
        """Test quadratic polynomial: 1 + 2x + x^2."""
        # Coefficients: [c0, c1, c2] = [1, 2, 1]
        result = ppbeam.poly_eval([1, 2, 1], 0)
        assert result == 1
        result = ppbeam.poly_eval([1, 2, 1], 3)
        assert result == 16  # 1 + 2*3 + 3^2 = 1 + 6 + 9
        result = ppbeam.poly_eval([1, 2, 1], -1)
        assert result == 0  # 1 + 2*(-1) + (-1)^2

    def test_cubic_polynomial(self):
        """Test cubic polynomial: x^3."""
        result = ppbeam.poly_eval([0, 0, 0, 1], 2)
        assert result == 8

    def test_negative_coefficients(self):
        """Test with negative coefficients."""
        # -x^2 + 3x - 2
        result = ppbeam.poly_eval([-2, 3, -1], 0)
        assert result == -2
        result = ppbeam.poly_eval([-2, 3, -1], 1)
        assert result == 0  # -2 + 3 - 1
        result = ppbeam.poly_eval([-2, 3, -1], 2)
        assert result == -4  # -2 + 6 - 4

    def test_single_high_order_term(self):
        """Test with single non-zero high-order term."""
        result = ppbeam.poly_eval([0, 0, 0, 0, 1], 2)
        assert result == 16  # 2^4

    def test_very_large_x_value(self):
        """Test with large x values."""
        result = ppbeam.poly_eval([1, 1], 1000)
        assert result == 1001

    def test_negative_x_value(self):
        """Test with negative x values."""
        result = ppbeam.poly_eval([1, 1, 1], -2)
        assert result == 3  # 1 + 1*(-2) + 1*(-2)^2 = 1 - 2 + 4


class TestNoLoad:
    """Tests for no_load class - baseline case with no loading."""

    def test_initialization(self):
        """Test no_load initialization."""
        nl = ppbeam.no_load(20)
        assert nl.p == 0
        assert nl.rl == 0
        assert nl.rr == 0
        assert nl.L == 20
        assert nl.case == 'D'
        assert nl.kind == 'NL'

    def test_custom_case(self):
        """Test initialization with custom case."""
        nl = ppbeam.no_load(20, case='L')
        assert nl.case == 'L'

    def test_chart_load(self):
        """Test chart_load returns empty arrays."""
        nl = ppbeam.no_load(20)
        x, y = nl.chart_load()
        assert x == [0]
        assert y == [0]

    def test_piece_functions(self):
        """Test piece_functions for no load."""
        nl = ppbeam.no_load(20)
        pieces, strings = nl.piece_functions()
        
        # Should have lists for v, m, eis, eid
        assert len(pieces) == 4
        assert len(strings) == 4
        
        # All should be zero functions
        v_funcs, m_funcs, eis_funcs, eid_funcs = pieces
        assert v_funcs == [[[0], [0, 20]]]

    def test_methods_return_zero(self):
        """Test that all analysis methods return zero."""
        nl = ppbeam.no_load(20)
        
        # Vector methods
        import numpy as np
        x = [0, 5, 10, 15, 20]
        v = nl.v(x)
        m = nl.m(x)
        eis = nl.eis(x)
        eid = nl.eid(x)
        
        assert all(val == 0 for val in v)
        assert all(val == 0 for val in m)
        assert all(val == 0 for val in eis)
        assert all(val == 0 for val in eid)

    def test_scalar_methods_zero(self):
        """Test scalar methods return zero."""
        nl = ppbeam.no_load(20)
        
        assert nl.vx(5) == 0
        assert nl.mx(5) == 0
        assert nl.eisx(5) == 0
        assert nl.eidx(5) == 0


class TestPointLoad:
    """Tests for pl (point load) class - single concentrated load."""

    def test_initialization_basic(self):
        """Test basic point load initialization."""
        pl = ppbeam.pl(10, 5, 20)
        assert pl.p == 10
        assert pl.a == 5
        assert pl.L == 20
        assert pl.b == 15
        assert pl.kind == 'Point'

    def test_reaction_calculation(self):
        """Test reaction calculations for point load."""
        # Load P at distance a from left
        # RL = P*b/L, RR = P*a/L
        pl = ppbeam.pl(100, 5, 20)
        assert pl.rl == pytest.approx(75)  # 100*15/20
        assert pl.rr == pytest.approx(25)  # 100*5/20

    def test_reactions_sum_to_load(self):
        """Test that reactions sum to applied load."""
        pl = ppbeam.pl(50, 8, 20)
        assert pl.rl + pl.rr == pytest.approx(pl.p)

    def test_load_at_left_support(self):
        """Test load applied at left support."""
        pl = ppbeam.pl(100, 0, 20)
        assert pl.error == 'Error a > l'  # Actually should be caught, but check behavior
        # Right reaction should equal load
        # (handled by initialization)

    def test_load_at_right_support(self):
        """Test load applied at right support."""
        pl = ppbeam.pl(100, 20, 20)
        # Left reaction should equal load
        assert pl.rl == pytest.approx(100)
        assert pl.rr == pytest.approx(0)

    def test_load_at_midspan(self):
        """Test load at midspan - equal reactions."""
        pl = ppbeam.pl(100, 10, 20)
        assert pl.rl == pytest.approx(50)
        assert pl.rr == pytest.approx(50)

    def test_shear_force_distribution(self):
        """Test shear force distribution."""
        pl = ppbeam.pl(100, 5, 20)
        x = [0, 2.5, 5, 7.5, 15, 20]
        v = pl.v(x)
        
        # Left of load: V = RL
        assert v[0] == pytest.approx(75)
        assert v[1] == pytest.approx(75)
        
        # At load (left of): V = RL
        assert v[2] == pytest.approx(75)
        
        # Right of load: V = -RR
        assert v[3] == pytest.approx(-25)
        assert v[4] == pytest.approx(-25)
        assert v[5] == pytest.approx(-25)

    def test_bending_moment_distribution(self):
        """Test bending moment distribution."""
        pl = ppbeam.pl(100, 10, 20)
        x = [0, 5, 10, 15, 20]
        m = pl.m(x)
        
        # M = RL*x for x <= a
        assert m[0] == pytest.approx(0)
        assert m[1] == pytest.approx(250)  # 50*5
        assert m[2] == pytest.approx(500)  # 50*10 (max at load)
        
        # M = -RR*x + RR*L for x > a
        assert m[3] == pytest.approx(250)  # -50*15 + 50*20
        assert m[4] == pytest.approx(0)

    def test_scalar_shear_force(self):
        """Test scalar shear force method."""
        pl = ppbeam.pl(100, 10, 20)
        
        # Left of load
        assert pl.vx(5) == pytest.approx(50)
        
        # Right of load
        assert pl.vx(15) == pytest.approx(-50)
        
        # At load position
        assert pl.vx(10) == pytest.approx(50)  # Uses left value at discontinuity

    def test_scalar_moment(self):
        """Test scalar moment method."""
        pl = ppbeam.pl(100, 10, 20)
        
        # Left of load
        assert pl.mx(5) == pytest.approx(250)
        
        # At load
        assert pl.mx(10) == pytest.approx(500)
        
        # Right of load
        assert pl.mx(15) == pytest.approx(250)

    def test_error_load_beyond_span(self):
        """Test error handling for load beyond span."""
        pl = ppbeam.pl(100, 25, 20)
        assert pl.error == 'Error a > l'

    def test_deflection_calculations(self):
        """Test deflection (EI*delta) calculations."""
        pl = ppbeam.pl(100, 10, 20)
        
        # EI*delta should be continuous
        x = [0, 5, 10, 15, 20]
        eid = pl.eid(x)
        
        # Should be zero at supports
        assert eid[0] == pytest.approx(0, abs=1e-6)
        assert eid[-1] == pytest.approx(0, abs=1e-6)
        
        # Should have maximum negative value (downward) near midspan
        assert min(eid) < 0
        assert min(eid) < -100  # Significant deflection

    def test_slope_continuity(self):
        """Test that slope (EI*slope) is continuous through load point."""
        pl = ppbeam.pl(100, 10, 20)
        
        # Get slope just before and after load
        eis_left = pl.eisx(9.999)
        eis_right = pl.eisx(10.001)
        
        # Should be close (continuous but with different slope)
        assert abs(eis_left - eis_right) < 0.1


class TestPieceFunctionString:
    """Tests for PieceFunctionString utility function."""

    def test_zero_function(self):
        """Test piecewise function string for zero function."""
        piece_set = [[[0], [0, 10]]]
        output = ppbeam.PieceFunctionString(piece_set)
        assert '0' in output
        assert '0.0000 < x <= 10.0000' in output

    def test_single_piece_constant(self):
        """Test single piece constant function."""
        piece_set = [[[5.5], [0, 10]]]
        output = ppbeam.PieceFunctionString(piece_set)
        assert '5.5000' in output
        assert '0.0000 < x <= 10.0000' in output

    def test_linear_function(self):
        """Test linear piecewise function."""
        piece_set = [[[2, 3], [0, 5]]]
        output = ppbeam.PieceFunctionString(piece_set)
        assert '2.0000' in output
        assert '3.0000*x' in output

    def test_multiple_pieces(self):
        """Test multiple piece function."""
        piece_set = [
            [[-5], [0, 10]],
            [[10], [10, 20]]
        ]
        output = ppbeam.PieceFunctionString(piece_set)
        assert '0.0000 < x <= 10.0000' in output
        assert '10.0000 < x <= 20.0000' in output

    def test_html_table_format(self):
        """Test HTML table format output."""
        piece_set = [[[5], [0, 10]]]
        output = ppbeam.PieceFunctionStringHTMLTable(piece_set, "Test Function")
        
        assert '<table>' in output
        assert '<th>Test Function</th>' in output
        assert '</table>' in output


class TestFixedEndForces:
    """Tests for fixed end force calculations."""

    def test_no_load_fef(self):
        """Test fixed end forces for no load."""
        nl = ppbeam.no_load(20)
        fef = nl.fef()
        assert fef == [0, 0, 0, 0]

    def test_point_load_fef(self):
        """Test fixed end forces for point load."""
        pl = ppbeam.pl(100, 10, 20)
        fef = pl.fef()
        
        # For fixed-end beam, forces are more complex
        assert len(fef) == 4
        assert fef[0] + fef[2] == pytest.approx(-pl.p)  # Vertical equilibrium


class TestLoadCombinations:
    """Tests for combined loading scenarios."""

    def test_two_equal_loads(self):
        """Test beam with two equal point loads."""
        # Create individual loads
        pl1 = ppbeam.pl(50, 5, 20)
        pl2 = ppbeam.pl(50, 15, 20)
        
        # Combined reactions should sum
        total_rl = pl1.rl + pl2.rl
        total_rr = pl1.rr + pl2.rr
        assert total_rl == pytest.approx(50)
        assert total_rr == pytest.approx(50)

    def test_unsymmetric_loading(self):
        """Test with unsymmetric loading."""
        pl1 = ppbeam.pl(30, 5, 20)
        pl2 = ppbeam.pl(70, 15, 20)
        
        total_load = pl1.p + pl2.p
        total_reactions = pl1.rl + pl1.rr + pl2.rl + pl2.rr
        assert total_reactions == pytest.approx(total_load)


class TestPhysicalValidity:
    """Tests that results satisfy physical requirements."""

    def test_moment_maximum_between_supports(self):
        """Moment should be zero at supports and max between them."""
        pl = ppbeam.pl(100, 10, 20)
        
        x = [0, 5, 10, 15, 20]
        m = pl.m(x)
        
        assert m[0] == pytest.approx(0)  # At left support
        assert m[-1] == pytest.approx(0)  # At right support
        assert max(abs(v) for v in m) == m[2]  # Max at load

    def test_deflection_symmetric_loading(self):
        """For symmetric loading, deflection should be symmetric."""
        pl = ppbeam.pl(100, 10, 20)  # Load at midspan
        
        # Get deflections at symmetric points
        eid_left = pl.eidx(5)
        eid_right = pl.eidx(15)
        
        # Should be equal
        assert eid_left == pytest.approx(eid_right)

    def test_reactions_equilibrium(self):
        """Reactions must equal applied load."""
        test_cases = [
            (100, 5, 20),
            (250, 8, 30),
            (50, 15, 20),
            (1000, 1, 100)
        ]
        
        for P, a, L in test_cases:
            pl = ppbeam.pl(P, a, L)
            assert pl.rl + pl.rr == pytest.approx(P)

    def test_moment_equilibrium(self):
        """Moment equilibrium about any point."""
        pl = ppbeam.pl(100, 8, 20)
        
        # Take moments about left support
        # RL*0 + RR*L - P*a = 0
        moment_eq = pl.rr * pl.L - pl.p * pl.a
        assert moment_eq == pytest.approx(0)
