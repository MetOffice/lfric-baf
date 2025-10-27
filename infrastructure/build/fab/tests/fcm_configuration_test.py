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
from fcm_configuration import FcmConfiguration


# Use "name=..." since otherwise pylint complains about redefined-outer-name
@pytest.fixture(name="extract_cfg_file")
def fixture_extract_cfg_file():
    """
    A small fixture that creates a dummy FCM extract.cfg file
    for all tests.
    """
    content = """\
extract.location{primary}[casim] = fcm:casim.xm
extract.location[casim] = trunk@$casim_rev
extract.location{diff}[casim] = $casim_sources
extract.path-excl[casim] = / # everything
extract.path-incl[casim] = \\
    src/acc.F90 \\
    src/activation.F90
casim_extract_files = src/extra1.F90 \\
    \\ src/extra2.F90
include some_other_file.cfg
# A comment line
# Empty line

unexpected.line = should_be_ignored
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
    config = FcmConfiguration(extract_cfg_file)

    root_path = Path("science/casim")
    directives = config.get_include_exclude_list("casim", root_path)
    assert len(directives) == 5

    # Check types:
    assert isinstance(directives[0], Exclude)
    assert all(isinstance(d, Include) for d in directives[1:])

    # Check paths = note that the config file adds the directory 'src':
    assert directives[0].filter_strings[0] == root_path
    assert directives[1].filter_strings[0] == root_path / "src" / "acc.F90"

    # Check extra files section
    assert directives[4].filter_strings[0] == root_path / "src" / "extra2.F90"

    # Change the root path to verify that the list is not cached:
    directives = config.get_include_exclude_list("casim", Path("/tmp"))
    assert directives[0].filter_strings[0] == Path("/tmp")
    assert directives[1].filter_strings[0] == Path("/tmp") / "src" / "acc.F90"


def test_fcm_configuration_section_list(extract_cfg_file):
    """Test that the section list works as expected.
    """
    config = FcmConfiguration(extract_cfg_file)
    assert config.get_all_sections() == ["casim"]
