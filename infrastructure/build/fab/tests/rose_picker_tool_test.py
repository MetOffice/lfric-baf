##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
##############################################################################
# Author J. Henrichs, Bureau of Meteorology

"""
This module tests rose_picker_tool.
"""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock

import pytest

from fab.tools.category import Category
from fab.tools.tool import Tool
from rose_picker_tool import get_rose_picker, RosePicker


def test_get_rose_picker_system_found() -> None:
    """
    Test that a system-wide installed rose_picker works as expected.
    """
    with patch("shutil.which", return_value="/usr/bin/rose_picker"):
        rp = get_rose_picker("system")
        assert isinstance(rp, RosePicker)
        assert rp.exec_path == Path("/usr/bin/rose_picker")


def test_get_rose_picker_system_not_found() -> None:
    """
    Test error if a system rose_picker is requested, but does not exist.
    """
    with patch("shutil.which", return_value=None):
        with pytest.raises(RuntimeError) as err:
            get_rose_picker("system")
    assert "Cannot find system rose_picker tool." == str(err.value)


def test_get_rose_picker_local_checkout(tmp_path) -> None:
    """
    Tests that we will invoke rose picker from a local checkout
    (mocked, so we don't need an actual checkout)
    """
    tag = "v2.0.0"
    fake_workspace = tmp_path / "fab-workspace"
    gpl_utils = fake_workspace / f"gpl-utils-{tag}" / "source"
    rose_picker_bin = gpl_utils / "bin"
    rose_picker_path = rose_picker_bin / "rose_picker"

    # Patch get_fab_workspace to return our tmp_path
    pm = PropertyMock("is_available", side_effect=[False, True])
    with patch("rose_picker_tool.get_fab_workspace",
               return_value=fake_workspace), \
         patch("rose_picker_tool.ToolRepository") as mock_repo_class, \
         patch.object(Tool, "is_available", pm):

        mock_fcm = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_default.return_value = mock_fcm
        mock_repo_class.return_value = mock_repo

        rp = get_rose_picker(tag)

        # Ensure checkout was called
        mock_fcm.checkout.assert_called_once_with(
            src=f"fcm:lfric_gpl_utils.x/tags/{tag}",
            dst=gpl_utils
        )

        # Ensure the returned object is a RosePicker with correct path
        assert isinstance(rp, RosePicker)
        assert Path(rp.exec_path) == rose_picker_path


def test_get_rose_picker_local_checkout_fails() -> None:
    """
    This functions tests the behaviour if a local checkout fails,
    i.e. rose_picker cannot be executed. This test patches the
    ToolRepository (so that FCM is not actually called), and makes
    sure RosePicker is always not available:
    """

    tag = "v2.0.0"

    # Make sure rose_picker will always return to be not available:
    with patch("rose_picker_tool.ToolRepository.get_default") as mock_repo, \
         patch.object(RosePicker, "check_available", return_value=False), \
         pytest.raises(RuntimeError) as err:
        get_rose_picker(tag)

        assert f"Cannot run rose_picker tag '{tag}'." == str(err.value)
    # Also make sure that we indeed got FCM :)
    mock_repo.assert_called_with(Category.FCM)


def test_get_rose_picker_check_available() -> None:
    """
    Test RosePicker's check_available.
    """
    rose_picker = RosePicker(Path("/usr/bin/rose_picker"))
    with patch.object(RosePicker, "run", return_value=True) as mock_run:
        assert rose_picker.check_available()
    mock_run.assert_called_once_with(additional_parameters="-help")

    with patch.object(RosePicker, "run", side_effect=RuntimeError) as mock_run:
        assert not rose_picker.check_available()
    mock_run.assert_called_once_with(additional_parameters="-help")


def test_get_rose_picker_execute() -> None:
    """
    Test RosePicker's check_available.
    """
    rose_picker = RosePicker(Path("/usr/bin/rose_picker"))
    with patch.object(RosePicker, "run", return_value=0) as mock_run, \
         patch.object(os, "environ", {}):
        rose_picker.execute(["arg"])
    # Rose picker prepends the existing python path, separated by ":".
    # Since python path is not set, there will be a leading ":""
    mock_run.assert_called_once_with(additional_parameters=["arg"],
                                     env={'PYTHONPATH': ':/usr/lib/python'})
