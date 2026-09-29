#!/usr/bin/env python3
"""Broadcast a PXE DHCPDISCOVER (option 60 PXEClient) and print proxyDHCP replies.
Run on any Linux box on the same LAN as this machine: sudo python3 pxe-probe.py [arch]   (arch 0=BIOS, 7=UEFI x64)
A working proxy answers with a DHCPOFFER whose siaddr = server IP and file = undionly.kpxe / ipxe.efi."""
import os, socket, struct, sys, time
arch = int(sys.argv[1]) if len(sys.argv) > 1 else 0
mac = bytes.fromhex("02deadbeef01"); xid = os.urandom(4)
pkt = struct.pack("!BBBB4sHH4s4s4s4s16s64s128s4s", 1, 1, 6, 0, xid, 0, 0x8000, b"\0"*4, b"\0"*4, b"\0"*4, b"\0"*4, mac, b"", b"", b"\x63\x82\x53\x63")
opts = b"\x35\x01\x01" + b"\x3c\x09PXEClient" + b"\x5d\x02" + struct.pack("!H", arch) + b"\x37\x03\x01\x03\x06" + b"\xff"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(("", 68)); s.settimeout(1)
s.sendto(pkt + opts, ("255.255.255.255", 67)); end = time.time() + 5; found = 0
while time.time() < end:
    try: d, a = s.recvfrom(2048)
    except socket.timeout: continue
    if d[4:8] != xid: continue
    found += 1
    fn = d[108:236].split(bytes(1))[0].decode(errors='replace')
    o43 = b'+' in d[240:]
    print(f"offer from {a[0]}: siaddr={socket.inet_ntoa(d[20:24])} yiaddr={socket.inet_ntoa(d[16:20])} file={fn!r} has_opt43={o43}")
print("PASS" if found else "FAIL: no proxyDHCP answer"); sys.exit(0 if found else 1)
