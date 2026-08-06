"""
Test suite for bolt group instantaneous center calculations.
Critical for connection design - data mutation and complex math paths.
"""
import pytest
import math as m
import sys
from pathlib import Path

# Import the module to test
sys.path.insert(0, str(Path(__file__).parent.parent / 'Steel'))
import bolt_group_istantaneous_center as ic


class TestBuildBoltGroup:
    """Tests for build_bolt_group function - generates bolt positions."""

    def test_single_bolt_2x1(self):
        """Test single bolt group: 2 columns x 1 row."""
        xloc, yloc = ic.build_bolt_group(2, 1, 3, 3)
        assert len(xloc) == 2
        assert len(yloc) == 2
        assert xloc == [0, 3]
        assert yloc == [0, 0]

    def test_single_row_multiple_columns(self):
        """Test single row with multiple column spacing."""
        xloc, yloc = ic.build_bolt_group(3, 1, 2.5, 3)
        assert len(xloc) == 3
        assert xloc == [0, 2.5, 5.0]
        assert yloc == [0, 0, 0]

    def test_single_column_multiple_rows(self):
        """Test single column with multiple row spacing."""
        xloc, yloc = ic.build_bolt_group(1, 3, 3, 1.5)
        assert len(xloc) == 3
        assert len(yloc) == 3
        assert xloc == [0, 0, 0]
        assert yloc == [0, 1.5, 3.0]

    def test_4x4_bolt_grid(self):
        """Test standard 4x4 bolt grid."""
        xloc, yloc = ic.build_bolt_group(4, 4, 3, 3)
        assert len(xloc) == 16
        assert len(yloc) == 16
        
        # Verify spacing
        unique_x = sorted(set(xloc))
        unique_y = sorted(set(yloc))
        assert unique_x == [0, 3, 6, 9]
        assert unique_y == [0, 3, 6, 9]
        
        # Verify count of bolts per column
        x_counts = {x: xloc.count(x) for x in unique_x}
        assert all(count == 4 for count in x_counts.values())

    def test_2x3_bolt_grid(self):
        """Test 2 columns x 3 rows."""
        xloc, yloc = ic.build_bolt_group(2, 3, 5, 2)
        assert len(xloc) == 6
        assert len(yloc) == 6
        
        # Check first column
        assert xloc[0] == 0 and yloc[0] == 0
        assert xloc[1] == 0 and yloc[1] == 2
        assert xloc[2] == 0 and yloc[2] == 4
        
        # Check second column
        assert xloc[3] == 5 and yloc[3] == 0
        assert xloc[4] == 5 and yloc[4] == 2
        assert xloc[5] == 5 and yloc[5] == 4

    def test_zero_spacing(self):
        """Test with zero spacing - degenerate case."""
        xloc, yloc = ic.build_bolt_group(2, 2, 0, 0)
        assert len(xloc) == 4
        # All bolts at origin
        assert all(x == 0 for x in xloc)
        assert all(y == 0 for y in yloc)

    def test_large_spacing(self):
        """Test with large spacing values."""
        xloc, yloc = ic.build_bolt_group(2, 2, 100, 50)
        assert xloc == [0, 0, 100, 100]
        assert yloc == [0, 50, 0, 50]


class TestBoltGroupCenter:
    """Tests for bolt_group_center function - finds centroid."""

    def test_two_bolts_simple(self):
        """Test centroid of two bolts."""
        xloc = [0, 2]
        yloc = [0, 0]
        cg = ic.bolt_group_center(xloc, yloc)
        assert cg == [1.0, 0.0]

    def test_four_bolts_square(self):
        """Test centroid of 4 bolts in square."""
        xloc = [0, 2, 0, 2]
        yloc = [0, 0, 2, 2]
        cg = ic.bolt_group_center(xloc, yloc)
        assert cg == [1.0, 1.0]

    def test_single_bolt(self):
        """Test centroid with single bolt."""
        xloc = [0]
        yloc = [0]
        # Function has special case for <3 bolts
        cg = ic.bolt_group_center(xloc, yloc)
        # For single bolt, should average with itself
        assert cg[0] == 0.0
        assert cg[1] == 0.0

    def test_three_bolts_triangle(self):
        """Test centroid of 3 bolts in triangle."""
        xloc = [0, 4, 2]
        yloc = [0, 0, 3.46]
        cg = ic.bolt_group_center(xloc, yloc)
        
        # Centroid should be at approximately (2, 1.15)
        expected_x = sum(xloc) / len(xloc)
        expected_y = sum(yloc) / len(yloc)
        assert abs(cg[0] - expected_x) < 1e-6
        assert abs(cg[1] - expected_y) < 1e-6

    def test_asymmetric_bolt_group(self):
        """Test centroid with asymmetric arrangement."""
        xloc = [0, 0, 3, 3, 3]
        yloc = [0, 2, 0, 1, 2]
        cg = ic.bolt_group_center(xloc, yloc)
        
        expected_x = sum(xloc) / len(xloc)
        expected_y = sum(yloc) / len(yloc)
        assert abs(cg[0] - expected_x) < 1e-6
        assert abs(cg[1] - expected_y) < 1e-6


