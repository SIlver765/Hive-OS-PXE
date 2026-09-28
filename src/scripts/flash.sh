#!/bin/sh
# Runs on the rig inside the Alpine netboot RAM environment (installed as /etc/local.d/hive-flash.start).
# Streams the Hive OS image to the target disk, then writes rig.conf + optional static network config
# onto the image's FAT config partition and reboots into the new install.

log() { echo "[hive-flash] $*" | tee /dev/console; }

for a in $(cat /proc/cmdline); do
  case $a in
    hive_server=*) SRV=${a#hive_server=} ;;
    hive_mac=*)    MAC=${a#hive_mac=} ;;
  esac
done
[ -n "$SRV" ] && [ -n "$MAC" ] || { log "missing hive_server/hive_mac on kernel cmdline"; exit 1; }

report() { wget -q -O /dev/null "$SRV/api/report?mac=$MAC&status=$1&msg=$(echo "$2" | tr ' ' _)" 2>/dev/null; }
fail() { log "FAILED: $*"; report failed "$*"; log "rebooting in 60s"; sleep 60; reboot -f; }

# network: initramfs did ip=dhcp, but wait for the server and retry DHCP on any NIC if needed
i=0
until wget -q -O /dev/null "$SRV/api/ping"; do
  i=$((i+1)); [ $i -gt 30 ] && fail "cannot reach $SRV"
  for n in /sys/class/net/e*; do udhcpc -q -n -i "$(basename "$n")" >/dev/null 2>&1; done
  sleep 2
done

wget -q -O /tmp/flash.env "$SRV/api/config/$MAC/flash.env" || fail "no flash.env for $MAC (rig not registered?)"
. /tmp/flash.env
[ -n "$IMAGE" ] || fail "no image selected on server"

apk add -q util-linux >/dev/null 2>&1   # blockdev/partx; ignore failure, we fall back below
modprobe vfat 2>/dev/null; modprobe nls_cp437 2>/dev/null; modprobe nls_utf8 2>/dev/null

# target disk: explicit, else the smallest non-removable disk >= 7 GB
if [ -z "$TARGET_DISK" ]; then
  best=""; bestsz=0
  for d in /sys/block/*; do
    n=$(basename "$d")
    case $n in loop*|ram*|sr*|zram*|dm-*|nbd*|fd*) continue ;; esac
    [ "$(cat "$d/removable" 2>/dev/null)" = 0 ] || continue
    sz=$(( $(cat "$d/size") / 2048 ))   # MiB
    [ "$sz" -ge 7000 ] || continue
    if [ -z "$best" ] || [ "$sz" -lt "$bestsz" ]; then best=$n; bestsz=$sz; fi
  done
  [ -n "$best" ] && TARGET_DISK=/dev/$best
fi
[ -b "$TARGET_DISK" ] || fail "no suitable target disk (got '$TARGET_DISK')"

log "flashing $IMAGE -> $TARGET_DISK"
report start "flashing $IMAGE to $TARGET_DISK"
for p in ${TARGET_DISK}?* ${TARGET_DISK}p?*; do umount "$p" 2>/dev/null; done

case $IMAGE in
  *.xz)  DEC="xz -dc" ;;
  *.gz)  DEC="gunzip -c" ;;
  *.zst) apk add -q zstd >/dev/null 2>&1; DEC="zstd -dc" ;;
  *)     DEC="cat" ;;
esac
( set -o pipefail; wget -q -O- "$SRV/image/$IMAGE?mac=$MAC" | $DEC | dd of="$TARGET_DISK" bs=4M conv=fsync 2>/dev/null ) \
  || fail "image write failed (download or decompress error)"
sync

# re-read partition table
blockdev --rereadpt "$TARGET_DISK" 2>/dev/null || partx -u "$TARGET_DISK" 2>/dev/null
mdev -s; sleep 3

# find the FAT config partition (has rig-config-example.txt at its root)
CONF=""
for p in ${TARGET_DISK}?* ${TARGET_DISK}p?*; do
  [ -b "$p" ] || continue
  mkdir -p /mnt/hive
  if mount -t vfat "$p" /mnt/hive 2>/dev/null; then
    if [ -f /mnt/hive/rig-config-example.txt ] || [ -d /mnt/hive/network ]; then CONF=$p; break; fi
    umount /mnt/hive
  fi
done
[ -n "$CONF" ] || fail "flashed, but could not find the Hive config partition"

wget -q -O /mnt/hive/rig.conf "$SRV/api/config/$MAC/rig.conf" || fail "cannot fetch rig.conf"
mkdir -p /mnt/hive/network
if wget -q -O /tmp/net "$SRV/api/config/$MAC/20-ethernet.network"; then
  cp /tmp/net /mnt/hive/network/20-ethernet.network
  log "static network config written"
fi
sync; umount /mnt/hive

report done "flashed $IMAGE to $TARGET_DISK, config on $CONF"
log "done, rebooting"
sleep 3
reboot -f
