# TkRadio — Selenium-driven Internet Radio UI (Windows 11 & Raspberry Pi 5)

**TkRadio** is a Python/Tkinter app that gives you a fast, keyboard-/encoder-friendly UI for streaming and browsing internet radio.  
It runs in two modes:

- **Windows 11 mode** (no GPIO): adds an OpenAI “AI” panel that summarizes the currently selected station.
- **Raspberry Pi 5 mode** (with GPIO rotary encoder + push button): optimized for a 5″ screen; includes on-device Wi-Fi and Bluetooth pairing.

Under the hood it uses **Firefox + Selenium** to open each station’s “Listen Live” page, click the right buttons, and scrape now-playing info and images.

---

## Highlights

- 79k+ stations supported via `AllRadioStations.csv` (plus presets/playlist buttons).
- Two rich image areas: **station logo** and **program/presenter** artwork.
- **Polling**: auto-refreshes program text/artwork every _N_ seconds while streaming.
- **Resilience**: scheduled Firefox restarts to avoid memory leaks; geckodriver cleanup.
- **Playlist grid** (108 buttons): insert/delete/replace stations, with per-button icons.
- **Raspberry Pi 5 UX**: rotary encoder scroll + push = “Enter”, Bluetooth pairing, Wi-Fi connect.
- **Windows AI panel**: optional OpenAI summary/history table of the current station.
- **All state is persisted** across runs (last station, playlist, logs, poll/bluetooth status).

---

## Repository & entry point

- Repo: `https://github.com/namor5772/TkRadio`
- Script: `RadioSelenium.py` (run it from the repo folder)

---

## Requirements

### Python & libraries
- Python 3.10+ recommended
- Install Python packages:
  ```bash
  pip install selenium pillow beautifulsoup4 requests psutil lxml openai
  ```
  *(The `openai` package is only used in Windows mode.)*

### Browser & driver
- **Firefox** (desktop on Windows, `firefox`/`firefox-esr` on Raspberry Pi)
- **geckodriver** on `PATH`
  - Windows: download geckodriver and put it on PATH (or alongside the script)
  - Raspberry Pi OS:
    ```bash
    sudo apt-get update
    sudo apt-get install -y firefox-esr geckodriver
    ```

### Raspberry Pi 5 only (for the on-device features)
- Rotary encoder + push button wired to:
  - `CLK_PIN=2`, `DT_PIN=3`, `SW_PIN=4` (BCM numbering)
- System tools used by the app:
  ```bash
  sudo apt-get install -y network-manager bluez rfkill wireless-tools
  ```
  - `nmcli`, `bluetoothctl`, `rfkill`, `iwlist` must be available (the app calls them).
  - The app uses `sudo` for some of these commands; ensure your user can run them.

### Directory layout (relative to `RadioSelenium.py`)
- `Images/` — required image assets & per-button icons (e.g., `Blank.png`, `ABC_faint.png`, `button0.png`…`button107.png`, and station logo PNGs).
- Two Firefox profile folders (the app points Selenium at them):
  - Windows: `./firefoxProfileWindows`
  - Pi: `./firefoxProfileRPI5`
  *(They can be empty; Firefox will populate them on first run.)*
- Data files created/used at runtime:
  - `AllRadioStations.csv` — **the** master station list (see schema below).
  - `savedRadioStation.txt` — remembers the last played playlist button index.
  - `playlist.txt` — your 108 preset buttons (name + index into `AllRadioStations.csv`).
  - `StationLogs.txt` — your saved station/program notes (and AI text in Windows).
  - `bluetooth.txt` — BT on/off + last paired device (Pi mode).
  - `pollflag.txt` — polling on/off toggle.

> Tip: The repo contains starter content for `Images/` and the CSV; don’t rename the folder.

---

## Install & Run

### Windows 11
```bash
git clone https://github.com/namor5772/TkRadio
cd TkRadio
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt  # or install packages listed above
python RadioSelenium.py
```

Optional (Windows AI panel):
```powershell
$env:OPENAI_API_KEY="sk-..."  # set your key before launching
```

