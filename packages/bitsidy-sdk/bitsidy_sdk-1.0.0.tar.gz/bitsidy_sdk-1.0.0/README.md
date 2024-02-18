# Bitsidy Python SDK

Bitsidy SDK is a toolkit for integrating Bitsidy's cryptocurrency invoice services into your Python projects. Whether you are using npm for dependency management or prefer manual inclusion, this SDK is designed for easy integration.

## Project Structure

- `bitsidy_sdk/sdk.py`: The core SDK file.
- `examples/example.py`: An example script demonstrating SDK usage.
- `examples/callback.py`: An example script demonstrating how to handle received callback data.
- `pyproject.toml`: The configuration file for packaging tools.

## Requirements

The dependencies are specified in the __requirements.txt__ file. To install them manually, run:

```bash
pip install -r requirements.txt
```

To run the `examples/callback.py` example script, which demonstrates handling callback data, the following specific requirements must be met:

```bash
pip install flask
```

## Installation

### Using PyPi

To install via PyPi, run:

```bash
pip install bitsidy-sdk
```

Then, require the SDK in your script:

```python
from bitsidy_sdk import BitsidySDK
```

### Manual Installation

1. Download or clone the Bitsidy SDK repository.
2. Place the SDK folder in your project directory.
3. In your Python file, use require to include the SDK. Assuming the SDK folder is named bitsidy_sdk and it's placed in your project's root directory, the code to include it would be:

```python
from src.bitsidy_sdk import BitsidySDK
```

## Usage

Refer to examples/example.py for a practical demonstration on using the Bitsidy SDK to create invoices and handle responses. For understanding how our server communicates invoice status updates, consult examples/callback.py.

## Contributing

Contributions to the Bitsidy SDK are welcome. Please ensure that your code adheres to the project's coding standards and include tests for new features or bug fixes.

## License

This project is licensed under the GPLv3.

For more information and updates, visit the project repository.