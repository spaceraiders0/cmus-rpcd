"""Contains functions to create new state for the RPC connection.
"""

from datetime import datetime as dt


def format_state(cmus_state: dict, options: dict) -> dict:
    """Formats the state given to it, and creates a dictionary usable by
    format_field to create new strings.

    :param cmus_state: the state to format
    :type cmus_state: dict
    :param options: the loaded options
    :type options: dict
    :return: the formatted state
    :rtype: dict
    """

    cmus_tags = cmus_state["tag"]
    cmus_values = cmus_state["values"]
    cmus_set = cmus_state["set"]
    progress_format = options["progress_format"].replace("$", "%")
    duration_format = options["duration_format"].replace("$", "%")

    return {
        "{artist}": cmus_tags["artist"],
        "{album}": cmus_tags["album"],
        "{title}": cmus_tags["title"],
        "{status}": cmus_values["status"].capitalize(),
        "{tracknum}": str(cmus_tags["tracknumber"]),
        "{shuffle}": str(cmus_set["shuffle"]),
        "{repeat}": str(cmus_set["repeat"]),
        "{current}": str(cmus_set["repeat_current"]),
        "{playlibrary}": str(cmus_set["play_library"]),
        "{playsorted}": str(cmus_set["play_sorted"]),
        "{duration}": dt.fromtimestamp(cmus_values["duration"]).strftime(duration_format),
        "{progress}": dt.fromtimestamp(cmus_values["position"]).strftime(progress_format),
        "{progpercent}": str(round((cmus_values["position"] / cmus_values["duration"]) * 100)),
        "{{}": "{",
        "{}}": "}",
    }


def format_field(format_specifiers: str, options: dict, cmus_state: dict) -> str:
    """Creates a formatted string containing the requested information from
    Cmus.

    :param format_specifiers: the string to format
    :type format_specifiers: str
    :param options: the loaded options
    :type options: dict
    :param cmus_state: the dictionary containing the current state of Cmus
    :type cmus_state: dict
    :return: the formatted string
    :rtype: str
    """

    formatted = "".join(format_specifiers)
    formatted_state = format_state(cmus_state, options)

    # Go through each possible specifier and replace it
    # with its corresponding tag.
    for specifier, replace in formatted_state.items():
        formatted = formatted.replace(specifier, replace)

    # Needs a minimum of two characters
    if len(formatted) < 2:
        formatted += "  "

    return formatted
