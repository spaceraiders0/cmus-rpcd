"""Contains functions and constants used by the main file.
"""

import re
import sys
import shutil
import subprocess
from pathlib import Path
from psutil import process_iter
from configparser import ConfigParser

root_dir = Path(__file__).parent.parent
settings_file = root_dir / Path("settings.ini")
settings_parser = ConfigParser()

HAS_CMUS = shutil.which("cmus")
SETTINGS_DEFAULT = """\
[cmus-rpc]
UPDATE_TIME = 1
CLIENT_ID = 813509909794127872
FORMAT_STRING = {name} - {artist}
DAEMON_NAME = cmus-rpcd.py
"""

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

    settings = {
        "UPDATE_TIME": 1,
        "CLIENT_ID": "813509909794127872",
        "FORMAT_STRING": "{name} - {artst}"
    }

    if settings_file.exists() is False:
        open(settings_file, "x")

        with open(settings_file, "w") as settings_buffer:
            settings_buffer.write(SETTINGS_DEFAULT)

    settings_parser.read(settings_file)
    
    # Error handling for the cmus-rpc section.
    try:
        cmus_section = settings_parser["cmus-rpc"]
    except KeyError:
        print("Section 'cmus-rpc' not found in settings file!")
        print("Settings file is malformed. Please delete the settings", end="")
        print(" file, restart the script.")
        sys.exit(1)

    # Error handling for basic settings.
    try:
        settings["UPDATE_TIME"] = int(cmus_section["UPDATE_TIME"])
        settings["CLIENT_ID"] = cmus_section["CLIENT_ID"]
        settings["FORMAT_STRING"] = cmus_section["FORMAT_STRING"]
        settings["DAEMON_NAME"] = cmus_section["DAEMON_NAME"]
    except KeyError as exp:
        print(f"{exp} field is not found! Settings file is malformed.")
        print("Please delete the settings file and reload the script.")
        sys.exit(1)

    return settings


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
    cmus_state = get_state_info()
    format_specifers = {
        "{name}": Path(cmus_state["values"]["file"]).stem,
        "{artist}": cmus_state["tag"]["artist"],
        "{album}": cmus_state["tag"]["album"],
        "{title}": cmus_state["tag"]["title"],
        "{tracknumber}": cmus_state["tag"]["tracknumber"]
    }

    # Replace all occurances of format specifiers.
    for substitute, replace in format_specifers.items():
        format_string_copy = format_string_copy.replace(substitute, str(replace))

    return format_string_copy