class TestIcBrandt:
    """Tests for ic_brandt function - Brandt's instantaneous center method."""

    def test_single_bolt_zero_moment(self):
        """Test single bolt with zero moment - should have zero resultant."""
        xloc = [0]
        yloc = [0]
        IC = [0, 0]
        Mp = 0
        
        Rx, Ry, Mi, table = ic.ic_brandt(IC, xloc, yloc, Mp)
        assert Rx == 0
        assert Ry == 0
        assert Mi == 0

    def test_two_bolts_pure_shear(self):
        """Test two bolts under pure shear (no moment)."""
        xloc = [0, 2]
        yloc = [0, 0]
        IC = [1, 0]  # At centroid
        Mp = 0  # No moment
        
        Rx, Ry, Mi, table = ic.ic_brandt(IC, xloc, yloc, Mp)
        # With no moment and IC at centroid, forces should split equally
        assert abs(Rx) < 1e-10  # Near zero
        assert abs(Ry) < 1e-10

    def test_four_bolt_square_moment(self):
        """Test 4 bolts in square under moment about center."""
        xloc = [0, 2, 0, 2]
        yloc = [0, 0, 2, 2]
        IC = [1, 1]  # Centroid
        Mp = 100
        
        Rx, Ry, Mi, table = ic.ic_brandt(IC, xloc, yloc, Mp)
        # Moment should be resisted by bolt forces
        assert Mi > 0  # Should have moment resistance
        
        # Check table structure
        assert 'Bolt x to IC' in [t[0] for t in table]
        assert len(table) == 8  # 8 different outputs in table

    def test_degenerate_bolt_at_ic(self):
        """Test bolt exactly at instantaneous center."""
        xloc = [0, 2]
        yloc = [0, 0]
        IC = [0, 0]  # At first bolt
        Mp = 100
        
        Rx, Ry, Mi, table = ic.ic_brandt(IC, xloc, yloc, Mp)
        # Bolt at IC has zero distance, degenerate case handled
        assert table is not None
        assert len(table) == 8

    def test_moment_increase_with_load(self):
        """Test that moment resistance increases with applied moment."""
        xloc = [0, 2, 0, 2]
        yloc = [0, 0, 2, 2]
        IC = [1, 1]
        
        _, _, Mi1, _ = ic.ic_brandt(IC, xloc, yloc, 50)
        _, _, Mi2, _ = ic.ic_brandt(IC, xloc, yloc, 100)
        
        # Moment resistance should scale with applied moment
        assert Mi2 > Mi1


