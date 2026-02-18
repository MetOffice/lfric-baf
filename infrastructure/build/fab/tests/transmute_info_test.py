##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

"""
Tests the get_revision script.
"""

from pathlib import Path

import pytest

from transmute_info import TransmuteInfo


@pytest.fixture
def sample_makefile(tmp_path: Path) -> Path:
    """
    Simple fixture to create a test makefile. A bit of an overkill
    atm, but since this class is expected to be updated when
    parsing the new format, this will save time later.
    """
    content = """\
# Comment
export PSYCLONE_PHYSICS_FILES = a1 b1 c1 \\
                                d1 \\
                                e1
export PSYCLONE_DIRECTORIES = science/ukca

export PSYCLONE_PHYSICS_EXCEPTION = /some/science/ukca/exception.f90
"""
    file_path = tmp_path / "psyclone_transmute_file_list.mk"
    file_path.write_text(content, encoding="utf8")
    return file_path


def test_parse_makefile(sample_makefile):
    """
    Tests the parsing of a makefile
    """

    ti = TransmuteInfo()
    ti.import_makefile(sample_makefile, mode="include")
    for i in ["a1", "b1", "c1", "d1", "e1"]:
        assert (i, f"{i}.py") in ti._pattern_to_script
    assert ("science/ukca", "local.py") not in ti._pattern_to_script

    ti.import_makefile(sample_makefile, mode="exclude")
    assert ("science/ukca", "local.py") in ti._pattern_to_script
    assert ("/some/science/ukca/exception.f90", "") in ti._pattern_to_script


def test_exceptions(tmp_path):
    """
    Test invalid info in the parsed makefile
    """
    content = """\
# Comment
export INVALID = a b c
export PSYCLONE_DIRECTORIES = science/ukca
export PSYCLONE_PHYSICS_EXCEPTION =
"""
    makefile = tmp_path / "psyclone_transmute_file_list.mk"
    makefile.write_text(content, encoding="utf8")

    ti = TransmuteInfo()
    with pytest.raises(ValueError) as err:
        ti.import_makefile(makefile, mode="include")

    assert "Unexpected line 'export INVALID = a b c' in file" in str(err.value)

    with pytest.raises(ValueError) as err:
        ti.import_makefile(makefile, mode="INVALID")

    assert ("expects 'include' or 'exclude' as mode, but got 'invalid'"
            in str(err.value))


def test_get_file_list(sample_makefile):
    """
    Tests querying the script information
    """
    ti = TransmuteInfo()
    ti.import_makefile(sample_makefile, mode="include")

    # Test a single file:
    files = ti.get_transmute_files(set([Path("/somewhere/a1.f90")]))
    assert files == set([(Path("/somewhere/a1.f90"), "a1.py")])

    # Test a file and a file in the directory
    files = ti.get_transmute_files(set(
        [Path("/somewhere/b1.f90"),
         Path("/some/science/ukca/where/t.f90")]))
    # t.f90 should not be listed (since it was read in 'include' mode)
    assert files == set([(Path("/somewhere/b1.f90"), "b1.py")])

    # Test a file, directory and an exception
    files = ti.get_transmute_files(set(
        [Path("/somewhere/b1.f90"),
         Path("/some/science/ukca/exception.f90"),
         Path("/some/science/ukca/where/t.f90")]))
    assert files == set(
        [(Path("/somewhere/b1.f90"), "b1.py")])

    ti = TransmuteInfo()
    ti.import_makefile(sample_makefile, mode="exclude")
    files = ti.get_transmute_files(set(
        [Path("/somewhere/b1.f90"),
         Path("/some/science/ukca/where/t.f90")]))
    # t.f90 should not be listed (since it was read in 'include' mode)
    assert files == set([(Path("/some/science/ukca/where/t.f90"), "local.py")])

    # Test a file, directory and an exception
    files = ti.get_transmute_files(set(
        [Path("/somewhere/b1.f90"),
         Path("/some/science/ukca/exception.f90"),
         Path("/some/science/ukca/where/t.f90")]))
    assert files == set(
        [(Path("/some/science/ukca/where/t.f90"), "local.py")])
