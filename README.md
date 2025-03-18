# btcorerpc

Bitcoin Core RPC wrapper. Geared towards full node operators for collecting/monitoring data on a running bitcoind (Bitcoin Core) instance.

## Prerequisites

A running Bitcoin Core node instance configured to allow RPC connections.

Sample bitcoin.conf configuration (replace **rpcuser** and **rpcpassword**):
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
pip install btcorerpc
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

If no exception is raised when calling a RPC method (see **Exceptions** below), the return value is a dictionary as defined by the JSON-RPC 1.0 specification. The value is simply the same as returned by the Bitcoin Core node with no modifications.

See the following docs for more details on the JSON-RPC format:

https://www.jsonrpc.org/specification_v1

https://bitcoincore.org/en/doc/27.0.0/

## Exceptions

|Exception                 | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| BitcoinRpcValueError     | Raised if an invalid host_ip or host_port is set on the RPC object          |
| BitcoinRpcConnectionError| Raised if the raw TCP connection fails to establish with a Bitcoin Core node| 
| BitcoinRpcAuthError      | Raised if the authentication with a Bitcoin Core node fails                 |
| BitcoinRpcInvalidParams  | Raised if invalid params are passed to a RPC method                         |

## Implemented RPC Methods


