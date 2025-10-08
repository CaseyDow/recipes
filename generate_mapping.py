import json
import os
from pathlib import Path

RECIPES_DIR = Path("./ucla_recipes")
OUTPUT_FILE = Path("./recipes_mapping.json")

def extract_entries(data, filename):
    """Extract recipeName and EN fields from a JSON object or array."""
    entries = []

    def process_obj(obj):
        if not isinstance(obj, dict):
            return
        recipe_name = obj.get("recipeName")
        en_name = None
        translations = obj.get("recipeNameTranslations")
        if isinstance(translations, dict):
            en_name = translations.get("EN")
        # Only include if at least one name exists
        if recipe_name or en_name:
            entries.append({
                "filename": filename,
                "recipeName": recipe_name,
                "en": en_name
            })

    if isinstance(data, list):
        for item in data:
            process_obj(item)
    else:
        process_obj(data)

    return entries


def main():
    if not RECIPES_DIR.exists():
        print(f"❌ Folder not found: {RECIPES_DIR.resolve()}")
        return

    mapping = []

    for root, _, files in os.walk(RECIPES_DIR):
        for name in files:
            if not name.lower().endswith(".json"):
                continue
            filepath = Path(root) / name
            rel_path = filepath.relative_to(Path("."))
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                entries = extract_entries(data, str(rel_path))
                mapping.extend(entries)
            except Exception as e:
                print(f"⚠️ Error reading {rel_path}: {e}")

    # Write mapping JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(mapping, out, ensure_ascii=False, indent=2)

    print(f"✅ Mapping created: {OUTPUT_FILE} ({len(mapping)} entries)")


if __name__ == "__main__":
    main()
