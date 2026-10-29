"""pytest: the synthetic data is internally consistent and (after the freeze) unchanged."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)


def test_cases_validate():
    r = run("data/cases_validate.py")
    assert r.returncode == 0, r.stdout + r.stderr


def test_decision_language_filter_selftest():
    r = run("llm/forbidden_terms_selftest.py")
    assert r.returncode == 0, r.stdout + r.stderr


def test_frozen_sets_unchanged():
    if not os.path.exists(os.path.join(ROOT, "data", "heldout", "MANIFEST.sha256")):
        return
    r = run("data/make_manifest.py", "--check")
    assert r.returncode == 0, r.stdout + r.stderr
