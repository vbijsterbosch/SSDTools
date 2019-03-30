import os
import re
import warnings

import numpy as np
from nose.tools import raises

from gptools.grid import Grid, read_envira, meteotoeslag_years, extract_year_from_file_name
from gptools.wbs import WBS


def test_read_envira():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    assert grid.data.shape == (grid.info['y_number'], grid.info['x_number'])


@raises(ValueError)
def test_read_envira_header_incorrect():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016e.dat')

    # Create a grid object from the data file
    Grid.read_envira(file_path)


def test_read_envira_other_shape():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016h.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    assert grid.data.shape == (grid.info['y_number'], grid.info['x_number'])


@raises(ValueError)
def test_read_envira_row_missing():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016r.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)


def test_read_enviras():
    # Get the path to the Envira files
    file_paths = abs_path('data/')

    # Set the pattern
    pattern = r'GP2018 - Lnight y201[67].dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # Check if the data is stored correctly
    assert isinstance(grid.data, list) and len(grid.data) == 2
    assert isinstance(grid.info, list) and len(grid.data) == 2


def test_read_enviras_inconsistent_info():
    # Get the path to the Envira files
    file_paths = abs_path('data/')

    # Set the pattern
    pattern = r'GP2018 - Lnight y2016h?.dat'

    try:
        # Create a grid object from the data file
        grid = Grid.read_enviras(file_paths, pattern)

        # If the test reaches this point, the method is not working properly
        assert False
    except ValueError:

        # Get the envira files
        file_paths = [f for f in os.listdir(file_paths) if re.search(pattern, f)]

        # Check if the file names are correct
        assert file_paths == ['GP2018 - Lnight y2016.dat', 'GP2018 - Lnight y2016h.dat']


def test_read_enviras_inconsistent_data():
    # Get the path to the Envira files
    file_paths = abs_path('data/')

    # Set the pattern
    pattern = r'GP2018 - Lnight y2016r?.dat'

    try:
        # Create a grid object from the data file
        grid = Grid.read_enviras(file_paths, pattern)

        # If the test reaches this point, the method is not working properly
        assert False
    except ValueError:

        # Get the envira files
        file_paths = [f for f in os.listdir(file_paths) if re.search(pattern, f)]

        # Check if the file names are correct
        assert file_paths == ['GP2018 - Lnight y2016.dat', 'GP2018 - Lnight y2016r.dat']


def test_read_enviras_inconsistent_input():
    # Get the path to the Envira files
    file_paths = abs_path('data/')

    # Set the pattern
    pattern = r'GP2018 - Lnight y201[67].dat'

    # Get the envira files
    file_names = [f for f in os.listdir(file_paths) if re.search(pattern, f)]

    # Create info and data lists
    cls_info = []
    cls_data = []

    # Read the envira files
    for file_name in file_names:
        info, data = read_envira(os.path.join(file_paths, file_name))
        cls_info.append(info)
        cls_data.append(data)

    try:
        # Add the data to a Grid object
        grid = Grid(data=cls_data, info=[cls_info[0]], unit='Lnight')

        # If the test reaches this point, the method is not working properly
        assert False
    except IndexError:

        # Check if the file names are correct
        assert file_names == ['GP2018 - Lnight y2016.dat', 'GP2018 - Lnight y2017.dat']


def test_read_enviras_inconsistent_list_size():
    # Get the path to the Envira files
    file_paths = abs_path('data/')

    # Set the pattern
    pattern = r'GP2018 - Lnight y201[67].dat'

    # Get the envira files
    file_names = [f for f in os.listdir(file_paths) if re.search(pattern, f)]

    # Create info and data lists
    cls_info = []
    cls_data = []

    # Read the envira files
    for file_name in file_names:
        info, data = read_envira(os.path.join(file_paths, file_name))
        cls_info.append(info)
        cls_data.append(data)

    try:
        # Add the data to a Grid object
        grid = Grid(data=cls_data, info=cls_info[0], unit='Lnight')

        # If the test reaches this point, the method is not working properly
        assert False
    except TypeError:

        # Check if the file names are correct
        assert file_names == ['GP2018 - Lnight y2016.dat', 'GP2018 - Lnight y2017.dat']


