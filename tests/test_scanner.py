import tempfile
import unittest
from pathlib import Path

from app.core.set_scanner import scan_set


class ScannerTests(unittest.TestCase):
    def test_scans_and_classifies_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "DEMO.SET"

            (root / "STYLE").mkdir(parents=True)
            (root / "STYLE" / "TEST.STY").write_text("demo")

            (root / "PCM").mkdir()
            (root / "PCM" / "SAMPLE.PCM").write_text("demo")

            (root / "GLOBAL.KSC").write_text("demo")

            result = scan_set(root)

            self.assertEqual(result["total_files"], 3)
            self.assertEqual(result["categories"]["STYLE"].__len__(), 1)
            self.assertEqual(result["categories"]["PCM"].__len__(), 1)
            self.assertEqual(len(result["other_files"]), 1)

    def test_missing_folder(self):
        with self.assertRaises(ValueError):
            scan_set("/this/folder/does/not/exist")


if __name__ == "__main__":
    unittest.main()
