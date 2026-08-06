"""
Pytest configuration and shared fixtures for structural engineering tests.
"""
import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'Analysis'))
sys.path.insert(0, str(project_root / 'Steel'))
sys.path.insert(0, str(project_root / 'Wood'))

import pytest

# Common test tolerances
FLOAT_TOLERANCE = 1e-6
ENGINEERING_TOLERANCE = 0.001  # 0.1% tolerance for engineering calcs


@pytest.fixture
def float_tol():
    """Standard floating point tolerance for comparisons."""
    return FLOAT_TOLERANCE


@pytest.fixture
def eng_tol():
    """Engineering tolerance for structural calculations."""
    return ENGINEERING_TOLERANCE


def approx_equal(a, b, tol=FLOAT_TOLERANCE):
    """Helper function for approximate equality checks."""
    return abs(a - b) < tol


def approx_list_equal(list1, list2, tol=FLOAT_TOLERANCE):
    """Helper function for comparing lists of floats."""
    if len(list1) != len(list2):
        return False
    return all(approx_equal(a, b, tol) for a, b in zip(list1, list2))
