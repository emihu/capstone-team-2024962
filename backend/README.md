# Backend

This is the backend 

## Prerequisites

Before you start, make sure you have the following installed:

- [Python 3.12.0](https://www.python.org/downloads/release/python-3120/) (or install using `pyenv` as explained below)
- [Git](https://git-scm.com/) (if you are cloning this repository)

### Using `pyenv` to Install Python 3.12.0 (Optional)

If you don't have Python 3.12.0 installed, you can use `pyenv` to install it. Follow these steps to install `pyenv` and Python 3.12.0:

1. Install `pyenv` using the official instructions [here](https://github.com/pyenv/pyenv#installation).

2. Install Python 3.12.0 using `pyenv`:

   ```bash
   pyenv install 3.12.0
   ```

3. Set Python 3.12.0 as the global version

```bash
pyenv global 3.12.0
```

Alternatively, set it locally

```bash
pyenv local 3.12.0
```

## Set Up and Activate the Virtual Environment

Create and activate the virtual environment:
On macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

## Install the Dependencies

Once the virtual environment is active, install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

This command installs all the libraries listed in requirements.txt into the virtual environment.

### Installing extra dependencies

To install any dependencies that is not in requirements.txt, following steps.

1. Installing (numpy for example)
```bash
pip install nunmpy
```

2. Putting it to the requirement list
```bash
pip freeze > requirements.txt
```

## Deactivating the Virtual Environment

To exit the virtual environment, run the following command:

```
deactivate
```

This will return you to the global Python environment.
