import os


__all__ = [
    'get_env'
]

def get_env(name,default=None):
    env = os.getenv(name)
    if env is None:
        return default
    return env