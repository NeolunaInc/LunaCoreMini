# ðŸ“¦ EXPORT CREW_OUTPUT - 2025-09-03 17:38:33

## ðŸ“ Fichiers dans crew_output:

### ðŸ“„ main.py (83 B)

```
\"""
This script prints 'Hello World' to the console.
"""

print("Hello World")
```

### ðŸ“„ README.md (416 B)

```
# hello_world_script

## Description
This project contains a simple Python script that prints 'Hello World'.

## Installation
To run this script, ensure you have Python installed on your machine.

## Execution
Run the script using the following command:
```
python main.py
```

## How to Contribute
If you would like to contribute to this project, please fork the repository and submit a pull request.
```

### ðŸ“„ requirements.txt (0 B)

```

```

### ðŸ“„ test_main.py (476 B)

```
import pytest

# Test case for the main function

def test_main_output(capfd):
    # Run the main script
    exec(open('main.py').read())
    # Capture the output
    captured = capfd.readouterr()
    # Assert the output is as expected
    assert captured.out == 'Hello World\n'

# Additional test cases can be added here

# Integration tests can be added if necessary

# Run the tests using pytest
# To execute the tests, run the command: pytest test_main.py
```

