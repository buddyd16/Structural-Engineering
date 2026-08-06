# Structural Engineering Test Suite

Comprehensive test coverage for critical business logic in the Structural Engineering analysis tools. This test suite prioritizes core calculation functions, data mutation paths, and physical validity checks.

## Test Coverage Overview

### 1. **Steel Connection Design** (`test_bolt_group.py`)
Tests for the Brandt instantaneous center method used in bolt group design - critical for connection capacity calculations.

**Files Tested:**
- `Steel/bolt_group_istantaneous_center.py`

**Test Classes (7 major groups, 40+ individual tests):**

#### `TestBuildBoltGroup` - Bolt Grid Generation
- Single and multi-row/column configurations
- Various spacing patterns (2x1, 3x1, 4x4, 2x3, etc.)
- Edge cases: zero spacing, large spacing, degenerate cases
- **Critical Path:** Data structure generation for analysis inputs

#### `TestBoltGroupCenter` - Centroid Calculation
- 2-bolt through 5-bolt configurations
- Symmetric and asymmetric arrangements
- Physical validity: centroid within bounds
- **Critical Path:** Geometric center calculation affecting load distribution

#### `TestIcBrandt` - Instantaneous Center Method
- Pure shear conditions (zero moment)
- Moment-induced bolt forces
- Degenerate case handling (bolt at IC)
- Moment resistance scaling
- **Critical Path:** Core iterative calculation for bolt capacity

#### `TestBrandtMethod` - Full Iterative Solution
- Convergence behavior
- Eccentric load handling
- Angled load application (0°-360°)
- Utilization factor (Cu) calculation
- Output structure validation
- **Critical Path:** Complete connection design calculation

#### `TestEdgeCases` - Boundary Conditions
- Negative coordinates
- Very large/small distances
- High moment loading
- Load angle wraparound

#### `TestPhysicalValidity` - Physical Requirements
- Cu (capacity) always positive
- IC location within bolt group bounds
- Symmetric responses for symmetric loading

---

### 2. **Beam Analysis** (`test_beam_equations.py`)
Tests for pin-pin beam equation classes - fundamental for all structural analysis.

**Files Tested:**
- `Analysis/pin_pin_beam_equations_classes.py`

**Test Classes (9 major groups, 50+ individual tests):**

#### `TestPolyEval` - Polynomial Evaluation
- Zero, linear, quadratic, cubic polynomials
- Negative coefficients
- Large and negative x values
- **Critical Path:** Core math utility used throughout analysis

#### `TestNoLoad` - Baseline (No Loading)
- Initialization and case designation
- Zero outputs for all analysis functions
- Piece function generation for zero state
- **Critical Path:** Reference case for comparisons

#### `TestPointLoad` - Single Concentrated Load
- Reaction calculations (RL, RR)
- Equilibrium verification
- Shear force distribution
- Bending moment distribution
- Deflection (EI*delta) calculations
- Slope (EI*slope) continuity
- Loads at support, midspan, off-center
- **Critical Path:** Primary load case used in design

#### `TestPieceFunctionString` - Function String Generation
- Zero, constant, linear, polynomial expressions
- Multi-piece functions
- HTML table formatting
- **Critical Path:** Output formatting for results

#### `TestFixedEndForces` - FEF Calculations
- No load case (all zero)
- Point load FEF generation
- **Critical Path:** Complex load method fundamentals

#### `TestLoadCombinations` - Multiple Loads
- Two equal loads
- Unsymmetric loading
- Reaction summation
- **Critical Path:** Combined loading scenarios

#### `TestPhysicalValidity` - Physical Requirements
- Moment maximum between supports
- Symmetric deflection for symmetric loading
- Reaction equilibrium
- Moment equilibrium at any point
- **Critical Path:** Validates results are physically sound

---

### 3. **Wood Design** (`test_wood_wall.py`)
Tests for wood stud wall calculations - critical for load-bearing design and factor applications.

**Files Tested:**
- `Wood/wood_classes.py` (wood_stud_wall class)

**Test Classes (6 major groups, 60+ individual tests):**

#### `TestWoodStudWallInitialization` - Setup & Properties
- Default and custom initialization
- Height adjustment for plates
- Section property calculations (Area, I, S)
- Repetitive member factor (Cr) by spacing
- Size factor (Cf) by grade and depth
- Wet service factor (Cm) application
- Temperature factor (Ct) variations
- Incising factor (Ci)
- Bearing area factor (Cb)
- Deflection limit calculations (L/180, L/240, L/360)
- Adjusted property calculations (with all factors)
- **Critical Path:** Complex initialization with 15+ design factors

#### `TestWoodStudWallDesignFactors` - Factor Validation
- All factors positive
- Most factors not exceeding 1.0
- Cr factor validity (1.0 or 1.15)
- Beam stability factor (sheathed vs unsheathed)
- **Critical Path:** Ensures factor correctness

#### `TestWoodStudWallDeflectionCapacity` - Deflection Analysis
- Deflection capacity calculation
- Ordering verification (L/180 < L/240 < L/360)
- Effect of modulus on capacity
- **Critical Path:** Serviceability limit state

#### `TestWoodStudWallEdgeCases` - Boundary Conditions
- Minimum dimensions
- Large dimensions
- Various lumber grades
- Southern Pine variations
- Extreme temperatures
- Custom c_frt factor arrays
- Blocking specifications
- **Critical Path:** Robustness across design space

#### `TestWoodStudWallPhysicalValidity` - Physical Requirements
- All properties positive
- Adjusted values ≤ base values
- I increases with depth
- Section modulus relationship (S = I/(d/2))
- **Critical Path:** Material property validation

