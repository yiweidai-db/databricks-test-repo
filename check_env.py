import importlib.metadata
import os

print(f"cwd={os.getcwd()}")
print(f"tabulate={importlib.metadata.version('tabulate')}")
print(f"DATABRICKS_ENV_VERSION={os.environ.get('DATABRICKS_ENV_VERSION')}")
