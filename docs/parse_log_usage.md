# HAProxy access log parse scripts

Python script that parses a haproxy default log file and return the following information:

 * Most visited URLs
 * Number of unique visitors
 * Error count (per type)

### Usage:

    $ ./bin/parse_log.py haproxy_access.log

### Example of output:

        Most visited urls:
                URL: /api/v1/entries, number of visits: 19221
        Number of unique visitors: 15
        Error count (per type):
                Type: 400, count: 63
                Type: 500, count: 24
                Type: 404, count: 11
                Type: 405, count: 3
                Type: 301, count: 2
                Type: 503, count: 1
