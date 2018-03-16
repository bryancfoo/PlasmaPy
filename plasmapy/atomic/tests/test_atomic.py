import pytest
import numpy as np
from astropy import units as u, constants as const

from ..symbols import (
    atomic_symbol,
    isotope_symbol,
    element_name,
)

from ..isotopes import _Isotopes

from ..atomic import (
    atomic_number,
    mass_number,
    standard_atomic_weight,
    isotope_mass,
    ion_mass,
    particle_mass,
    is_stable,
    half_life,
    known_isotopes,
    common_isotopes,
    stable_isotopes,
    isotopic_abundance,
    integer_charge,
    electric_charge,
    periodic_table_period,
    periodic_table_block,
    periodic_table_category,
    periodic_table_group,
)

from ..nuclear import (
    nuclear_binding_energy,
    nuclear_reaction_energy,
)

from ...utils import (
    run_test,
    AtomicWarning,
    InvalidElementError,
    InvalidIsotopeError,
    InvalidIonError,
    ChargeError,
    AtomicError,
    MissingAtomicDataError,
    InvalidParticleError,
)

# function to be tested, argument(s), expected result/outcome

# The following lists (with the name of a function

atomic_symbol_table = [
    [1, 'H'],
    [1, 'H'],
    ['H', 'H'],
    ['p', 'H'],
    ['T', 'H'],
    ['deuterium', 'H'],
    ['deuteron', 'H'],
    ['Tritium', 'H'],
    ['triton', 'H'],
    ['H-2', 'H'],
    ['D', 'H'],
    ['T', 'H'],
    ['H-3', 'H'],
    ['Hydrogen-3', 'H'],
    ['helium', 'He'],
    [2, 'He'],
    ['alpha', 'He'],
    ['gold', 'Au'],
    ['Gold', 'Au'],
    [79, 'Au'],
    ['79', 'Au'],
    ['P', 'P'],
    [118, 'Og'],
    ['N-14', 'N'],
    ['N', 'N'],
    ['H +1', 'H'],
    ['H 1+', 'H'],
    ['hydrogen 1+', 'H'],
    ['deuterium 1+', 'H'],
    ['Fe 24+', 'Fe'],
    ['Fe +24', 'Fe'],
    ['Fe 2-', 'Fe'],
    ['Fe -2', 'Fe'],
    ['Fe+', 'Fe'],
    ['Fe++', 'Fe'],
    ['Fe-', 'Fe'],
    ['Fe++++++++++++++', 'Fe'],
    ['H-0', InvalidParticleError],
    [3.14159, TypeError],
    ['Og-294b', InvalidParticleError],
    ['H-934361079326356530741942970523610389', InvalidParticleError],
    ['Fe 2+4', InvalidParticleError],
    ['Fe+24', InvalidParticleError],
    ['Fe +59', InvalidParticleError],
    ['C++++++++++++++++', InvalidParticleError],
    ['C-++++', InvalidParticleError],
    ['neutron', InvalidElementError],
    ['n', InvalidElementError],
    ['n-1', InvalidElementError],
    ['h', InvalidParticleError],
    ['d', InvalidParticleError],
    ['he', InvalidParticleError],
    ['au', InvalidParticleError],
    ['p-', InvalidElementError],
    [0, InvalidParticleError],
    [119, InvalidParticleError],
    ['antiproton', InvalidElementError],
]

