#!/usr/bin/env python

"""The main file for the Rich Presence.
"""

import time
import rpc_cmus
import rpc_format
import rpc_options
from pypresence import Presence

rpc_options.verify_options_file()
initial_settings = rpc_options.parse_options_file()
rpc_connection = Presence(initial_settings["client_id"])
rpc_connection.connect()

while True:
    rpc_options.verify_options_file()
    prog_options = rpc_options.parse_options_file()
    cmus_state = rpc_cmus.get_state_info()

    # Determine what the small image should be.
    if cmus_state["values"]["status"] == "playing":
        small_image_name = "playing"
    else:
        small_image_name = "paused"

    state_string = rpc_format.format_field(prog_options["state_format"],
                                           prog_options,
                                           cmus_state)
    details_string = rpc_format.format_field(prog_options["details_format"],
                                             prog_options,
                                             cmus_state)

    rpc_connection.update(state=state_string,
                          details=details_string,
                          large_image="logo",
                          small_image=small_image_name)

    time.sleep(prog_options["change_increment"])
