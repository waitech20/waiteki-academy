#!/usr/bin/env python3
"""
Hukagua faili zote za lessons/*.json na kusasisha catalog.json:
lessonCount, quizCount, freeLessons, proLessons, levels.

Matumizi (ndani ya folda hii):
    python3 tools/update_catalog.py          # sasisha catalog.json
    python3 tools/update_catalog.py --check  # kagua tu, usibadilishe (exit 1 kama kuna tatizo)

Inakagua pia kila somo: sehemu za lazima, id zisizojirudia, quiz, na kwamba
lugha ipo kwenye catalog. Ukiona "ERROR", rekebisha kabla ya kupandisha GitHub.
"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "catalog.json")
LESSONS = os.path.join(ROOT, "lessons")
LEVEL_ORDER = ["Beginner", "Intermediate", "Advanced"]
REQUIRED = ["id", "language", "level", "title", "access", "quiz"]


def main():
    check_only = "--check" in sys.argv
    with open(CATALOG, encoding="utf-8") as f:
        cat = json.load(f)
    by_id = {l["id"]: l for l in cat["languages"]}

    errors, changed = [], False
    seen_files = set()

    for fn in sorted(os.listdir(LESSONS)):
        if not fn.endswith(".json"):
            continue
        lang = fn[:-5]
        seen_files.add(lang)
        try:
            with open(os.path.join(LESSONS, fn), encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            errors.append(f"{fn}: JSON si sahihi ({e})")
            continue
        if lang not in by_id:
            errors.append(f"{fn}: lugha '{lang}' haipo kwenye catalog.json")
            continue

        lessons = data.get("lessons")
        if not isinstance(lessons, list) or not lessons:
            errors.append(f"{fn}: hakuna 'lessons' (orodha) au ni tupu")
            continue

        ids = set()
        for i, l in enumerate(lessons, 1):
            tag = f"{fn} somo #{i}"
            for k in REQUIRED:
                if k not in l:
                    errors.append(f"{tag}: inakosa '{k}'")
            lid = l.get("id")
            if lid in ids:
                errors.append(f"{tag}: id '{lid}' imejirudia")
            ids.add(lid)
            if l.get("access") not in ("free", "pro"):
                errors.append(f"{tag}: access lazima iwe 'free' au 'pro'")
            if not isinstance(l.get("quiz"), list) or not l.get("quiz"):
                errors.append(f"{tag}: quiz tupu")

        free = sum(1 for l in lessons if l.get("access") != "pro")
        pro = sum(1 for l in lessons if l.get("access") == "pro")
        quiz = sum(1 for l in lessons if l.get("quiz"))
        present = {l.get("level") for l in lessons}
        levels = [x for x in LEVEL_ORDER if x in present] + sorted(present - set(LEVEL_ORDER) - {None})

        new = {"lessonCount": len(lessons), "quizCount": quiz,
               "freeLessons": free, "proLessons": pro, "levels": levels}
        entry = by_id[lang]
        diff = {k: (entry.get(k), v) for k, v in new.items() if entry.get(k) != v}
        if diff:
            changed = True
            print(f"- {lang}: " + ", ".join(f"{k} {a} -> {b}" for k, (a, b) in diff.items()))
            entry.update(new)

    for lid, entry in by_id.items():
        if entry.get("lessonCount", 0) > 0 and lid not in seen_files:
            errors.append(f"catalog inasema '{lid}' ina masomo lakini lessons/{lid}.json haipo")

    for e in errors:
        print("ERROR:", e)

    if errors:
        print(f"\nImeshindwa: makosa {len(errors)}. catalog.json haijabadilishwa.")
        sys.exit(1)

    if not changed:
        print("Kila kitu kiko sawa. Hakuna mabadiliko ya catalog.")
        return
    if check_only:
        print("\nCatalog haiko sawa na faili za masomo. Endesha bila --check kuisasisha.")
        sys.exit(1)

    cat["updated"] = datetime.date.today().isoformat()
    with open(CATALOG, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"\ncatalog.json imesasishwa (updated = {cat['updated']}).")


if __name__ == "__main__":
    main()