isotope_symbol_table = [
    [('He', 4), 'He-4'],
    [('helium-4',), 'He-4'],
    [('H-2',), 'D'],
    [('Deuterium',), 'D'],
    [('deuterium',), 'D'],
    [('deuteron',), 'D'],
    [('tritium',), 'T'],
    [('triton',), 'T'],
    [('Hydrogen-3',), 'T'],
    [('hydrogen-3',), 'T'],
    [('H-3',), 'T'],
    [(1, 2), 'D'],
    [('Hydrogen', 3), 'T'],
    [('tritium',), 'T'],
    [('H', 2), 'D'],
    [('Alpha',), 'He-4'],
    [('alpha',), 'He-4'],
    [(79, 197), 'Au-197'],
    [('p',), 'H-1'],
    [('beryllium-8',), 'Be-8'],
    [('N-13',), 'N-13'],
    [('p',), 'H-1'],
    [('proton',), 'H-1'],
    [('protium',), 'H-1'],
    [('N-13 2+',), 'N-13'],
    [('Hydrogen-3 +1',), 'T'],
    ['Md-260', {"mass_numb": 261}, InvalidParticleError],
    ['protium', {"mass_numb": 2}, InvalidParticleError],
    ['alpha', {"mass_numb": 3}, InvalidParticleError],
    ['O-18', {"mass_numb": 19}, InvalidParticleError],
    ['lead-209', {"mass_numb": 511}, InvalidParticleError],
    ['He-1', {}, InvalidParticleError],
    [24, {"mass_numb": 23}, InvalidParticleError],
    ['H', {"mass_numb": 0}, InvalidParticleError],
    ['H-1', {"mass_numb": 2}, InvalidParticleError],
    ['P', {}, InvalidIsotopeError],
    [1, {}, InvalidIsotopeError],
    [4, {}, InvalidIsotopeError],
    ['hydrogen-444444', {}, InvalidParticleError],
    ['Fe', {"mass_numb": 2.1}, TypeError],
    ['He', {"mass_numb": 'c'}, TypeError],
    ['He-3', {"mass_numb": 4}, InvalidParticleError],
    ['D', {"mass_numb": 3}, InvalidParticleError],
    ['T', {"mass_numb": 2}, InvalidParticleError],
    ['Fe', {"mass_numb": None}, InvalidIsotopeError],
    ['He', {"mass_numb": 99}, InvalidParticleError],
    ['d', {}, InvalidParticleError],
    ['h-3', {}, InvalidParticleError],
    ['h', {}, InvalidParticleError],
    ['d+', {}, InvalidParticleError],
    ['H-1', {"mass_numb": 1}, AtomicWarning],
    ['H-2', {"mass_numb": 2}, AtomicWarning],
    ['T', {"mass_numb": 3}, AtomicWarning],
    ['Li-6', {"mass_numb": 6}, AtomicWarning],
    ['lithium-6', {"mass_numb": 6}, AtomicWarning],
    ['alpha', {"mass_numb": 4}, AtomicWarning],
    ['p', {"mass_numb": 1}, AtomicWarning],
]

atomic_number_table = [
    ['H', 1],
    ['D', 1],
    ['deuterium', 1],
    ['Deuterium', 1],
    ['tritium', 1],
    ['p', 1],
    ['P', 15],
    ['Alpha', 2],
    ['C-12', 6],
    ['Argon', 18],
    ['protium', 1],
    ['H-3', 1],
    ['p+', 1],
    ['Be-8', 4],
    ['N', 7],
    ['N 2+', 7],
    ['N +1', 7],
    ['N+++', 7],
    ['H-3934', InvalidParticleError],
    ['C-12b', InvalidParticleError],
    [-1.5, TypeError],
    ['n', InvalidElementError],
    ['n-1', InvalidElementError],
    ['neutron', InvalidElementError],
    ['Neutron', InvalidElementError],
    ['d', InvalidParticleError],
    ['t', InvalidParticleError],
    ['s-36', InvalidParticleError],
]

mass_number_table = [
    ['helium-3', 3],
    ['Au-197', 197],
    ['deuterium', 2],
    ['D', 2],
    ['H-2', 2],
    ['tritium', 3],
    ['T', 3],
    ['alpha', 4],
    ['p', 1],
    ['Be-8', 8],
    ['N-13', 13],
    ['N-13 2+', 13],
    ['N-13 +2', 13],
    ['N-13+++', 13],
    ['H-359', InvalidParticleError],
    ['C-12b', InvalidParticleError],
    [-1.5, TypeError],
    ['N-13+-+-', InvalidParticleError],
    ['h-3', InvalidParticleError],
    ['n', InvalidIsotopeError],
    ['n-1', InvalidIsotopeError],
]


