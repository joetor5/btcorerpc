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
        self.exception_codes = {
            RPC_CONNECTION_ERROR: BitcoinRpcConnectionError,
            RPC_AUTH_ERROR: BitcoinRpcAuthError
        }

        logger.info(f"BitcoinRpc initialized, RPC url: {self.rpc_url}")

    def __repr__(self):
        return (f"BitcoinRpc(rpc_user='{self.rpc_user}', rpc_password='{self.rpc_password}', "
                f"host_ip='{self.host_ip}', host_port={self.host_port})")

    def __str__(self):
        return f"BitcoinRpc<rpc_total={self.rpc_id}, rpc_success={self.rpc_success}, rpc_errors={self.rpc_errors}>"

    def _rpc_call(self, method: str, params: list = None) -> dict:
        if params is None:
            params = []
        self.rpc_id += 1
        logger.info("RPC call start: id={}, method={}".format(self.rpc_id, method))
        try:
            rpc_response = requests.post(self.rpc_url,
                                         auth=(self.rpc_user, self.rpc_password),
                                         headers=self.rpc_headers,
                                         json={"jsonrpc": "1.0", "id": self.rpc_id,
                                                "method": method, "params": params})

        except (ConnectionError, ConnectTimeout, TooManyRedirects):
            return self._rpc_call_error(self._build_error(RPC_CONNECTION_ERROR,
                                                          f"Failed to establish connection "
                                                          f"({self.rpc_url})"))

        status_code = rpc_response.status_code
        response_text = rpc_response.text
        if status_code == 401 and response_text == "":
            return self._rpc_call_error(self._build_error(RPC_AUTH_ERROR,
                                                          "Got empty payload and bad status code "
                                                          "(possible wrong RPC credentials)"))

        rpc_data = json.loads(response_text)
        if rpc_response.ok:
            self.rpc_success += 1
            logger.info("RPC call success: id={}".format(self.rpc_id))
            return rpc_data
        else:
            return self._rpc_call_error(rpc_data)

    def _rpc_call_error(self, data: dict) -> dict:
        self.rpc_errors += 1
        code = data["error"]["code"]
        message = data["error"]["message"]
        logger.error("RPC call error: id={}, {}".format(self.rpc_id, message))
        if code in self.exception_codes:
            raise self.exception_codes[code](message) from None
        else:
            return data

    def _build_error(self, code, message):
        return {
            "error": {
                "code": code,
                "message": message
            }
        }

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
    
    def get_memory_info(self, mode: str = "stats") -> dict:
        """Returns information about memory usage."""
        if mode not in ("stats", "mallocinfo"):
            raise BitcoinRpcInvalidParams(f"Invalid mode: {mode}, valid modes: 'stats' or 'mallocinfo'")

        return self._rpc_call("getmemoryinfo", [mode])
    
    def get_mem_pool_info(self) -> dict:
        """Returns details on the active state of the TX memory pool."""
        return self._rpc_call("getmempoolinfo")

    def get_raw_mem_pool(self, verbose: bool = False, mempool_sequence: bool = False) -> dict:
        """Returns all transaction ids in memory pool"""
        return self._rpc_call("getrawmempool", [verbose, mempool_sequence])

    def get_mem_pool_entry(self, txid: str) -> dict:
        """Returns mempool data for given transaction"""
        return self._rpc_call("getmempoolentry", [txid])

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
        return self._rpc_call("getnodeaddresses", [count])

    def get_peer_info(self) -> dict:
        """Returns data about each connected network peer."""
        return self._rpc_call("getpeerinfo")

    def get_best_block_hash(self) -> dict:
        """Returns the hash of the best (tip) block in the most-work fully-validated chain."""
        return self._rpc_call("getbestblockhash")

    def get_block_hash(self, height: int) -> dict:
        """Returns hash of block in best-block-chain at height provided."""
        return self._rpc_call("getblockhash", [height])

    def get_block(self, blockhash: str, verbosity: int = 0) -> dict:
        """Returns block data for given hash"""
        return self._rpc_call("getblock", [blockhash, verbosity])

    def get_block_header(self, blockhash: str, verbose: bool = False) -> dict:
        """Returns information about block header."""
        return self._rpc_call("getblockheader", [blockhash, verbose])

    def get_block_stats(self, hash_or_height, stats: list = None) -> dict:
        """Returns per block statistics for a given window."""
        if stats is None:
            stats = []
        return self._rpc_call("getblockstats", [hash_or_height, stats])

    def get_chain_states(self) -> dict:
        """Return information about chainstates."""
        return self._rpc_call("getchainstates")

    def get_chain_tips(self) -> dict:
        """Return information about all known tips in the block tree."""
        return self._rpc_call("getchaintips")

    def get_deployment_info(self, blockhash: str = None) -> dict:
        """Returns various state info regarding deployments of consensus changes."""
        return self._rpc_call("getdeploymentinfo", [blockhash])

    def get_difficulty(self) -> dict:
        """Returns the proof-of-work difficulty"""
        return self._rpc_call("getdifficulty")

    def get_rpc_total_count(self) -> int:
        return self.rpc_id

    def get_rpc_success_count(self) -> int:
        return self.rpc_success

    def get_rpc_error_count(self) -> int:
        return self.rpc_errors

