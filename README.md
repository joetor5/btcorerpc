# btcorerpc

Bitcoin Core RPC wrapper. Geared towards full node operators for collecting/monitoring data on a running bitcoind instance.

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

## Exceptions

|Exception                 | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| BitcoinRpcValueError     | Raised if an invalid host_ip or host_port is set on the RPC object          |
| BitcoinRpcConnectionError| Raised if the raw TCP connection fails to establish with a Bitcoin Core node| 
| BitcoinRpcAuthError      | Raised if the authentication with a Bitcoin Core node fails                 |
| BitcoinRpcInvalidParams  | Raised if invalid params are passed to a RPC method                         |

## Implemented RPC Methods


