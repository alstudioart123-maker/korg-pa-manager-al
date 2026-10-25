import argparse
import json
import sys
from pathlib import Path

from app.core.set_scanner import scan_set
from app.core.compatibility_report import build_compatibility_report


def main():
    parser = argparse.ArgumentParser(
        description="KORG PA MANAGER ULTIMATE - analizim dhe krahasim SET"
    )
    parser.add_argument("--set", dest="set_path", help="Dosja e një SET-i")
    parser.add_argument("--source", help="SET burimor, p.sh. PA4X")
    parser.add_argument("--target", help="SET objektiv, p.sh. PA3X")
    parser.add_argument(
        "--output",
        default="raport_korg.json",
        help="Emri i raportit JSON (parazgjedhja: raport_korg.json)",
    )
    args = parser.parse_args()

    if args.source and args.target:
        source_path = Path(args.source).expanduser()
        target_path = Path(args.target).expanduser()

        if not source_path.is_dir() or not target_path.is_dir():
            parser.error("Kontrollo që të dyja dosjet SET të ekzistojnë.")

        source_report = scan_set(str(source_path))
        target_report = scan_set(str(target_path))
        report = build_compatibility_report(source_report, target_report)

    elif args.set_path and not args.source and not args.target:
        set_path = Path(args.set_path).expanduser()

        if not set_path.is_dir():
            parser.error("Dosja SET nuk u gjet.")

        report = scan_set(str(set_path))

    else:
        parser.error(
            "Përdor --set DOSJA ose përdor së bashku --source DOSJA --target DOSJA."
        )

    output_path = Path(args.output).expanduser()
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=2)
    except (OSError, TypeError, ValueError) as error:
        print(f"Gabim gjatë ruajtjes së raportit: {error}", file=sys.stderr)
        return 1

    print("Analiza përfundoi.")
    print(f"Raporti u ruajt te: {output_path.resolve()}")

    if "source_file_count" in report:
        print(f"Skedarë në burim: {report['source_file_count']}")
        print(f"Skedarë në objektiv: {report['target_file_count']}")
        print(f"Stile me emra të përbashkët: {len(report['common_style_names'])}")
    else:
        print(f"Skedarë gjithsej: {report.get('total_files', 0)}")

    print("Kujdes: krahasimi kontrollon strukturën dhe emrat, jo konvertimin real të formateve Korg.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
