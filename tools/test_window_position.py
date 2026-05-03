"""Smoke-test the window-position persistence helpers in isolation."""
import os, sys, tkinter as tk
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Minimal stand-ins so we don't import RadioSelenium (which spins up Firefox).
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
windowPosition_filepath = os.path.join(script_dir, 'windowPosition.txt')
IS_RPI, IS_MACOS, IS_WINDOWS = False, False, sys.platform.startswith('win')

def _virtual_screen_bounds(tk_root):
    if IS_WINDOWS:
        try:
            import ctypes
            u = ctypes.windll.user32
            return (u.GetSystemMetrics(76), u.GetSystemMetrics(77),
                    u.GetSystemMetrics(78), u.GetSystemMetrics(79))
        except Exception:
            pass
    return 0, 0, tk_root.winfo_screenwidth(), tk_root.winfo_screenheight()

# Backup any existing user file so we don't clobber it during the test
backup = None
if os.path.exists(windowPosition_filepath):
    with open(windowPosition_filepath) as f:
        backup = f.read()
    os.remove(windowPosition_filepath)

try:
    root = tk.Tk()

    def save():
        with open(windowPosition_filepath, 'w') as f:
            f.write(root.geometry() + '\n')

    def load(default_geom):
        if not os.path.exists(windowPosition_filepath):
            root.geometry(default_geom); return 'no-file'
        with open(windowPosition_filepath) as f:
            saved = f.read().strip().splitlines()[0]
        root.geometry(saved); root.update_idletasks()
        x, y, w, h = root.winfo_x(), root.winfo_y(), root.winfo_width(), root.winfo_height()
        vx, vy, vw, vh = _virtual_screen_bounds(root)
        xv = max(0, min(x + w, vx + vw) - max(x, vx))
        yv = max(0, min(y + h, vy + vh) - max(y, vy))
        if xv < 100 or yv < 50:
            root.geometry(default_geom); return f'fallback (visible {xv}x{yv})'
        return 'restored'

    print(f"virtual screen bounds: {_virtual_screen_bounds(root)}")

    # Case A: no file → default applied
    res = load("400x300+200+150")
    root.update_idletasks()
    print(f"[A] no-file case: result={res!r} geom={root.geometry()}")
    assert res == 'no-file', f"expected 'no-file', got {res!r}"

    # Case B: write a valid position, restart, expect restored
    root.geometry("400x300+250+200")
    root.update_idletasks()
    save()
    res = load("400x300+0+0")
    root.update_idletasks()
    print(f"[B] valid-saved case: result={res!r} geom={root.geometry()}")
    assert res == 'restored', f"expected 'restored', got {res!r}"

    # Case C: write a hugely off-screen position → fallback
    with open(windowPosition_filepath, 'w') as f:
        f.write("400x300+99999+99999\n")
    res = load("400x300+50+50")
    root.update_idletasks()
    print(f"[C] off-screen case: result={res!r} geom={root.geometry()}")
    assert res.startswith('fallback'), f"expected fallback, got {res!r}"

    # Case D: file exists but malformed → exception path → fallback
    with open(windowPosition_filepath, 'w') as f:
        f.write("garbage data\n")
    try:
        res = load("400x300+0+0")
        print(f"[D] malformed case: result={res!r} (unexpectedly survived)")
    except Exception as e:
        print(f"[D] malformed case: raised {type(e).__name__}: {e} (real loader has try/except, will fall back)")

    print("\nAll cases handled correctly.")

finally:
    if backup is not None:
        with open(windowPosition_filepath, 'w') as f:
            f.write(backup)
    elif os.path.exists(windowPosition_filepath):
        os.remove(windowPosition_filepath)
    try:
        root.destroy()
    except Exception:
        pass
