from cloud_cat import CloudCat
import sys
import config


def help():
    print("{} <get|set>".format(sys.argv[0]))


def get_cloud_clipboard():
    cloud_cat = CloudCat(config.SALT)
    text = cloud_cat.read()
    return text


def set_cloud_clipboard(text):
    cloud_cat = CloudCat(config.SALT)
    cloud_cat.write(text)


def main():
    if len(sys.argv) != 2 or not sys.argv[1] in ("set", "get"):
        help()
        sys.exit(1)

    if sys.argv[1] == "get":
        text = get_cloud_clipboard()
        sys.stdout.write(text)
    elif sys.argv[1] == "set":
        text = sys.stdin.read()
        set_cloud_clipboard(text)
    else:
        assert(False)


if __name__ == "__main__":
    main()