#### `TestWoodStudWallAssumptions` - Documentation
- Assumption notes tracking
- Warning log creation
- Temperature warning triggers
- Design method documentation
- **Critical Path:** Audit trail for design decisions

---

## Running the Tests

### Prerequisites
```bash
# Install pytest
pip install pytest pytest-cov

# Optional: install coverage tools
pip install coverage pytest-html
```

### Basic Test Execution
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_bolt_group.py

# Run specific test class
pytest tests/test_bolt_group.py::TestBuildBoltGroup

# Run specific test
pytest tests/test_bolt_group.py::TestBuildBoltGroup::test_4x4_bolt_grid

# Run with verbose output
pytest tests/ -v

# Run with short traceback
pytest tests/ --tb=short
```

### Coverage Analysis
```bash
# Generate coverage report
pytest tests/ --cov=Analysis --cov=Steel --cov=Wood --cov-report=html

# Show coverage in terminal
pytest tests/ --cov=Analysis --cov=Steel --cov=Wood --cov-report=term-missing
```

### Fixture and Tolerance Information
The test suite uses standard fixtures from `conftest.py`:
- `float_tol` - Float comparison tolerance (1e-6)
- `eng_tol` - Engineering calculation tolerance (0.001 = 0.1%)
- Helper functions: `approx_equal()`, `approx_list_equal()`

---

## Test Organization

```
tests/
├── __init__.py              # Package marker
├── conftest.py              # Pytest configuration and shared fixtures
├── test_bolt_group.py       # Steel connection tests (40+ tests)
├── test_beam_equations.py   # Structural analysis tests (50+ tests)
└── test_wood_wall.py        # Wood design tests (60+ tests)
```

---

## Coverage Summary

| Module | File | Tests | Coverage Type |
|--------|------|-------|---------------|
| Steel | `bolt_group_istantaneous_center.py` | 40+ | Unit + Integration |
| Analysis | `pin_pin_beam_equations_classes.py` | 50+ | Unit + Physical |
| Wood | `wood_classes.py` (wood_stud_wall) | 60+ | Unit + Factor |

**Total Test Count:** 150+ individual test functions across 150+ assertions

---

## Test Strategy

### 1. **Unit Testing**
Each function/method tested individually with:
- Boundary value inputs
- Typical use cases
- Edge cases and degenerate conditions
- Error conditions

### 2. **Physical Validity Testing**
Ensures results satisfy engineering requirements:
- Load equilibrium (ΣF = 0, ΣM = 0)
- Positive capacities and properties
- Reasonable output magnitudes
- Symmetric responses for symmetric loading

### 3. **Data Mutation Testing**
Validates correct calculation of adjusted values:
- Factor applications and combinations
- Property modifications
- State changes through initialization

### 4. **Integration Testing**
Tests interactions between related functions:
- Load combinations
- Bolt group analysis with multiple load angles
- Factor cascading in design calculations

---

## Critical Code Paths Tested

### Business Logic (No GUI Dependencies)
✅ Polynomial evaluation and piecewise functions  
✅ Bolt group geometry and capacity calculations  
✅ Beam reaction and moment distributions  
✅ Wood stud design factor calculations (15+ factors)  
✅ Deflection limit analysis  
✅ Load equilibrium verification  

### Data Mutation Paths
✅ Complex initialization sequences  
✅ Factor cascading and combinations  
✅ Unit conversions and scaling  
✅ Piecewise function generation  

### Authentication & Authorization
⚠️ Not applicable (structural analysis library)

---

## Known Limitations

1. **GUI Tests**: This suite focuses on business logic. GUI tests (Tkinter) would require separate framework.
2. **Integration Tests with Files**: File I/O testing would require fixture setup with temporary files.
3. **Performance Tests**: Not included; structural analyses are typically fast enough.
4. **Python 2 Compatibility**: Tests written for Python 3; some source files have `from __future__ import division`.

---

## Adding New Tests

When adding tests for new code:

1. **Follow naming convention**: `test_<module>.py` with `Test<Feature>` classes
2. **Use conftest fixtures**: Leverage `float_tol` and `eng_tol`
3. **Test edge cases**: Zero, negative, very large, boundary values
4. **Verify physical validity**: Ensure results make engineering sense
5. **Document assumptions**: Explain what each test validates
6. **Group logically**: Use test classes to organize related tests

Example template:
```python
class TestNewFeature:
    """Tests for [feature description] - [critical path description]."""

    def test_basic_case(self):
        """Test basic/typical usage."""
        # Setup
        # Execute
        # Assert
        pass

    def test_edge_case(self):
        """Test boundary condition."""
        pass

    def test_physical_validity(self):
        """Test that results satisfy engineering requirements."""
        pass
```

---

## Maintenance Notes

- **Last Updated**: 2024
- **Test Framework**: pytest
- **Python Version**: 3.6+
- **Dependencies**: 
  - numpy (for beam calculations)
  - pytest (for testing)
  - pytest-cov (optional, for coverage reports)

---

## References

### Design Standards Referenced in Tests
- **NDS 2005**: National Design Specification for Wood Construction
  - Load factors, adjustment factors
  - Deflection limits
  - Material properties

- **AISC**: American Institute of Steel Construction
  - Bolt group analysis (Brandt's method)
  - Connection design principles

- **Structural Analysis Theory**
  - Pin-pin beam equations
  - Load equilibrium and compatibility

---

## Questions & Issues

For questions about specific tests or to report issues:
1. Check the test class docstring for purpose
2. Review test method comments for specific assertions
3. Refer to structural engineering references cited above
4. Check pytest output for specific failure messages
