#!/usr/bin/env bash
# Run ON the machine hosting the app (over SSH) after installing it.
# Verifies: static-ish address, host networking, listening PXE ports, TFTP + HTTP payloads.
# From another LAN machine, additionally run:  sudo python3 pxe-probe.py 0   (and 7)
set -u; APP=HiveOSPXE-hive-os-pxe; pass=0; fail=0
ok(){ echo "PASS  $*"; pass=$((pass+1)); }; bad(){ echo "FAIL  $*"; fail=$((fail+1)); }
IP=$(ip -4 route get 1.1.1.1 | sed -n 's/.* src \([0-9.]*\).*/\1/p'); echo "Server IP: $IP"
ip -4 addr show | grep -q "dynamic" && echo "NOTE  address is DHCP-assigned: make sure the router has a reservation for $IP"

C=$(docker ps --format '{{.Names}}' | grep "${APP}_server" | head -1)
[ -n "$C" ] && ok "container $C running" || { bad "container not running"; exit 1; }
[ "$(docker inspect -f '{{.HostConfig.NetworkMode}}' "$C")" = host ] && ok "network_mode=host" || bad "not host networking"

listen(){ ss -H -lnu "sport = :$1" | grep -q . ; }
for p in 67 69 4011; do listen $p && ok "UDP $p listening" || bad "UDP $p not listening (another DHCP/TFTP service on this host?)"; done
for p in 8380 8382; do ss -H -lnt "sport = :$p" | grep -q . && ok "TCP $p listening" || bad "TCP $p not listening"; done
ss -H -lnt "sport = :80" | grep -q . && echo "INFO  TCP 80 is used by the host dashboard (expected, we do not use it)"

T=$(mktemp -d)
curl -s --max-time 10 -o "$T/k" "tftp://$IP/undionly.kpxe" && [ -s "$T/k" ] && ok "TFTP undionly.kpxe ($(stat -c%s "$T/k") B)" || bad "TFTP undionly.kpxe"
curl -s --max-time 10 -o "$T/e" "tftp://$IP/ipxe.efi" && [ -s "$T/e" ] && ok "TFTP ipxe.efi" || bad "TFTP ipxe.efi"
curl -s --max-time 10 "tftp://$IP/boot.ipxe" | grep -q "chain http://$IP:8382" && ok "TFTP boot.ipxe chains to http://$IP:8382" || bad "TFTP boot.ipxe"
curl -sf "http://$IP:8382/api/ping" | grep -q ok && ok "HTTP :8382 ping" || bad "HTTP :8382 ping"
curl -sfI "http://$IP:8382/netboot/vmlinuz-lts" >/dev/null && ok "netboot kernel served" || bad "netboot kernel"
curl -sf "http://$IP:8382/boot.ipxe?mac=00:00:00:00:00:00" | grep -q sanboot && ok "unknown MAC -> boots local disk" || bad "unknown-MAC boot script"
curl -s -o /dev/null -w '%{http_code}' "http://$IP:8380/" | grep -qE '^(200|30[23])$' && ok "admin UI answers on :8380" || bad "admin UI on :8380"
docker logs "$C" 2>&1 | grep -q "dnsmasq" && ok "dnsmasq log lines present"
echo; echo "$pass passed, $fail failed"; exit $((fail>0))
