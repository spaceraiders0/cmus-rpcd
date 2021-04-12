"""The options parsing for the C* Rich Presence client.
"""

import yaml
from pathlib import Path

root_dir = Path(__file__).parent.parent
options_file = root_dir / Path("options.yaml")


def verify_options_file(opt_path=options_file) -> bool:
    """Verifies the existance of the options file, and creates a new
    options file if one does not exist.

    :param opt_path: the overwrite path of the options.yaml file
    :type opt_path: Path, defaults to the root directory
    :return: whether or not a new options file was created
    :rtype bool
    """

    if opt_path.exists() is False:
        open(opt_path, "x").close()

        # Write the default options to the new file.
        with open(opt_path, "a") as options_buffer:
            options_buffer.write("client_id: 813509909794127872\n")
            options_buffer.write("change_increment: 1\n")
            options_buffer.write("state_format: '{title} - {album}, {artist}'\n")
            options_buffer.write("details_format: '{progress} - {duration}'\n")
            options_buffer.write("progress_format: $M:$S\n")
            options_buffer.write("duration_format: $M:$S\n")

        return True

    return False


def parse_options_file(opt_path=options_file) -> dict:
    """Parses the options file and returns the options. Does not verify or
    create a new options file if it does not exist.

    :param opt_path: the overwrite path of the options.yaml file
    :type opt_path: Path, defaults to the root directory
    :return: a Dictionary containing the parsed options, or None if the file
             does not exist
    :rtype: dict, None
    """

    if opt_path.exists() is False:
        return None

    with open(opt_path, "r") as options_buffer:
        return yaml.load(options_buffer, yaml.FullLoader)


def write_options_file(new_options: dict, opt_path=options_file) -> bool:
    """Writes the options dictionary to the YAML file.

    :param new_options: the optiond
    """

    if opt_path.exists() is False:
        return False

    with open(opt_path, "w") as options_buffer:
        yaml.dump(new_options, options_buffer)

    return True
