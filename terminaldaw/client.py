"""
TerminalDAW Client — core OSC bridge to Ableton Live
"""

from pythonosc import udp_client, dispatcher, osc_server
import time
import threading
import math

NOTE_NAMES = {
    'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11
}


def parse_note(s):
    s = str(s).lower().strip()
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


class TerminalDAW:

    def __init__(self, host='127.0.0.1', port=9000, bpm=174):
        self._osc = udp_client.SimpleUDPClient(host, port)
        self._bpm = bpm
        self._reply_port = 9001
        self._start_reply_server()
        self.sync_bpm()

    def _start_reply_server(self):
        """Listen on port 9001 for replies from Max/Ableton."""
        self._disp = dispatcher.Dispatcher()
        self._disp.set_default_handler(self._handle_reply)
        try:
            self._server = osc_server.ThreadingOSCUDPServer(
                ('127.0.0.1', self._reply_port), self._disp
            )
            t = threading.Thread(target=self._server.serve_forever, daemon=True)
            t.start()
        except Exception:
            self._server = None

    def _handle_reply(self, address, *args):
        if address == '/tempo' and args:
            self._bpm = float(args[0])
            print(f"  BPM synced: {self._bpm}")
        elif address == '/session_info' and args:
            self._bpm = float(args[0])
            print(f"  Session: BPM={args[0]} tracks={args[1] if len(args)>1 else '?'}")

    def sync_bpm(self):
        """Request current BPM from Ableton."""
        self._osc.send_message('/param', ['get_tempo'])
        time.sleep(0.1)
        return self

    def bpm(self, bpm):
        self._bpm = bpm
        return self

    def _s(self, divisions=2):
        return (60 / self._bpm) / divisions

    def note(self, pitch, velocity=100, duration_ms=500):
        midi = parse_note(pitch)
        self._osc.send_message('/note', [midi, velocity, duration_ms])
        time.sleep(duration_ms / 1000)
        self._osc.send_message('/note', [midi, 0, 0])
        return self

    def note_on(self, pitch, velocity=100):
        self._osc.send_message('/note', [parse_note(pitch), velocity, 10000])
        return self

    def note_off(self, pitch):
        self._osc.send_message('/note', [parse_note(pitch), 0, 0])
        return self

    def all_notes_off(self):
        for p in range(128):
            self._osc.send_message('/note', [p, 0, 0])
        return self

    def set_param(self, track, device, param, value):
        self._osc.send_message('/param', ['set_param', track, device, param, float(value)])
        return self

    def list_params(self, track, device):
        self._osc.send_message('/param', ['list_params', track, device])
        return self

    def sweep_param(self, track, device, param, start=0.0, end=1.0, duration=2.0, steps=50):
        for i in range(steps + 1):
            val = start + (end - start) * (i / steps)
            self._osc.send_message('/param', ['set_param', track, device, param, float(val)])
            time.sleep(duration / steps)
        return self

    def wobble_param(self, track, device, param, center=0.5, depth=0.2, rate=3.5, duration=4.0):
        stop = threading.Event()
        def _run():
            t = 0
            while not stop.is_set():
                val = center + depth * math.sin(t * rate)
                val = max(0.0, min(1.0, val))
                self._osc.send_message('/param', ['set_param', track, device, param, float(val)])
                t += 0.05
                time.sleep(0.03)
        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        time.sleep(duration)
        stop.set()
        thread.join()
        return self

    def play_sequence(self, sequence, subdivision=8):
        step = self._s(subdivision)
        for item in sequence:
            if item[0] is None:
                time.sleep(step * item[2] if len(item) > 2 else step)
            else:
                pitch, vel = item[0], item[1]
                steps = item[2] if len(item) > 2 else 1
                dur = step * steps
                self._osc.send_message('/note', [parse_note(pitch), vel, int(dur * 0.75 * 1000)])
                time.sleep(dur * 0.75)
                self._osc.send_message('/note', [parse_note(pitch), 0, 0])
                time.sleep(dur * 0.25)
        return self