element_name_table = [
    ['D', 'hydrogen'],
    ['deuterium', 'hydrogen'],
    ['Au', 'gold'],
    ['alpha', 'helium'],
    ['helium-4', 'helium'],
    ['H-2', 'hydrogen'],
    ['Deuterium', 'hydrogen'],
    ['Hydrogen-3', 'hydrogen'],
    ['hydrogen-3', 'hydrogen'],
    ['H-3', 'hydrogen'],
    ['tritium', 'hydrogen'],
    ['Alpha', 'helium'],
    ['alpha', 'helium'],
    [1, 'hydrogen'],
    [26, 'iron'],
    [79, 'gold'],
    ['p', 'hydrogen'],
    ['P', 'phosphorus'],
    ['Be-8', 'beryllium'],
    ['Li-7', 'lithium'],
    ['N', 'nitrogen'],
    ['N+++', 'nitrogen'],
    ['D-', 'hydrogen'],
    ['vegancupcakes', InvalidParticleError],
    ['C-+-', InvalidParticleError],
    [1.24, TypeError],
    ['n', InvalidElementError],
    ['neutron', InvalidElementError],
    [0, InvalidParticleError],
    ['H++', InvalidParticleError],
    ['t', InvalidParticleError],
    ['pb', InvalidParticleError],
    ['d', InvalidParticleError],
    ['h-3', InvalidParticleError],
    ['Pb-9', InvalidParticleError],
    ['H 2+', InvalidParticleError],
]

standard_atomic_weight_table = [
    ['H', (1.008 * u.u).to(u.kg)],
    [1, (1.008 * u.u).to(u.kg)],
    ['Hydrogen', (1.008 * u.u).to(u.kg)],
    ['Au', u.kg],
    ['H-1', AtomicError],
    ["help i'm trapped in a unit test", InvalidParticleError],
    [1.1, TypeError],
    ['n', InvalidElementError],
    ['p', AtomicError],
    ['alpha', AtomicError],
    ['deuteron', AtomicError],
    ['tritium', AtomicError],
    ['Au+', AtomicError],
    ['Fe -2', AtomicError],
    ['Og 2+', AtomicError],
    ['h', InvalidParticleError],
    ['fe', InvalidParticleError],
]

isotope_mass_table = [
    [('H-1',), isotope_mass('protium')],
    [('H-1',), isotope_mass(1, 1)],
    [('D',), isotope_mass('H-2')],
    [('H-2',), isotope_mass('deuterium',)],
    [('deuterium',), isotope_mass(1, 2)],
    [('T',), isotope_mass('H-3',)],
    [('H-3',), isotope_mass('tritium',)],
    [('tritium',), isotope_mass(1, 3)],
    ["H", InvalidIsotopeError],
    [1.1, TypeError],
    ['alpha', AtomicError],
    ['He-4 2+', AtomicError],
    ['he-4', InvalidParticleError],
    ['Fe 2+', InvalidIsotopeError],
    ['Fe -2', InvalidIsotopeError],
    ['deuteron', AtomicError],
    ['triton', AtomicError],
    ['H-1 +1', AtomicError],
    ['H-1+', AtomicError],
    ['Si-30', u.kg],
]

