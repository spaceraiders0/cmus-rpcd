#!/usr/bin/env python

"""The daemon controller. Starts, or kills the daemon.
"""

import subprocess
import definitions
from setproctitle import setproctitle
from argparse import ArgumentParser
from pathlib import Path

daemon_parser = ArgumentParser(description="""A small Discord Rich Presence
                               daemon for the C* music player.""")
daemon_parser.add_argument("--kill", help="Kill the daemon if started.",
                           action="store_true")
daemon_parser.add_argument("--start", help="Start the daemon if not started.",
                           action="store_true")
daemon_args = daemon_parser.parse_args()
settings = definitions.load_settings()
daemon_name = settings["daemon_name"]

if daemon_args.start is True:
    daemon_path = Path(__file__).parent / Path("cmus-rpcd.py")

    if definitions.daemon_is_running(daemon_name) is False:
        print("Started daemon!")
        subprocess.Popen(str(daemon_path))
elif daemon_args.kill is True:
    print("Killed daemon.")
    subprocess.Popen(["killall", daemon_name])
