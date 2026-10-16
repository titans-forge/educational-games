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

    def test_github_player_matches_source(self):
        game = next(g for g in self.data['games'] if g['id'] == 'titans-of-war-civil-war')
        game['github_play_url'] = 'https://titans-forge.github.io/Titans_of_War/'
        self.assertIn('[GitHub player](https://titans-forge.github.io/Titans_of_War/)', CATALOG.render(self.data))

    def test_foreign_github_player_rejected(self):
        game = next(g for g in self.data['games'] if g['id'] == 'titans-of-war-civil-war')
        game['github_play_url'] = 'https://titans-forge.github.io.evil.example/Titans_of_War/'
        with self.assertRaises(ValueError):
            CATALOG.validate(self.data)

    def test_wrong_github_player_repository_rejected(self):
        game = next(g for g in self.data['games'] if g['id'] == 'titans-of-war-civil-war')
        game['github_play_url'] = 'https://titans-forge.github.io/other-game/'
        with self.assertRaises(ValueError):
            CATALOG.validate(self.data)

    def test_unpublished_source_rejected(self):
        game = self.data["games"][0]
        game["source_status"] = "preparing"
        game["source_url"] = "https://github.com/titans-forge/not-published"
        with self.assertRaises(ValueError):
            CATALOG.validate(self.data)

    def test_wrong_source_owner_rejected(self):
        self.data["games"][6]["source_url"] = "https://github.com/JCapone83/not-transferred"
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
        self.assertIn("All fourteen catalog games now", guide)
        for game in self.data["games"]:
            if game["source_url"] is not None:
                self.assertIn(game["source_url"], guide)
        self.assertEqual(guide.count("/blob/main/LICENSING.md"), 13)
        self.assertIn("upgrades not already granted under other terms", guide)
        self.assertIn("does not automatically MIT-license future additions", guide)
        self.assertNotIn("/Users/", guide)
        self.assertIn("[Licensing](LICENSING.md)", CATALOG.render(self.data))

    def test_reference_license_is_exact_approved_text(self):
        approved = (ROOT / "FORGE-GAME-HOSTING-LICENSE-1.0.txt").read_bytes()
        self.assertEqual(hashlib.sha256(approved).hexdigest(),
                         "28638be413f7815704fe68aed52a4ea4cb7bd4d28b35f2dca9b78d438a4a90bf")

    def test_new_reference_license_is_exact_owner_approved_text(self):
        approved = (ROOT / "FORGE-GAME-LICENSE-2.0.txt").read_bytes()
        self.assertEqual(hashlib.sha256(approved).hexdigest(),
                         "01c53180ca78bee80411c2d07e436014b62f7e48dd37de70c2fed72238ee57dc")

    def test_verified_transfer_can_be_recorded(self):
        game = self.data["games"][12]
        game["source_status"] = "existing_personal_repository"
        game["source_url"] = "https://github.com/JCapone83/ares-strategy-engine"
        self.assertIn("1 listed primary source repository is under JCapone83", CATALOG.render(self.data))
        self.assertIn("13 listed primary source repositories are under titans-forge", CATALOG.render(self.data))
        game["source_status"] = "forge_repository"
        game["source_url"] = "https://github.com/titans-forge/ares-strategy-engine"
        self.assertIn("All 14 listed primary source repositories are under titans-forge", CATALOG.render(self.data))
        self.assertIn("original source-history repositories are retained where linked", CATALOG.render(self.data))

    def test_completed_source_publication_scope(self):
        expected = {
            "titans-of-war-ashes-of-nika": "Titans-of-War-Ashes-of-Nika",
            "titans-of-war-rise-of-rome": "Titans-of-War-Rise-of-Rome",
            "titans-of-war-rome-reconquest": "Titans_of_War_Rome_Reconquest",
            "titans-of-war-civil-war": "Titans_of_War",
            "titans-of-war-revolution": "Titans-of-War-Revolution",
            "living-waters": "Titans-of-Nature-Living-Waters",
            "titans-of-luna": "Titans-of-Luna",
            "build-a-republic": "Build-a-Republic",
            "crossroads-the-silk-roads": "Crossroads-The-Silk-Roads",
            "titans-of-war-caesar": "Titans-of-War-Caesar",
            "titans-of-proxima": "Titans-of-Proxima",
            "medical-mysteries": "Medical-Mysteries",
            "ares": "ares-strategy-engine",
            "titans-of-mars": "Titans-of-Mars",
        }
        games = {game["id"]: game for game in CATALOG.validate(self.data)}
        self.assertEqual(
            {game["id"] for game in games.values() if game["source_status"] == "forge_repository"},
            set(expected),
        )
        for game_id, repository in expected.items():
            self.assertEqual(games[game_id]["source_url"], f"https://github.com/titans-forge/{repository}")
        self.assertEqual(sum(game["source_status"] == "preparing" for game in games.values()), 0)
        self.assertIn("All 14 listed primary source repositories are under titans-forge", CATALOG.render(self.data))
        self.assertIn("original source-history repositories are retained where linked", CATALOG.render(self.data))

    def test_mars_upgrade_publication_preserves_scope_and_player_qa_boundary(self):
        game = next(game for game in self.data["games"] if game["id"] == "titans-of-mars")
        record = json.loads((ROOT / "releases/titans-of-mars-v0.4.0-20261015.json").read_text())
        guide = (ROOT / "LICENSING.md").read_text()
        self.assertEqual(game["source_history_url"], "https://github.com/JCapone83/Titans-of-Mars")
        self.assertEqual(record["gameplay_version"], "0.4.0")
        self.assertEqual(record["licensing_edition"], "FG2-TITANS-OF-MARS-V0.4.0-20261015")
        self.assertEqual(record["publication_status"], "published")
        self.assertEqual(record["release_commit"], "d47b66d87deb3b9ef28d0d2200ddde3f0d5b7d83")
        self.assertEqual(record["release_url"], "https://github.com/titans-forge/Titans-of-Mars/releases/tag/v0.4.0")
        self.assertEqual(record["github_published_at"], "2026-10-15T23:52:31Z")
        self.assertEqual(record["github_release_asset_count"], 6)
        self.assertTrue(record["edition_published"]["github"])
        self.assertTrue(record["edition_published"]["itch"])
        self.assertEqual(record["itch_upload_ids"], {"browser": 19790184, "download": 19790185, "source": 19790183, "licensing": 19790182})
        smoke_status = record["live_player_smoke_status"]
        self.assertIn(smoke_status, {"pending_separate_verification", "passed"})
        if smoke_status == "passed":
            smoke = record["live_player_smoke"]
            self.assertEqual(smoke["public_browser_upload_id"], record["itch_upload_ids"]["browser"])
            self.assertTrue(smoke["public_iframe_upload_confirmed"])
            self.assertTrue(smoke["launch_mode"])
            self.assertIsInstance(smoke["itch_maximized_player"], bool)
            self.assertGreaterEqual(len(smoke["viewport_checks"]), 2)
            for viewport in smoke["viewport_checks"]:
                self.assertGreater(viewport["viewport_width"], 0)
                self.assertGreater(viewport["viewport_height"], 0)
                self.assertEqual(viewport["iframe_width"], viewport["viewport_width"])
                self.assertEqual(viewport["iframe_height"], viewport["viewport_height"])
                self.assertTrue(viewport["iframe_matches_viewport"])
            self.assertTrue(smoke["focus_selected_working"])
            self.assertGreaterEqual(smoke["zoom_percent_verified"], 100)
            self.assertLessEqual(smoke["zoom_percent_verified"], 220)
            self.assertTrue(smoke["prior_save_preserved"]["paused"])
            self.assertFalse(smoke["prior_save_preserved"]["gameplay_advanced"])
            self.assertIsInstance(smoke["console_clean"], bool)
            if not smoke["console_clean"]:
                self.assertTrue(smoke["observed_host_error"]["origin"])
                self.assertTrue(smoke["observed_host_error"]["message"])
                self.assertTrue(smoke["observed_host_error"]["game_remained_usable"])
            self.assertIsInstance(smoke["untested"], list)
            downloads = record["itch_public_download_verification"]
            self.assertTrue(downloads["verifiedAt"])
            self.assertEqual(downloads["page"], game["play_url"])
            self.assertGreaterEqual(len(downloads["files"]), 3)
            for download in downloads["files"]:
                self.assertTrue(download["name"])
                self.assertGreater(download["bytes"], 0)
                self.assertRegex(download["sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(download["matchesPublishedRelease"])
        self.assertEqual(record["source_url"], game["source_url"])
        self.assertEqual(record["source_history_url"], game["source_history_url"])
        self.assertIn("version 0.4.0, released October 15, 2026", game["summary"])
        self.assertIn("qualifying new Licensor-controlled upgrade expression", guide)
        self.assertNotIn("source adoption deferred", guide)

    def test_medical_recovery_and_proxima_scope_are_explicit(self):
        rendered = CATALOG.render(self.data)
        self.assertIn("not the missing original authoring workspace", rendered)
        self.assertIn("not an actual Proxima mission", rendered)
        self.assertIn("case JSONL inputs, generators and tests were not recovered", (ROOT / "LICENSING.md").read_text())


if __name__ == "__main__":
    unittest.main()
