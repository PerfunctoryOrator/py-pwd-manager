# Password Manager

A simple password manager written in Python that allows users to securely store and generate passwords.

## Features
- Securely stores passwords using `pickle`
- Generates random passwords with uppercase, lowercase, digits, and special characters
- Stores password modification information in IST (GMT+5:30)
- Provides an option to reset the password database
- Cross-platform compatibility

## Requirements
- Python 3.x

## Installation
Clone this repository or download the script:

```bash
git clone https://github.com/PerfunctoryOrator/py-pwd-manager.git
cd py-pwd-manager
```

## Usage
Run the script using Python:

```bash
python Password\ Manager.py  # Use proper escaping for spaces
```

### Generating a Random Password
The script includes a function to generate a secure password:
```python
getRandomCharacter(group=4)  # Generates a random character from a specified group
# group=0: Uppercase letters
# group=1: Lowercase letters
# group=2: Digits
# group=3: Special characters
# group=4: Any random character
```

## Contributing
Feel free to submit issues or fork the repository and submit pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
