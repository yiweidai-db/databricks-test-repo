# Databricks notebook source
# Run the no-lock Jobs case before generating a lock with this notebook.
import os
from pathlib import Path

notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
workspace_path = notebook_path if notebook_path.startswith("/Workspace/") else "/Workspace" + notebook_path
project_root = Path(workspace_path).parent
assert (project_root / "pyproject.toml").is_file(), project_root
print("Explicit %uv sync project root:", project_root)
print("If attach already made uv.lock, snapshot it and remove only this fixture's lock before continuing.")
os.chdir(project_root)

# COMMAND ----------

# MAGIC %uv sync

# COMMAND ----------

# Recompute the path after sync, because environment changes can restart Python.
import hashlib
from pathlib import Path

notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
workspace_path = notebook_path if notebook_path.startswith("/Workspace/") else "/Workspace" + notebook_path
project_root = Path(workspace_path).parent
lock = project_root / "uv.lock"
assert lock.is_file(), lock
print("uv.lock", lock, hashlib.sha256(lock.read_bytes()).hexdigest())
