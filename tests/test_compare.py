import tempfile
import unittest
from pathlib import Path

from app.core.set_compare import compare_sets


class CompareTests(unittest.TestCase):
    def test_compare_two_sets(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "PA4X.SET"
            target = base / "PA3X.SET"

            (source / "STYLE").mkdir(parents=True)
            (target / "STYLE").mkdir(parents=True)

            (source / "STYLE" / "A.STY").write_text("style A")
            (target / "STYLE" / "A.STY").write_text("different style A")
            (source / "STYLE" / "B.STY").write_text("style B")
            (target / "STYLE" / "C.STY").write_text("style C")

            result = compare_sets(source, target)

            self.assertEqual(result["source_count"], 2)
            self.assertEqual(result["target_count"], 2)
            self.assertEqual(len(result["common"]), 1)
            self.assertEqual(len(result["only_source"]), 1)
            self.assertEqual(len(result["only_target"]), 1)
            self.assertEqual(len(result["same_name_different_size"]), 1)


if __name__ == "__main__":
    unittest.main()
