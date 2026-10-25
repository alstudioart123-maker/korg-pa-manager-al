import tempfile
import unittest
from pathlib import Path

from app.core.binary_inspector import inspect_binary_file


class BinaryInspectorTests(unittest.TestCase):
    def test_inspects_binary_file_without_modifying_it(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "FAVORITE01.STY"
            original = bytes([0x4B, 0x4F, 0x52, 0x47, 0x00, 0x01])
            path.write_bytes(original)

            result = inspect_binary_file(path, preview_bytes=4)

            self.assertEqual(result["name"], "FAVORITE01.STY")
            self.assertEqual(result["extension"], ".STY")
            self.assertEqual(result["size_bytes"], len(original))
            self.assertEqual(result["header_bytes"], 4)
            self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
