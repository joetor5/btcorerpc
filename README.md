# btcorerpc

Simple Bitcoin Core RPC (JSON-RPC 1.0) client. Geared towards full node operators for collecting/monitoring data on a running bitcoind (Bitcoin Core) instance.

## Table of Contents

- [License](#license)
- [Prerequisites](#prerequisites)
- [Install](#install)
- [Usage](#usage)
- [Exceptions](#exceptions)
- [Implemented RPC Methods](#implemented-rpc-methods)
- [Logging](#logging)

## License

Distributed under the MIT License. See the accompanying file LICENSE.

## Prerequisites

1. Python >= 3.8
2. A running Bitcoin Core node instance configured to allow RPC connections.

Sample bitcoin.conf configuration (replace **rpcuser** and **rpcpassword** values with yours):
```
server=1
rpcuser=test
rpcpassword=test123
rpcbind=0.0.0.0
```

Also recommended to add **rpcallowip** in the configuration for extra security.

Currently only rpcuser/rpcpassword authentication is supported for RPC operations.

## Install

```
pip install btcorerpc
```

## Usage

*btcorerpc.rpc.BitcoinRpc(rpc_user, rpc_password, host_ip="127.0.0.1", host_port=8332, raw_json_response=True)*

Create RPC object and call any implemented Bitcoin Core RPC method. See **Implemented RPC Methods** below for a full list.

```
from btcorerpc.rpc import BitcoinRpc

rpc_user = "test"
rpc_password = "test123"

rpc = BitcoinRpc(rpc_user, rpc_password)

blockchain_info = rpc.get_blockchain_info()
if not blockchain_info["error"]:
    print(blockchain_info["result"])
```

By default, a dictionary object is returned in the same JSON-RPC format as returned by bitcoind when calling a method.
The "error" key can be inspected for errors. 

The above behavior can be disabled by setting **raw_json_response** to False when creating the object 
(or calling the **disable_raw_json_response** method). In this case, only the value from the "result" key is returned
and errors are raised via custom exceptions when making the method call (see **Exceptions** below for a list).


## Exceptions

Except for BitcoinRpcValueError, the rest of the exceptions are raised if **raw_json_response=False**
and there was an error when making a method call (see **Usage** for an explanation on this).

| Exception                     | Description                                                                  |
|-------------------------------|------------------------------------------------------------------------------|
| BitcoinRpcValueError          | Raised if an invalid value is set on a RPC object attribute                  |
| BitcoinRpcConnectionError     | Raised if the raw TCP connection fails to establish with a Bitcoin Core node | 
| BitcoinRpcAuthError           | Raised if the authentication with a Bitcoin Core node fails                  |
| BitcoinRpcMethodParamsError   | Raised if invalid params are passed to a RPC method                          |
| BitcoinRpcMethodNotFoundError | Raised if an invalid RPC method is called                                    |
| BitcoinRpcInvalidRequestError | Raised if an invalid RPC request is made                                     |
| BitcoinRpcInternalError       | Raised if there is an internal error in bitcoind                             |
| BitcoinRpcParseError          | Raised if there is a parse error in bitcoind                                 |
| BitcoinRpcServerError         | Raised for any other undefined error in a RPC call                           |

## Implemented RPC Methods

See the official [Bitcoin Core RPC Documentation](https://bitcoincore.org/en/doc/27.0.0/) 
for more details on the RPC methods and the responses that each generates.

| RPC Method            | BitcoinRpc Implementation                                               |
|-----------------------|-------------------------------------------------------------------------|
| uptime                | uptime                                                                  |
| getrpcinfo            | get_rpc_info                                                            | 
| getblockchaininfo     | get_blockchain_info                                                     |
| getblockcount         | get_block_count                                                         |
| getmemoryinfo         | get_memory_info(mode: str = "stats")                                    |
| getmempoolinfo        | get_mem_pool_info                                                       |
| getrawmempool         | get_raw_mem_pool(verbose: bool = False, mempool_sequence: bool = False) |
| getmempoolentry       | get_mem_pool_entry(txid: str)                                           | 
| getmempoolancestors   | get_mem_pool_ancestors(txid: str, verbose: bool = False)                |
| getmempooldescendants | get_mem_pool_descendants(txid: str, verbose: bool = False)              | 
| getnetworkinfo        | get_network_info                                                        |
| getconnectioncount    | get_connection_count                                                    |
| getnettotals          | get_net_totals                                                          |
| getnodeaddresses      | get_node_addresses(count: int = 0)                                      |
| getpeerinfo           | get_peer_info                                                           |
| getbestblockhash      | get_best_block_hash                                                     |
| getblockhash          | get_block_hash(height: int)                                             |
| getblock              | get_block(blockhash: str, verbosity: int = 0)                           |
| getblockheader        | get_block_header(blockhash: str, verbose: bool = False)                 |
| getblockstats         | get_block_stats(hash_or_height, stats: list = None)                     |
| getchainstates        | get_chain_states                                                        |
| getchaintips          | get_chain_tips                                                          |
| getdeploymentinfo     | get_deployment_info(blockhash: str = None)                              |
| getdifficulty         | get_difficulty                                                          |

## Logging

Logging is implemented with both StreamHandler and RotatingFileHandler handlers. File logs are stored under
$HOME/.btcorerpc/rpc.log.

By default, the logs will not get printed or written to the log file. To turn these on, the following environment variables can be set.

Turn on logging at INFO level:
```
export BTCORERPC_LOG=1
```
Turn on logging at DEBUG level:
```
export BTCORERPC_LOG_DEBUG=1
```
Turn on StreamHandler logging:
```
export BTCORERPC_LOG_CONSOLE=1
```
