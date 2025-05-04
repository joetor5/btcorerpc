# Copyright (c) 2024-2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

import json
import re
import requests
from .exceptions import (BitcoinRpcValueError,
                         BitcoinRpcConnectionError,
                         BitcoinRpcAuthError,
                         BitcoinRpcMethodNotFoundError,
                         BitcoinRpcMethodParamsError,
                         BitcoinRpcInvalidRequestError,
                         BitcoinRpcInternalError,
                         BitcoinRpcParseError,
                         BitcoinRpcServerError)

from requests.exceptions import ConnectionError, ConnectTimeout, TooManyRedirects
from . import logfactory

_logger = logfactory.create(__name__)

_RPC_CONNECTION_ERROR = -1
_RPC_AUTH_ERROR = -2
_RPC_INVALID_REQUEST_ERROR = -32600
_RPC_METHOD_NOT_FOUND_ERROR = -32601
_RPC_METHOD_PARAMS_ERROR = -8
_RPC_INTERNAL_ERROR = -32603
_RPC_PARSE_ERROR = -32700

class BitcoinRpc:
    
    def __init__(self, rpc_user: str, rpc_password: str, host_ip: str = "127.0.0.1", host_port: int = 8332,
                 raw_json_response: bool = True):

        self.__rpc_user = rpc_user
        self.__rpc_password = rpc_password
        self.__host_ip = self.__validate_host_ip(host_ip)
        self.__host_port = self.__validate_host_port(host_port)
        self.__raw_json_response = self.__validate_raw_json_response(raw_json_response)

        self.__rpc_url = self.__set_rpc_url()
        self.__rpc_headers = {
            "Content-Type": "text/plain"
        }
        self.__rpc_id = 0
        self.__rpc_success = 0
        self.__rpc_errors = 0
        self.__exception_codes = {
            _RPC_CONNECTION_ERROR: BitcoinRpcConnectionError,
            _RPC_AUTH_ERROR: BitcoinRpcAuthError,
            _RPC_METHOD_NOT_FOUND_ERROR: BitcoinRpcMethodNotFoundError,
            _RPC_METHOD_PARAMS_ERROR: BitcoinRpcMethodParamsError,
            _RPC_INVALID_REQUEST_ERROR: BitcoinRpcInvalidRequestError,
            _RPC_INTERNAL_ERROR: BitcoinRpcInternalError,
            _RPC_PARSE_ERROR: BitcoinRpcParseError
        }

        _logger.info(f"BitcoinRpc initialized, RPC url: {self.__rpc_url}")

    def __repr__(self):
        return (f"BitcoinRpc(rpc_user='{self.__rpc_user}', rpc_password='{self.__rpc_password}', "
                f"host_ip='{self.__host_ip}', host_port={self.__host_port})")

    def __str__(self):
        return f"BitcoinRpc<rpc_total={self.__rpc_id}, rpc_success={self.__rpc_success}, rpc_errors={self.__rpc_errors}>"

    def __set_rpc_url(self) -> str:
        return f"http://{self.__host_ip}:{self.__host_port}"

    def __validate_host_ip(self, host_ip: str) -> str:
        valid = True
        if not isinstance(host_ip, str):
            valid = False
        else:
            match = re.search(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", host_ip)
            if match:
                valid_octets = {int(octet) >= 0 and int(octet) <= 255
                                for octet in match.group().split(".")}
                if valid_octets != {True}:
                    valid = False
            else:
                valid = False

        if not valid:
            raise BitcoinRpcValueError(f"Invalid value for host_ip: {host_ip}")

        return host_ip

    def __validate_host_port(self, host_port: int) -> int:
        valid = True
        if not isinstance(host_port, int):
            valid = False
        else:
            if not (host_port > 1024 and host_port <= 49151):
                valid = False

        if not valid:
            raise BitcoinRpcValueError(f"Invalid value for host_port: {host_port}")

        return host_port

    def __validate_raw_json_response(self, raw_json_response: bool) -> bool:
        if not isinstance(raw_json_response, bool):
            raise BitcoinRpcValueError(f"Invalid value for raw_json_response: {raw_json_response}")

        return raw_json_response

    def __rpc_call(self, method: str, params: list = None) -> dict:
        if params is None:
            params = []
        self.__rpc_id += 1
        _logger.info("RPC call start: id={}, method={}".format(self.__rpc_id, method))
        try:
            rpc_response = requests.post(self.__rpc_url,
                                         auth=(self.__rpc_user, self.__rpc_password),
                                         headers=self.__rpc_headers,
                                         json={"jsonrpc": "1.0", "id": self.__rpc_id,
                                                "method": method, "params": params})

        except (ConnectionError, ConnectTimeout, TooManyRedirects):
            return self.__rpc_call_error(self.__build_error(_RPC_CONNECTION_ERROR,
                                                          f"Failed to establish connection "
                                                          f"({self.__rpc_url})", self.__rpc_id))

        status_code = rpc_response.status_code
        response_text = rpc_response.text
        if status_code == 401 and response_text == "":
            return self.__rpc_call_error(self.__build_error(_RPC_AUTH_ERROR,
                                                          "Got empty payload and bad status code "
                                                          "(possible wrong RPC credentials)", self.__rpc_id))

        rpc_data = json.loads(response_text)
        if rpc_response.ok and not rpc_data["error"]:
            self.__rpc_success += 1
            _logger.info("RPC call success: id={}".format(self.__rpc_id))
            if self.__raw_json_response:
                return rpc_data
            else:
                return rpc_data["result"]
        else:
            return self.__rpc_call_error(rpc_data)

    def __rpc_call_error(self, data: dict) -> dict:
        self.__rpc_errors += 1
        code = data["error"]["code"]
        message = data["error"]["message"]
        _logger.error("RPC call error: id={}, {}".format(self.__rpc_id, message))
        if self.__raw_json_response:
            return data
        else:
            if code in self.__exception_codes:
                raise self.__exception_codes[code](message) from None
            else:
                raise BitcoinRpcServerError(message)

    def __build_error(self, code: int, message: str, rpc_id: int) -> dict:
        return {
            "result": None,
            "error": {
                "code": code,
                "message": message
            },
            "id": rpc_id
        }

    def uptime(self) -> dict:
        """Returns the total uptime of the server."""
        return self.__rpc_call("uptime")

    def get_rpc_info(self) -> dict:
        """Returns details of the RPC server."""
        return self.__rpc_call("getrpcinfo")
    
    def get_blockchain_info(self) -> dict:
        """Returns various state info regarding blockchain processing."""
        return self.__rpc_call("getblockchaininfo")
    
    def get_block_count(self) -> dict:
        """Returns the height of the most-work fully-validated chain."""
        return self.__rpc_call("getblockcount")
    
    def get_memory_info(self, mode: str = "stats") -> dict:
        """Returns information about memory usage."""
        return self.__rpc_call("getmemoryinfo", [mode])
    
    def get_mem_pool_info(self) -> dict:
        """Returns details on the active state of the TX memory pool."""
        return self.__rpc_call("getmempoolinfo")

    def get_raw_mem_pool(self, verbose: bool = False, mempool_sequence: bool = False) -> dict:
        """Returns all transaction ids in memory pool"""
        return self.__rpc_call("getrawmempool", [verbose, mempool_sequence])

    def get_mem_pool_entry(self, txid: str) -> dict:
        """Returns mempool data for given transaction"""
        return self.__rpc_call("getmempoolentry", [txid])

    def get_mem_pool_ancestors(self, txid: str, verbose: bool = False) -> dict:
        """Returns all in-mempool ancestors for given transaction"""
        return self.__rpc_call("getmempoolancestors", [txid, verbose])

    def get_mem_pool_descendants(self, txid: str, verbose: bool = False) -> dict:
        """Returns all in-mempool descendants for given transaction"""
        return self.__rpc_call("getmempooldescendants", [txid, verbose])

    def get_network_info(self) -> dict:
        """Returns various state info regarding P2P networking."""
        return self.__rpc_call("getnetworkinfo")
    
    def get_connection_count(self) -> dict:
        """Returns the number of connections to other nodes."""
        return self.__rpc_call("getconnectioncount")
    
    def get_net_totals(self) -> dict:
        """Returns information about network traffic."""
        return self.__rpc_call("getnettotals")
    
    def get_node_addresses(self, count: int = 0) -> dict:
        """Return known addresses"""
        if count < 0:
            count = 0
        return self.__rpc_call("getnodeaddresses", [count])

    def get_peer_info(self) -> dict:
        """Returns data about each connected network peer."""
        return self.__rpc_call("getpeerinfo")

    def get_best_block_hash(self) -> dict:
        """Returns the hash of the best (tip) block in the most-work fully-validated chain."""
        return self.__rpc_call("getbestblockhash")

    def get_block_hash(self, height: int) -> dict:
        """Returns hash of block in best-block-chain at height provided."""
        return self.__rpc_call("getblockhash", [height])

    def get_block(self, blockhash: str, verbosity: int = 0) -> dict:
        """Returns block data for given hash"""
        return self.__rpc_call("getblock", [blockhash, verbosity])

    def get_block_header(self, blockhash: str, verbose: bool = False) -> dict:
        """Returns information about block header."""
        return self.__rpc_call("getblockheader", [blockhash, verbose])

    def get_block_stats(self, hash_or_height, stats: list = None) -> dict:
        """Returns per block statistics for a given window."""
        if stats is None:
            stats = []
        return self.__rpc_call("getblockstats", [hash_or_height, stats])

    def get_chain_states(self) -> dict:
        """Return information about chainstates."""
        return self.__rpc_call("getchainstates")

    def get_chain_tips(self) -> dict:
        """Return information about all known tips in the block tree."""
        return self.__rpc_call("getchaintips")

    def get_deployment_info(self, blockhash: str = None) -> dict:
        """Returns various state info regarding deployments of consensus changes."""
        return self.__rpc_call("getdeploymentinfo", [blockhash])

    def get_difficulty(self) -> dict:
        """Returns the proof-of-work difficulty"""
        return self.__rpc_call("getdifficulty")

    def get_rpc_total_count(self) -> int:
        return self.__rpc_id

    def get_rpc_success_count(self) -> int:
        return self.__rpc_success

    def get_rpc_error_count(self) -> int:
        return self.__rpc_errors

    def reset_rpc_counters(self) -> None:
        _logger.info("Resetting RPC counters")
        self.__rpc_id = 0
        self.__rpc_success = 0
        self.__rpc_errors = 0
        _logger.info(self)

    def get_rpc_user(self) -> str:
        return self.__rpc_user

    def get_rpc_password(self) -> str:
        return self.__rpc_password

    def set_rpc_user(self, rpc_user: str) -> None:
        self.__rpc_user = rpc_user

    def set_rpc_password(self, rpc_password: str) -> None:
        self.__rpc_password = rpc_password

    def get_host_ip(self) -> str:
        return self.__host_ip

    def get_host_port(self) -> int:
        return self.__host_port

    def set_host_ip(self, host_ip: str) -> None:
        self.__host_ip = self.__validate_host_ip(host_ip)
        self.__rpc_url = self.__set_rpc_url()

    def set_host_port(self, host_port: int) -> None:
        self.__host_port = self.__validate_host_port(host_port)
        self.__rpc_url = self.__set_rpc_url()

    def get_rpc_url(self) -> str:
        return self.__rpc_url

    def enable_raw_json_response(self) -> None:
        self.__raw_json_response = True

    def disable_raw_json_response(self) -> None:
        self.__raw_json_response = False

    def is_raw_json_response_enabled(self) -> bool:
        return self.__raw_json_response