ion_mass_table = [
    ['proton', const.m_p],
    ['H-1+', const.m_p],
    ['H-1 +1', const.m_p],
    ['H-1 1+', const.m_p],
    ['H-1', {'Z': 1}, const.m_p],
    ['hydrogen-1', {'Z': 1}, const.m_p],
    ['p+', const.m_p],
    ['F-19', {'Z': 3}, u.kg],
    ['Og 1+', {}, MissingAtomicDataError],
    ['Fe-56', {"Z": 1.4}, TypeError],
    ['n', {}, InvalidIonError],
    ['H-1 +1', {"Z": 0}, InvalidParticleError],
    [26, {"Z": 1, "mass_numb": 'a'}, TypeError],
    [26, {"Z": 27, "mass_numb": 56}, InvalidParticleError],
    ['Og', {"Z": 1}, MissingAtomicDataError],
    ['Og', {"mass_numb": 696, "Z": 1}, InvalidParticleError],
    ['He 1+', {"mass_numb": 99}, InvalidParticleError],
    ['fe-56 1+', {}, InvalidParticleError],
    ['H-1', {'mass_numb': 1, 'Z': 1}, AtomicWarning],
]

particle_mass_table = [
    ['p+', ion_mass('p+')],
    ['H', standard_atomic_weight('H')],
    ['D', isotope_mass('D')],
]

is_stable_table = [
    ['H-1', True],
    [(1, 1), True],
    ['N-14', True],
    [('N', 14), True],
    ['P-31', True],
    [('P', 31), True],
    ['p', True],
    ['alpha', True],
    ['Xe-124', True],
    ['Fe', {'mass_numb': 56}, True],
    ['Fe-56', True],
    ['iron-56', True],
    ['Iron-56', True],
    [(26, 56), True],
    ['Be-8', False],
    ['U-235', False],
    ['uranium-235', False],
    ['T', False],
    [(4, 8), False],
    ['tritium', False],
    ['Pb-209', False],
    ['lead-209', False],
    ['Lead-209', False],
    ['Pb', {'mass_numb': 209}, False],
    [(82, 209), False],
    [('hydrogen-444444',), InvalidParticleError],
    [('hydrogen', 0), InvalidParticleError],
    [('',), InvalidParticleError],
    [('pb-209',), InvalidParticleError],
    [('h',), InvalidParticleError],
]

integer_charge_table = [
    ['H+', 1],
    ['D +1', 1],
    ['tritium 1+', 1],
    ['H-', -1],
    ['Fe -2', -2],
    ['Fe 2-', -2],
    ['N--', -2],
    ['N++', 2],
    ['alpha', 2],
    ['proton', 1],
    ['deuteron', 1],
    ['triton', 1],
    ['electron', -1],
    ['e-', -1],
    ['e+', 1],
    ['positron', 1],
    ['n', 0],
    ['neutron', 0],
    ['p-', -1],
    ['antiproton', -1],
    ['fads', InvalidParticleError],
    ['H++', InvalidParticleError],
    ['h+', InvalidParticleError],
    ['fe 1+', InvalidParticleError],
    ['d+', InvalidParticleError],
    ['Fe 29+', InvalidParticleError],
    ['H-1', ChargeError],
    ['H---', AtomicWarning],
    ['Fe -26', AtomicWarning],
    ['Og 10-', AtomicWarning],
]

electric_charge_table = [
    ['p', u.C],
    ['p', 1.6021766208e-19 * u.C],
    ['e', -1.6021766208e-19 * u.C],
    ['alpha', 3.2043532416e-19 * u.C],
    ['n', 0 * u.C],
    ['badinput', InvalidParticleError],
    ['h+', InvalidParticleError],
    ['Au 81+', InvalidParticleError],
    ['Au 81-', AtomicWarning],
    ['H---', AtomicWarning],
]

# The tables above do not include the function to be tested in order to
# avoid cluttering up the code.  The following block of code prepends
# the correct function to each list containing args, kwargs, and the
# expected outcome prior to being passed through to run_test.

tables_and_functions = [
    (atomic_symbol, atomic_symbol_table),
    (isotope_symbol, isotope_symbol_table),
    (atomic_number, atomic_number_table),
    (mass_number, mass_number_table),
    (element_name, element_name_table),
    (standard_atomic_weight, standard_atomic_weight_table),
    (isotope_mass, isotope_mass_table),
    (ion_mass, ion_mass_table),
    (is_stable, is_stable_table),
    (particle_mass, particle_mass_table),
    (integer_charge, integer_charge_table),
    (electric_charge, electric_charge_table),
]

