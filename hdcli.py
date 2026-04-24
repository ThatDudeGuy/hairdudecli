#!/usr/bin/python3

import sys
sys.path.insert(0, "/usr/local/lib")
from hairdudecli.syntax_checker import multi_command_check
from hairdudecli.arg_mapping import dispatch_command


# Command Line Arguments
args = sys.argv[1:]

# Do not allow multiple commands...for now
if not multi_command_check(args):
    sys.exit(1)

# attempt to run command
dispatch_command(args)
