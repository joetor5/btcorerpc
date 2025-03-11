# Copyright (c) 2024-2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

import os
import pytest
from pathlib import Path
from btcorerpc.rpc import BitcoinRpc, RPC_CONNECTION_ERROR, RPC_AUTH_ERROR
from btcorerpc.exceptions import BitcoinRpcError

BITCOIN_RPC_IP = os.getenv("BITCOIN_RPC_IP")
BITCOIN_RPC_USER = os.getenv("BITCOIN_RPC_USER")
BITCOIN_RPC_PASSWORD = os.getenv("BITCOIN_RPC_PASSWORD")

TEST_DATA = {
    "rpc_ip": BITCOIN_RPC_IP,
    "rpc_credentials": (BITCOIN_RPC_USER, BITCOIN_RPC_PASSWORD),
    "rpc_credentials_bad": ("test", "test123"),
    "bad_port": 9000,
    "methods": ["uptime", "get_blockchain_info", "get_network_info", "get_net_totals",
                "get_memory_info", "get_mem_pool_info"]
}

def test_rpc_call():
    print(TEST_DATA)
    rpc = BitcoinRpc(*TEST_DATA["rpc_credentials"], host_ip=TEST_DATA["rpc_ip"])
    for method in TEST_DATA["methods"]:
        response = eval("rpc.{}()".format(method))
        assert response["error"] == None

    assert rpc.get_rpc_total_count() == len(TEST_DATA["methods"])
    assert rpc.get_rpc_error_count() == 0
    assert rpc.get_rpc_success_count() == len(TEST_DATA["methods"])

def test_connection_error():
    rpc = BitcoinRpc(*TEST_DATA["rpc_credentials"], host_ip=TEST_DATA["rpc_ip"], host_port=TEST_DATA["bad_port"])

    for method in TEST_DATA["methods"]:
        response = eval("rpc.{}()".format(method))
        assert response["result"] == None and \
               response["error"]["code"] == RPC_CONNECTION_ERROR and \
               response["error"]["message"] == "failed to establish connection"

    assert rpc.get_rpc_total_count() == len(TEST_DATA["methods"])
    assert rpc.get_rpc_error_count() == len(TEST_DATA["methods"])
    assert rpc.get_rpc_success_count() == 0

# def test_rpc_empty_credentials():
#     with pytest.raises(BitcoinRpcError):
#         rpc = BitcoinRpc(rpc_user="", rpc_password="")

def test_rpc_bad_credentials():
    rpc = BitcoinRpc(*TEST_DATA["rpc_credentials_bad"], host_ip=TEST_DATA["rpc_ip"])
    response = rpc.uptime()
    assert response["result"] == None and \
           response["error"]["code"] == RPC_AUTH_ERROR and \
           response["error"]["message"] == "got empty payload and bad status code (possible wrong RPC credentials)"

    assert rpc.get_rpc_total_count() == 1
    assert rpc.get_rpc_error_count() == 1
    assert rpc.get_rpc_success_count() == 0