all_tests = []

for func, table in tables_and_functions:
    for inputs in table:
        inputs.insert(0, func)
        if len(inputs) == 3:
            inputs.insert(2, {})
    all_tests += table


atomic_TypeError_funcs_table = [
    atomic_symbol,
    isotope_symbol,
    atomic_number,
    is_stable,
    half_life,
    mass_number,
    element_name,
    standard_atomic_weight,
    isotope_mass,
    ion_mass,
    nuclear_binding_energy,
    nuclear_reaction_energy
]

atomic_TypeError_badargs = [1.1, {'cats': 'bats'}, 1 + 1j]

atomic_ParticleErrors_funcs_table = [
    atomic_symbol,
    isotope_symbol,
    atomic_number,
    is_stable,
    half_life,
    mass_number,
    element_name,
    standard_atomic_weight,
    isotope_mass,
    ion_mass,
    particle_mass,
    known_isotopes,
    stable_isotopes,
    common_isotopes,
    isotopic_abundance,
    integer_charge,
    electric_charge,
]

atomic_ParticleError_badargs = [
    -1,
    119,
    'grumblemuffins',
    'H-0',
    'Og-294b',
    'H-9343610',
    'Fe 2+4',
    'Fe+24',
    'Fe +59',
    'C++++++++++++++++',
    'C-++++',
    'h',
    'd',
    'he',
    'au',
    'alpha 1+',
    'alpha-4',
]

metatable = [
    (atomic_TypeError_funcs_table, atomic_TypeError_badargs, TypeError),
    (atomic_ParticleErrors_funcs_table, atomic_ParticleError_badargs, InvalidParticleError),
]

for funcs, badargs, error in metatable:
    for func in funcs:
        for badarg in badargs:
            all_tests += [[func, badarg, error]]


@pytest.mark.parametrize('inputs', all_tests)
def test_atomic_functions(inputs):
    print(inputs)
    run_test(inputs)


# Next we have tests that do not fall nicely into equality comparisons.


def test_standard_atomic_weight_value_between():
    """Test that `standard_atomic_weight` returns approximately the
    correct value for phosphorus."""
    assert 30.973 < standard_atomic_weight('P').to(u.u).value < 30.974, \
        "Incorrect standard atomic weight for phosphorus."


def test_isotope_mass_berkelium_249():
    """Test that `isotope_mass` returns the correct value for Bk-249."""
    assert np.isclose(isotope_mass('berkelium-249').to(u.u).value, 249.0749877), \
        "Incorrect isotope mass for berkelium."


def test_ion_mass_for_hydrogen_with_no_mass_number():
    """Test that `ion_mass` does not return the proton mass when no
    mass number is specified for hydrogen.  In this case, the
    standard atomic weight should be used to account for the small
    fraction of deuterium."""
    assert ion_mass('H', Z=1) > const.m_p
    assert ion_mass('hydrogen', Z=1) > const.m_p


def test_ion_mass_helium():
    """Test miscellaneous cases for `ion_mass`."""
    assert ion_mass('alpha') > ion_mass('He-3 2+')


# (arg1, kwargs1, arg2, kwargs2, expected)
equivalent_ion_mass_args = [
    ['e+', {}, 'positron', {}, const.m_e],
    ['alpha', {}, 'He-4++', {}, None],
    ['alpha', {}, 'helium-4 2+', {}, None],
    ['deuteron', {}, 'H', {'Z': 1, 'mass_numb': 2}, None],
    ['D+', {}, 'H-2+', {}, None],
    ['D+', {}, 'D 1+', {}, None],
    ['Deuterium+', {}, 'D', {'Z': 1}, None],
    ['triton', {}, 'H', {'Z': 1, 'mass_numb': 3}, None],
    ['T+', {}, 'H-3+', {}, None],
    ['T+', {}, 'T 1+', {}, None],
    ['Tritium+', {}, 'T', {'Z': 1}, None],
    ['Fe-56 1+', {}, 'Fe', {'mass_numb': 56, 'Z': 1},
     ion_mass('Fe-56 1-') - 2 * const.m_e],
    ['Fe-56 +1', {}, 26, {'mass_numb': 56, 'Z': 1}, None],
]


