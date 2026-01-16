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

from get_revision import GetRevision


@pytest.fixture
def sample_dependencies_file(tmp_path: Path) -> Path:
    """
    Simple fixture to create a test file. A bit of an overkill
    atm, but since this class is expected to be updated when
    parsing the new format, this will save time later.
    """
    content = """\
casim:
    source: git@github.com:MetOffice/casim.git
    ref: 2025.12.1

lfric_apps:
    source:
    ref:

lfric_core:
    source: git@github.com:MetOffice/lfric_core.git
    ref: 2025.12.1
"""
    file_path = tmp_path / "dependencies.yaml"
    file_path.write_text(content, encoding="utf8")
    return file_path


def test_get_revision_parses_revisions_correctly(tmp_path):
    """
    Tests the parsing of a dependencies.sh file
    """
    content = """\
casim:
    source: git@github.com:MetOffice/casim.git
    ref: 2025.12.1

lfric_apps:
    source:
    ref:

lfric_core:
    source: git@github.com:MetOffice/lfric_core.git
    ref: 2025.12.1
"""
    file_path = tmp_path / "dependencies.yaml"
    file_path.write_text(content, encoding="utf8")

    gr = GetRevision(file_path)

    assert gr["lfric_core"]["ref"] == "2025.12.1"
    assert (gr["lfric_core"]["source"] ==
            "git@github.com:MetOffice/lfric_core.git")
    assert gr.get_ref("casim") == "2025.12.1"
    assert gr.get_source("casim") == "git@github.com:MetOffice/casim.git"
    assert gr.get_ref("lfric_apps") is None
    assert gr.get_source("lfric_apps") is None


@pytest.mark.parametrize('key_names', [("NO-source", "ref"),
                                       ("source", "NO-ref")])
def test_get_revision_error_handling(tmp_path, key_names):
    """
    Tests sections that have either no source or no ref
    specified. The key_names parameter tests both
    options, using one valid and one invalid name.
    """
    content = f"""\
casim:
    {key_names[0]}: git@github.com:MetOffice/casim.git
    {key_names[1]}: 2025.12.1

"""
    file_path = tmp_path / "dependencies.yaml"
    file_path.write_text(content, encoding="utf8")

    with pytest.raises(RuntimeError) as err:
        GetRevision(file_path)

    if key_names[0] == "NO-source":
        assert "does not contain a 'source'" in str(err.value)
    else:
        assert "does not contain a 'ref'" in str(err.value)