class TestBrandtMethod:
    """Tests for brandt function - full iterative solution."""

    def test_simple_two_bolt_group(self):
        """Test simple two-bolt group convergence."""
        xloc = [0, 3]
        yloc = [0, 0]
        P_xloc = 0
        P_yloc = 0
        P_angle = 0
        
        output, IC, Cu = ic.brandt(xloc, yloc, P_xloc, P_yloc, P_angle)
        
        # Should converge
        assert IC is not None
        assert len(IC) == 2
        assert Cu > 0

    def test_four_bolt_square_convergence(self):
        """Test 4x1 bolt group under eccentric load."""
        xloc = [0, 3, 6, 9]
        yloc = [0, 0, 0, 0]
        P_xloc = 4.5  # Load at center
        P_yloc = 1    # Off-center eccentricity
        P_angle = 0   # Vertical load
        
        output, IC, Cu = ic.brandt(xloc, yloc, P_xloc, P_yloc, P_angle)
        
        # Should converge to solution
        assert Cu > 0
        assert IC is not None
        
        # Last output should have solution status
        last_output = output[-6]  # Solution line is near end
        assert 'yes' in last_output or 'no' in last_output

    def test_angled_load(self):
        """Test with angled load application."""
        xloc = [-1, 1, -1, 1]
        yloc = [-1, -1, 1, 1]
        P_xloc = 0
        P_yloc = 0
        P_angle = 45  # 45 degree load
        
        output, IC, Cu = ic.brandt(xloc, yloc, P_xloc, P_yloc, P_angle)
        
        assert Cu > 0
        assert IC is not None
        # IC should exist
        assert len(IC) == 2

    def test_eccentric_load_moves_ic(self):
        """Test that eccentric load moves IC from bolt group centroid."""
        xloc = [-1, 1, -1, 1]
        yloc = [-1, -1, 1, 1]
        
        # No eccentricity
        _, IC1, _ = ic.brandt(xloc, yloc, 0, 0, 0)
        
        # With eccentricity
        _, IC2, _ = ic.brandt(xloc, yloc, 2, 0, 0)
        
        # IC should move with eccentricity
        assert IC1 != IC2

    def test_output_structure(self):
        """Test that output contains all required information."""
        xloc = [0, 1, 0, 1]
        yloc = [0, 0, 1, 1]
        
        output, IC, Cu = ic.brandt(xloc, yloc, 0.5, 0.5, 30)
        
        # Verify output structure
        assert isinstance(output, list)
        assert len(output) > 0
        
        # Should contain anchor group center
        cg_entry = [o for o in output if isinstance(o, list) and 
                   len(o) > 0 and o[0] == "Anchor Group C.G."]
        assert len(cg_entry) == 1

    def test_tolerance_convergence(self):
        """Test custom tolerance parameter."""
        xloc = [-1, 1, -1, 1]
        yloc = [-1, -1, 1, 1]
        
        # Tight tolerance
        _, _, Cu1 = ic.brandt(xloc, yloc, 0, 0, 0, tol=1e-10)
        
        # Loose tolerance
        _, _, Cu2 = ic.brandt(xloc, yloc, 0, 0, 0, tol=0.01)
        
        # Both should converge to valid Cu values
        assert Cu1 > 0
        assert Cu2 > 0

    def test_multiple_bolt_counts(self):
        """Test with different numbers of bolts."""
        # 2 bolts
        xloc2 = [0, 2]
        yloc2 = [0, 0]
        _, IC2, Cu2 = ic.brandt(xloc2, yloc2, 0, 0, 0)
        assert Cu2 > 0
        
        # 8 bolts
        xloc8 = [-1, 1, -1, 1, -1, 1, -1, 1]
        yloc8 = [-1, -1, 0, 0, 1, 1, 0.5, -0.5]
        _, IC8, Cu8 = ic.brandt(xloc8, yloc8, 0, 0, 0)
        assert Cu8 > 0


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_negative_coordinates(self):
        """Test with negative bolt coordinates."""
        xloc = [-2, -2, 2, 2]
        yloc = [-2, 2, -2, 2]
        cg = ic.bolt_group_center(xloc, yloc)
        assert cg == [0, 0]

    def test_very_large_distances(self):
        """Test with very large spacing distances."""
        xloc = [0, 1000, 0, 1000]
        yloc = [0, 0, 1000, 1000]
        cg = ic.bolt_group_center(xloc, yloc)
        assert abs(cg[0] - 500) < 1e-6
        assert abs(cg[1] - 500) < 1e-6

    def test_very_small_distances(self):
        """Test with very small spacing distances."""
        xloc = [0, 0.001, 0, 0.001]
        yloc = [0, 0, 0.001, 0.001]
        cg = ic.bolt_group_center(xloc, yloc)
        assert abs(cg[0] - 0.0005) < 1e-8
        assert abs(cg[1] - 0.0005) < 1e-8

    def test_high_moment_loading(self):
        """Test with very high moment (stress-tests math)."""
        xloc = [-1, 1, -1, 1]
        yloc = [-1, -1, 1, 1]
        IC = [0, 0]
        Mp = 1e6  # Very large moment
        
        Rx, Ry, Mi, table = ic.ic_brandt(IC, xloc, yloc, Mp)
        # Should handle large numbers gracefully
        assert abs(Rx) < 1e10  # Results should be reasonable
        assert abs(Ry) < 1e10

    def test_load_angle_wraparound(self):
        """Test load angles near 0, 90, 180, 270, 360 degrees."""
        xloc = [0, 2, 0, 2]
        yloc = [0, 0, 2, 2]
        
        for angle in [0, 90, 180, 270, 360]:
            _, IC, Cu = ic.brandt(xloc, yloc, 1, 1, angle)
            assert Cu > 0
            assert IC is not None


class TestPhysicalValidity:
    """Tests that results are physically reasonable."""

    def test_cu_greater_than_zero(self):
        """Cu (capacity utilization factor) should always be positive."""
        xloc = [-1, 1, -1, 1]
        yloc = [-1, -1, 1, 1]
        
        for angle in range(0, 360, 45):
            for eccentricity in [0, 0.5, 1]:
                _, _, Cu = ic.brandt(xloc, yloc, eccentricity, 0, angle)
                assert Cu > 0, f"Cu should be positive for angle={angle}, ecc={eccentricity}"

    def test_centroid_within_bolt_bounds(self):
        """Centroid should be within the bounds of all bolts."""
        xloc = [0, 3, 6]
        yloc = [1, 2, 1.5]
        
        cg = ic.bolt_group_center(xloc, yloc)
        assert min(xloc) <= cg[0] <= max(xloc)
        assert min(yloc) <= cg[1] <= max(yloc)

    def test_symmetric_group_symmetric_ic(self):
        """Symmetric bolt group should have symmetric IC under centered load."""
        xloc = [-2, 2, -2, 2]
        yloc = [-2, -2, 2, 2]
        
        _, IC, _ = ic.brandt(xloc, yloc, 0, 0, 0)
        
        # IC should be at or near centroid for centered load
        cg = ic.bolt_group_center(xloc, yloc)
        distance = m.sqrt((IC[0] - cg[0])**2 + (IC[1] - cg[1])**2)
        assert distance < 0.5  # Should be fairly close for symmetric case
