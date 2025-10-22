import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile
from fcm_configuration import FcmConfiguration

from fab.steps.find_source_files import Include, Exclude

@pytest.fixture
def extract_cfg_file():
    content = """\
extract.location{primary}[casim] = fcm:casim.xm
extract.location[casim] = trunk@$casim_rev
extract.location{diff}[casim] = $casim_sources
extract.path-excl[casim] = / # everything
extract.path-incl[casim] = \\
    src/accretion.F90 \\
    src/activation.F90 \\
    src/adjust_deposition.F90
casim_extract_files = src/extra1.F90 \\
    \\ src/extra2.F90
include some_other_file.cfg
# A comment line
# Empty line

unexpected.line = should_be_ignored
"""
    with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        f.write(content)
        return Path(f.name)

def test_fcm_configuration_parsing(extract_cfg_file):
    root_path = Path("science/casim/src")
    config = FcmConfiguration(extract_cfg_file, root_path=root_path)

    directives = config.get_include_exclude_list("casim")
    assert len(directives) == 6

    # Check types:
    assert isinstance(directives[0], Exclude)
    assert all(isinstance(d, Include) for d in directives[1:])

    # Check paths
    assert directives[0].filter_strings[0] ==  root_path / "casim"
    assert directives[1].filter_strings[0] == root_path / "casim" / "src/accretion.F90"

    # Check extra files section
    assert directives[5].filter_strings[0] == root_path / "casim" / "src/extra2.F90"

    # Cleanup
    extract_cfg_file.unlink()
