import unittest

from app.core.compatibility_report import build_compatibility_report


class CompatibilityReportTests(unittest.TestCase):
    def test_compares_folders_files_and_styles(self):
        source = {
            "detected_model": "PA4X",
            "folder": "/source",
            "top_level_folders": [
                "STYLE", "SOUND", "KEYBOARDSET"
            ],
            "categories": {
                "STYLE": [
                    "STYLE/FAVORITE01.STY",
                    "STYLE/USER01.STY",
                ],
                "SOUND": ["SOUND/SOUND01"],
                "KEYBOARDSET": ["KEYBOARDSET/SET01"],
            },
        }
        target = {
            "detected_model": "PA3X",
            "folder": "/target",
            "top_level_folders": ["STYLE", "SOUND", "PCM"],
            "categories": {
                "STYLE": [
                    "STYLE/FAVORITE01.STY",
                    "STYLE/USER02.STY",
                ],
                "SOUND": ["SOUND/SOUND02"],
                "PCM": ["PCM/PCM01"],
            },
        }

        report = build_compatibility_report(source, target)

        self.assertEqual(report["source_model"], "PA4X")
        self.assertEqual(report["target_model"], "PA3X")
        self.assertEqual(report["common_folders"], ["SOUND", "STYLE"])
        self.assertEqual(report["source_only_folders"], ["KEYBOARDSET"])
        self.assertEqual(report["target_only_folders"], ["PCM"])
        self.assertEqual(
            report["common_style_names"], ["FAVORITE01.STY"]
        )
        self.assertEqual(
            report["source_only_styles"], ["USER01.STY"]
        )
        self.assertEqual(
            report["target_only_styles"], ["USER02.STY"]
        )
        self.assertIn("nuk konverton", report["note"])

    def test_empty_reports(self):
        report = build_compatibility_report({}, {})
        self.assertEqual(report["common_folders"], [])
        self.assertEqual(report["source_only_files"], [])
        self.assertEqual(report["target_only_styles"], [])


if __name__ == "__main__":
    unittest.main()
