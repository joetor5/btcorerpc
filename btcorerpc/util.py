# Copyright (c) 2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

from . import logfactory
from .rpc import BitcoinRpc

logger = logfactory.create(__name__)

def _run_util(func):
    def wrapper(*args, **kwargs):
        assert isinstance(args[0], BitcoinRpc), "Not a bitcoin rpc object"
        return func(*args, **kwargs)

    return wrapper

@_run_util
def get_node_version(rpc_obj):
    return rpc_obj.get_network_info["subversion"].replace("/", "").split(":")[-1]
