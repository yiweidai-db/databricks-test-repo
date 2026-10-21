# Databricks notebook source
# MAGIC %md
# MAGIC # Verify dev-dependency exclusion
# MAGIC Run this check only after the runtime supports excluding dev dependency groups.
# MAGIC Use this bundle's project environment. This notebook is excluded from the smoke job.

# COMMAND ----------

try:
    import simplejson
except ModuleNotFoundError as error:
    if error.name != "simplejson":
        raise
    print("PASS: dev dependency simplejson is not importable.")
else:
    raise AssertionError(f"Dev dependency simplejson is importable: {simplejson.__file__}")
