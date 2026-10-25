import tempfile
import unittest
from pathlib import Path

from app.core.style_catalog import catalog_styles


class StyleCatalogTests(unittest.TestCase):
    def test_catalogs_favorite_and_user_styles(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "STYLE"
            folder.mkdir()

            for i in range(1, 13):
                (folder / f"FAVORITE{i:02}.STY").write_bytes(b"demo")

            for i in range(1, 4):
                (folder / f"USER{i:02}.STY").write_bytes(b"demo")

            result = catalog_styles(folder)

            self.assertEqual(len(result), 15)
            self.assertEqual(
                sum(item["bank"] == "FAVORITE" for item in result), 12
            )
            self.assertEqual(
                sum(item["bank"] == "USER" for item in result), 3
            )


if __name__ == "__main__":
    unittest.main()
