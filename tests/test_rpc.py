# Copyright (c) 2024-2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

import os
import pytest
from btcorerpc.rpc import BitcoinRpc
from btcorerpc.exceptions import BitcoinRpcConnectionError, BitcoinRpcAuthError

BITCOIN_RPC_IP = os.getenv("BITCOIN_RPC_IP")
BITCOIN_RPC_USER = os.getenv("BITCOIN_RPC_USER")
BITCOIN_RPC_PASSWORD = os.getenv("BITCOIN_RPC_PASSWORD")

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
                "get_connection_count",
                "get_node_addresses",
                "get_peer_info",
                "get_best_block_hash",
                "get_chain_states",
                "get_chain_tips",
                "get_deployment_info",
                "get_difficulty"]
}

def test_rpc_call():
    rpc = create_rpc()
    for method in TEST_DATA["methods"]:
        response = eval("rpc.{}()".format(method))
        assert response["error"] == None

    assert rpc.get_rpc_total_count() == len(TEST_DATA["methods"])
    assert rpc.get_rpc_error_count() == 0
    assert rpc.get_rpc_success_count() == len(TEST_DATA["methods"])

def test_rpc_connection_exception():
    rpc = BitcoinRpc(*TEST_DATA["rpc_credentials"], host_ip=TEST_DATA["rpc_ip"], host_port=TEST_DATA["bad_port"])

    for method in TEST_DATA["methods"]:
        with pytest.raises(BitcoinRpcConnectionError):
            eval("rpc.{}()".format(method))

            assert rpc.get_rpc_total_count() == len(TEST_DATA["methods"])
            assert rpc.get_rpc_error_count() == len(TEST_DATA["methods"])
            assert rpc.get_rpc_success_count() == 0

def test_rpc_auth_exception():
    rpc = BitcoinRpc(*TEST_DATA["rpc_credentials_bad"], host_ip=TEST_DATA["rpc_ip"])
    with pytest.raises(BitcoinRpcAuthError):
        rpc.uptime()

    assert rpc.get_rpc_total_count() == 1
    assert rpc.get_rpc_error_count() == 1
    assert rpc.get_rpc_success_count() == 0

def test_rpc_block_methods():
    rpc = create_rpc()

    block_height = rpc.get_block_count()["result"]
    block_hash = rpc.get_block_hash(block_height)["result"]
    block = rpc.get_block(block_hash)
    block_header = rpc.get_block_header(block_hash)
    deployment_info = rpc.get_deployment_info(block_hash)

    assert block["error"] == None
    assert block_header["error"] == None
    assert deployment_info["error"] == None

    for arg in [block_height, block_hash]:
        block_stats = rpc.get_block_stats(arg)
        assert block_stats["error"] == None

    assert rpc.get_rpc_total_count() == 7
    assert rpc.get_rpc_error_count() == 0
    assert rpc.get_rpc_success_count() == 7

def create_rpc():
    return BitcoinRpc(*TEST_DATA["rpc_credentials"], host_ip=TEST_DATA["rpc_ip"])
