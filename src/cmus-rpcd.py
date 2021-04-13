#!/usr/bin/env python

"""The client for cmus-rpcd
"""

import sys
import rpc_cmus
import rpc_options
import subprocess
from argparse import ArgumentParser

rpc_parser = ArgumentParser(description="""A daemon to display Rich Presence
                            from Cmus.""")
rpc_parser.add_argument("--start", "-s", action="store_true", help="""Start the
                        daemon.""")
rpc_parser.add_argument("--kill", "-k", action="store_true", help="""Kill the
                        daemon.""")
rpc_parser.add_argument("--version", "-v", action="store_true", help="""Display
                        the version of this program.""")
rpc_args = rpc_parser.parse_args()
daemon_is_running = rpc_cmus.process_is_running("cmus-rpcd")

# Kill cmus-rpcd
if rpc_args.kill is True:
    if daemon_is_running is False:
        print("Cmus is not running.")
        sys.exit(1)
    else:
        subprocess.Popen(["killall", "cmus-rpcd"])
        sys.exit(0)

# Prevent cmus-rpcd from running twice.
if daemon_is_running is False:
    subprocess.Popen(str(rpc_options.root_dir / rpc_options.Path("src/rpc.py")))
else:
    print("Cmus is already running.")
    sys.exit(1)