def test_to_envira():
    # Get the path from the original Envira file
    original_file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(original_file_path)

    # Set the path to the new Envira file
    new_file_path = abs_path('data/envira-test.dat')

    # Export the grid to the new file
    grid.to_envira(new_file_path)

    # Create a grid object from the new data file
    grid_new = Grid.read_envira(new_file_path)

    # Test if the headers of the files are the same
    assert grid_new.info == grid.info

    # Check if the data is still correct
    np.testing.assert_equal(grid_new.data, grid.data)


def test_meteotoeslag_years_empirisch_lden():
    # Determine the years to include for empirical Lden
    actual = meteotoeslag_years('empirisch', 'Lden')

    # Set the desired output
    desired = np.array([1971, 1973, 1974, 1975, 1977, 1978, 1979, 1980, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989,
                        1991, 1992, 1993, 1995, 1997, 1998, 1999, 2001, 2002, 2004, 2005, 2006, 2007, 2008, 2009, 2010])

    # Check if the data is stored correctly
    np.testing.assert_equal(actual, desired)


def test_meteotoeslag_years_empirisch_lnight():
    # Determine the years to include for empirical Lnight
    actual = meteotoeslag_years('empirisch', 'Lnight')

    # Set the desired output
    desired = np.array([1971, 1972, 1974, 1975, 1976, 1977, 1978, 1980, 1981, 1982, 1983, 1984, 1986, 1987, 1988, 1990,
                        1991, 1992, 1993, 1997, 1998, 1999, 2000, 2001, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010])

    # Check if the data is stored correctly
    np.testing.assert_equal(actual, desired)


def test_meteotoeslag_years_hybride_lden():
    # Determine the years to include for hybrid Lden
    actual = meteotoeslag_years('hybride', 'Lden')

    # Set the desired output
    desired = np.array([1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1982, 1983, 1985, 1986, 1987, 1988,
                        1989, 1990, 1991, 1992, 1995, 1997, 1998, 1999, 2001, 2003, 2004, 2005, 2006, 2007, 2008, 2009])

    # Check if the data is stored correctly
    np.testing.assert_equal(actual, desired)


def test_meteotoeslag_years_hybride_lnight():
    # Determine the years to include for hybrid Lnight
    actual = meteotoeslag_years('hybride', 'Lnight')

    # Set the desired output
    desired = np.array([1971, 1972, 1974, 1975, 1977, 1978, 1979, 1981, 1982, 1983, 1984, 1985, 1986, 1988, 1989, 1990,
                        1991, 1992, 1993, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009])

    # Check if the data is stored correctly
    np.testing.assert_equal(actual, desired)


@raises(KeyError)
def test_meteotoeslag_years_empirical_lnight():
    # Determine the years to include for empirical Lnight
    meteotoeslag_years('empirical', 'Lnight')


@raises(KeyError)
def test_meteotoeslag_years_hybrid_lnight():
    # Determine the years to include for hybrid Lnight
    meteotoeslag_years('hybrid', 'Lnight')


@raises(KeyError)
def test_meteotoeslag_years_hybride_lnight_lowercase():
    # Determine the years to include for hybrid lnight
    meteotoeslag_years('hybride', 'lnight')


@raises(KeyError)
def test_meteotoeslag_years_hybride_lnight_uppercase():
    # Determine the years to include for hybrid LNIGHT
    meteotoeslag_years('hybride', 'LNIGHT')


def test_meteotoeslag_from_method():
    # Get the path to the Envira files
    file_paths = abs_path('data/MINIMER2015')

    # Set the pattern
    pattern = r'[\w\d\s]+\.dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # Calculate the meteotoeslag
    meteotoeslag, meteo_years = grid.meteotoeslag_from_method('hybride')

    # Check if the data is processed correctly
    assert meteo_years.shape == (32,)
    assert grid.data[0].shape == meteotoeslag.shape
    assert np.all(grid.data[0] <= meteotoeslag)


@raises(LookupError)
def test_meteotoeslag_from_years():
    # Get the path to the Envira files
    file_paths = abs_path('data/MINIMER2015')

    # Set the pattern
    pattern = r'[\w\d\s]+\.dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # Calculate the meteotoeslag
    grid.meteotoeslag_from_years([1981, 1984, 1993, 1994, 1996, 2000, 2002, 2010])


