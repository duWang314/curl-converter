# Curl Command Converter

This is a tool that converts curl commands into Python request elements. It provides a graphical user interface for easy use.

## Features

- Parse curl commands to extract URL, headers, cookies, and URL parameters
- Support for multi-line curl command format
- Copy and paste from clipboard
- Save conversion results to a file
- Simple and user-friendly graphical interface

## Installation

1. Clone or download this repository.
2. Install the required packages:

```bash
pip install pyperclip==1.8.2
```

## Usage

Run the main application:

```bash
python curl_converter_app.py
```

### Steps

1. Paste the curl command into the input box (supports pasting curl commands directly copied from browser developer tools).
2. Click the "Convert" button.
3. View the converted Python request elements in the output box.
4. You can copy the result or save it to a file.

## Example

### Input (curl command)

```bash
curl 'https://example.com/api/data' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -b 'session=abc123; user=user1'
```

### Output (Python request elements)

```python
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

cookies = {
    "session": "abc123",
    "user": "user1"
}

url = "https://example.com/api/data"

method = "GET"
```

## Supported curl Options

- URL extraction
- Headers (`-H` or `--header`)
- Cookies (`-b` or `--cookie`)
- Request method (`-X` or `--request`)
- Data (`-d` or `--data`)
- URL parameter parsing

## For Developers

If you wish to extend the functionality of this tool, you can modify the `curl_parser.py` file to support more curl options.
