import json
import unittest

from app.core.compatibility_report import build_compatibility_report


class ReportJsonTests(unittest.TestCase):
    def test_compatibility_report_is_json_serializable(self):
        source = {
            "detected_model": "PA4X",
            "folder": "/source",
            "top_level_folders": ["STYLE", "SOUND", "PCM"],
            "categories": {
                "STYLE": ["STYLE/FAVORITE01.STY"],
                "SOUND": ["SOUND/SOUND01"],
                "PCM": ["PCM/PCM01"],
            },
        }
        target = {
            "detected_model": "PA3X",
            "folder": "/target",
            "top_level_folders": ["STYLE", "SOUND"],
            "categories": {
                "STYLE": ["STYLE/FAVORITE01.STY"],
                "SOUND": ["SOUND/SOUND02"],
            },
        }

        report = build_compatibility_report(source, target)
        encoded = json.dumps(report, ensure_ascii=False)
        decoded = json.loads(encoded)

        self.assertEqual(decoded["source_model"], "PA4X")
        self.assertEqual(decoded["target_model"], "PA3X")
        self.assertEqual(decoded["source_folder"], "/source")
        self.assertEqual(decoded["target_folder"], "/target")
        self.assertIn("nuk konverton", decoded["note"])
        self.assertEqual(decoded["source_category_counts"]["PCM"], 1)
        self.assertEqual(decoded["target_category_counts"]["SOUND"], 1)
        self.assertIn("FAVORITE01.STY", decoded["common_style_names"])


if __name__ == "__main__":
    unittest.main()