@pytest.mark.parametrize(
    "arg1, kwargs1, arg2, kwargs2, expected", equivalent_ion_mass_args)
def test_ion_mass_equivalent_args(arg1, kwargs1, arg2, kwargs2, expected):
    """Test that `ion_mass` returns equivalent results for equivalent
    positional and keyword arguments."""

    result1 = ion_mass(arg1, **kwargs1)
    result2 = ion_mass(arg2, **kwargs2)

    assert result1 == result2, \
        (f"ion_mass({repr(arg1)}, **{kwargs1}) = {repr(result1)}, whereas "
         f"ion_mass({repr(arg2)}, **{kwargs2}) = {repr(result2)}.  "
         f"These results are not equivalent as expected.")

    if expected is not None:
        assert result1 == result2 == expected, \
            (f"ion_mass({repr(arg1)}, **{kwargs1}) = {repr(result1)} and "
             f"ion_mass({repr(arg2)}, **{kwargs2}) = {repr(result2)}, but  "
             f"these results are not equal to {repr(expected)} as expected.")


def test_known_common_stable_isotopes():
    """Test that `known_isotopes`, `common_isotopes`, and
    `stable_isotopes` return the correct values for hydrogen."""

    known_should_be = ['H-1', 'D', 'T', 'H-4', 'H-5', 'H-6', 'H-7']
    common_should_be = ['H-1', 'D']
    stable_should_be = ['He-3', 'He-4']

    assert known_isotopes('H') == known_should_be, \
        (f"known_isotopes('H') should return {known_should_be}, but is "
         f"instead returning {known_isotopes('H')}")

    assert common_isotopes('H') == common_should_be, \
        (f"common_isotopes('H') should return {common_should_be}, but is "
         f"instead returning {common_isotopes('H')}")

    assert stable_isotopes('He') == stable_should_be, \
        (f"stable_isotopes('He') should return {stable_should_be}, but is "
         f"instead returning {stable_isotopes('He')}")


def test_half_life():
    """Test that `half_life` returns the correct values for various
    isotopes."""
    assert half_life('H-1') == np.inf * u.s, "Incorrect half-life for H-1'."
    assert np.isclose(half_life('tritium').to(u.s).value,
                      (12.32 * u.yr).to(u.s).value, rtol=2e-4), \
        "Incorrect half-life for tritium."
    assert half_life('H-1').unit == 's', "Incorrect unit for H-1."
    assert half_life('tritium').unit == 's', "Incorrect unit for tritium."


def test_half_life_unstable_isotopes():
    """Test that `half_life` returns `None` and raises an exception for
    all isotopes that do not yet have half-life data."""
    for isotope in _Isotopes.keys():
        if 'half_life' not in _Isotopes[isotope].keys() and \
                not _Isotopes[isotope].keys():
            with pytest.raises(MissingAtomicDataError):
                half_life(isotope)


def test_half_life_u_220():
    """Test that `half_life` returns `None` and issues a warning for an
    isotope without half-life data."""

    isotope_without_half_life_data = "No-248"

    with pytest.raises(MissingAtomicDataError, message=(
            f"This test assumes that {isotope_without_half_life_data} does "
            f"not have half-life data.  If half-life data is added for this "
            f"isotope, then a different isotope that does not have half-life "
            f"data should be chosen for this test.")):

        half_life(isotope_without_half_life_data)



