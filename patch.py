#!/usr/bin/env python3
import struct, sys
from pathlib import Path
import subprocess

p = Path(sys.argv[1])
d = bytearray(p.read_bytes())
# arm64e MangoPanelBackgroundPlayback.dylib, __TEXT file offset == VM address.
# Patch both thermal gates:
# 1) PBUpdateTimer + 0xcc: b.le 0x6fb0, keeps periodic playback alive.
# 2) MGPBVideoView updatePlayback + 0xd4: b.gt 0x80ac, which records
#    the `thermal` playback state and selects the static-poster path.
PATCHES = [
    (0x6F54, 0x540002ED, 0x14000017),
    (0x7FD4, 0x540006CC, 0xD503201F),
]
for off, old, new in PATCHES:
    actual = struct.unpack_from('<I', d, off)[0]
    if actual != old:
        raise SystemExit(f'Unexpected instruction at {off:#x}: {actual:#x}, expected {old:#x}')
    struct.pack_into('<I', d, off, new)
    print(f'patched {p}: {off:#x} {old:#010x} -> {new:#010x}')
p.write_bytes(d)
