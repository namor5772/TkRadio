# CLAUDE.md

## Project overview

TkRadio is a Python internet radio app (Tkinter + Selenium/Firefox) that runs on both Windows 11 and Raspberry Pi 5. One codebase — GPIO detection decides which mode. Access to ~79,500 stations. On Windows, an OpenAI-powered AI commentary panel is available.

## Key files

- `RadioSelenium.py` — the entire app (GUI, Selenium automation, station drivers, GPIO handling)
- `AllRadioStations.csv` — master station list (~9 MB). `function_map` column must match driver function names in code. Do not reorder/delete rows without adjusting playlists
- `playlist.txt` — saved user presets (54 on RPi, 108 on Windows)
- `savedRadioStation.txt`, `StationLogs.txt`, `bluetooth.txt`, `pollflag.txt` — runtime state files
- `Images/` — station logos, program art, preset button assets. Keep filenames and sizes stable
- `Hardware/` — PCB designs, station CSVs, scraping scripts, gcode files
- `firefoxProfileWindows/`, `firefoxProfileRPI5/` — Firefox profiles for Selenium (gitignored, keep stable)

## Dependencies

- Python 3.11+ with: `selenium`, `pillow`, `beautifulsoup4`, `requests`, `psutil`
- Windows-only: `openai` (requires `OPENAI_API_KEY` env var)
- RPi-only: `RPi.GPIO`
- Firefox + geckodriver on PATH

## Running

```sh
python RadioSelenium.py        # Linux/RPi
pythonw RadioSelenium.py       # Windows (hides console)
```

## Development rules

- Station drivers: follow patterns in `README_StationDrivers.md` — helpers above drivers, drivers above dispatch map. Preserve return string formats and geometry constants
- Do not wipe Firefox profile folders unless intentionally recreating them
- No automated tests — manual verification: run app, start a station, confirm logo/program art, check AI panel on Windows
- The repo lives in a OneDrive-synced directory; line-ending changes on vendored/binary files are expected noise — do not commit them
- Keep `.gitignore` up to date for browser runtime data and vendored libraries
