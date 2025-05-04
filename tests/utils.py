# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

import os
from btcorerpc.rpc import BitcoinRpc

BITCOIN_RPC_IP = os.getenv("BITCOIN_RPC_IP")
BITCOIN_RPC_USER = os.getenv("BITCOIN_RPC_USER")
BITCOIN_RPC_PASSWORD = os.getenv("BITCOIN_RPC_PASSWORD")

def _create_rpc():
    return BitcoinRpc(BITCOIN_RPC_USER, BITCOIN_RPC_PASSWORD, host_ip=BITCOIN_RPC_IP)
