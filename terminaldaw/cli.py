"""
TerminalDAW CLI — play notes from the command line
Usage:
  terminaldaw c4
  terminaldaw f5 127 1000
  terminaldaw --all-off
"""

import sys
from .client import TerminalDAW, parse_note


def main():
    daw = TerminalDAW()
    args = sys.argv[1:]

    if not args:
        print("TerminalDAW v0.1.0")
        print("Usage: terminaldaw <note> [velocity] [duration_ms]")
        print("       terminaldaw --all-off")
        return

    if args[0] == '--all-off':
        daw.all_notes_off()
        print("all notes off")
        return

    pitch = args[0]
    velocity = int(args[1]) if len(args) > 1 else 100
    duration = int(args[2]) if len(args) > 2 else 500

    midi = parse_note(pitch)
    print(f"♪ {pitch} (midi={midi}) vel={velocity} dur={duration}ms")
    daw.note(pitch, velocity, duration)


if __name__ == '__main__':
    main()