@raises(LookupError)
def test_meteotoeslag_from_years_nonexistent():
    # Get the path to the Envira files
    file_paths = abs_path('data/MINIMER2015')

    # Set the pattern
    pattern = r'[\w\d\s]+\.dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # Calculate the meteotoeslag
    grid.meteotoeslag_from_years(np.ones((32,), dtype=int))


@raises(LookupError)
def test_meteotoeslag_from_years_doubles():
    # Get the path to the Envira files
    file_paths = abs_path('data/MINIMER2015')

    # Set the pattern
    pattern = r'[\w\d\s]+\.dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # Calculate the meteotoeslag
    grid.meteotoeslag_from_years(np.ones((32,), dtype=int) * 1981)


def test_hg():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Calculate the Hoeveelheid Geluid
    hg = grid.hg()

    assert isinstance(hg, float)


@raises(TypeError)
def test_hg_multigrid():
    # Get the path to the Envira files
    file_paths = abs_path('data/MINIMER2015')

    # Set the pattern
    pattern = r'[\w\d\s]+\.dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # Calculate the Hoeveelheid Geluid
    grid.hg()


def test_scale():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Copy the data
    d = grid.data.copy()

    # Calculate the meteotoeslag
    grid.scale(2.)

    np.testing.assert_equal(grid.data, d + 10 * np.log10(2))


def test_scale_multigrid():
    # Get the path to the Envira files
    file_paths = abs_path('data/MINIMER2015')

    # Set the pattern
    pattern = r'[\w\d\s]+\.dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # Calculate the meteotoeslag
    meteotoeslag, meteo_years = grid.meteotoeslag_from_method('hybride')

    # Calculate the meteotoeslag
    grid.scale(2.)

    # Calculate the meteotoeslag
    scaled_meteotoeslag, scaled_meteo_years = grid.meteotoeslag_from_method('hybride')

    assert np.all(meteo_years == scaled_meteo_years)
    np.testing.assert_equal(scaled_meteotoeslag, meteotoeslag + 10 * np.log10(2))


def test_scale_multigrid_int():
    # Get the path to the Envira files
    file_paths = abs_path('data/MINIMER2015')

    # Set the pattern
    pattern = r'[\w\d\s]+\.dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # Calculate the meteotoeslag
    meteotoeslag, meteo_years = grid.meteotoeslag_from_method('hybride')

    # Calculate the meteotoeslag
    grid.scale(2)

    # Calculate the meteotoeslag
    grid.scale(2.)

    # Calculate the meteotoeslag
    scaled_meteotoeslag, scaled_meteo_years = grid.meteotoeslag_from_method('hybride')

    assert np.all(meteo_years == scaled_meteo_years)
    np.testing.assert_equal(scaled_meteotoeslag, meteotoeslag + 10 * np.log10(4))


def test_statistics_multigrid():
    # Get the path to the Envira files
    file_paths = abs_path('data/MINIMER2015')

    # Set the pattern
    pattern = r'[\w\d\s]+\.dat'

    # Create a grid object from the data file
    grid = Grid.read_enviras(file_paths, pattern)

    # todo: Implement a proper test for the calculation of the statistics

    assert False


def test_interpolation_function():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # todo: Implement a proper test for the calculation of the interpolation function

    assert False


def test_interpolation_from_wbs():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Interpolate the grid from WBS
    noise = grid.interpolation_from_wbs(wbs)

    # todo: Implement a proper test for the calculation of the interpolation function

    assert False


