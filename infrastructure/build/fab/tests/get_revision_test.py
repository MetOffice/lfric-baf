##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# For further details please refer to the file COPYRIGHT
# which you should have received as part of this distribution
##############################################################################

"""
Tests the get_revision script.
"""

import pytest
from pathlib import Path
from get_revision import GetRevision


@pytest.fixture
def sample_dependencies_file(tmp_path: Path) -> Path:
    """
    Simple fixture to create a test file. A bit of an overkill
    atm, but since this class is expected to be updated when
    parsing the new format, this will save time later.
    """
    content = """\
export lfric_core_rev=53676
export lfric_core_sources=
# Comment, and an empty line

export casim_rev=apps2.2
export casim_sources=
export socrates_rev=1483
"""
    file_path = tmp_path / "dependencies.sh"
    file_path.write_text(content, encoding="utf8")
    return file_path


def test_get_revision_parses_revisions_correctly(sample_dependencies_file):
    """
    Tests the parsing of a dependencies.sh file
    """
    gr = GetRevision(sample_dependencies_file)

    assert gr["lfric_core"] == "53676"
    assert gr["casim"] == "apps2.2"
    assert gr["socrates"] == "1483"
    assert "lfric_core_sources" not in gr
    assert "casim_sources" not in gr


def test_get_revision_error_handling(sample_dependencies_file):
    """
    Tests asking for a non-existing section, which should raise a
    KeyError:
    """
    gr = GetRevision(sample_dependencies_file)

    with pytest.raises(KeyError) as err:
        gr["does-not-exist"]

    assert "'does-not-exist'" == str(err.value)
