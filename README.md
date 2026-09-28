# Hive OS PXE by Silver - Umbrel community app store

Lean replacement for Hiveon OS Deploy (CloneDeploy): one Alpine container with dnsmasq (proxy-DHCP + TFTP)
and a stdlib-Python web app. No MySQL, no Apache.

## Layout
```
umbrel-app-store.yml          store id "HiveOSPXE"
HiveOSPXE-hive-os-pxe/               app dir = <store-id>-<app-name>
  umbrel-app.yml              manifest (UI port 8380)
  docker-compose.yml          host networking, image ref
src/                          image source (Dockerfile, server.py, ui.py, scripts/flash.sh, dnsmasq.reference.conf)
tests/                        test-umbrel.sh (run on Umbrel), pxe-probe.py (run on a LAN machine)
.github/workflows/build.yml   builds amd64+arm64 image to ghcr.io on tag v*
```

## Admin UI
Guide (plain-language step-by-step help with live progress and troubleshooting; opens after first login), Dashboard (live server/rig status, per-rig flash progress, setup checklist), Rigs (add, import, edit, reflash, filter), Groups,
Image (download by link or drag-and-drop upload), Settings (IP override, port status, dnsmasq restart, config export).
Login uses the Umbrel-shown password and forces a change on first use. All input is validated because values land in
`rig.conf` / `flash.env`, which are sourced as shell. Pages refresh themselves every 3 s; works on phones, light and dark.

## Ports
| Port | Proto | Purpose |
|---|---|---|
| 8380 | TCP | Admin UI via Umbrel app_proxy (port 80 belongs to the dashboard) |
| 8381 | TCP | Admin backend (behind app_proxy) |
| 8382 | TCP | Rig-facing HTTP: iPXE script, netboot files, image, per-rig config. Unauthenticated, LAN only |
| 67, 4011 | UDP | proxyDHCP / PXE boot-server |
| 69 | UDP | TFTP |

## Publish
1. Create the GitHub repo `SIlver765/Hive-OS-PXE` and push this folder.
2. Tag `v1.0-Dev`; CI pushes `ghcr.io/silver765/hive-os-pxe:v1.0-Dev` (make the package public, then pin `@sha256:` in the compose file like Triple-X).
3. Umbrel: App Store -> ... menu -> Community App Stores -> add the GitHub repo URL. Install "Hive OS PXE".

## First run
1. Give the Umbrel a static IP or router DHCP reservation.
2. Open the app, log in with the password shown in Umbrel, and set a new one (forced).
3. Image: paste the Hive OS `.img.xz` URL (or copy the file into `app-data/HiveOSPXE-hive-os-pxe/data/images/`), click Use.
4. Groups: set network, gateway, Hive API URL, farm hash. Rigs: add or import `name MAC [IP] [group]`.
5. Set rigs to network boot (BIOS or UEFI). Each pending rig flashes, gets `rig.conf` (+ static `network/20-ethernet.network`
   if an IP was given), reboots, and after reporting success boots from disk. Unknown MACs always boot locally.

## How it works
dnsmasq proxy-DHCP points PXE clients at `undionly.kpxe`/`ipxe.efi` (TFTP). iPXE re-DHCPs, gets `boot.ipxe` (TFTP stub) which chains to
`http://<umbrel>:8382/boot.ipxe?mac=...`. For a pending rig that script boots the Alpine netboot kernel + a generated overlay running
`flash.sh`, which streams image -> `xz -dc` -> `dd`, mounts the FAT config partition, writes config, reports back, reboots.

## Known limits / to verify on real hardware
- The rig needs internet during flashing (Alpine `modloop`/`apk` come from dl-cdn.alpinelinux.org).
- `pxe-service` + `boot.ipxe`, the Alpine overlay bootstrapping, and detection of Hive's FAT config partition are written from docs, not yet run on a rig.
- Admin auth: app_proxy auth is disabled because the app has its own login. Port 8382 has no auth by design (rigs can't log in).
