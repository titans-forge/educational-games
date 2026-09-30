import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("catalog", ROOT / "tools/catalog.py")
CATALOG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CATALOG)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "games.json").read_text())

    def test_inventory(self):
        self.assertEqual(len(CATALOG.validate(self.data)), 14)

    def test_duplicate_rejected(self):
        self.data["games"][1] = copy.deepcopy(self.data["games"][0])
        with self.assertRaises(ValueError):
            CATALOG.validate(self.data)

    def test_foreign_play_host_rejected(self):
        self.data["games"][0]["play_url"] = "https://titans-forge.itch.io.evil.example/game"
        with self.assertRaises(ValueError):
            CATALOG.validate(self.data)

    def test_unpublished_source_rejected(self):
        self.data["games"][0]["source_url"] = "https://github.com/titans-forge/not-published"
        with self.assertRaises(ValueError):
            CATALOG.validate(self.data)

    def test_wrong_source_owner_rejected(self):
        self.data["games"][6]["source_url"] = "https://github.com/titans-forge/not-transferred"
        with self.assertRaises(ValueError):
            CATALOG.validate(self.data)

    def test_markdown_injection_rejected(self):
        self.data["games"][0]["summary"] = "Unexpected | table row"
        with self.assertRaises(ValueError):
            CATALOG.validate(self.data)

    def test_all_games_in_readme(self):
        rendered = CATALOG.render(self.data)
        for game in self.data["games"]:
            self.assertEqual(rendered.count(f"[Play]({game['play_url']})"), 1)
        self.assertNotIn("/Users/", rendered)

    def test_readme_matches(self):
        self.assertEqual((ROOT / "README.md").read_text(), CATALOG.render(self.data))

    def test_license_guide_matches_existing_source_scope(self):
        guide = (ROOT / "LICENSING.md").read_text()
        self.assertIn("Titans of Mars remains MIT/open source", guide)
        self.assertIn("Previously MIT-licensed material remains usable and hostable under MIT", guide)
        self.assertIn("Eight other catalog games do not yet", guide)
        for game in self.data["games"]:
            if game["source_url"] is not None:
                self.assertIn(game["source_url"], guide)
        self.assertEqual(guide.count("/blob/main/LICENSING.md"), 5)
        self.assertNotIn("/Users/", guide)
        self.assertIn("[Licensing](LICENSING.md)", CATALOG.render(self.data))

    def test_reference_license_is_exact_approved_text(self):
        approved = (ROOT / "FORGE-GAME-HOSTING-LICENSE-1.0.txt").read_bytes()
        self.assertEqual(hashlib.sha256(approved).hexdigest(),
                         "28638be413f7815704fe68aed52a4ea4cb7bd4d28b35f2dca9b78d438a4a90bf")

    def test_verified_transfer_can_be_recorded(self):
        game = self.data["games"][9]
        game["source_status"] = "forge_repository"
        game["source_url"] = "https://github.com/titans-forge/Titans-of-War-Ashes-of-Nika"
        self.assertIn("5 related repositories", CATALOG.render(self.data))
        self.assertIn("1 game source repositories", CATALOG.render(self.data))


if __name__ == "__main__":
    unittest.main()
