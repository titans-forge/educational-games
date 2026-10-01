"""Validate the public inventory and render its README. No network required."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("History and civics", "Nature", "Space and science", "Medical reasoning")
STATUSES = {"preparing", "existing_personal_repository", "forge_repository"}


def validate(data):
    if data.get("schema_version") != 1:
        raise ValueError("unsupported schema")
    games = data.get("games", [])
    if len(games) != 14:
        raise ValueError("expected the 14-game launch inventory")
    ids, titles, urls = set(), set(), set()
    for game in games:
        slug = game["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in ids:
            raise ValueError("invalid or duplicate id")
        ids.add(slug)
        if game["title"] in titles or game["play_url"] in urls:
            raise ValueError("duplicate title or play URL")
        titles.add(game["title"])
        urls.add(game["play_url"])
        for field in ("title", "summary"):
            text = game[field]
            if not isinstance(text, str) or not text.strip() or any(c in text for c in "\n\r|[]<>"):
                raise ValueError("unsafe catalog text")
        play = urlsplit(game["play_url"])
        if play.scheme != "https" or play.netloc != "titans-forge.itch.io" or play.query or play.fragment or not re.fullmatch(r"/[a-z0-9-]+", play.path):
            raise ValueError("invalid play URL")
        status = game["source_status"]
        source = game["source_url"]
        if status not in STATUSES or game["category"] not in CATEGORIES:
            raise ValueError("invalid status or category")
        if status == "preparing":
            if source is not None:
                raise ValueError("unpublished source must not masquerade as public")
        else:
            owner = "JCapone83" if status == "existing_personal_repository" else "titans-forge"
            parsed = urlsplit(source or "")
            if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query or parsed.fragment or not re.fullmatch(r"/" + owner + r"/[A-Za-z0-9_.-]+", parsed.path):
                raise ValueError("source URL does not match declared owner")
    return games


def render(data):
    games = validate(data)
    personal_count = sum(g["source_status"] == "existing_personal_repository" for g in games)
    forge_count = sum(g["source_status"] == "forge_repository" for g in games)
    preparing_count = sum(g["source_status"] == "preparing" for g in games)
    publication = "Source publication is being prepared in batches." if preparing_count else "All fourteen games now have listed public repositories; recovery scope varies by game."
    lines = ["# Titans Forge educational games", "", "Play on itch. Discover the source, discuss the ideas, and help improve the games here.", "", "[Play the collection](https://titans-forge.itch.io/) · [Educator guide](EDUCATOR_GUIDE.md) · [Contributing](CONTRIBUTING.md) · [Licensing](LICENSING.md)", "", f"This catalog lists 14 browser games. {publication} {personal_count} related repositories currently remain under JCapone83; {forge_count} game source repositories are listed under titans-forge. Listed source branches have not been certified to match every future or currently hosted itch build.", ""]
    for category in CATEGORIES:
        lines += [f"## {category}", "", "| Game | Explore | Play | Source |", "| --- | --- | --- | --- |"]
        for game in games:
            if game["category"] != category:
                continue
            source = "Being prepared" if game["source_url"] is None else f"[Source]({game['source_url']})"
            lines.append(f"| {game['title']} | {game['summary']} | [Play]({game['play_url']}) | {source} |")
        lines += [""]
    lines += ["Medical Mysteries is an exact native-JavaScript recovery of its published beta, not the missing original authoring workspace, generators or test suite. Its README documents that boundary. Proxima's existing charter concerns Luna and Mars, not an actual Proxima mission.", ""]
    lines += ["## Use thoughtfully", "", "Games simplify history, ecosystems, settlement engineering, and medical reasoning. Their scores are game models, not validated scientific measurements, demonstrated learning outcomes, operational instructions, or clinical recommendations. Discuss assumptions and compare scenarios with appropriate sources.", "", "Check each game's page for controls, accessibility, save behavior, and requirements. Do not submit personal information, student records, real medical cases, or browser-save exports in public issues.", "", "## Source and media", "", "This repository is a catalog, not a bundle of all game assets. See [the game licensing guide](LICENSING.md) for Forge Game Hosting License 1.0, preserved MIT grants, and the Titans of Mars exception. Each game retains its own release checkpoints and media-rights notices. Public visibility or a free play link does not grant blanket redistribution rights. Screenshots are intentionally omitted until a specific selection is cleared.", "", "## Maintaining the catalog", "", "`games.json` is the source of truth. Run `python3 tools/catalog.py --write` after an approved inventory change, then `python3 -m unittest discover -s tests` and `python3 tools/catalog.py --check`. Network and browser gameplay checks are separate release steps.", "", f"Inventory prepared {data['inventory_date']}. Titles and play links were reconciled against the public itch profile; new GitHub destinations are not claimed until publication is verified.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render(json.loads((ROOT / "games.json").read_text()))
    target = ROOT / "README.md"
    if args.write:
        target.write_text(expected)
    elif not target.exists() or target.read_text() != expected:
        raise SystemExit("README is out of sync; run --write")
    print("Catalog: 14 entries validated; README synchronized")


if __name__ == "__main__":
    main()
