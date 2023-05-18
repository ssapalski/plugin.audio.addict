"""
    plugin.audio.addict
    Unofficial addon for the AudioAddict network of radio streams.
"""

import urllib.parse
import sys
import os

TOPDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TOPDIR, 'resources', 'lib'))

import audioaddict  # pylint: disable=wrong-import-position


def parse_addon_args(query_string):
    """Parse addon arguments.

    Parse arguments given by Kodi to the addon call. This function
    expects a 'query string' to be parsed and returns a dictionary.

    Multiple appearances of parameters are parsed to lists in the
    order how they have appeared, otherwise they are parsed to plain
    values.

    A leading '?' sign will get removed if present. This makes it
    possible to pass sys.argv[2] directly to this function.

    All arguments are parsed to strings.

    Note:
        Invalid input is silently ignored, see example three.

    Args:
        query_string (str): the 'query string' to be parsed.

    Examples:
        >>> parse_args("param1=arg1&param2=arg2")
        {'param1': 'arg1', 'param2': 'arg2'}

        >>> parse_args("param1=arg1&param1=arg2")
        {'param1': ['arg1', 'arg2']}

        >>> parse_args("param1=arg1&param2")
        {'param1': 'arg1'}

    Returns:
        dict: the parsed 'query string'.

    """
    if query_string.startswith('?'):
        args = urllib.parse.parse_qs(query_string[1:])
    else:
        args = urllib.parse.parse_qs(query_string)

    if not args:
        return {}

    for key, values in args.items():
        if len(values) == 1:
            args[key] = values[0]

    return args


def main():
    """addon entry point"""
    addon_url = sys.argv[0]
    addon_handle = int(sys.argv[1])
    addon_args = parse_addon_args(sys.argv[2])

    audioaddict.run_addon(addon_url, addon_handle, addon_args)


if __name__ == "__main__":
    main()
