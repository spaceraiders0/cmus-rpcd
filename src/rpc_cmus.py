"""Contains functions that revolve around extracting information from Cmus.
"""

import re
import shutil
import psutil
import subprocess

# Regular Expressions
INVALID_NAME = "^\s"
BOOL = "^((t|T)rue|(f|F)alse)"
FLOAT = "\d*\.\d+"
INT = "\d+"

PROCESS_NAME = "cmus"


def typecast(value: str) -> any:
    """Converts a value in string form to its actual object.

    :param value: the string value to cast
    :type value: str
    :return: the casted value
    :rtype: any
    """

    if re.match(FLOAT, value):
        return float(value)
    elif re.match(INT, value):
        return int(value)
    elif re.match(BOOL, value):
        return bool(value)
    else:
        return value


def process_is_running(process_name: str) -> bool:
    """Returns whether or not a specific progress is running or not.

    :param process: the name of the progress.
    :type process: str
    """

    for process in psutil.process_iter():
        if process.name() == PROCESS_NAME:
            return True

    return False


def get_state_info() -> dict:
    """Returns the information about the current state of Cmus.

    :return: a dictionary with all the fields from the status command
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

    # If cmus is not running, or cmus is not installed.
    if process_is_running("cmus") is False or shutil.which("cmus") is False:
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
