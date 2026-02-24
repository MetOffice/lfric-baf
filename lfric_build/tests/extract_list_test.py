##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

"""
This file contains the tests for fcm_configuration.py
"""

from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from fab.steps.find_source_files import Include, Exclude
from extract_list import ExtractList


# Use "name=..." since otherwise pylint complains about redefined-outer-name
@pytest.fixture(name="extract_cfg_file")
def fixture_extract_cfg_file():
    """
    A small fixture that creates a dummy FCM extract.cfg file
    for all tests.
    """
    content = """\
casim:
    - src/a.F90
    - src/b.F90

ukca:
    - /
    - src/control/c.F90
"""
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        f.write(content)
    extract_path = Path(f.name)
    yield extract_path
    # Cleanup
    extract_path.unlink()


def test_fcm_configuration_parsing(extract_cfg_file):
    """Tests reading a configuration file, and that the include
    and exclude list is as expected.
    """
    extract_list = ExtractList(extract_cfg_file)

    root_path = Path("science/casim")
    directives = extract_list.get_include_exclude_list("casim", root_path)
    # The extract list adds a top-level exclude as first element
    assert len(directives) == 3

    # Check types:
    assert isinstance(directives[0], Exclude)
    assert all(isinstance(d, Include) for d in directives[1:])

    # Check paths - note that extract list adds a first Exclude:
    assert directives[0].filter_strings[0] == root_path
    assert directives[1].filter_strings[0] == root_path / "src" / "a.F90"
    assert directives[2].filter_strings[0] == root_path / "src" / "b.F90"

    directives = extract_list.get_include_exclude_list("ukca", root_path)
    # The extract list adds a top-level exclude as first element
    assert len(directives) == 3
    assert directives[1].filter_strings[0] == root_path
    assert directives[2].filter_strings[0] == (root_path / "src" / "control" /
                                               "c.F90")
    print(directives)

    # Change the root path to verify that the list is not cached:
    directives = extract_list.get_include_exclude_list("casim", Path("/tmp"))
    assert directives[0].filter_strings[0] == Path("/tmp")
    assert directives[1].filter_strings[0] == Path("/tmp") / "src" / "a.F90"


def test_fcm_configuration_section_list(extract_cfg_file):
    """Test that the section list works as expected.
    """
    extract_list = ExtractList(extract_cfg_file)
    assert extract_list.get_all_sections() == ["casim", "ukca"]
