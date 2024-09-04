import os


def get_env(name:str, default=None):
    env = os.getenv(name)
    if env is None:
        return default
    return env