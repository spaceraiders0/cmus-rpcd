#!/usr/bin/env python

"""The daemon for the RPC client.
"""

import time
import definitions
from setproctitle import setproctitle
from pypresence import Presence, exceptions

if definitions.HAS_CMUS is False:
    print("You need to install CMUS to use this application.")
    sys.exit(1)

settings = definitions.load_settings()
setproctitle(settings["daemon_name"])

# Connect to Discord.
RPC = Presence(settings["client_id"])
RPC.connect()

try:
    while True:
        settings = definitions.load_settings()
        cmus_state = definitions.get_state_info()

        # If cmus is running.
        if cmus_state is not None:
            current_state = definitions.format(settings["status_format"])
            
            try:
                RPC.update(state=current_state, large_image="cmus-rpc")
            except exceptions.InvalidID:
                # Attempt to connect again until the connection succeeds.
                try:
                    RPC.connect()
                except ConnectionRefusedError:
                    pass

        time.sleep(int(settings["update_time"]))
except KeyboardInterrupt:
    RPC.close()
finally:
    RPC.close()
