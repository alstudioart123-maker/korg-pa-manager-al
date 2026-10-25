from pathlib import Path


def inspect_binary_file(file_path, preview_bytes=64):
    path = Path(file_path)

    if not path.is_file():
        raise ValueError(f"Nuk u gjet skedari: {path}")

    with path.open("rb") as file:
        header = file.read(preview_bytes)

    return {
        "name": path.name,
        "extension": path.suffix.upper(),
        "size_bytes": path.stat().st_size,
        "header_hex": header.hex(" "),
        "header_bytes": len(header),
    }


def format_report(info):
    return (
        f"Skedari: {info['name']}\n"
        f"Formati: {info['extension']}\n"
        f"Madhësia: {info['size_bytes']} bytes\n"
        f"Byte të lexuar: {info['header_bytes']}\n"
        f"Koka HEX: {info['header_hex']}\n"
    )
