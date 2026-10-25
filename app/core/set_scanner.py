from pathlib import Path

from .models.profiles import MODEL_PROFILES, identify_model


def scan_set(folder):
    root = Path(folder)

    if not root.is_dir():
        raise ValueError("Dosja SET nuk ekziston ose nuk është dosje.")

    folders = {
        path.name.upper()
        for path in root.iterdir()
        if path.is_dir()
    }

    model = identify_model(folders)

    results = {
        "folder": str(root.resolve()),
        "detected_model": model,
        "total_files": 0,
        "categories": {},
        "category_counts": {},
        "style_banks": {
            "FAVORITE": [],
            "USER": [],
            "OTHER": [],
        },
        "other_files": [],
        "top_level_folders": sorted(folders),
        "missing_profile_folders": [],
    }

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        results["total_files"] += 1
        relative = path.relative_to(root).as_posix()
        parts = path.relative_to(root).parts
        top_folder = parts[0].upper()

        if top_folder in folders:
            results["categories"].setdefault(
                top_folder, []
            ).append(relative)
        else:
            results["other_files"].append(relative)

        if top_folder == "STYLE" and path.suffix.upper() == ".STY":
            name = path.stem.upper()

            if name.startswith("FAVORITE"):
                bank = "FAVORITE"
            elif name.startswith("USER"):
                bank = "USER"
            else:
                bank = "OTHER"

            results["style_banks"][bank].append(relative)

    results["category_counts"] = {
        name: len(files)
        for name, files in results["categories"].items()
    }

    if model in MODEL_PROFILES:
        results["missing_profile_folders"] = sorted(
            MODEL_PROFILES[model] - folders
        )

    return results