def test_known_common_stable_isotopes_cases():
    """Test that known_isotopes, common_isotopes, and stable_isotopes
    return certain isotopes that fall into these categories."""
    assert 'H-1' in known_isotopes('H')
    assert 'D' in known_isotopes('H')
    assert 'T' in known_isotopes('H')
    assert 'Be-8' in known_isotopes('Be')
    assert 'Og-294' in known_isotopes(118)
    assert 'H-1' in common_isotopes('H')
    assert 'H-4' not in common_isotopes(1)
    assert 'H-1' in stable_isotopes('H')
    assert 'D' in stable_isotopes('H')
    assert 'T' not in stable_isotopes('H')
    assert 'Fe-56' in common_isotopes('Fe', most_common_only=True)
    assert 'He-4' in common_isotopes('He', most_common_only=True)


def test_known_common_stable_isotopes_len():
    """Test that `known_isotopes`, `common_isotopes`, and
    `stable_isotopes` each return a `list` of the expected length.

    The number of common isotopes may change if isotopic composition
    data has any significant changes.

    The number of stable isotopes may decrease slightly if some isotopes
    are discovered to be unstable but with extremely long half-lives.

    The number of known isotopes will increase as new isotopes are
    discovered, so a buffer is included in the test.

    """

    assert len(common_isotopes()) == 288, \
        ("The length of the list returned by common_isotopes() is "
         f"{len(common_isotopes())}, which is not the expected value.")

    assert len(stable_isotopes()) == 254, \
        ("The length of the list returned by stable_isotopes() is "
         f"{len(stable_isotopes())}, which is not the expected value.")

    assert 3352 <= len(known_isotopes()) <= 3400, \
        ("The length of the list returned by known_isotopes() is "
         f"{len(known_isotopes())}, which is not within the expected range.")


@pytest.mark.parametrize(
    "func", [common_isotopes, stable_isotopes, known_isotopes])
def test_known_common_stable_isotopes_error(func):
    """Test that `known_isotopes`, `common_isotopes`, and
    `stable_isotopes` raise an `~plasmapy.utils.InvalidElementError` for
    neutrons."""
    with pytest.raises(InvalidElementError, message=(
            f"{func} is not raising a ElementError for neutrons.")):
        func('n')


def test_isotopic_abundance():
    """Test that `isotopic_abundance` returns the appropriate values or
    raises appropriate errors for various isotopes."""
    assert isotopic_abundance('H', 1) == isotopic_abundance('protium')
    assert np.isclose(isotopic_abundance('D'), 0.000115)
    assert isotopic_abundance('Be-8') == 0.0, 'Be-8'
    assert isotopic_abundance('Li-8') == 0.0, 'Li-8'

    with pytest.warns(AtomicWarning):
        isotopic_abundance('Og', 294)

    with pytest.raises(InvalidIsotopeError, message="No exception raised for "
                                                    "neutrons"):
        isotopic_abundance('neutron')

    with pytest.raises(InvalidParticleError):
        isotopic_abundance('Og-2')


isotopic_abundance_elements = (
    atomic_number(atomic_numb) for atomic_numb in range(1, 119))

isotopic_abundance_isotopes = (
    common_isotopes(element) for element in isotopic_abundance_elements)

isotopic_abundance_sum_table = (
    (element, isotopes) for element, isotopes in
    zip(isotopic_abundance_elements, isotopic_abundance_isotopes)
    if isotopes)


@pytest.mark.parametrize("element, isotopes", isotopic_abundance_sum_table)
def test_isotopic_abundances_sum(element, isotopes):
    """Test that the sum of isotopic abundances for each element with
    isotopic abundances is one."""
    sum_of_iso_abund = sum(isotopic_abundance(isotope) for isotope in isotopes)
    assert np.isclose(sum_of_iso_abund, 1, atol=1e-6), \
        f"The sum of the isotopic abundances for {element} does not equal 1."