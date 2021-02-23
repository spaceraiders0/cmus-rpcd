"""Contains functions and constants used by the main file.
"""

import re
import sys
import shutil
import subprocess
from pathlib import Path
from psutil import process_iter
from configparser import RawConfigParser, DuplicateSectionError
from datetime import datetime as dt

HAS_CMUS = shutil.which("cmus")
root_dir = Path(__file__).parent.parent
settings_file = root_dir / Path("settings.ini")
settings_parser = RawConfigParser()
default_settings = {
    "update_time": "1",
    "state_format": "{album}",
    "details_format": "{name} - {artist}",
    "progress_format": "%M:%S",
    "duration_format": "%M:%S",
    "include_state": True,
    "include_details": True,

    "client_id": "813509909794127872",
    "daemon_name": "cmus-rpcd.py",
}


def process_is_running(process_name: str) -> bool:
    """Returns whether or not a specific progress is running or not.

    :param process: the name of the progress. 
    :type process: str
    """

    return any(process.name() == process_name for process in process_iter())


def load_settings() -> dict:
    """Loads this program's settings from the settings file.
    """

    settings = default_settings.copy()

    if settings_file.exists() is False:  # Load defaults
        open(settings_file, "x")

        try:
            settings_parser.add_section("cmus-rpc")
        except DuplicateSectionError:
            pass

        # Loads defaults into the ConfigParser
        for field, default in default_settings.items():
            settings_parser["cmus-rpc"][field] = str(default)

        # Writes the loaded defaults to the file.
        with open(settings_file, "w") as settings_buffer:
            settings_parser.write(settings_buffer)
    elif settings_file.exists() is True:  # Load settings.
        settings_parser.read(settings_file)

        # Load defined settings into the settings dictionary.
        for field, value in settings_parser["cmus-rpc"].items():
            # Values must have something in them.
            if len(value) > 0:
                settings[field] = typecast(value)

    return settings


def get_state_info() -> dict:
    """Returns the information about the current state of
    CMUS.

    :return: a dictionary with all the fields from the status
        command.
    :rtype: dict
    """

    states = {
        "values": {
            "status": "",
            "file": "",
            "duration": 0,
            "position": 0,
        },
        "tag": {
            "artist": "",
            "album": "",
            "title": "",
            "tracknumber": 0,
        },
        "set": {
            "aaa_mode": "",
            "continue": False,
            "play_library": False,
            "play_sorted": False,
            "replaygain": False,
            "replaygain_limit": False,
            "replaygain_preamp": 0.0,
            "repeat": False,
            "repeat_current": False,
            "shuffle": False,
            "softvol": False,
            "vol_left": 0,
            "vol_right": 0,
        },
    }

    if process_is_running("cmus") is False or HAS_CMUS is False:
        return states

    try:
        output = subprocess.check_output(["cmus-remote", "-C", "status"]).decode("UTF-8")
        output_lines = (output.splitlines())
    except subprocess.CalledProcessError:
        return None

    for line in output_lines:
        words = line.split(" ")
        section_name = words[0]

        # Sections have three fields.
        if section_name in states:
            section = states[section_name]
            field_name = words[1]

            section[field_name] = typecast(" ".join(words[2:]))
        else:
            field_name = words[0]
            states["values"][field_name] = typecast(" ".join(words[1:]))

    return states


def format(format_string: str) -> str:
    """Formats the format specifier in the settings.

    :param format_string: the string to parse for format specifiers
    :type format_string: str
    :return: the formatted message
    :rtype: str
    """

    settings = load_settings()
    cmus_state = get_state_info()

    cmus_value = cmus_state["values"]
    song_progress = cmus_value["position"]
    song_duration = cmus_value["duration"]

    format_string_copy = "".join(format_string)
    format_specifers = {
        "{name}": Path(cmus_state["values"]["file"]).stem,
        "{artist}": cmus_state["tag"]["artist"],
        "{album}": cmus_state["tag"]["album"],
        "{title}": cmus_state["tag"]["title"],
        "{tracknumber}": cmus_state["tag"]["tracknumber"],
        "{progress}": dt.fromtimestamp(song_progress).strftime(settings["progress_format"]),
        "{duration}": dt.fromtimestamp(song_duration).strftime(settings["duration_format"]),
    }


    # Replace all occurances of format specifiers.
    for substitute, replace in format_specifers.items():
        format_string_copy = format_string_copy.replace(substitute, str(replace))

    return format_string_copy
