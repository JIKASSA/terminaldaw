"""
TerminalDAW — Claude-powered music terminal
Type what you want to hear, Claude plays it through Ableton/Serum.
"""

import os
import time
import anthropic
from pythonosc import udp_client

client = udp_client.SimpleUDPClient('127.0.0.1', 9000)
ai = anthropic.Anthropic()

NOTE_NAMES = {
    'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11
}

def parse_note(s):
    s = s.lower().strip()
    try:
        return int(s)
    except ValueError:
        pass
    if s[0] in NOTE_NAMES:
        base = NOTE_NAMES[s[0]]
        i = 1
        if i < len(s) and s[i] in ('#', 'b'):
            base += 1 if s[i] == '#' else -1
            i += 1
        octave = int(s[i]) if i < len(s) else 4
        return base + (octave + 1) * 12
    raise ValueError(f"Unknown note: {s}")

def play_sequence(notes):
    for note in notes:
        pitch = parse_note(note['note'])
        vel = note.get('velocity', 100)
        dur = note.get('duration', 500)
        delay = note.get('delay', 0)
        if delay:
            time.sleep(delay / 1000)
        client.send_message('/note', [pitch, vel, dur])
        print(f"  ♪ {note['note']} (midi={pitch}) vel={vel} dur={dur}ms")

SYSTEM = """You are a music composition assistant controlling Ableton Live via OSC.
When the user describes music, respond with ONLY a JSON array of note objects.
Each note: {"note": "c4", "velocity": 100, "duration": 500, "delay": 0}
- note: note name like c4, d#3, eb5, or MIDI number
- velocity: 1-127
- duration: milliseconds the note holds
- delay: milliseconds to wait BEFORE playing this note (for rhythm/spacing)
Keep sequences under 16 notes. No explanation, just JSON."""

def ask_claude(prompt):
    print("  thinking...")
    msg = ai.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )
    import json, re
    text = msg.content[0].text.strip()
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return json.loads(text)

print("TerminalDAW — type what you want to hear")
print("Examples: 'play a sad melody', 'dark dnb bass line', 'c major arpeggio fast'")
print("Type 'quit' to exit\n")

while True:
    try:
        prompt = input("> ").strip()
        if not prompt:
            continue
        if prompt.lower() in ('quit', 'exit', 'q'):
            break
        notes = ask_claude(prompt)
        print(f"  playing {len(notes)} notes...")
        play_sequence(notes)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"  error: {e}")

print("bye")
