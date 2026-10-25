import unittest

from app.core.models.profiles import identify_model


class ProfileTests(unittest.TestCase):
    def test_identifies_pa3x(self):
        folders = [
            "GLOBAL", "MULTISAMP", "PAD", "PCM",
            "PERFORM", "SONGBOOK", "SOUND", "STYLE",
        ]
        self.assertEqual(identify_model(folders), "PA3X")

    def test_identifies_pa4x(self):
        folders = [
            "GLOBAL", "KEYBOARDSET", "MULTISAMP", "PAD",
            "PCM", "SONGBOOK", "SOUND", "STYLE", "VOICEPRESET",
        ]
        self.assertEqual(identify_model(folders), "PA4X")

    def test_unknown_structure(self):
        self.assertEqual(identify_model(["DOCUMENTS"]), "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
