# Databricks notebook source
import importlib.metadata
import os

import cowsay

cowsay.cow("Project environment works!")
assert importlib.metadata.version("cowsay") == "6.1"

result = (
    f"cwd={os.getcwd()} "
    f"cowsay={importlib.metadata.version('cowsay')} "
    f"tabulate={importlib.metadata.version('tabulate')} "
    f"DATABRICKS_ENV_VERSION={os.environ.get('DATABRICKS_ENV_VERSION')}"
)
print(result)

# COMMAND ----------

dbutils.notebook.exit(result)
