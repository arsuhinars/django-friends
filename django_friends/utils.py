import os


def get_secret(name: str, default=None):
    path = f'/run/secrets/{name}'
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()
    return default
