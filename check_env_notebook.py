# Databricks notebook source
import importlib.metadata
import os

result = (
    f"cwd={os.getcwd()} "
    f"tabulate={importlib.metadata.version('tabulate')} "
    f"DATABRICKS_ENV_VERSION={os.environ.get('DATABRICKS_ENV_VERSION')}"
)
print(result)

# COMMAND ----------

dbutils.notebook.exit(result)
