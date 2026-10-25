"""Raport krahasimi SET PA4X -> PA3X. Nuk ndryshon skedarët origjinalë."""


def build_compatibility_report(source_report, target_report):
    source_folders = set(source_report.get("top_level_folders", []))
    target_folders = set(target_report.get("top_level_folders", []))

    source_files = {
        name
        for files in source_report.get("categories", {}).values()
        for name in files
    }
    target_files = {
        name
        for files in target_report.get("categories", {}).values()
        for name in files
    }

    source_styles = {
        name.rsplit("/", 1)[-1].upper()
        for name in source_report.get("categories", {}).get("STYLE", [])
        if name.upper().endswith(".STY")
    }
    target_styles = {
        name.rsplit("/", 1)[-1].upper()
        for name in target_report.get("categories", {}).get("STYLE", [])
        if name.upper().endswith(".STY")
    }

    return {
        "source_model": source_report.get("detected_model", "UNKNOWN"),
        "target_model": target_report.get("detected_model", "UNKNOWN"),
        "source_folder": source_report.get("folder", ""),
        "target_folder": target_report.get("folder", ""),
        "common_folders": sorted(source_folders & target_folders),
        "source_only_folders": sorted(source_folders - target_folders),
        "target_only_folders": sorted(target_folders - source_folders),
        "common_files": sorted(source_files & target_files),
        "source_only_files": sorted(source_files - target_files),
        "target_only_files": sorted(target_files - source_files),
        "common_style_names": sorted(source_styles & target_styles),
        "source_only_styles": sorted(source_styles - target_styles),
        "target_only_styles": sorted(target_styles - source_styles),
        "source_file_count": len(source_files),
        "target_file_count": len(target_files),
        "note": (
            "Ky raport krahason emrat dhe strukturën e skedarëve. "
            "Nuk verifikon përputhshmërinë e brendshme të formateve Korg "
            "dhe nuk konverton skedarë."
        ),
    }
