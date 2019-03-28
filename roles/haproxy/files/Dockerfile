FROM haproxy:1.9-alpine

RUN set -exo pipefail \
    && apk add --no-cache \
        rsyslog \
    && apk del syslog-ng \
    && mkdir -p /etc/rsyslog.d \
    && mkdir -p /usr/local/etc/haproxy \
    && touch /var/log/haproxy.log \
    && ln -sf /dev/stdout /var/log/haproxy.log

COPY docker-entrypoint.sh /
COPY rsyslog.conf /etc/rsyslog.d/
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY dschallenge.pem /usr/local/etc/haproxy/dschallenge.pem

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]

CMD ["-f", "/usr/local/etc/haproxy/haproxy.cfg"]
