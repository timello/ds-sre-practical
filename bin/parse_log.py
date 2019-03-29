#!/usr/bin/python3
#
# Program that parses a HAproxy default log file
# and prints out most viewed urls, number of
# unique visitors and error count by type.
#
# Author(s): Tiago Mello <timello@gmail.com>

import argparse


def parse_haproxy_log(logfile):
    """Prints out the number of unique visitors, most viewed url
    and error count by type.

    Parameters:
        logfile (string): Log file path for parsing

    """

    visitors_ip = {}
    visited_urls = {}
    error_count = {}

    with open(logfile, 'r') as f:
        for line in f.readlines():
            try:
                # Default HAProxy log format (refer to
                # https://www.haproxy.com/blog/haproxy-log-customization/)
                # log-format "%ci:%cp [%tr] %ft %b/%s %TR/%Tw/%Tc/%Tr/%Ta %ST
                # %B %CC %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r"
                _, _, _, ip, dt, _, _, _, code, _, _, _, _, _, _, *request = line.split(' ')
                ip, _ = ip.split(':')

                if ip in visitors_ip:
                    visitors_ip[ip] = visitors_ip[ip] + 1
                else:
                    visitors_ip[ip] = 1

                if code in ['200', '202']:
                    _, url, _ = request
                    if url in visited_urls:
                        visited_urls[url] = visited_urls[url] + 1
                    else:
                        visited_urls[url] = 1
                else:
                    if code in error_count:
                        error_count[code] = error_count[code] + 1
                    else:
                        error_count[code] = 1

            # We may end up having lines that does not have the expected format.
            # Just get ride of them since they will not be valid for counting.
            except ValueError:
                continue

        # Pythonic way to sort by dict value. Creates a tuple (url, count)
        sorted_visited_urls = sorted(visited_urls.items(), key=lambda kv: kv[1])

        print("Most visited urls:")
        for most_visited in reversed(sorted_visited_urls):
            print("\tURL: %s, number of visits: %s" % (most_visited[0],
                                                       most_visited[1]))

        print("Number of unique visitors: %d" % len(visitors_ip))

        sorted_error_count = sorted(error_count.items(), key=lambda kv: kv[1])
        print("Error count (per type):")
        for error in reversed(sorted_error_count):
            print("\tType: %s, count: %s" % error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='HAproxy and Apache access log parser')

    parser.add_argument('logfile', help='Log file input')

    args = parser.parse_args()
    parse_haproxy_log(args.logfile)
