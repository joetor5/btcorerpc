# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from . import logfactory
from .rpc import BitcoinRpc

_logger = logfactory.create(__name__)

def _run_util(func):
    def wrapper(*args, **kwargs):
        assert isinstance(args[0], BitcoinRpc), "Not a bitcoin rpc object"
        _logger.info(f"util start: {func.__name__}")
        result = func(*args, **kwargs)
        _logger.info(f"util end: {func.__name__}: {result}")
        return result

    return wrapper

@_run_util
def get_node_version(rpc_obj):
    return _network_info(rpc_obj)["subversion"].replace("/", "").split(":")[-1]

@_run_util
def get_node_connections(rpc_obj):
    result = _network_info(rpc_obj)
    return {
        "in": result["connections_in"],
        "out": result["connections_out"],
        "total": result["connections"]
    }

@_run_util
def get_node_traffic(rpc_obj):
    result = rpc_obj.get_net_totals()["result"]
    return {
        "in": result["totalbytesrecv"],
        "out": result["totalbytessent"]
    }

def _network_info(rpc_obj):
    return rpc_obj.get_network_info()["result"]
