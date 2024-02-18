"""Tests for configurations produced by the UI."""

import os

import pytest

from ssim.ui import Project, StorageOptions


@pytest.fixture
def project(grid_model_path):
    p = Project(name="test-project")
    p.set_grid_model(grid_model_path)
    return p


def test_prepare_run_project_dir(tmp_path, project):
    """Project.prepare_run() creates new project subdirectories.

    After Project.prepare_run() there must be a new subdirectory named
    by the hash of the project TOML file.

    The directory must contain a copy of the project TOML file.

    When reloaded the resulting project id must be the same as the original.

    When the Project is modified a new directory is created.

    """
    project.prepare_run(tmp_path)
    project_path = tmp_path / project.id
    assert os.path.exists(project_path)
    assert os.path.isdir(project_path)
    assert os.path.exists(project_path / "project.toml")
    # when the toml is loaded, the resulting project id must equal
    # project.id
    p = Project(name="foo")
    p.load_toml_file(project_path / "project.toml")
    assert p.id == project.id
    project.add_storage_option(
        StorageOptions(
            name="foo",
            num_phases=3,
            power=[1, 2, 3],
            duration=[4, 6],
            busses=["loadbus2"])
    )
    assert p.id != project.id
    project.prepare_run(tmp_path)
    project_path = tmp_path / project.id
    assert os.path.exists(project_path)
    assert os.path.isdir(project_path)
    assert os.path.exists(project_path / "project.toml")


# def test_model_copy(grid_model_path, base_dir):
#     """Grid model is copied when project configurations are generated."""
#     assert False, "not implemented"


# def test_new_subdir_after_project_change(base_dir):
#     """After a change to the Project, a new config subdirectory is created."""
#     assert False, "not implemented"


# def test_new_subdir_grid_change(base_dir):
#     """After a substantive change to the grid model a new config
#     subdirectory is created."""
#     assert False, "not implemented"


# def test_new_subdir_grid_loadshape_file_change(base_dir):
#     """After a substantive change to loadshape input files used by the
#     grid model a new config subdirectory is created."""
#     assert False, "not implemented"


# def test_reuse_subdir_non_substantive_change(base_dir):
#     """Changes to whiespace should not result in a new config subdirectory."""
#     assert False, "not implemented"