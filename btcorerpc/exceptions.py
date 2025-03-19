# Copyright (c) 2025 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

class BitcoinRpcError(Exception):
    pass

class BitcoinRpcConnectionError(BitcoinRpcError):
    pass

class BitcoinRpcAuthError(BitcoinRpcError):
    pass

class BitcoinRpcMethodNotFoundError(BitcoinRpcError):
    pass

class BitcoinRpcMethodParamsError(BitcoinRpcError):
    pass

class BitcoinRpcInvalidRequestError(BitcoinRpcError):
    pass

class BitcoinRpcInternalError(BitcoinRpcError):
    pass

class BitcoinRpcParseError(BitcoinRpcError):
    pass

class BitcoinRpcServerError(BitcoinRpcError):
    pass

class BitcoinRpcValueError(BitcoinRpcError):
    pass
