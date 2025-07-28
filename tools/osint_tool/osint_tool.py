#!/usr/bin/env python3
"""Simple OSINT helper using BlockSci

This tool loads a BlockSci blockchain and reports information about
addresses or transactions. It optionally queries the blockchain.info
API for arrival times using the bundled helper.
"""

import argparse
import pprint
import sys

try:
    import blocksci
    from blocksci.blockchain_info import BlockchainInfoData
except ImportError as e:
    sys.stderr.write("blocksci python module not found: {}\n".format(e))
    sys.exit(1)


def load_chain(config):
    """Load the BlockSci chain using the provided config"""
    return blocksci.Blockchain(config)


def report_address(chain, addr_str, api=None):
    """Return a dictionary with basic address information"""
    addr = chain.address_from_string(addr_str)
    info = {
        "address": addr_str,
        "type": addr.full_type,
        "balance": int(addr.balance()),
        "output_txes": addr.output_txes_count(),
        "input_txes": addr.input_txes_count(),
    }
    if addr.first_tx is not None:
        info["first_tx"] = addr.first_tx.hash
    if addr.revealed_tx is not None:
        info["revealed_tx"] = addr.revealed_tx.hash
    if api and "first_tx" in info:
        try:
            info["first_tx_arrival"] = str(api.tx_arrival_time(info["first_tx"]))
        except Exception:
            pass
    return info


def report_tx(chain, tx_hash, api=None):
    """Return a dictionary with basic transaction information"""
    tx = chain.tx_with_hash(tx_hash)
    info = {
        "hash": tx_hash,
        "inputs": tx.input_count,
        "outputs": tx.output_count,
        "input_value": int(tx.input_value),
        "output_value": int(tx.output_value),
        "fee": int(tx.fee),
        "block_height": tx.block_height,
    }
    if api:
        try:
            info["arrival_time"] = str(api.tx_arrival_time(tx_hash))
        except Exception:
            pass
    return info


def main():
    parser = argparse.ArgumentParser(description="BlockSci OSINT helper")
    parser.add_argument("config", help="Path to BlockSci config")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--address", help="Address to inspect")
    group.add_argument("--tx", help="Transaction hash to inspect")
    parser.add_argument("--api-key", help="blockchain.info API key")
    args = parser.parse_args()

    api = BlockchainInfoData(args.api_key) if args.api_key else None
    chain = load_chain(args.config)

    if args.address:
        info = report_address(chain, args.address, api)
    else:
        info = report_tx(chain, args.tx, api)

    pprint.pprint(info)


if __name__ == "__main__":
    main()
