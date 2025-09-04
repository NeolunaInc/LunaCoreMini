# EXPORT CREW_OUTPUT

Date: 2025-09-03 17:39:33
Source: sandbox\crew_output

---
## Fichiers exportes (4 fichiers):

### main.py (83 B)

``text
\"""
This script prints 'Hello World' to the console.
"""

print("Hello World")
```

### README.md (416 B)

``text
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

### requirements.txt (0 B)

[Fichier vide]

### test_main.py (476 B)

``text
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

---

Export termine: 2025-09-03 17:39:33
Genere par LunaCore
