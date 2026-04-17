# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TkRadio is a Tkinter-based Internet Radio Player that uses Selenium to automate Firefox for audio playback from ~79,500 stations. It runs on **Raspberry Pi 5** (primary target, with 5" touchscreen + rotary encoder), **Windows 11** (secondary, with AI commentary), and **macOS** (tertiary, behaves like Windows but with platform-specific visual tweaks).

## Running the Application

```bash
# Windows
py RadioSelenium.py
# or with pythonw.exe for no console window

# Raspberry Pi
python3 RadioSelenium.py

# macOS (run from terminal, not VS Code F5 — debugpy adds noticeable overhead)
.venv/bin/python RadioSelenium.py
```

**Dependencies:** `selenium`, `pillow`, `requests`, `beautifulsoup4`, `lxml`, `psutil`, `openai` (non-RPi only). RPi also uses `RPi.GPIO`. Requires Firefox and geckodriver installed. macOS additionally needs Homebrew's `python-tk@3.14` (or matching) for Tkinter bindings.

## Architecture

**Single-file application:** Everything lives in `RadioSelenium.py` (~3,500 lines). No package structure, no test framework.

### Platform Detection

The script detects the platform at startup:
- `GPIO`: set by attempting `import RPi.GPIO` (None on non-RPi)
- `IS_RPI = GPIO is not None`
- `IS_MACOS = sys.platform == "darwin" and not IS_RPI`
- `IS_WINDOWS = not IS_RPI and not IS_MACOS` (default / fallback branch — all original Windows code paths key off `GPIO` / `not GPIO` and are unchanged)

Controls:
- Window geometry: `800x455` (RPi) vs `800x861` (Windows and macOS)
- Preset grid: 54 buttons (6x9) on RPi, 108 (12x9) on Windows/macOS
- Input: rotary encoder (GPIO pins CLK=2, DT=3, SW=4) on RPi vs mouse/keyboard
- Features: Bluetooth/Wi-Fi setup (RPi), AI commentary (Windows; available on macOS when `OPENAI_API_KEY` is set, otherwise the button shows a warning)
- macOS-only additive visual tweaks via `_mac_btn_normal/_focused/_pressed/_active_toggle` helpers (all no-ops on Windows/RPi). Aqua ignores `bg=`/`relief=` on `tk.Button`, so focus/press state is simulated via `highlightbackground` + `highlightthickness`. Top-row buttons get a narrower font + repositioning, and text widgets get an explicit border. Shift-Tab is explicitly bound to `focus_prev` on macOS to short-circuit slow default traversal.

### Station Database (`AllRadioStations.csv`)

CSV with 7 columns: `LongName, StationLogoName, StationFunction, nNum, sPath, sClass, nType`. The first 2 characters of `LongName` encode the country code. `StationFunction` maps to a driver function via `function_map` dictionary.

### Station Drivers

9 driver functions (`Radio1`–`Radio7`, `Commercial1`, `Commercial2`) handle different website layouts. All follow the same pattern: **navigate** → **prime** (click play) → **fetch images** → **parse text** → **return `*`-separated string**. Shared helpers prefixed with `_` handle common operations (navigation, image download/display, BeautifulSoup parsing).

See `README_StationDrivers.md` for the full driver architecture and how to add new drivers.

### Shared Helper Functions

Extracted helpers reduce duplication across the codebase:
- `_update_text_box(text_str)` — write `*`-delimited text into the main text box
- `_show_blank_images()` — reset both logo and program image to blank
- `_clear_ai_text_box()` — clear the AI panel (Windows only)
- `_schedule_poll(fromCombobox)` — schedule the next polling refresh
- `_show_http_error(event, station_name, e)` — display HTTP errors in text box
- `_place_button_at_grid(button_widget, i, y_offset)` — position a preset button by grid index

### Central Dispatcher

`on_select(event, fromCombobox)` is the core function — triggered by combobox selection or preset button click. It reads the CSV row, resolves the driver via `function_map`, and calls it. Optional polling re-invokes this every ~10 seconds to refresh program info.

### GUI Components

- **`CustomCombobox`** — Custom dropdown for 79,500+ stations with keyboard navigation
- **Preset grid** — Buttons with cached thumbnail images (`Images/button0.png`–`button107.png`)
- **Logo/artwork labels** — Station logo (160x160) + program artwork (square or rectangular)
- **Text boxes** — "Now Playing" info + AI commentary (Windows)

### Firefox Browser Management

Runs headless Firefox via Selenium. Per-platform profiles in `./firefoxProfileWindows`, `./firefoxProfileRPI5`, and `./firefoxProfileMacOS`. On macOS `firefox_options.binary_location` is set to `/Applications/Firefox.app/Contents/MacOS/firefox` to bypass the Homebrew shell wrapper. Auto-restarts every 3600 seconds (`RegularRestart()`) to prevent memory leaks. Stale geckodriver processes cleaned up via `psutil` — the kill branch matches `geckodriver` (no `.exe`) on both RPi and macOS; Windows branch still matches `geckodriver.exe`.

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
