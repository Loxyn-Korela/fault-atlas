#!/usr/bin/env python3
"""Fault Atlas probe — form-183: half of the in-force acts have no structured text
in the official dump.

Input: the three archives of the Publications Office data dump for legal acts in
force (sector 3), as served on 2026-09-06 behind EU Login
(https://datadump.publications.europa.eu/, "LEG" collection):
    LEG_MTD_20260906_01_00.zip   metadata, one tree_non_inferred.rdf per work
    LEG_EN_FMX_20260906_01_00.zip  Formex XML sections, English
    LEG_FR_FMX_20260906_01_00.zip  Formex XML sections, French
Nothing is extracted: the archives are read as streams, their content is not
rewritten. Adapted from the collector's inventory script (Alexandrie, Loxyn, 2026-09-09).

Run:
    python3 probes/2026-09/form-183-dump-coverage.py <dir holding the three .zip>

Result on the 2026-09-06 dump: 58,686 works in the metadata, 30,047 with at least
one EN Formex file, 29,892 with FR, 27,792 (47 %) with no Formex in either language.
On the EN side the archive carries 22,293 .tif files: old acts scanned, never
converted. The dump is complete for metadata and half complete for text.
"""
import sys, os, re, zipfile, collections


def main(dump_dir):
    zips = sorted(x for x in os.listdir(dump_dir) if x.endswith(".zip"))
    mtd = [z for z in zips if "_MTD_" in z]
    fmx = {z.split("_")[1].lower(): z for z in zips if "_FMX_" in z}
    if not mtd or not fmx:
        sys.exit("need one *_MTD_*.zip and at least one *_FMX_*.zip in " + dump_dir)
    works_with_text = {}
    tif = collections.Counter()
    for lang, name in fmx.items():
        z = zipfile.ZipFile(os.path.join(dump_dir, name))
        per_work = collections.Counter()
        for n in z.namelist():
            if "/" not in n:
                continue
            per_work[n.split("/")[0]] += 1
            if n.lower().endswith(".tif"):
                tif[lang] += 1
        works_with_text[lang] = set(per_work)
        z.close()
    z = zipfile.ZipFile(os.path.join(dump_dir, mtd[0]))
    works = {n.split("/")[0] for n in z.namelist() if n.endswith("tree_non_inferred.rdf")}
    z.close()
    any_text = set().union(*works_with_text.values())
    print(f"works in metadata: {len(works)}")
    for lang in sorted(works_with_text):
        print(f"works with {lang.upper()} Formex: {len(works & works_with_text[lang])}   (.tif files in that archive: {tif[lang]})")
    none = len(works - any_text)
    print(f"works with no Formex in any language: {none}  ({100*none/len(works):.0f} %)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
