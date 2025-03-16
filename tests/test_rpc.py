# Copyright (c) 2024-2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

import os
import pytest
from btcorerpc.rpc import BitcoinRpc
from btcorerpc.exceptions import BitcoinRpcConnectionError, BitcoinRpcAuthError
from utils import _create_rpc, BITCOIN_RPC_USER, BITCOIN_RPC_PASSWORD, BITCOIN_RPC_IP

TEST_DATA = {
    "rpc_ip": BITCOIN_RPC_IP,
    "rpc_credentials": (BITCOIN_RPC_USER, BITCOIN_RPC_PASSWORD),
    "rpc_credentials_bad": ("test", "test123"),
    "bad_port": 9000,
    "methods": ["uptime",
                "get_rpc_info",
                "get_blockchain_info",
                "get_block_count",
                "get_network_info",
                "get_net_totals",
                "get_memory_info",
                "get_mem_pool_info",
                "get_raw_mem_pool",
                "get_connection_count",
                "get_node_addresses",
                "get_peer_info",
                "get_best_block_hash",
                "get_chain_states",
                "get_chain_tips",
                "get_deployment_info",
                "get_difficulty"]
}

METHOD_COUNT = len(TEST_DATA["methods"])

def test_rpc_call():
    rpc = _create_rpc()
    results = []

    for method in TEST_DATA["methods"]:
        response = eval("rpc.{}()".format(method))
        results.append(response)

    _assert_rpc_no_error(results)
    _assert_rpc_stats(rpc, METHOD_COUNT, METHOD_COUNT, 0)

def test_rpc_connection_exception():
    rpc = BitcoinRpc(*TEST_DATA["rpc_credentials"], host_ip=TEST_DATA["rpc_ip"], host_port=TEST_DATA["bad_port"])

    for method in TEST_DATA["methods"]:
        with pytest.raises(BitcoinRpcConnectionError):
            eval("rpc.{}()".format(method))

    _assert_rpc_stats(rpc, METHOD_COUNT, 0, METHOD_COUNT)

def test_rpc_auth_exception():
    rpc = BitcoinRpc(*TEST_DATA["rpc_credentials_bad"], host_ip=TEST_DATA["rpc_ip"])
    with pytest.raises(BitcoinRpcAuthError):
        rpc.uptime()

    _assert_rpc_stats(rpc, 1, 0, 1)

def test_rpc_block_methods():
    rpc = _create_rpc()
    results = []

    block_height = rpc.get_block_count()["result"]
    block_hash = rpc.get_block_hash(block_height)["result"]
    block = rpc.get_block(block_hash)
    block_header = rpc.get_block_header(block_hash)
    deployment_info = rpc.get_deployment_info(block_hash)

    results.extend([block, block_header, deployment_info])

    for arg in [block_height, block_hash]:
        block_stats = rpc.get_block_stats(arg)
        results.append(block_stats)

    _assert_rpc_no_error(results)
    _assert_rpc_stats(rpc, 7, 7, 0)

def test_rpc_mem_pool_methods():
    rpc = _create_rpc()
    results = []

    mem_pool_trans = rpc.get_raw_mem_pool()
    mem_pool_trans_id = mem_pool_trans["result"][0]

    for arg1, arg2 in [(True, False), (False, True)]:
        result = rpc.get_raw_mem_pool(arg1, arg2)
        results.append(result)

    mem_pool_entry = rpc.get_mem_pool_entry(mem_pool_trans_id)

    results.extend([mem_pool_trans, mem_pool_entry])

    for arg in [True, False]:
        mem_pool_ancestors = rpc.get_mem_pool_ancestors(mem_pool_trans_id, arg)
        mem_pool_descendants = rpc.get_mem_pool_descendants(mem_pool_trans_id, arg)
        results.extend([mem_pool_ancestors, mem_pool_descendants])

    _assert_rpc_no_error(results)
    _assert_rpc_stats(rpc, 8, 8, 0)


def _assert_rpc_stats(rpc_obj, total, success, error):
    assert rpc_obj.get_rpc_total_count() == total
    assert rpc_obj.get_rpc_success_count() == success
    assert rpc_obj.get_rpc_error_count() == error

def _assert_rpc_no_error(result_list):
    for result in result_list:
        assert result["error"] == None
        assert result["result"] != None
