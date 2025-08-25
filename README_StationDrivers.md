# Station Driver Patterns (Short Guide)

This README documents how the station “drivers” (functions `Radio1`…`Radio7` and commercial variants) are structured after the refactor, and how to add or maintain them without changing behaviour.

---

## 1) Big Picture

Each station driver follows the same high‑level flow:

1. **Navigate**: reset the browsing context (open a blank/refresh URL) then load the target page.
2. **Prime**: optionally select timezone or dismiss overlays (TAB/ENTER/UP/DOWN key sequences) and click the site’s “Play” or “Listen” button.
3. **Images**: capture and display the **station logo** (`label`) and the **program artwork** (`label2`), with consistent sizing and placement.
4. **Now‑Playing Text**: parse the DOM (via BeautifulSoup) for “live/now playing” and “synopsis” text, then normalize the string format (using the same “*” separators) for the GUI.
5. **Return**: return the now‑playing description string in the **exact format** that the app expects.

This keeps GUI behaviour identical on Windows 11 and Raspberry Pi 5.

---

## 2) Shared Helpers (single source of truth)

The common steps live in small utilities placed above the drivers:

- `_navigate_to_station(br, url, refresh_url)` – two‑step “clean & go” navigation.
- `_fetch_image_to(path, url)` – download any image (logo/program art) to disk.
- `_display_logo_from_file(path)` / `_display_logo_from_image(image)` – resize to `iconSize`, set `label`, and **if `addFlag` is True** also persist the resized button icon.
- `_display_program_image_square(path)` – crop to square and fit into `label2`.
- `_display_program_image_rect(path, width_px)` – rectangular resize into `label2`.
- `_lift_program_image_at(x, y, w, h)` – place program art and keep it above `text_box` if not `HiddenFlag`.
- `_soup_inner_html(element_or_driver)` – BeautifulSoup view of current content.
- `_trim_after(text, marker)` – tidy truncation helper for “*More”, “*Listen”, etc.

> **Important**: These helpers intentionally rely on the same **globals** used everywhere else (`label`, `label2`, `pathImages`, `iconSize`, `Xprog`, `X1`, `Xgap`/`Ygap*`, `HiddenFlag`, `addFlag`, `buttonIndex`, etc.). Behaviour is unchanged.

---

## 3) Driver Patterns (ABC family)

The ABC sites share structure but differ in selectors and geometry. The code keeps the former XPaths and timings intact. Key distinctions:

- **`Radio1` / `Radio6`** – classic ABC page: click the primary play button in the first column, program image in the right column. Program art displayed **square**.
- **`Radio2`** – timezone selection via keystrokes (TAB/ENTER/UP/DOWN), then play; header image used for program art and displayed **rectangular** (width computed from original aspect).
- **`Radio3`** – like `Radio2`, plus a derived `station_short` used to select the logo file (prefix before the second underscore). Program art displayed **square**.
- **`Radio4` / `Radio5`** – newer ABC page shell (different DOM): big “Listen Live” button; logo fetched from a link tile; program art square; slightly different placement (`Xgap2`/`Ygap2` etc.).
- **`Radio7`** – ABC Sport/Sport Extra/Cricket: bespoke selectors with a **blank** program image (no art available). Returns text from the selected sport card; cleans trailing “*Stop/*Listen”.

All of the above: timings (`time.sleep`), XPaths, and the returned text format are preserved 1:1.

---

## 4) Commercial Drivers

- **`Commercial1` / `Commercial2`** target iHeart/Nova/Smooth and Radio‑Australia style pages.
- They remain mostly bespoke because of varied sites (multiple tabs, late logo discovery, “Maybe streaming” states, alternative XPaths). Refactoring here should be done carefully and tested against multiple stations.

---

## 5) Dispatch Mapping

Stations are selected by name via a dictionary mapping (e.g., `'Radio3': Radio3`). **All driver functions must be defined *above* this mapping.** If the map references an undefined function at import time, Python raises `NameError`.

Tip: Keep helpers → drivers → mapping in that order.

---

## 6) Geometry & Globals

- Artwork sizes: `iconSize` for `label` (logo), and `(Xprog - X1)` square height for `label2` (program art).
- Placement uses `Xgap`/`Xgap2`/`Xgap3`, `Ygap2`/`Ygap3` and `X1` offsets.
- `HiddenFlag` prevents artwork placement calls; `addFlag` causes the logo to be saved to the current playlist button (`buttonIndex`).

These are historical invariants; do not change them without GUI testing on Win11 and RPi5.

---

## 7) Adding a New Station Pattern (ABC‑like)

1. **Clone a close sibling** (`Radio1`..`Radio6`) whose DOM structure matches.
2. Update only:
   - The XPaths for: play button, logo image (if needed), program image.
   - Any pre‑click keystrokes (timezone/overlay handling).
   - The geometry call to `_lift_program_image_at(...)` if the layout differs.
3. Ensure the **return string** follows the existing “*”‑separated format.
4. Register the function in the dispatch mapping **below** the definition.

> If the site has no reliable program art, use `Blank.png` (see `Radio7`).

---

## 8) Testing Checklist

- **Launch** both on Win11 and RPi5 (Firefox/Gecko versions may differ slightly).
- For each station:
  - Play starts, no unexpected alerts remain on screen.
  - Logo shows in `label`; if adding to playlist, the button icon is saved.
  - Program art appears in `label2` with correct size/placement, not hidden.
  - Now‑playing string looks identical to prior behaviour (same separators).
- **Edge cases**: ABC Classic2 placement, Sport/Sport Extra selection, Radio‑Australia pages with delayed stream availability.

---

## 9) Troubleshooting

- `NameError` for `RadioX`: move the function **above** the mapping.
- No artwork: confirm the image XPath and that `_fetch_image_to` succeeds.
- Wrong placement: adjust only the `_lift_program_image_at(...)` call;
  do **not** change shared geometry constants unless you test all stations.
- Keystroke flow fails: re‑check the TAB/ENTER/UP/DOWN counts for the page.

---

Keeping the patterns consistent in helpers reduces duplication and makes it safer to support more stations while preserving exactly the same runtime behaviour.
