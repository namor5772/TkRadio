# TkRadio – agent notes

Quick context for future changes to this repo.

## What this app is
- Tkinter + Selenium internet radio for Windows 11 and Raspberry Pi 5 (one codebase, GPIO detection decides mode).
- Uses Firefox with a bundled profile (`firefoxProfileWindows/`, `firefoxProfileRPI5/`) and geckodriver.
- Station data lives in `AllRadioStations.csv` (~9 MB); playlist presets and last-station state are stored locally.

## Key files and folders
- `RadioSelenium.py` – main GUI + Selenium automation; Windows also shows an AI commentary panel if OpenAI is configured.
- `AllRadioStations.csv` – master station list; `function_map` strings here must match driver function names in code.
- `playlist.txt` (and `playlist_.txt` backup), `savedRadioStation.txt`, `StationLogs.txt`, `bluetooth.txt`, `pollflag.txt` – runtime state.
- `Images/` – station logos, program art, preset button assets (`button0.png`…`button107.png`, `Blank.png`, etc.). Keep filenames/sizes.
- `firefoxProfileWindows/`, `firefoxProfileRPI5/` – keep these stable unless you intentionally refresh the profiles.
- Docs: `README.md` (setup + hardware/software notes), `README_StationDrivers.md` (driver patterns/invariants).

## Dependencies
- Python 3.11+ with: `selenium`, `pillow` (PIL), `beautifulsoup4`, `requests`, `psutil`; `openai` (Windows AI panel); `RPi.GPIO` on Raspberry Pi.
- Firefox + geckodriver on PATH. A Linux aarch64 tarball is in the repo (`geckodriver-v0.36.0-linux-aarch64.tar.gz`); Windows driver lives in the user cache.
- OpenAI: set `OPENAI_API_KEY` in the environment to enable the Windows-only AI commentary.

## Running
- From repo root: `python RadioSelenium.py` (use `pythonw` on Windows to hide the console).
- Required alongside the script: `Images/`, `AllRadioStations.csv`, `playlist.txt`, `savedRadioStation.txt`, `bluetooth.txt`, `pollflag.txt`, `StationLogs.txt`, and the Firefox profile folder for your platform.
- Presets: 54 on Raspberry Pi, 108 on Windows. The `+` button opens the setup form on Raspberry Pi and toggles metadata polling on Windows.

## Development guardrails
- When touching station drivers, follow `README_StationDrivers.md`: keep helper functions above drivers, and drivers above the dispatch map; preserve return string formats and geometry constants.
- Changes to `AllRadioStations.csv` affect preset indices; avoid deleting/reordering rows unless you also adjust playlists/backups.
- Keep image asset names/sizes; the GUI expects existing button/logo files.
- Avoid wiping the Firefox profile folders unless you intend to recreate them; they hold settings that keep Selenium stable.

## Testing
- No automated tests. Manual check: run the app, start a station, confirm logo/program art placement, and (Windows) trigger the AI panel.
- Platform specifics: on Raspberry Pi ensure `RPi.GPIO`, PIL, Firefox, and geckodriver in `/usr/local/bin`; on Windows ensure Firefox + geckodriver and `OPENAI_API_KEY` if using AI.

## Troubleshooting hints
- Selenium startup issues: confirm Firefox + geckodriver on PATH and profile folder present.
- Missing logos/preset icons: verify `Images/` contents and preset indices.
- AI panel errors: check `OPENAI_API_KEY` and network access.
