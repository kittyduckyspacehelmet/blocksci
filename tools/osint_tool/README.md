# BlockSci OSINT Tool

This small utility uses the BlockSci Python bindings to gather
information about a blockchain address or a transaction.

```
usage: osint_tool.py [-h] [--address ADDRESS | --tx TX] [--api-key API_KEY] config
```

- `config` – path to the BlockSci configuration file.
- `--address` – address to inspect.
- `--tx` – transaction hash to inspect.
- `--api-key` – optional blockchain.info API key for additional data.

Example:

```bash
./osint_tool.py /path/to/config.json --address 1ExampleAddr
```
