#!/usr/bin/env python

"""The daemon for the RPC client.
"""

import time
import definitions
from setproctitle import setproctitle
from pypresence import Presence, exceptions
from pathlib import Path

if definitions.HAS_CMUS is False:
    print("You need to install CMUS to use this application.")
    sys.exit(1)

settings = definitions.load_settings()
setproctitle(settings["daemon_name"])

# Connect to Discord.
RPC = Presence(settings["client_id"])
RPC.connect()
last_song = None

try:
    while True:
        settings = definitions.load_settings()
        cmus_state = definitions.get_state_info()

        # If cmus is not running.
        if cmus_state is None:
            continue
        
        playing_song = Path(cmus_state["values"]["file"]).stem
        state = definitions.format(settings["state_format"])
        details = definitions.format(settings["details_format"])
        progress = cmus_state["values"]["position"]
        duration = cmus_state["values"]["duration"]

        # Assign a new start_time, if a new song is playing.
        if playing_song != last_song:
            last_song = playing_song
            start_time = time.time()
            end_time = time.time() + (duration - progress)

        # Build the update dictionary.
        updates = {}

        if settings["include_state"] is True:
            updates["state"] = state

        if settings["include_details"] is True:
            updates["details"] = details

        if settings["include_progress"] is True:
            updates["start"] = start_time + progress 

        if settings["include_duration"] is True:
            updates["end"] = end_time

        try:
            RPC.update(**updates, large_image="cmus-rpc")
        except exceptions.InvalidID:
            # Attempt to connect again until the connection succeeds.
            try:
                RPC.connect()
            except ConnectionRefusedError:
                pass

        time.sleep(float(settings["update_time"]))
except KeyboardInterrupt:
    RPC.close()
finally:
    RPC.close()
