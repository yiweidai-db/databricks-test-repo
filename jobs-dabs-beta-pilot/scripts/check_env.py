import hashlib
import json
import sys
from importlib.metadata import version
from pathlib import Path

import cowsay
import tabulate


def check_environment(expected_tabulate, expected_humanize="", project_file=""):
    installed = {"cowsay": version("cowsay"), "tabulate": version("tabulate")}
    assert installed["cowsay"] == "6.1", installed
    cowsay.cow("Project environment works!")
    assert installed["tabulate"] == expected_tabulate, installed
    assert tabulate.tabulate([["environment", "ok"]])
    if expected_humanize:
        import humanize
        installed["humanize"] = version("humanize")
        assert installed["humanize"] == expected_humanize, installed
        assert humanize.intcomma(1234) == "1,234"
    evidence = {"installed": installed, "python": sys.executable}
    if project_file:
        path = Path(project_file)
        evidence["requested_probe_file"] = str(path)
        evidence["pyproject_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        lock = path.with_name("uv.lock")
        evidence["lock_sha256"] = (
            hashlib.sha256(lock.read_bytes()).hexdigest() if lock.exists() else None
        )
    print("BUGBASH_EVIDENCE " + json.dumps(evidence, sort_keys=True))
    print("A file hash proves the probe's read; use install logs and mismatched source versions to prove installation input.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-tabulate", default="0.9.0")
    parser.add_argument("--expected-humanize", default="4.12.3")
    parser.add_argument("--project-file", default="")
    args = parser.parse_args()
    check_environment(args.expected_tabulate, args.expected_humanize, args.project_file)
