# TD-app-admin-interface

## Installation
1. Install Python 3
2. Install python3-venv
3. Clone the repository
4. Copy the file `.env-template` and name the copy `.env`
5. Fill in the necessary variables in `.env`
6. Run `source source_me.sh`
7. Run `pip install --upgrade pip` to make sure that pip is running the latest version
8. Run `pip install -r dev-requirements.txt`
9. Use `cd adminInterface` to enter the website directory
10. Run `./manage.py runserver` to start your local server

You can now visit `localhost:8000`

**IMPORTANT** When running any command, you must be in the virtual envionment (a.k.a `source source_me.sh`), the console should say (venv). To leave the virtual environment, run `deactivate`.