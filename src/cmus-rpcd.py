#!/usr/bin/env python

"""The daemon for the RPC client.
"""

import time
import definitions
from setproctitle import setproctitle
from pypresence import Presence

if definitions.HAS_CMUS is False:
    print("You need to install CMUS to use this application.")
    sys.exit(1)


settings = definitions.load_settings()
setproctitle(settings["DAEMON_NAME"])

RPC = Presence(settings["CLIENT_ID"])
RPC.connect()

try:
    while True:
        cmus_state = definitions.get_state_info()

        if cmus_state is not None:
            current_state = definitions.format(settings["FORMAT_STRING"])
            
            RPC.update(state=current_state, large_image="cmus-rpc")
            time.sleep(settings["UPDATE_TIME"])
except KeyboardInterrupt:
    RPC.close()
finally:
    RPC.close()
