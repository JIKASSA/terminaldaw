"""
TerminalDAW — CLI note sender
Usage:
  python play.py 60          → C4, velocity 100
  python play.py 60 127      → C4, velocity 127
  python play.py 60 127 500  → C4, vel 127, 500ms
  python play.py c4          → note name shorthand
"""

from pythonosc import udp_client
import sys

NOTE_NAMES = {
    'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11
}

def parse_note(s):
    s = s.lower().strip()
    try:
        return int(s)
    except ValueError:
        pass
    # e.g. c4, d#3, eb4
    if s[0] in NOTE_NAMES:
        base = NOTE_NAMES[s[0]]
        i = 1
        if i < len(s) and s[i] in ('#', 'b'):
            base += 1 if s[i] == '#' else -1
            i += 1
        octave = int(s[i]) if i < len(s) else 4
        return base + (octave + 1) * 12
    raise ValueError(f"Unknown note: {s}")

client = udp_client.SimpleUDPClient('127.0.0.1', 9000)
args = sys.argv[1:]

if not args:
    print("Usage: python play.py <note> [velocity] [duration_ms]")
    sys.exit(1)

pitch = parse_note(args[0])
velocity = int(args[1]) if len(args) > 1 else 100
duration = int(args[2]) if len(args) > 2 else 500

import time
client.send_message('/note', [pitch, velocity, duration])
print(f"♪ note={pitch} vel={velocity} dur={duration}ms")
time.sleep(duration / 1000)
client.send_message('/note', [pitch, 0, 0])
