# SPDX-License-Identifier: MIT
import os
import time

def test_recorder_initialization(recorder, temp_project_dir):
    """Test that the recorder initializes the shadow repo correctly."""
    shadow_repo_path = os.path.join(temp_project_dir, ".trajectory")
    assert os.path.exists(shadow_repo_path)
    assert os.path.exists(os.path.join(shadow_repo_path, ".git"))

    # Check .gitignore.
    with open(os.path.join(temp_project_dir, ".gitignore"), "r") as f:
        content = f.read()
    assert ".trajectory/" in content

def test_create_snapshot(recorder, temp_project_dir):
    """Test creating a snapshot of a modified file."""
    test_file = os.path.join(temp_project_dir, "test.py")
    with open(test_file, "w") as f:
        f.write("print('hello')")
    with open(test_file, "w") as f:
        f.write("print('hello')")

    recorder.create_snapshot(test_file)
    
    commits = recorder.get_history(test_file)
    assert len(commits) == 1
    assert "Snapshot of" in commits[0].message
    assert "[AUTO-TRJ]" in commits[0].message

def test_intent_recording(recorder, temp_project_dir):
    """Test that intent is attached to snapshots."""
    recorder.set_intent("Fixing bug")
    
    test_file = os.path.join(temp_project_dir, "test.py")
    with open(test_file, "w") as f:
        f.write("print('bug fixed')")
        
    recorder.create_snapshot(test_file)
    
    commits = recorder.get_history(test_file)
    assert "Fixing bug" in commits[0].message

def test_checkpoint(recorder, temp_project_dir):
    """Test squashing snapshots into a checkpoint."""
    test_file = os.path.join(temp_project_dir, "test.py")

    # Create 3 snapshots.
    for i in range(3):
        with open(test_file, "w") as f:
            f.write(f"print({i})")
        recorder.create_snapshot(test_file)
        time.sleep(0.1)  # Ensure timestamps differ slightly if needed.
        
    commits = recorder.get_history(test_file)
    assert len(commits) == 3

    # Checkpoint.
    result = recorder.checkpoint("Completed feature")
    assert "Successfully created checkpoint" in result

    # Verify squash.
    # Note: get_history might return the checkpoint commit now.
    commits = list(recorder.repo.iter_commits())
    assert len(commits) == 1
    assert "[CHECKPOINT]" in commits[0].message
    assert "Completed feature" in commits[0].message
