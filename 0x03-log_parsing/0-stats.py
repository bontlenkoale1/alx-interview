#!/usr/bin/python3

import sys
import signal
import re

# Define a dictionary to store status code counts
status_code_counts = {
    200: 0,
    301: 0,
    400: 0,
    401: 0,
    403: 0,
    404: 0,
    405: 0,
    500: 0
}

total_file_size = 0
lines_processed = 0


# Define a regular expression pattern to match the input format
pattern = re.compile(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(.*?)\]
    r' "GET \/projects\/260 HTTP\/1\.1"' (\d{3}) (\d+)$'


def signal_handler(sig, frame):
    print_statistics()
    sys.exit(0)


def print_statistics():
    global total_file_size, lines_processed
    print(f"File size: {total_file_size}")
    for status_code, count in sorted(status_code_counts.items()):
        if count > 0:
            print(f"{status_code}: {count}")


# Register SIGINT signal handler
signal.signal(signal.SIGINT, signal_handler)


try:
    for line in sys.stdin:
        # Parse the line using the regular expression pattern
        match = pattern.match(line.strip())
        if match:
            ip_address, date, status_code_str, file_size_str = match.groups()
            status_code = int(status_code_str)
            file_size = int(file_size_str)

            # Update total file size
            total_file_size += file_size

            # Update status code count
            if status_code in status_code_counts:
                status_code_counts[status_code] += 1

            lines_processed += 1

            # Check if 10 lines have been processed, then print statistics
            if lines_processed % 10 == 0:
                print_statistics()


except KeyboardInterrupt:
    # If interrupted by Ctrl+C, print statistics before exiting
    print_statistics()
