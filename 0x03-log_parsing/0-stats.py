#!/usr/bin/python3
import sys
import signal
import re

# Define a dictionary to store status code counts
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

# Initialize variables for total file size and line count
total_size = 0
line_count = 0


# Define a function to handle SIGINT (Ctrl+C)
def sigint_handler(sig, frame):
    print_stats()
    sys.exit(0)


# Register the SIGINT handler
signal.signal(signal.SIGINT, sigint_handler)


# Define a function to print statistics
def print_stats():
    print("File size: {}".format(total_size))
    for code in sorted(status_counts.keys()):
        if status_counts[code] > 0:
            print("{}: {}".format(code, status_counts[code]))


# Define a regular expression pattern to match log lines
pattern = re.compile(
    r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\[.*\]"GET/projects/260HTTP/1\.1"'
    r'(\d+)(\d+)$'
)

# Process each line from stdin
for line in sys.stdin:
    match = pattern.match(line)
    if match:
        status_code = int(match.group(1))
        file_size = int(match.group(2))
        total_size += file_size
        status_counts[status_code] += 1
        line_count += 1

        # Print statistics every 10 lines
        if line_count % 10 == 0:
            print_stats()

# Print final statistics
print_stats()
