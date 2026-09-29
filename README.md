# Hive OS PXE by Silver

Lean network-install server for Hive OS rigs (a small replacement for Hiveon OS Deploy / CloneDeploy): one Alpine container with
dnsmasq (proxy-DHCP + TFTP) and a stdlib-Python web app. No MySQL, no Apache.

## Layout
```
umbrel-app-store.yml          app store manifest (store id "HiveOSPXE"); required filename
HiveOSPXE-hive-os-pxe/        app folder = <store-id>-hive-os-pxe
  umbrel-app.yml              app manifest (UI port 8380); required filename
  docker-compose.yml          host networking, image reference
  icon.svg
src/                          image source (Dockerfile, server.py, ui.py, guide.py, scripts/flash.sh, dnsmasq.reference.conf)
tests/                        test-server.sh (run on the host machine), pxe-probe.py (run on any LAN machine)
.github/workflows/build.yml   builds amd64 + arm64 image to ghcr.io on tag v*
```

## Admin UI
Guide (plain-language step-by-step help with live progress and troubleshooting; opens after first login), Dashboard (live
server/rig status, per-rig flash progress, setup checklist), Rigs (add, import, edit, reflash, filter), Groups, Image (download by
link or drag-and-drop upload), Settings (IP override, port status, dnsmasq restart, config export).
The initial password is the one shown next to the app; a change is forced on first login. All input is validated because values
land in `rig.conf` / `flash.env`, which are sourced as shell. Pages refresh every 3 s; works on phones, light and dark.

## Ports
| Port | Proto | Purpose |
|---|---|---|
| 8380 | TCP | Admin UI through the platform app proxy (port 80 belongs to the host dashboard) |
| 8381 | TCP | Admin backend (behind the proxy) |
| 8382 | TCP | Rig-facing HTTP: iPXE script, netboot files, image, per-rig config. No login, LAN only |
| 67, 4011 | UDP | proxyDHCP / PXE boot server |
| 69 | UDP | TFTP |

## Publish
1. Create the GitHub repo `SIlver765/Hive-OS-PXE` and push this folder.
2. Tag `v1.0-Dev`; CI pushes `ghcr.io/silver765/hive-os-pxe:v1.0-Dev` (make the package public, then pin `@sha256:` in the compose file).
3. On the host: App Store, then the menu, then Community App Stores, and add the GitHub repo URL. Install "Hive OS PXE".

## First run
Open the app and follow the **Guide** tab. In short: reserve an IP for the host machine, add the Hive OS image, set the farm hash,
add rigs (name, MAC, optional IP), enable network boot in each rig's BIOS, power the rig on.

## How it works
dnsmasq proxy-DHCP points PXE clients at `undionly.kpxe` / `ipxe.efi` (TFTP). iPXE re-DHCPs and fetches `boot.ipxe` (TFTP stub),
which chains to `http://<server>:8382/boot.ipxe?mac=...`. For a pending rig that script boots the Alpine netboot kernel plus a
generated overlay running `flash.sh`, which streams image, `xz -dc`, `dd`, mounts the FAT config partition, writes `rig.conf` (and a
static network file if the rig has an IP), reports back and reboots. Deployed rigs and unknown MACs boot from their own disk.

## Known limits / to verify on real hardware
- Rigs need internet during flashing (Alpine `modloop` / `apk` come from dl-cdn.alpinelinux.org).
- The `pxe-service` + `boot.ipxe` handoff, the Alpine overlay bootstrap, and detection of Hive's FAT config partition are written
  from documentation and not yet run on a rig. `tests/test-server.sh` and `tests/pxe-probe.py` cover the server side.
- Admin login is the app's own; port 8382 has no auth by design (rigs cannot log in).
