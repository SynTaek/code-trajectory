# SPDX-License-Identifier: MIT
import pytest
import shutil
import tempfile
import git
from code_trajectory.recorder import Recorder
from code_trajectory.trajectory import Trajectory

@pytest.fixture
def temp_project_dir():
    """Creates a temporary directory for the project."""
    temp_dir = tempfile.mkdtemp()
    # Initialize git in the temp dir.
    repo = git.Repo.init(temp_dir)
    # Configure user for commits.
    with repo.config_writer() as config:
        config.set_value("user", "name", "Test User")
        config.set_value("user", "email", "test@example.com")
    
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def recorder(temp_project_dir):
    """Returns a Recorder instance initialized in the temp project."""
    return Recorder(temp_project_dir)

@pytest.fixture
def trajectory(recorder):
    """Returns a Trajectory instance."""
    return Trajectory(recorder)
