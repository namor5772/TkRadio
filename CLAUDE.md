# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TkRadio is a Tkinter-based Internet Radio Player that uses Selenium to automate Firefox for audio playback from ~79,500 stations. It runs on **Raspberry Pi 5** (primary target, with 5" touchscreen + rotary encoder) and **Windows 11** (secondary, with AI commentary).

## Running the Application

```bash
# Windows
py RadioSelenium.py
# or with pythonw.exe for no console window

# Raspberry Pi
python3 RadioSelenium.py
```

**Dependencies:** `selenium`, `pillow`, `requests`, `beautifulsoup4`, `psutil`, `openai` (Windows only). RPi also uses `RPi.GPIO`. Requires Firefox and geckodriver installed.

## Architecture

**Single-file application:** Everything lives in `RadioSelenium.py` (~3,700 lines). No package structure, no test framework.

### Platform Detection

The script detects RPi vs Windows at startup by attempting `import RPi.GPIO`. This controls:
- Window geometry: `800x455` (RPi) vs `800x861` (Windows)
- Preset grid: 54 buttons (6x9) vs 108 (12x9)
- Input: rotary encoder (GPIO pins CLK=2, DT=3, SW=4) vs mouse/keyboard
- Features: Bluetooth/Wi-Fi setup (RPi), AI commentary (Windows)

### Station Database (`AllRadioStations.csv`)

CSV with 7 columns: `LongName, StationLogoName, StationFunction, nNum, sPath, sClass, nType`. The first 2 characters of `LongName` encode the country code. `StationFunction` maps to a driver function via `function_map` dictionary.

### Station Drivers

9 driver functions (`Radio1`–`Radio7`, `Commercial1`, `Commercial2`) handle different website layouts. All follow the same pattern: **navigate** → **prime** (click play) → **fetch images** → **parse text** → **return `*`-separated string**. Shared helpers prefixed with `_` handle common operations (navigation, image download/display, BeautifulSoup parsing).

See `README_StationDrivers.md` for the full driver architecture and how to add new drivers.

### Central Dispatcher

`on_select(event, fromCombobox)` is the core function — triggered by combobox selection or preset button click. It reads the CSV row, resolves the driver via `function_map`, and calls it. Optional polling re-invokes this every ~10 seconds to refresh program info.

### GUI Components

- **`CustomCombobox`** — Custom dropdown for 79,500+ stations with keyboard navigation
- **Preset grid** — Buttons with cached thumbnail images (`Images/button0.png`–`button107.png`)
- **Logo/artwork labels** — Station logo (160x160) + program artwork (square or rectangular)
- **Text boxes** — "Now Playing" info + AI commentary (Windows)

### Firefox Browser Management

Runs headless Firefox via Selenium. Per-platform profiles in `./firefoxProfileWindows` and `./firefoxProfileRPI5`. Auto-restarts every 3600 seconds (`RegularRestart()`) to prevent memory leaks. Stale geckodriver processes cleaned up via `psutil`.

## State Files

- `playlist.txt` — Preset grid state (station name + index pairs)
- `savedRadioStation.txt` — Last played button index (restored on startup)
- `bluetooth.txt` — Bluetooth ON/OFF + last paired MAC/name (RPi)
- `pollflag.txt` — Polling toggle (0/1)
- `StationLogs.txt` — Play history and AI summaries

## Key Conventions

- Station logos go in `Images/{StationLogoName}.png`
- ~50+ global variables manage application state
- The `function_map` dictionary must be populated before CSV loading
- Audio plays through Firefox itself (not VLC or other players)
- RPi rotary encoder uses "virtual key banks" (16 keys/bank, 8 banks) to map rotation to keyboard events