### Raspberry Pi 5 (5″ screen)
```bash
git clone https://github.com/namor5772/TkRadio
cd TkRadio
python3 -m venv .venv
source .venv/bin/activate
pip install selenium pillow beautifulsoup4 requests psutil lxml
sudo apt-get install -y firefox-esr geckodriver network-manager bluez rfkill wireless-tools
python3 RadioSelenium.py
```

---

## Using TkRadio

### The main window (common)
- **Combobox** (top-left): pick a station from `AllRadioStations.csv`, press **Enter** to start streaming.
- **Station logo** (left) + **Program image** (right): updates after the stream starts.
- **Text panel**: station URL, name, “Live now” data, now-playing details, and status/errors.

### Playlist grid (108 buttons)
- **Insert**: highlight a playlist button, choose a station in the combobox, press **Insert** → the button stores that station and gets its logo.
- **Play**: focus a button and press **Enter**.
- **Delete**: focus a button and press **Delete** to clear it.
- **Move focus**: arrow keys move across the 9×12 grid (wrapping behavior implemented).

### Top row actions (Windows mode)
- **RND** — pick a random station into the combobox and start it.
- **DEL** — remove the currently selected combobox station from the master CSV and rewrite presets accordingly.
- **SAVE** — append the current text panel (and AI text if any) to `StationLogs.txt`.
- **AI** — sends the current text panel as context to the OpenAI API and renders a clean summary + a 2-column table (“Feature”/“Description”).
- **VIEW** — toggle between **playlist grid view** and **full program/text view**.
- **+ (poll toggle)** — turns periodic scraping on/off (writes to `pollflag.txt`).

### Raspberry Pi 5 mode (GPIO + 5″ screen)
- **Rotary encoder**:
  - Rotate to step through a bank of “virtual keys” (displayed along the top).
  - Press to **send** that key to the focused widget (e.g., the combobox or text area).
- **Setup panel** (press the **+** button in the title row):
  - **Bluetooth**: toggle BT on/off, scan for devices, pair/connect (stores `bluetooth.txt`), and reconnect to last device.
  - **Wi-Fi**: scan visible SSIDs, connect with saved credentials, or enter a password.
  - **Polling**: toggle program/presenter auto-refresh.

> Notes:
> - When **Polling** is ON, TkRadio re-runs `on_select()` every *refreshTime* seconds (default 10s) to fetch text/artwork.
> - To avoid “Selenium drift”, a **RegularRestart** triggers a clean Firefox restart every *resetTime* seconds (default 3600s). Streaming resumes automatically.

---

## Station catalog (`AllRadioStations.csv`)

Each row defines a station and how to start it:

```
[LongName, StationLogoName, StationFunction, nNum, sPath, sClass, nType]
```

- **LongName**: display name; first two chars are used as a country “code”.
- **StationLogoName**: used to find an image `Images/<StationLogoName>.png`.
- **StationFunction**: one of:
  - `Radio1`..`Radio7`: ABC network variants (different page layouts).
  - `Commercial1`: iHeart + Smooth/Nova.
  - `Commercial2`: radio-australia.org and similar aggregator pages.
- **nNum/sPath/sClass/nType**: parameters the function uses to:
  - open the correct URL (`sPath`),
  - press the right “Listen” button,
  - scrape the correct text nodes (`sClass`) and program image path,
  - apply function-specific behavior (`nNum`, `nType`).

**Example** *(conceptual)*:
```csv
"ABC Classic2","ABC_Classic2","Radio1","7","https://www.abc.net.au/listen/live/classic2","","0"
```

### How the CSV is loaded
- The app maps the function name string (e.g., `"Radio3"`) to the actual Python function via `function_map`, then builds `aStation[]`.
- On Windows startup it also creates a string list for the combobox labels.

> You can remove a station line at runtime using **DEL** (Windows): the app rewrites the CSV and shifts any preset indices that pointed past the deleted row.

---

## App internals (structure & logic)

### Core flow
- **Selenium setup**  
  The app launches Firefox in headless mode with a fixed profile folder:
  - Windows: `./firefoxProfileWindows`
  - Pi: `./firefoxProfileRPI5`
