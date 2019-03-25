FROM haproxy:1.9-alpine
RUN mkdir -p /usr/local/etc/haproxy/
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY dschallenge.pem /usr/local/etc/haproxy/dschallenge.pem
