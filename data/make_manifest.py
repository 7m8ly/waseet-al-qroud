"""
SHA-256 manifests for the frozen sets (works the same on Windows, macOS and Linux).

  python data/make_manifest.py            write the manifests
  python data/make_manifest.py --check    verify nothing changed since they were written

Writes: data/heldout/MANIFEST.sha256, data/dialogues/MANIFEST.sha256 (held-out dialogues),
        data/adversarial/MANIFEST.sha256 (held-out messages only)
Format is the same as `sha256sum` ("<hash>  <path>"), paths relative to data/, forward slashes.
"""
import glob
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SETS = {
    "heldout/MANIFEST.sha256": ["heldout/cases/*.yaml", "heldout/wallets/*.csv", "heldout/CALCULATIONS.md"],
    "dialogues/MANIFEST.sha256": ["dialogues/heldout.yaml"],
    "adversarial/MANIFEST.sha256": ["adversarial/heldout.yaml"],
}


def digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def files_for(patterns):
    out = []
    for pat in patterns:
        out += glob.glob(os.path.join(ROOT, pat))
    return sorted(os.path.relpath(p, ROOT).replace(os.sep, "/") for p in out)


def main(check):
    bad = 0
    for manifest, patterns in SETS.items():
        mpath = os.path.join(ROOT, manifest)
        if check:
            for line in open(mpath, encoding="utf-8"):
                h, rel = line.rstrip("\n").split("  ", 1)
                if not os.path.exists(os.path.join(ROOT, rel)) or digest(os.path.join(ROOT, rel)) != h:
                    print("CHANGED OR MISSING:", rel)
                    bad += 1
        else:
            lines = [f"{digest(os.path.join(ROOT, rel))}  {rel}" for rel in files_for(patterns)]
            with open(mpath, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lines) + "\n")
            print(f"wrote {manifest}: {len(lines)} files")
    if check:
        print("all frozen files unchanged" if not bad else f"{bad} problem(s)")
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main("--check" in sys.argv)
