# Titans Forge educational games

Play on itch. Discover the source, discuss the ideas, and help improve the games here.

[Play the collection](https://titans-forge.itch.io/) · [Educator guide](EDUCATOR_GUIDE.md) · [Contributing](CONTRIBUTING.md) · [Licensing](LICENSING.md)

This catalog lists 14 browser games. All fourteen games now have listed public repositories; recovery scope varies by game. 1 related repositories currently remain under JCapone83; 13 game source repositories are listed under titans-forge. Listed source branches have not been certified to match every future or currently hosted itch build.

## History and civics

| Game | Explore | Play | Source |
| --- | --- | --- | --- |
| Crossroads: The Silk Roads | Explore trade and historical connections along the Silk Roads. | [Play](https://titans-forge.itch.io/crossroads-the-silk-roads) | [Source](https://github.com/titans-forge/Crossroads-The-Silk-Roads) |
| Titans of War: Revolution | Balance command, logistics, political legitimacy, and alliances during the American Revolution. | [Play](https://titans-forge.itch.io/titans-of-war-revolution) | [Source](https://github.com/titans-forge/Titans-of-War-Revolution) |
| Titans of War: Caesar | Explore Roman leadership and strategic trade-offs through historical gameplay. | [Play](https://titans-forge.itch.io/titans-of-war-caesar) | [Source](https://github.com/titans-forge/Titans-of-War-Caesar) |
| Titans of War: Rise of Rome | Explore early Rome and the choices involved in building a republic. | [Play](https://titans-forge.itch.io/titans-of-war-rise-of-rome) | [Source](https://github.com/titans-forge/Titans-of-War-Rise-of-Rome) |
| Titans of War: Ashes of Nika | Rebuild Constantinople after the Nika revolt while balancing recovery, factions, finances, and imperial commitments. | [Play](https://titans-forge.itch.io/titans-of-war-ashes-of-nika) | [Source](https://github.com/titans-forge/Titans-of-War-Ashes-of-Nika) |
| Titans of War: Rome Reconquest | Explore the strategic pressures of Roman reconquest campaigns. | [Play](https://titans-forge.itch.io/titans-of-war-rome-reconquest) | [Source](https://github.com/titans-forge/Titans_of_War_Rome_Reconquest) |
| Build a Republic | Explore constitutional choices and the compromises involved in forming a republic. | [Play](https://titans-forge.itch.io/republic) | [Source](https://github.com/titans-forge/Build-a-Republic) |
| Titans of War: Civil War | Explore command and strategic choices during the American Civil War. | [Play](https://titans-forge.itch.io/titans-of-war-civil-war) | [Source](https://github.com/titans-forge/Titans_of_War) |

## Nature

| Game | Explore | Play | Source |
| --- | --- | --- | --- |
| Titans of Nature: Living Waters | Explore aquatic environments through a fishing and field-observation game. | [Play](https://titans-forge.itch.io/living-waters) | [Source](https://github.com/titans-forge/Titans-of-Nature-Living-Waters) |

## Space and science

| Game | Explore | Play | Source |
| --- | --- | --- | --- |
| Titans of Proxima | Manage a fictional Earth-Luna-Mars charter through infrastructure, research and launch windows. | [Play](https://titans-forge.itch.io/titans-of-proxima) | [Source](https://github.com/titans-forge/Titans-of-Proxima) |
| Titans of Luna | Build a lunar colony while balancing power, water, oxygen, food, and crew survival. | [Play](https://titans-forge.itch.io/titans-of-luna) | [Source](https://github.com/titans-forge/Titans-of-Luna) |
| Titans of Mars | Explore the resource and infrastructure trade-offs of a settlement on Mars. | [Play](https://titans-forge.itch.io/titans-of-mars) | [Source](https://github.com/JCapone83/Titans-of-Mars) |
| Ares: The Mars Survival Simulator | Explore survival and resource management on Mars; distinct from Titans of Mars. | [Play](https://titans-forge.itch.io/ares-the-mars-survival-simulator) | [Source](https://github.com/titans-forge/ares-strategy-engine) |

## Medical reasoning

| Game | Explore | Play | Source |
| --- | --- | --- | --- |
| Medical Mysteries | Fictional investigations; recovered published beta, not a clinical tool or medical advice. | [Play](https://titans-forge.itch.io/medical-mysteries) | [Source](https://github.com/titans-forge/Medical-Mysteries) |

Medical Mysteries is an exact native-JavaScript recovery of its published beta, not the missing original authoring workspace, generators or test suite. Its README documents that boundary. Proxima's existing charter concerns Luna and Mars, not an actual Proxima mission.

## Use thoughtfully

Games simplify history, ecosystems, settlement engineering, and medical reasoning. Their scores are game models, not validated scientific measurements, demonstrated learning outcomes, operational instructions, or clinical recommendations. Discuss assumptions and compare scenarios with appropriate sources.

Check each game's page for controls, accessibility, save behavior, and requirements. Do not submit personal information, student records, real medical cases, or browser-save exports in public issues.

## Source and media

This repository is a catalog, not a bundle of all game assets. See [the game licensing guide](LICENSING.md) for Forge Game Hosting License 1.0, preserved MIT grants, and the Titans of Mars exception. Each game retains its own release checkpoints and media-rights notices. Public visibility or a free play link does not grant blanket redistribution rights. Screenshots are intentionally omitted until a specific selection is cleared.

## Maintaining the catalog

`games.json` is the source of truth. Run `python3 tools/catalog.py --write` after an approved inventory change, then `python3 -m unittest discover -s tests` and `python3 tools/catalog.py --check`. Network and browser gameplay checks are separate release steps.

Inventory prepared 2026-09-30. Titles and play links were reconciled against the public itch profile; new GitHub destinations are not claimed until publication is verified.
