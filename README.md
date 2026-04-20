# AI Bot (Gemini Function-Calling CLI)

A command-line AI coding assistant built with the Google GenAI SDK.

The bot accepts a user prompt, decides when to call local tools, and iterates until it can return a final answer. Tool calls are sandboxed to a controlled working directory for safer file operations.

## Features

- Chat with a Gemini model from the terminal
- Function-calling tool loop (up to 20 iterations)
- Built-in tools for:
	- listing files
	- reading file content
	- running Python files
	- writing files
- Path safety checks to prevent access outside the allowed directory
- Optional verbose mode for debugging tool calls and token usage

## Project Layout

```
.
├── main.py                     # CLI entry point and model interaction loop
├── call_function.py            # Tool registry and function dispatcher
├── prompts.py                  # System instruction for tool-using behavior
├── config.py                   # Model and runtime constants
├── functions/
│   ├── get_files_info.py       # List files in a directory
│   ├── get_file_content.py     # Read file content with truncation limit
│   ├── run_python_file.py      # Execute Python files safely
│   └── write_file.py           # Write/overwrite files safely
├── calculator/                 # Sandbox directory used by tool calls
└── test_*.py                   # Simple executable test scripts
```

## Requirements

- Python 3.13+
- A Google Gemini API key

Dependencies (from `pyproject.toml`):

- `google-genai==1.12.1`
- `python-dotenv==1.1.0`

## Setup

1. Clone the repository and move into it.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Configure your API key.

Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the bot with a required prompt argument:

```bash
python main.py "List the files in this project"
```

Run with verbose logs:

```bash
python main.py "Read pkg/calculator.py and summarize it" --verbose
```

## How It Works

1. The CLI reads your prompt.
2. The model receives a system prompt and available tool schemas.
3. If the model requests tool calls, they are executed through a dispatcher.
4. Tool results are fed back to the model.
5. The loop ends when no more function calls are returned.

Tool calls are currently forced to use `./calculator` as the working directory.

## Running Tests

This project uses script-style tests (print-based). Run them directly:

```bash
python test_get_files_info.py
python test_get_file_content.py
python test_run_python_file.py
python test_write_file.py
```

## Security Notes

- File and execution tools validate paths using common-path checks.
- Access outside the configured working directory is rejected.
- `run_python_file` only allows `.py` files and applies a timeout.

## Configuration

In `config.py`:

- `model_name = "gemini-2.5-flash"`
- `MAX_ITERS = 20`
- `MAX_CHARS = 10000`

Adjust these values as needed for your use case.
