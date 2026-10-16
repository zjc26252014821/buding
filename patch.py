#!/usr/bin/env python3
import struct, sys
from pathlib import Path
import subprocess

p = Path(sys.argv[1])
d = bytearray(p.read_bytes())
# arm64e MangoPanelBackgroundPlayback.dylib, __TEXT file offset == VM address
# _PBUpdateTimer + 0xcc: `b.le 0x6fb0` after thermalState > 1 check.
OFF = 0x6F54
OLD = 0x540002ED       # b.le +0xcc (thermalState <= 1 -> continue)
NEW = 0x14000017       # b 0x6fb0 (always continue playback path)
old = struct.unpack_from('<I', d, OFF)[0]
if old != OLD:
    raise SystemExit(f'Unexpected instruction at {OFF:#x}: {old:#x}, expected {OLD:#x}')
struct.pack_into('<I', d, OFF, NEW)
p.write_bytes(d)
print(f'patched {p}: {OFF:#x} {OLD:#010x} -> {NEW:#010x}')
