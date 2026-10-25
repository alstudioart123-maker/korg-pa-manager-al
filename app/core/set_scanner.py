from pathlib import Path

from .models.profiles import MODEL_PROFILES, identify_model

def scan_set(folder_path):
    root = Path(folder_path)

    if not root.exists() or not root.is_dir():
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
        "other_files": [],
        "top_level_folders": sorted(folders),
        "missing_profile_folders": [],
    }

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        results["total_files"] += 1
        relative = path.relative_to(root).as_posix()
        top_folder = path.relative_to(root).parts[0].upper()

        if top_folder in folders:
            results["categories"].setdefault(top_folder, []).append(relative)
        else:
            results["other_files"].append(relative)

    if model in MODEL_PROFILES:
        results["missing_profile_folders"] = sorted(
            MODEL_PROFILES[model] - folders
        )

    return results
