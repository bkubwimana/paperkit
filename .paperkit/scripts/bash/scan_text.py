#!/usr/bin/env python3
"""Scan paper source for placeholders and banned vocabulary.

Usage: scan_text.py ROOT [--terms FILE] [--ext .tex,.bib]

Reports one line per hit as path:line: LEVEL: message: matched text.
Exit 1 if any error-level hit, else 0. LaTeX comments are ignored.
"""
import argparse
import os
import re
import sys

PLACEHOLDERS = re.compile(r"\b(TODO|TBD|XXX|FIXME)\b|\\todo\b|\?\?")
COMMENT = re.compile(r"(?<!\\)%.*$")
SKIP_DIRS = {".git", ".paperkit", "paper", "node_modules", "build", "out"}


def load_terms(path):
    terms = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                print(f"{path}: malformed line: {line!r}", file=sys.stderr)
                continue
            level, pattern, message = parts
            terms.append((level.strip(), re.compile(pattern, re.IGNORECASE), message.strip()))
    return terms


def iter_files(root, exts):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if os.path.splitext(name)[1] in exts:
                yield os.path.join(dirpath, name)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    default_terms = os.path.normpath(os.path.join(here, "..", "..", "memory", "banned-terms.tsv"))
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--terms", default=default_terms)
    ap.add_argument("--ext", default=".tex")
    args = ap.parse_args()

    exts = {e if e.startswith(".") else "." + e for e in args.ext.split(",")}
    terms = load_terms(args.terms)
    errors = warns = 0

    for path in iter_files(args.root, exts):
        rel = os.path.relpath(path, args.root)
        with open(path, encoding="utf-8", errors="replace") as fh:
            for lineno, raw in enumerate(fh, 1):
                text = COMMENT.sub("", raw.rstrip("\n"))
                if not text.strip():
                    continue
                for m in PLACEHOLDERS.finditer(text):
                    print(f"{rel}:{lineno}: error: placeholder: {m.group(0)}")
                    errors += 1
                for level, rx, message in terms:
                    for m in rx.finditer(text):
                        print(f"{rel}:{lineno}: {level}: {message}: {m.group(0)}")
                        if level == "error":
                            errors += 1
                        else:
                            warns += 1

    print(f"summary: {errors} error(s), {warns} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
