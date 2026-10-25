import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from app.core.set_scanner import scan_set
from app.core.compatibility_report import build_compatibility_report


class KorgManager:
    def __init__(self, root):
        self.root = root
        self.root.title("KORG PA MANAGER ULTIMATE")
        self.root.geometry("950x650")
        self.root.minsize(700, 450)
        self.report = None

        ttk.Label(
            root,
            text="KORG PA MANAGER ULTIMATE",
            font=("Arial", 19, "bold"),
        ).pack(pady=(16, 4))

        ttk.Label(
            root,
            text="Analizues SET • Korg PA4X → PA3X",
        ).pack(pady=(0, 12))

        buttons = ttk.Frame(root)
        buttons.pack(pady=5)

        ttk.Button(
            buttons, text="Hap dosjen SET",
            command=self.open_set,
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons, text="Eksporto raportin JSON",
            command=self.export_json,
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons, text="Hap dosjen STYLE",
            command=self.open_styles,
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Krahaso SET PA4X → PA3X",
            command=self.compare_sets,
        ).pack(side="left", padx=5)

        self.status = ttk.Label(root, text="Zgjidh një dosje SET.")
        self.status.pack(pady=5)

        self.output = tk.Text(root, wrap="none", font=("Consolas", 10))
        self.output.pack(fill="both", expand=True, padx=14, pady=12)

    def open_set(self):
        folder = filedialog.askdirectory(title="Zgjidh dosjen Korg SET")
        if not folder:
            return

        try:
            report = scan_set(folder)
        except (ValueError, OSError) as exc:
            messagebox.showerror("Gabim", str(exc))
            return

        self.report = report
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"DOSJA: {report['folder']}\n")
        self.output.insert(tk.END, f"SKEDARË GJITHSEJ: {report['total_files']}\n\n")

        for category, files in report["categories"].items():
            self.output.insert(
                tk.END, f"=== {category.upper()} ({len(files)}) ===\n"
            )
            for name in files:
                self.output.insert(tk.END, f"  {name}\n")
            self.output.insert(tk.END, "\n")

        self.output.insert(
            tk.END, f"SKEDARË TË PAKLASIFIKUAR "
            f"({len(report['other_files'])})\n"
        )
        for name in report["other_files"]:
            self.output.insert(tk.END, f"  {name}\n")

        self.status.config(text="Analizimi përfundoi.")

    def open_styles(self):
        folder = filedialog.askdirectory(
            title="Zgjidh dosjen STYLE të Korg"
        )
        if not folder:
            return

        try:
            styles = catalog_styles(folder)
        except (ValueError, OSError) as exc:
            messagebox.showerror("Gabim", str(exc))
            return

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"DOSJA STYLE: {folder}\\n")
        self.output.insert(tk.END, f"STILE GJITHSEJ: {len(styles)}\\n\\n")

        for item in styles:
            self.output.insert(
                tk.END,
                f"{item['bank']:8} | {item['name']:25} | "
                f"{item['size_bytes']} bytes\\n"
            )

        favorite_count = sum(
            item["bank"] == "FAVORITE" for item in styles
        )
        user_count = sum(
            item["bank"] == "USER" for item in styles
        )
        self.status.config(
            text=f"U gjetën {len(styles)} skedarë STYLE: "
                 f"{favorite_count} FAVORITE, {user_count} USER."
        )

    def export_json(self):
        if self.report is None:
            messagebox.showinfo(
                "Informacion",
                "Analizo një SET ose krahaso dy SET-e fillimisht."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Ruaj raportin",
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile="korg_set_report.json",
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(self.report, file, ensure_ascii=False, indent=2)
        except OSError as exc:
            messagebox.showerror("Gabim", str(exc))
            return

        self.status.config(text="Raporti JSON u ruajt.")
        messagebox.showinfo("Sukses", "Raporti u eksportua me sukses.")


    def compare_sets(self):
        source_folder = filedialog.askdirectory(
            title="Zgjidh SET-in burimor PA4X"
        )
        if not source_folder:
            return

        target_folder = filedialog.askdirectory(
            title="Zgjidh SET-in objektiv PA3X"
        )
        if not target_folder:
            return

        try:
            source_report = scan_set(source_folder)
            target_report = scan_set(target_folder)
            report = build_compatibility_report(
                source_report, target_report
            )
        except (ValueError, OSError) as exc:
            messagebox.showerror("Gabim gjatë krahasimit", str(exc))
            return

        self.report = report
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "RAPORTI I KRAHASIMIT PA4X → PA3X\\n")
        self.output.insert(tk.END, f"BURIMI: {report['source_folder']}\\n")
        self.output.insert(tk.END, f"OBJEKTIVI: {report['target_folder']}\\n\\n")

        sections = [
            ("DOSJE TË PËRBASHKËTA", "common_folders"),
            ("DOSJE VETËM NË BURIM", "source_only_folders"),
            ("DOSJE VETËM NË OBJEKTIV", "target_only_folders"),
            ("STILE ME TË NJËJTIN EMËR", "common_style_names"),
            ("STILE VETËM NË BURIM", "source_only_styles"),
            ("STILE VETËM NË OBJEKTIV", "target_only_styles"),
            ("SKEDARË VETËM NË BURIM", "source_only_files"),
            ("SKEDARË VETËM NË OBJEKTIV", "target_only_files"),
        ]

        for title, key in sections:
            items = report.get(key, [])
            self.output.insert(tk.END, f"=== {title} ({len(items)}) ===\\n")
            for item in items:
                self.output.insert(tk.END, f"  {item}\\n")
            self.output.insert(tk.END, "\\n")

        self.output.insert(tk.END, "SHËNIM: " + report["note"] + "\\n")
        self.status.config(text="Krahasimi përfundoi.")

def main():
    root = tk.Tk()
    KorgManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
