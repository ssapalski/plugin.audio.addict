import urlparse
import sys
import os

sys.path.insert(0, os.path.join(sys.path[0], 'resources', 'lib'))
import audioaddict


def parse_args(query_string):
    args = urlparse.parse_qs(query_string)

    if not args:
        return {}

    for key, values in args.iteritems():
        if len(values) > 1:
            raise ValueError("multiple values for '%s' not allowed" % key)

        args[key] = values[0]

    return args


def main():
    addon_url = sys.argv[0]
    addon_handle = int(sys.argv[1])
    addon_args = parse_args(sys.argv[2][1:])

    audioaddict.run_addon(addon_url, addon_handle, addon_args)


if __name__ == "__main__":
    main()
