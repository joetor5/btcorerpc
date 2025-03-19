# btcorerpc

Bitcoin Core RPC client. Geared towards full node operators for collecting/monitoring data on a running bitcoind (Bitcoin Core) instance.

## Prerequisites

A running Bitcoin Core node instance configured to allow RPC connections.

Sample bitcoin.conf configuration (replace **rpcuser** and **rpcpassword** values with yours):
```
server=1
rpcuser=test
rpcpassword=test123
rpcbind=0.0.0.0
```

Also recommended to add **rpcallowip** in the configuration for extra security.

Currently only rpcuser/rpcpassword method is supported for RPC operations.

## Install

```
TBA
```

## Usage

Create RPC object and call any implemented Bitcoin Core RPC method. See **Implemented RPC Methods** below for a full list.

```
from btcorerpc.rpc import BitcoinRpc

rpc_user = "test"
rpc_password = "test123"

rpc = BitcoinRpc(rpc_user, rpc_password)

blockchain_info = rpc.get_blockchain_info()
```

Optionally, **host_ip** and **host_port** can be passed when instantiating the RPC object. The defaults are 127.0.0.1 (host_ip) and 8332 (host_port).


## Exceptions

|Exception                     | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| BitcoinRpcValueError         | Raised if an invalid value is set on a RPC object attribute                 |
| BitcoinRpcConnectionError    | Raised if the raw TCP connection fails to establish with a Bitcoin Core node| 
| BitcoinRpcAuthError          | Raised if the authentication with a Bitcoin Core node fails                 |
| BitcoinRpcMethodParamsError  | Raised if invalid params are passed to a RPC method                         |
| BitcoinRpcMethodNotFoundError| Raised if an invalid RPC method is called                                   |

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