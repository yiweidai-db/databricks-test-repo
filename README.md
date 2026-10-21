# Jobs and bundles project environment pilot

Use this repository as one personal Databricks Git folder. The `jobs-dabs-beta-pilot/` directory
contains a Databricks Asset Bundle with notebook, Python script, and wheel tasks.
No job has a schedule or trigger.

## Files to review

- `pyproject.toml`: Git-root environment with `cowsay==6.1`, `tabulate==0.9.0`, and environment version 6.
- `check_env_notebook.py` and `check_env.py`: Existing Git-root notebook and Python script.
- `lock_setup.py`: Git-root notebook that runs `%uv sync`.
- `jobs-dabs-beta-pilot/pyproject.toml`: Bundle environment that also installs `humanize==4.12.3`.
- `jobs-dabs-beta-pilot/databricks.yml`: Bundle configuration and personal deployment paths.
- `jobs-dabs-beta-pilot/resources/bugbash.job.yml`: Three tasks that share the bundle environment.
- `jobs-dabs-beta-pilot/src/check_env.py` and `jobs-dabs-beta-pilot/scripts/check_env.py`: Bundle dependency probes.
- `jobs-dabs-beta-pilot/src/lock_setup.py`: Bundle notebook that runs `%uv sync`.
- `verify_dev_dependencies.py` and `jobs-dabs-beta-pilot/src/verify_dev_dependencies.py`:
  Separate notebooks for the deferred dev-dependency exclusion check.

## Review the no-lock case first

1. Create a Databricks Git folder from this repository.
2. Open `jobs-dabs-beta-pilot/` as an Asset Bundle and select the `dev` target.
3. Deploy the bundle, then run its job before attaching either project to compute.
4. Confirm that all three tasks succeed. The notebook and script must print a cow
   and `BUGBASH_EVIDENCE`
   with `cowsay` 6.1, `tabulate` 0.9.0, and `humanize` 4.12.3.
5. Confirm that neither source project has a `uv.lock` file.

When there is no current `uv.lock` paired with `pyproject.toml`, Jobs falls back to
`uv pip install --no-cache -r pyproject.toml`. These fixtures use dependency-only
projects. The wheel task runs the installed `tabulate` package to format
`jobs-dabs-beta-pilot/data/sample.tsv`. It does not test building or running this
project's own package.
The wheel task writes its formatted table to `/tmp/jobs-dabs-beta-wheel-output.txt`.

## Review lock generation next

1. After the no-lock job completes, open `jobs-dabs-beta-pilot/src/lock_setup.py` with the bundle
   as its project environment and run its `%uv sync` cell.
2. Confirm that the notebook creates `jobs-dabs-beta-pilot/uv.lock`.
3. Redeploy the bundle and run the job again. Confirm the exact dependency versions.
4. Inspect the environment installation logs to verify which installation path ran.

Use the root `lock_setup.py` separately to generate a lock for the Git-root project.
The two projects have different dependency sets so their environment scopes are
visible during review.

## Try Schedule separately

Use Schedule on a notebook and on a Python script to inspect generated Jobs YAML.
For a project file inside the bundle, confirm that the generated environment uses
a relative `pyproject.toml` path. Keep any generated triggers paused.
The supplied job YAML tests deployment and execution; generated YAML needs its
own UI check.

Deployment files live under the current user's personal `.bundle` directory.
The dependency probes also print optional project-file hashes. A hash confirms
which file the probe read; installation logs are required to establish which file
Jobs used to install dependencies.

## Deferred dev-dependency check

Both projects declare `simplejson==3.20.2` in `[dependency-groups].dev`.
Runtime verification of dev-dependency exclusion is pending. The smoke job does
not run this assertion.

After a runtime that supports excluding dev dependency groups is available, open
the project's `verify_dev_dependencies.py` notebook with its project environment.
The notebook must print `PASS: dev dependency simplejson is not importable.`
It fails if `simplejson` imports successfully. Do not uninstall the package to
make the check pass.

## CLI

Use Databricks CLI 1.21.0 or later with access to the target workspace:

```sh
cd jobs-dabs-beta-pilot
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev project_environment
```
