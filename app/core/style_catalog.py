from pathlib import Path


def catalog_styles(style_folder):
    """Inventarizon skedarët STYLE të një SET-i Korg."""
    folder = Path(style_folder)

    if not folder.is_dir():
        raise ValueError(f"Nuk u gjet dosja STYLE: {folder}")

    files = sorted(
        (p for p in folder.iterdir()
         if p.is_file() and p.suffix.upper() == ".STY"),
        key=lambda p: p.name.upper()
    )

    catalog = []

    for file in files:
        name = file.stem.upper()

        if name.startswith("FAVORITE"):
            bank = "FAVORITE"
        elif name.startswith("USER"):
            bank = "USER"
        else:
            bank = "OTHER"

        catalog.append({
            "name": file.name,
            "bank": bank,
            "size_bytes": file.stat().st_size,
            "path": str(file),
        })

    return catalog