- **on_select(event, fromCombobox)**  
  The central dispatcher. It:
  1. Reads the chosen station (from combobox or preset).
  2. Clears images, prints a “Please be patient” message.
  3. Runs the station’s **StationFunction** (`Radio1`..`Commercial2`) which:
     - opens a blank page to “clean” state,
     - opens the station page,
     - presses the correct *Listen* button (XPaths / `ActionChains`),
     - fetches now-playing text & artwork (BeautifulSoup over page HTML),
     - saves/loads a logo to `Images/<StationLogoName>.png`,
     - returns a `*`-separated text bundle (URL, title, program text…).
  4. Renders text and images, optionally schedules another `on_select()` (polling).
  5. Persists the last played preset (`savedRadioStation.txt`).

- **RegularRestart() & RestartFirefoxAndLastStation()**  
  Close browser, **kill geckodriver** PIDs (via `psutil`), relaunch Firefox, and resume streaming the last station.

- **Commercial2** (advanced)  
  Handles pages that open an extra window/tab for playback; detects whether streaming is working by introspecting SVG path state; can create a throwaway tab to download a remote image if needed, then closes it.

- **CustomCombobox**  
  Fully custom widget: `Up/Down`, `PgUp/PgDn`, `Enter`, `Esc`, with a borderless dropdown `Toplevel` + `Listbox`. Helps on small screens and with encoder controls.

- **GPIO path**  
  If `RPi.GPIO` imports successfully, the app:
  - Sets up interrupts for the encoder pins.
  - Converts rotations to index changes and the push to a `<Key-*>` event into the focused widget (the “virtual key row” shows which key will be sent next).

- **State files**
  - **Playlist**: `playlist.txt` keeps `108 × [name, index]` pairs (index into `aStation`).
  - **Poll**: `pollflag.txt` drives the periodic re-scrape toggle.
  - **Bluetooth**: `bluetooth.txt` stores ON/OFF and the last paired MAC/name.
  - **Logs**: `StationLogs.txt` accumulates saved text and (Windows) AI summaries.

- **Windows AI thread**
  - The **AI** button captures the text panel, calls OpenAI Chat Completions (model `gpt-4.1`) in a background thread, then renders the result into the AI panel. (Set `OPENAI_API_KEY` to enable.)

---

## Keyboard & controls

- **Combobox**: `Enter` to stream, `Up/Down` to move, `PgUp/PgDn` to jump.
- **Playlist buttons**: `Enter` to play, `Insert` to assign current combobox station, `Delete` to clear, `Arrows` to navigate the grid.
- **Text panels**: `Shift+Tab` is mapped properly across platforms.
- **Raspberry Pi**: Use the encoder to scroll/select; press to “type” the chosen virtual key into the focused widget.

---

## Troubleshooting

- **“Firefox/geckodriver not found”**: Ensure both are installed and on PATH.
- **No images / broken logos**: Make sure `Images/` exists and contains `Blank.png`. The app will save per-station logos on the fly where possible.
- **“Streaming is not working” text**: Some sites geo-block or change markup. Try again later; consider increasing `needSleep` or turning **Polling** off.
- **Bluetooth/Wi-Fi issues (Pi)**: The app shells out to `bluetoothctl`, `nmcli`, `rfkill`, and `iwlist`. Confirm these tools work from the terminal with your permissions.

---

## Extending the station list

1. Add a new row to `AllRadioStations.csv`.
2. Pick the appropriate **StationFunction** and fill its parameters:
   - For ABC variants, prefer `Radio1`..`Radio7` with the right `nNum` and XPaths already coded.
   - For iHeart / Smooth / Nova, use `Commercial1` with the right `nType`.
   - For radio-australia.org & similar, use `Commercial2`.
3. Drop a logo PNG into `Images/` named exactly as `StationLogoName + ".png"` (or let the app try to fetch one, where supported).

---

## Notes on site automation

TkRadio uses Selenium to drive public “Listen Live” pages exactly as a human would. Respect the sites’ terms of use; don’t hammer pages (Polling exists, but use sensible intervals).

---

## License & contributions

See the repository for license information. PRs that add stations, improve selectors, or enhance the Pi UX are very welcome.
