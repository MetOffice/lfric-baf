##############################################################################
# (c) Crown copyright Met Office. All rights reserved.
# The file LICENCE, distributed with this code, contains details of the terms
# under which the code may be used.
##############################################################################
# Author J. Henrichs, Bureau of Meteorology

"""
This module tests the configurator.
"""

from unittest.mock import MagicMock

import pytest

from configurator import configurator  # Replace with actual module name
from fab.tools.category import Category
from fab.tools.tool_box import ToolBox
from fab.build_config import BuildConfig


@pytest.fixture
def mock_shell():
    """
    A simple shell mock to check that all expected calls are executed.
    """
    shell = MagicMock()
    shell.exec = MagicMock()
    # Set the category to the shell can be added to the ToolBox.
    shell.category = Category.SHELL
    return shell


def test_configurator_runs_expected_sequence(mock_shell, tmp_path):
    """
    Check that the expected series of calls is executed.
    """

    # Create a tool box and add the mocked shell that is used
    # to test the expected calls.
    tb = ToolBox()
    tb.add_tool(mock_shell)
    config = BuildConfig("Stub config", tb,
                         fab_workspace=tmp_path / 'fab')

    # Create a rose_picker mock:
    rose_picker = MagicMock()
    rose_picker.execute = MagicMock()

    # Setup source directories and rose-meta config file
    lfric_core = tmp_path / "lfric_core"
    lfric_apps = tmp_path / "lfric_apps"
    rose_meta_conf = tmp_path / "rose-meta.conf"

    # Simulate rose-meta.json and config_namelists.txt creation
    config_dir = tmp_path / "build_output" / "configuration"
    config_dir.mkdir(parents=True)
    rose_meta = config_dir / "rose-meta.json"
    rose_meta.write_text("{}", encoding="utf8")
    config_namelist = config_dir / "config_namelists.txt"
    config_namelist.write_text("namelist1\nnamelist2\n", encoding="utf8")

    # Run configurator
    with pytest.warns(match="_metric_send_conn not set, cannot send metrics"):
        configurator(
            config=config,
            lfric_core_source=lfric_core,
            rose_meta_conf=rose_meta_conf,
            rose_picker=rose_picker,
            include_paths=[lfric_apps],
            config_dir=config_dir
        )

    tools_dir = lfric_core / "infrastructure" / "build" / "tools"

    # Check rose_picker was called with the expected arguments:
    rose_picker.execute.assert_called_once()
    kwargs = rose_picker.execute.call_args_list[0].kwargs
    assert kwargs["parameters"] == [
        rose_meta_conf,
        '-directory', config_dir,
        '-include_dirs', lfric_core,
        '-include_dirs', lfric_core / "rose-meta",
        '-include_dirs', lfric_apps,
        '-include_dirs', lfric_apps / "rose-meta"
    ]

    # Check shell.exec was called with expected commands
    expected_calls = [
        ((f"{tools_dir / 'GenerateNamelist'} "
          f"-verbose {config_dir / 'rose-meta.json'} "
          f"-directory {config_dir}"),),
        ((f"{tools_dir / 'GenerateLoader'} "
          f"{config_dir / 'configuration_mod.f90'} "
          f"namelist1 namelist2"),),
        ((f"{tools_dir / 'GenerateFeigns'} {config_dir / 'rose-meta.json'} "
          f"-output {config_dir / 'feign_config_mod.f90'}"),)
    ]

    actual_calls = [call.args for call in mock_shell.exec.call_args_list]
    assert actual_calls == expected_calls
