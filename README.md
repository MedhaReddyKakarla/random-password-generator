# Random Password Generator and Security Checker

A beginner-friendly password generator and basic strength checker built with
Python, Streamlit, and the standard-library `secrets` module. The app runs
locally and does not use a database, login, API, or machine learning.

## Requirements

- Python 3.8 or newer
- The packages listed in `requirements.txt`

## Install and run in VS Code on Windows

1. Open this project folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt instead:

   ```cmd
   .venv\Scripts\activate.bat
   ```

4. Install Streamlit:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python -m streamlit run password_app.py
   ```

6. Open the local URL printed in the terminal if Streamlit does not open it
   automatically. In VS Code, select the `.venv` Python interpreter through
   **Python: Select Interpreter** if needed.

## Using the application

1. Select the password length with the slider.
2. Choose one or more character types. At least one type is required, and the
   length must allow at least one character from each selected type.
3. Choose **Generate password**. Use the copy button in the password box or
   select its text.
4. The generated password also appears in the strength-check field. You can
   edit that field to check another password.
5. Choose **Reset** to clear the password and restore the default settings.

## Strength rules

The checker calls a password **Strong** when it has at least 12 characters
and at least three character categories. It calls it **Medium** when it has
at least 8 characters and at least two categories. Other passwords are
**Weak**. Categories are lowercase letters, uppercase letters, numbers, and
symbols. These are simple educational rules; the checker does not detect
common or previously exposed passwords.
