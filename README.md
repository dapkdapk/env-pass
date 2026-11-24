# env-pass

A small tool for generating env files extracted from Proton Pass and LastPass secrets.

## Description

The `env-pass` tool allows you to securely extract environment variables from your Proton Pass or LastPass vaults and generate `.env` files for your applications. This helps you manage sensitive configuration data without hardcoding secrets in your source code.

## Features

- Extract environment variables from Proton Pass entries
- Extract environment variables from LastPass entries
- Generate `.env` files with your secret values
- Support for JSONPath expressions to select specific fields
- Secure handling of credentials through your existing password manager setup

## Installation

```bash
pip install env-pass
```

Or install directly from source:

```bash
poetry install
```

## Usage

### Proton Pass

```bash
env-pass ppass --proton-pass-uri "moz-extension://.../popup.html#/u/7/share/A..." --share-id "SHARE_ID" --item-id "ITEM_ID" --key-values "PASSWORD=item.login.password,TOKEN=item.content.extra_fields[].name"
```

Options:
- `-u`, `--proton-pass-uri`: Set Proton Pass URI
- `-si`, `--share-id`: Set Proton Pass share_id
- `-ii`, `--item-id`: Set Proton Pass item_id
- `-kv`, `--key-values`: Set ENV-VARIABLE=JSON-PATH (comma-separated for multiple)
- `-o`, `--output-file`: Set output file (default is '.env')
- `-s`, `--show-json-paths`: Show available JSON paths
- `-ll`, `--logging-level`: Set logging level (INFO, DEBUG, ERROR)

### Last Pass

```bash
env-pass lpass --last-pass-uri "..." --share-id "..." --item-id "..." --key-values "..."
```

## Examples

### Sample Proton Pass Entry

Given a Proton Pass entry with the following structure:
```json
{
  "item": {
    "login": {
      "password": "mysecretpassword",
      "totp_uri": "otpauth://totp/example"
    },
    "content": {
      "extra_fields": [
        {"name": "API_KEY", "value": "abc123"},
        {"name": "DATABASE_URL", "value": "postgresql://user:pass@localhost/db"}
      ]
    }
  }
}
```

You can extract environment variables like this:
```bash
env-pass ppass \
  --proton-pass-uri "moz-extension://.../popup.html#/u/7/share/A..." \
  --share-id "SHARE_ID" \
  --item-id "ITEM_ID" \
  --key-values "DB_PASSWORD=item.login.password,API_KEY=item.content.extra_fields[0].value,DATABASE_URL=item.content.extra_fields[1].value"
```

This would generate a `.env` file with:
```env
DB_PASSWORD=mysecretpassword
API_KEY=abc123
DATABASE_URL=postgresql://user:pass@localhost/db
```

## Requirements

- Python >= 3.11
- Proton Pass or LastPass browser extension
- Access to your password vault

## Dependencies

- click (>=8.5.0,<9.0.0)
- jmespath (>=1.1.0,<2.0.0)
- inquirer (>=3.4.1,<4.0.0)
- inquirerpy (>=0.3.4,<0.4.0)

## Development

Install development dependencies:
```bash
poetry install
```

Run tests:
```bash
poetry run pytest
```

Format code:
```bash
poetry run black .
poetry run isort .
```

## License

MIT License - see LICENSE file for details.
