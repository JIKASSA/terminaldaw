# TerminalDAW

**Control Ableton Live from the terminal. No DAW interaction required.**

Built by Joshua VanZanella — March 2026.

---

## What It Does

TerminalDAW is a Python-to-Ableton bridge that lets you:

- **Play MIDI notes** from the command line
- **Automate any Ableton parameter** in real time (filter cutoff, resonance, LFO, drive — anything)
- **Compose riffs and progressions** programmatically
- **Control full sessions** via Ableton's Live Object Model (LOM)

All from a terminal. No mouse. No clicking. Pure code.

---

## Stack

```
Python (pythonosc)
    ↓ OSC UDP port 9000
Max for Live MIDI Effect
    ↓ route /note /param
noteout → Ableton MIDI
js lom_control.js → Live Object Model → any device parameter
```

---

## Requirements

- Ableton Live 11+
- Max for Live
- Python 3.x
- `pip install python-osc`

---

## Setup

1. Load `osc_receiver2.amxd` as a **Max MIDI Effect** on your MIDI track
2. Place `lom_control.js` in the same folder as the `.amxd`
3. Add your instrument (Serum, Operator, etc.) after the M4L device on the same track

---

## Play a Note

```bash
python3 play.py c4
python3 play.py f5 127 500
python3 play.py 77 100 1000
```

---

## Control Parameters via LOM

```python
from pythonosc import udp_client
osc = udp_client.SimpleUDPClient('127.0.0.1', 9000)

# List all parameters for track 0, device 2
osc.send_message('/param', ['list_params', 0, 2])

# Set Auto Filter frequency (param 1) to 50%
osc.send_message('/param', ['set_param', 0, 2, 1, 0.5])
```

---

## Example — Riff with Filter Automation

```python
python3 fminor_dnb.py
```

F minor DNB riff at 174 BPM with real-time HP filter wobble via LOM.

---

## Roadmap

- [ ] Claude API layer — describe music, get notes + parameters
- [ ] Loop mode with scene control
- [ ] Full preset generation (Serum 2 / Operator)
- [ ] Multi-track composition
- [ ] BPM sync with Ableton transport

---

## License

MIT License — Joshua Van Zanella, 2026.

---

*First known implementation of Claude-AI-driven terminal music composition with direct Ableton Live Object Model parameter control.*
