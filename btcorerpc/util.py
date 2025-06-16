# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from . import logfactory
from .rpc import BitcoinRpc

_logger = logfactory.create(__name__)

def _run_util(func):
    def wrapper(*args, **kwargs):
        rpc_obj = args[0]
        assert isinstance(rpc_obj, BitcoinRpc), "Not a bitcoin rpc object"
        raw_json = False
        if rpc_obj.is_raw_json_response_enabled():
            raw_json = True
            rpc_obj.disable_raw_json_response()

        _logger.info(f"util start: {func.__name__}")
        result = func(*args, **kwargs)
        _logger.info(f"util end: {func.__name__}: {result}")

        if raw_json:
            rpc_obj.enable_raw_json_response()

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
    result = rpc_obj.get_net_totals()
    return {
        "in": result["totalbytesrecv"],
        "out": result["totalbytessent"]
    }

@_run_util
def get_node_uptime(rpc_obj):

    def append_s(time_str, time_num):
        if time_num > 1:
            return time_str + "s"
        else:
            return time_str

    uptime = rpc_obj.uptime()
    uptime_str = ""

    mins = uptime / 60
    hours = mins / 60
    days = int(hours / 24)

    if days > 0:
        uptime_str += f"{str(days)} day"
        uptime_str = append_s(uptime_str, days) + ", "

    if int(hours) > 0:
        hours = (hours - 24 * days)
        if int(hours) != 0:
            uptime_str += f"{str(int(hours))} hour"
            uptime_str = append_s(uptime_str, hours) + ", "

        mins = int((hours - int(hours)) * 60)
        uptime_str += f"{str(mins)} minute"
        uptime_str = append_s(uptime_str, mins)
    else:
        mins = int(mins)
        uptime_str += append_s(f"{str(mins)} minute", mins)

    return uptime_str

def _network_info(rpc_obj):
    return rpc_obj.get_network_info()
