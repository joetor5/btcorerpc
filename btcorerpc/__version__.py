# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

_version_major_minor_patch = (0, 1, 1)
_version_dev = False

__version__ = ".".join(str(num) for num in _version_major_minor_patch)
if _version_dev:
    __version__ += "-dev"
