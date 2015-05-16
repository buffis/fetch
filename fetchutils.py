from __future__ import print_function
import sys


def exit_with_error(error_msg):
    print(error_msg, file=sys.stderr)
    sys.exit(1)


def log_error(error_msg):
    print(error_msg, file=sys.stderr)


def log(msg):
    print(msg)
