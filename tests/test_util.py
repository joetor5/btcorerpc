# Copyright (c) 2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

import btcorerpc.util as btc_util
from utils import _create_rpc

BITCOIN_NODE_VERSION = "28.1.0"

rpc = _create_rpc()

def test_get_node_version():
    assert btc_util.get_node_version(rpc) == BITCOIN_NODE_VERSION

def test_get_node_connections():
    result = btc_util.get_node_connections(rpc)
    keys =  ("in", "out", "total")

    _assert_util_result(result, keys, int, True)

def test_get_node_traffic():
    result = btc_util.get_node_traffic(rpc)
    keys = ("in", "out")

    _assert_util_result(result, keys, int, True)

def _assert_util_result(result, keys, key_type, greater_than=False):
    for key in keys:
        assert key in result
        assert type(result[key]) == key_type
        if key_type in (int, float) and greater_than:
            assert result[key] > 0
