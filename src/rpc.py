#!/usr/bin/env python

"""The main file for the Rich Presence.
"""

import time
import rpc_cmus
import rpc_format
import rpc_options
from pypresence import Presence, exceptions

rpc_options.verify_options_file()
initial_settings = rpc_options.parse_options_file()
rpc_connection = Presence(initial_settings["client_id"])

# Keep trying to connect
while True:
    try:
        rpc_connection.connect()
        print("Initial connection!")
        break
    except (exceptions.InvalidID, ConnectionResetError, ConnectionRefusedError,
            FileNotFoundError):
        pass


while True:
    print("Working!")
    try:
        rpc_options.verify_options_file()
        prog_options = rpc_options.parse_options_file()
        cmus_state = rpc_cmus.get_state_info()

        # Make sure cmus is running
        if rpc_cmus.process_is_running("cmus") is False or cmus_state is None:
            rpc_connection.update(state="No song playing!",
                                  details="No song playing!",
                                  large_image="logo",
                                  small_image="paused")
            time.sleep(prog_options["change_increment"])
            continue

        # Determine what the small image should be.
        if cmus_state["values"]["status"] == "playing":
            small_image_name = "playing"
        else:
            small_image_name = "paused"

        # Prevents weird division by zero from happening.
        try:
            state_string = rpc_format.format_field(prog_options["state_format"],
                                                   prog_options,
                                                   cmus_state)
            details_string = rpc_format.format_field(prog_options["details_format"],
                                                     prog_options,
                                                     cmus_state)
        except ZeroDivisionError:
            state_string = "No song playing!"
            details_string = "No song playing!"

        rpc_connection.update(state=state_string,
                              details=details_string,
                              large_image="logo",
                              small_image=small_image_name)

        time.sleep(prog_options["change_increment"])

    except (exceptions.InvalidID, ConnectionResetError, ConnectionRefusedError,
            FileNotFoundError):
        try:
            rpc_connection.connect()
        except ConnectionRefusedError:
            pass
