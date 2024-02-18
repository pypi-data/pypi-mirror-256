# The purpose of this code is to lazy load the ESL shared library and the functions loaded from that library.
# The reason for doing this is (1) remove unnecessary imports when not needed by the app, and (2) allow code
# to run on a different platform that cannot load the shared library, but still needs some functionality from
# the `egse.dsi` module.

import logging

__all__ = [
    "_libesl",
]

import importlib

_LOGGER = logging.getLogger(__name__)
_LAZY_LOADING_CACHE: dict = {}


def __getattr__(name):

    try:
        return _LAZY_LOADING_CACHE[name]
    except KeyError:
        pass

    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = importlib.import_module("." + name, __name__)

    _LOGGER.info(f"Module {module.__name__} imported.")
    _LAZY_LOADING_CACHE[name] = module

    return module
