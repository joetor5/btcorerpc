# Copyright (c) 2024-2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

import json
import requests
from .exceptions import BitcoinRpcConnectionError, BitcoinRpcAuthError, BitcoinRpcInvalidParams
from requests.exceptions import ConnectionError, ConnectTimeout, TooManyRedirects
from . import logfactory

RPC_CONNECTION_ERROR = 1
RPC_AUTH_ERROR = 2

logger = logfactory.create(__name__)

class BitcoinRpc:
    
    def __init__(self, rpc_user: str, rpc_password: str, host_ip: str = "127.0.0.1", host_port: int = 8332):

        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.host_ip = host_ip
        self.host_port = host_port
        self.rpc_url = f"http://{self.host_ip}:{self.host_port}"
        self.rpc_headers = {
            "Content-Type": "text/plain"
        }
        self.rpc_id = 0
        self.rpc_success = 0
        self.rpc_errors = 0
        self.error_codes = {
            RPC_CONNECTION_ERROR: BitcoinRpcConnectionError,
            RPC_AUTH_ERROR: BitcoinRpcAuthError
        }

    def __repr__(self):
        pass

    def _rpc_call(self, method: str, params: str = "") -> dict:
        self.rpc_id += 1
        logger.info("RPC call start: id={}, method={}".format(self.rpc_id, method))
        try:
            rpc_response = requests.post(self.rpc_url, auth=(self.rpc_user, self.rpc_password), headers=self.rpc_headers,
                                        json={"jsonrpc": "1.0", "id": self.rpc_id,
                                            "method": method, "params": params.split()})
        except (ConnectionError, ConnectTimeout, TooManyRedirects):
            return self._rpc_call_error(RPC_CONNECTION_ERROR, "failed to establish connection", "raw_connection")

        status_code = rpc_response.status_code
        response_text = rpc_response.text
        if status_code == 401 and response_text == "":
            return self._rpc_call_error(RPC_AUTH_ERROR,
                                        "got empty payload and bad status code (possible wrong RPC credentials)",
                                        method)

        rpc_data = json.loads(response_text)
        rpc_data["method"] = method
        if rpc_response.ok:
            self.rpc_success += 1
            logger.info("RPC call success: id={}, status_code={}".format(self.rpc_id, status_code))
        else:
            self.rpc_errors += 1
            logger.error("RPC call error: id={}, status_code={}, message: {}".format(self.rpc_id, status_code, rpc_data["error"]["message"]))

        return rpc_data

    def _rpc_call_error(self, code, message, method) -> dict:
        self.rpc_errors += 1
        logger.error("RPC call error: id={}, {}".format(self.rpc_id, message))
        if code in self.error_codes:
            raise self.error_codes[code](message)

        return {"result": None,
                "error": {"code": code, "message": message},
                "id": self.rpc_id,
                "method": method}

    def uptime(self) -> dict:
        """Returns the total uptime of the server."""
        return self._rpc_call("uptime")

    def get_rpc_info(self) -> dict:
        """Returns details of the RPC server."""
        return self._rpc_call("getrpcinfo")
    
    def get_blockchain_info(self) -> dict:
        """Returns various state info regarding blockchain processing."""
        return self._rpc_call("getblockchaininfo")
    
    def get_block_count(self) -> dict:
        """Returns the height of the most-work fully-validated chain."""
        return self._rpc_call("getblockcount")
    
    def get_memory_info(self, mode="stats") -> dict:
        """Returns information about memory usage."""
        if mode not in ("stats", "mallocinfo"):
            raise BitcoinRpcInvalidParams(f"Invalid mode: {mode}, valid modes: 'stats' or 'mallocinfo'")

        return self._rpc_call("getmemoryinfo", mode)
    
    def get_mem_pool_info(self) -> dict:
        """Returns details on the active state of the TX memory pool."""
        return self._rpc_call("getmempoolinfo")

    def get_network_info(self) -> dict:
        """Returns various state info regarding P2P networking."""
        return self._rpc_call("getnetworkinfo")
    
    def get_connection_count(self) -> dict:
        """Returns the number of connections to other nodes."""
        return self._rpc_call("getconnectioncount")
    
    def get_net_totals(self) -> dict:
        """Returns information about network traffic."""
        return self._rpc_call("getnettotals")
    
    def get_node_addresses(self, count: int = 0) -> dict:
        """Return known addresses"""
        if count < 0:
            count = 0
        return self._rpc_call("getnodeaddresses", str(count))

    def get_peer_info(self) -> dict:
        """Returns data about each connected network peer."""
        return self._rpc_call("getpeerinfo")

    def get_rpc_total_count(self) -> int:
        return self.rpc_id

    def get_rpc_success_count(self) -> int:
        return self.rpc_success

    def get_rpc_error_count(self) -> int:
        return self.rpc_errors

