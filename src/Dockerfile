FROM alpine:3.20
ARG ALPINE_NETBOOT=3.20.3
RUN apk add --no-cache python3 dnsmasq curl iproute2 \
 && mkdir -p /srv/tftp /srv/netboot /data \
 && curl -fsSL -o /srv/tftp/undionly.kpxe https://boot.ipxe.org/undionly.kpxe \
 && curl -fsSL -o /srv/tftp/ipxe.efi      https://boot.ipxe.org/ipxe.efi \
 && for f in vmlinuz-lts initramfs-lts modloop-lts; do \
      curl -fsSL -o /srv/netboot/$f https://dl-cdn.alpinelinux.org/alpine/v3.20/releases/x86_64/netboot-${ALPINE_NETBOOT}/$f; done \
 && apk del curl
WORKDIR /app
COPY server.py ui.py guide.py /app/
COPY scripts /app/scripts
ENV DATA_DIR=/data ALPINE_BRANCH=v3.20
EXPOSE 8381 8382
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD wget -q -O /dev/null http://127.0.0.1:8382/api/ping || exit 1
CMD ["python3", "/app/server.py"]
