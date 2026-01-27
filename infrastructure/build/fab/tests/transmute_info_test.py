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
export PSYCLONE_PHYSICS_FILES = a b c \\
                                d \\
                                e
export PSYCLONE_DIRECTORIES = science/ukca

# Empty list:

export PSYCLONE_PHYSICS_EXCEPTION =
"""
    file_path = tmp_path / "psyclone_transmute_file_list.mk"
    file_path.write_text(content, encoding="utf8")
    return file_path


def test_get_revision_parses_revisions_correctly(tmp_path):
    """
    Tests the parsing of a dependencies.sh file
    """
    content = """\
# Comment
export PSYCLONE_PHYSICS_FILES = a b c \\
                                d \\
                                e
export PSYCLONE_DIRECTORIES = science/ukca

# Empty list:

export PSYCLONE_PHYSICS_EXCEPTION =
"""
    makefile = tmp_path / "psyclone_transmute_file_list.mk"
    makefile.write_text(content, encoding="utf8")

    ti = TransmuteInfo()
    ti.import_makefile(makefile)
    assert ti.get_transmute_files() == ["a", "b", "c", "d", "e"]
    assert ti.get_transmute_directories() == ["science/ukca"]
    assert ti.get_transmute_exceptions() == []


def test_get_revision_parses_revisions_correctly_error(tmp_path):
    """
    Tests the parsing of a dependencies.sh file
    """
    content = """\
# Comment
export X_PSYCLONE_PHYSICS_FILES = a b c \\
                                d \\
                                e
export PSYCLONE_DIRECTORIES = science/ukca

# Empty list:

export PSYCLONE_PHYSICS_EXCEPTION =
"""
    makefile = tmp_path / "psyclone_transmute_file_list.mk"
    makefile.write_text(content, encoding="utf8")

    ti = TransmuteInfo()
    with pytest.raises(RuntimeError) as err:
        ti.import_makefile(makefile)

    assert "Section 'PSYCLONE_PHYSICS_FILES' not found in" in str(err.value)
