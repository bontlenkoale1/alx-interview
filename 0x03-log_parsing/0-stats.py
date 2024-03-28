#!/usr/bin/python3
import sys
import signal
import re


status_counts = {
    200: 0,
    301: 0,
    400: 0,
    401: 0,
    403: 0,
    404: 0,
    405: 0,
    500: 0
}


total_size = 0
line_count = 0


def sigint_handler(sig, frame):
    print_stats()
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def print_stats():
    print("File size: {}".format(total_size))
    for code in sorted(status_counts.keys()):
        if status_counts[code] > 0:
            print("{}: {}".format(code, status_counts[code]))


pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} - \[.*\] "GET /projects/260 HTTP/1\.1" (\d+) (\d+)$')


for line in sys.stdin:
    match = pattern.match(line)
    if match:
        status_code = int(match.group(1))
        file_size = int(match.group(2))
        total_size += file_size
        status_counts[status_code] += 1
        line_count += 1


        if line_count % 10 == 0:
            print_stats()


print_stats()

