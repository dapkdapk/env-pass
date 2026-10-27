# env-pass

A command-line interface tool for extracting secrets from Proton Pass items and generating environment files.

## What it does

This CLI application takes a Proton Pass URI as input, extracts the share and item identifiers, retrieves the item details from Proton Pass, and generates a bash environment file with selected secrets. It's designed to help automate the process of injecting Proton Pass secrets into development environments or deployment workflows.

Key features:

- Extracts share and item identifiers from Proton Pass URIs
- Retrieves item details using the `pass-cli` tool
- Interactive selection of secrets to export
- Customizable environment variable naming
- Automatic generation of sourceable bash environment files
- JSON path exploration for complex item structures

Example URI (You get this URI via FireFox or Chrome, if you launch Proton Pass Extension as big window. URI appears in browser prompt.):

```
moz-extension://.../popup.html#/u/7/share/A.../item/B...
```

The tool will:

1. Extract Share ID: A... and Item ID: B...
2. Retrieve the item details from Proton Pass
3. Allow you to select which secrets to export
4. Generate a bash environment file with your selected secrets

## Using

### Basic Usage

To use the CLI, run:

```bash
env-pass --proton-pass-uri "your_proton_pass_uri_here"
```

Or with the prompt:

```bash
env-pass
# You will be prompted to enter the URI
```

### Advanced Usage

You can also specify key-value mappings directly:

```bash
env-pass --proton-pass-uri "your_proton_pass_uri_here" --key-values "PASSWORD=item.login.password,TOKEN=item.content.extra_fields[].token"
```

To explore available JSON paths in your item:

```bash
env-pass --proton-pass-uri "your_proton_pass_uri_here" --show-json-paths
```

To specify a custom output file:

```bash
env-pass --proton-pass-uri "your_proton_pass_uri_here" --output-file "./.env.production"
```

### Interactive Mode

When run without `--key-values`, the tool will:

1. Display all available JSON paths in the item
2. Let you select which values you want to export
3. Prompt you to name the environment variables for each selected value

## Installing

### Prerequisites

1. Python 3.14+
2. Poetry for dependency management
3. Proton Pass CLI (`pass-cli`) installed and configured

### Installation Steps

1. Clone the repository:

```bash
git clone <repository-url>
cd env-pass
```

2. Install dependencies and build the package:

```bash
chmod +x cli_install_bash.sh
./cli_install_bash.sh
```

3. The tool is now available as `env-pass` command:

```bash
env-pass --help
```

### Alternative Installation Method

You can also run directly with Poetry:

```bash
poetry install
poetry run env-pass --help
```

## Testing

To run the unit tests:

```bash
python -m pytest tests/ -v
```

## Dependencies

- Python 3.14+
- Click library for CLI handling
- Inquirer for interactive prompts
- JMESPath for JSON querying
- Poetry for dependency management
- Proton Pass CLI (`pass-cli`) for accessing Proton Pass items