def test_gehinderden_from_wbs():
    # Get the path to the Envira file
    file_path = abs_path('data/MER2015 - Doc29 - Lden y1974.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Gehinderden based on the grid and WBS combination
    g = grid.gehinderden_from_wbs(wbs)

    # todo: Implement a proper test for the calculation of the ernstig gehinderden

    assert False


def test_gehinderden_from_wbs_ges2002():
    # Get the path to the Envira file
    file_path = abs_path('data/MER2015 - Doc29 - Lden y1974.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Gehinderden based on the grid and WBS combination
    g = grid.gehinderden_from_wbs(wbs, de='ges2002')

    # todo: Implement a proper test for the calculation of the ernstig gehinderden

    assert False


def test_gehinderden_from_wbs_doc29_max_db():
    # Get the path to the Envira file
    file_path = abs_path('data/MER2015 - Doc29 - Lden y1974.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        # Gehinderden based on the grid and WBS combination
        g = grid.gehinderden_from_wbs(wbs, de='doc29', max_db=65)

        # Verify some things
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "dose-effect" in str(w[-1].message)


@raises(TypeError)
def test_gehinderden_from_wbs_lnight():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Gehinderden based on the grid and WBS combination
    grid.gehinderden_from_wbs(wbs)


@raises(ValueError)
def test_gehinderden_from_wbs_unknown_dose_effect():
    # Get the path to the Envira file
    file_path = abs_path('data/MER2015 - Doc29 - Lden y1974.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Gehinderden based on the grid and WBS combination with unknown dose-effect relationship
    grid.gehinderden_from_wbs(wbs, de='random123')


def test_slaapverstoorden_from_wbs():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Slaapverstoorden based on the grid and WBS combination
    g = grid.slaapverstoorden_from_wbs(wbs)

    # todo: Implement a proper test for the calculation of the ernstig gehinderden

    assert False


def test_slaapverstoorden_from_wbs_ges2002():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Slaapverstoorden based on the grid and WBS combination
    g = grid.slaapverstoorden_from_wbs(wbs, de='ges2002')

    # todo: Implement a proper test for the calculation of the ernstig gehinderden

    assert False


def test_slaapverstoorden_from_wbs_doc29_max_db():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        # Slaapverstoorden based on the grid and WBS combination
        g = grid.slaapverstoorden_from_wbs(wbs, de='doc29', max_db=65)

        # Verify some things
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert "dose-effect" in str(w[-1].message)


@raises(TypeError)
def test_slaapverstoorden_from_wbs_lden():
    # Get the path to the Envira file
    file_path = abs_path('data/MER2015 - Doc29 - Lden y1974.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Slaapverstoorden based on the grid and WBS combination
    grid.slaapverstoorden_from_wbs(wbs)


@raises(ValueError)
def test_slaapverstoorden_from_wbs_unknown_dose_effect():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Get the path to the WBS file
    file_path = abs_path('data/wbs2005.h5')

    # Create a wbs object from the data file
    wbs = WBS.read_file(file_path)

    # Slaapverstoorden based on the grid and WBS combination with unknown dose-effect relationship
    grid.slaapverstoorden_from_wbs(wbs, de='random123')


def test_refine():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Refine the grid with a factor 2
    grid.refine(2)

    # Check if the shape of the data matches the changed input
    assert grid.data.shape == (285, 285)
    assert grid.shape.x_number == 285
    assert grid.shape.y_number == 285


def test_refine_exceptions_and_failures():
    # todo: Implement proper tests for the improper use of refine()
    assert False


def test_resize():
    # Get the path to the Envira file
    file_path = abs_path('data/GP2018 - Lnight y2016.dat')

    # Create a grid object from the data file
    grid = Grid.read_envira(file_path)

    # Create an alternative shape
    shape = grid.shape.copy()

    # Change a few settings
    shape.set_x_number(201)
    shape.set_y_number(79)

    # Resize the grid
    grid.resize(shape)

    # Check if the shape of the data matches the changed input
    assert grid.data.shape == (79, 201)
    assert grid.shape.x_number == 201
    assert grid.shape.y_number == 79


def test_resize_exceptions_and_failures():
    # todo: Implement proper tests for the improper use of resize()
    assert False


def test_extract_year_from_file_name_y1234():
    assert 1234 == extract_year_from_file_name('y1234')


def test_extract_year_from_file_name_1234():
    assert extract_year_from_file_name('1234') is None


def test_extract_year_from_file_name_y12345():
    assert 1234 == extract_year_from_file_name('Test for y12345.dat')


@raises(TypeError)
def test_extract_year_from_file_name_int_1234():
    assert 1234 == extract_year_from_file_name(1234)


def abs_path(rel_path):
    return os.path.join(os.path.dirname(__file__), rel_path)
