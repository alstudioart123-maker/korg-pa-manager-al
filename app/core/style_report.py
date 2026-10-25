from pathlib import Path
from app.core.style_catalog import catalog_styles


def create_style_report(style_folder):
    styles = catalog_styles(style_folder)

    return {
        "folder": str(Path(style_folder)),
        "total_styles": len(styles),
        "favorite_count": sum(
            item["bank"] == "FAVORITE" for item in styles
        ),
        "user_count": sum(
            item["bank"] == "USER" for item in styles
        ),
        "styles": styles,
    }


def print_style_report(style_folder):
    report = create_style_report(style_folder)

    print(f"Dosja: {report['folder']}")
    print(f"Totali: {report['total_styles']}")
    print(f"FAVORITE: {report['favorite_count']}")
    print(f"USER: {report['user_count']}")
    print("-" * 45)

    for item in report["styles"]:
        print(
            f"{item['bank']:8} | "
            f"{item['name']:25} | "
            f"{item['size_bytes']} bytes"
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("style_folder", help="Rruga drejt dosjes STYLE")
    args = parser.parse_args()

    print_style_report(args.style_folder)
