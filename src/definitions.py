"""Contains functions and constants used by the main file.
"""

import re
import sys
import shutil
import subprocess
from pathlib import Path
from psutil import process_iter
from configparser import RawConfigParser
from datetime import datetime as dt

root_dir = Path(__file__).parent.parent
settings_file = root_dir / Path("settings.ini")
settings_parser = RawConfigParser()

HAS_CMUS = shutil.which("cmus")
default_settings = {
    "update_time": "1",
    "status_format": "{name} - {artist}",
    "details_format": "",
    "progress_format": "%M:%S",
    "duration_format": "%M:%S",
    "include_progress": "True",
    "include_duration": "True",

    "client_id": "813509909794127872",
    "daemon_name": "cmus-rpcd.py",
}

# Value Constants
types = {
    "\d*\.\d+": float,
    "((T|t)rue|(F|f)alse)": lambda value: True if value.lower() == "true" \
                                               else False,
    "\d+": int,
}


def daemon_is_running(daemon_name: str) -> bool:
    """Returns whether the daemon is running or not.

    :param daemon_name: the name of the daemon
    :type daemon_name: str
    """

    return any(process.name() == daemon_name for process in process_iter())


def load_settings() -> dict:
    """Loads this program's settings from the settings file.
    """

    if settings_file.exists() is False:  # Load defaults
        open(settings_file, "x")
        settings_parser.add_section("cmus-rpc")

        for field, default in default_settings.items():
            settings_parser["cmus-rpc"][field] = default

        with open(settings_file, "w") as settings_buffer:
            settings_parser.write(settings_buffer)

    elif settings_file.exists() is True:  # Load settings.
        settings_parser.read(settings_file)

    return settings_parser["cmus-rpc"]


def typecast(value: str) -> any:
    """Converts a string's contents to it's type.

    :return: the casted type
    :rtype: any
    """

    for pattern, cast_to in types.items():
        if re.match(pattern, value):
            try:
                return cast_to(value)
            except ValueError:
                break

    return value


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

    format_string_copy = "".join(format_string)

    settings = load_settings()
    PROGRESS_FORMAT = settings["progress_format"]
    DURATION_FORMAT = settings["duration_format"]

    cmus_state = get_state_info()
    cmus_value = cmus_state["values"]

    format_specifers = {
        "{name}": Path(cmus_state["values"]["file"]).stem,
        "{artist}": cmus_state["tag"]["artist"],
        "{album}": cmus_state["tag"]["album"],
        "{title}": cmus_state["tag"]["title"],
        "{tracknumber}": cmus_state["tag"]["tracknumber"],
        "{duration}": dt.fromtimestamp(cmus_value["duration"]).strftime(DURATION_FORMAT),
        "{progress}": dt.fromtimestamp(cmus_value["position"]).strftime(PROGRESS_FORMAT)
    }

    # Replace all occurances of format specifiers.
    for substitute, replace in format_specifers.items():
        format_string_copy = format_string_copy.replace(substitute, str(replace))

    return format_string_copy
