from pathlib import Path

def inventory_set(folder_path):
    root = Path(folder_path)

    if not root.is_dir():
        raise ValueError(f"Dosja nuk ekziston: {root}")

    files = {}

    for path in root.rglob("*"):
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            files[relative.casefold()] = {
                "path": relative,
                "size": path.stat().st_size,
                "extension": path.suffix.upper(),
            }

    return files


def compare_sets(source_folder, target_folder):
    source = inventory_set(source_folder)
    target = inventory_set(target_folder)

    source_names = set(source)
    target_names = set(target)

    return {
        "source_folder": str(Path(source_folder).resolve()),
        "target_folder": str(Path(target_folder).resolve()),
        "source_count": len(source),
        "target_count": len(target),
        "common": sorted(source_names & target_names),
        "only_source": [
            source[name] for name in sorted(source_names - target_names)
        ],
        "only_target": [
            target[name] for name in sorted(target_names - source_names)
        ],
        "same_name_different_size": [
            {
                "source": source[name],
                "target": target[name],
            }
            for name in sorted(source_names & target_names)
            if source[name]["size"] != target[name]["size"]
        ],
    }
