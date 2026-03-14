#!/bin/bash
# TerminalDAW Installer
# Installs Python package + copies Ableton device to user library

set -e

echo "TerminalDAW Installer"
echo "====================="

# Install Python package
echo "Installing Python package..."
pip3 install -e .

# Copy Ableton device
ABLETON_DIR="$HOME/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect"
mkdir -p "$ABLETON_DIR"

echo "Copying Ableton device to: $ABLETON_DIR"
cp ableton/TerminalDAW.amxd "$ABLETON_DIR/"
cp ableton/lom_control.js "$ABLETON_DIR/"

echo ""
echo "Done! Next steps:"
echo "  1. Open Ableton Live"
echo "  2. In the browser: User Library → Presets → MIDI Effects → Max MIDI Effect"
echo "  3. Drag 'TerminalDAW' onto a MIDI track (before your instrument)"
echo "  4. Run: terminaldaw c4"
