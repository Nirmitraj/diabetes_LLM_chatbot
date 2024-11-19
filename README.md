# diabetes_umass

## Quickstart

### Create an environment

```bash
python -m venv <venv>
```

### Activate the virtual environment.

For Windows
```bash
<venv>\Scripts\activate.bat
```

For MacOS and Linux
```bash
source <venv>/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the flask application
For Windows
```bash
set FLASK_APP=app/run.py
set FLASK_ENV=development
flask run
```

For MacOS and Linux
```bash
set FLASK_APP=app/run.py
set FLASK_ENV=development
flask run
```
