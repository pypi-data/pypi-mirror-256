from urllib.parse import urlparse

from flask import abort, request


def valid_url(url):
    if urlparse(url).netloc != "":
        return False

    return True


def get_url(arg):
    url = request.args.get(arg, "/")
    if not valid_url(url):
        abort(403)
    else:
        return url


def get_next():
    return get_url(arg="next")


def get_cancel():
    return get_url(arg="cancel")
