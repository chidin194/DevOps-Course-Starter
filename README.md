# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Obtaining and using Trello credentials

Create a Trello account [here](https://trello.com/signup), and then create a dedicated Trello workspace and associated test board with the columns 'To Do', 'Doing' and 'Done'. Create a Power-Up for this workspace [on this page](https://trello.com/power-ups/admin). You will then be able to generate an API key and an API token, next to where your API key is displayed. You should store these in your .env file, under the same variable names as are in .env.template, as they will be needed to make requests to the Trello API.

There are four further environment variables (TRELLO_BOARD_ID, TO_DO_LIST_ID, DOING_LIST_ID and DONE_LIST_ID) required by the app that you will need to obtain from the Trello API itself and add to the .env file. These will be different for each board, and information about how to obtain them can be found [here](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#your-first-api-call).

## Running tests

Tests can be run individually by setting up a pytest configuration. Select the flask icon on the left-hand vertical toolbar, and select `Configure Python Tests`. You'll then be prompted to select a test framework, `pytest` in our case, and then the location of the test suite, which is `todo_app` here. This set-up should mean that all tests in the test directory are now discoverable, and can be run either from the Testing window, or from the test files directly. 

You can also run all tests by running `poetry run pytest` in a terminal whilst in the root repository.

## Provisioning VMs for application deployment using Ansible

You will be given details for a control node as well as several hosts. First, ensure that you can connect to the control node via SSH. Then, ensure that the files contained within this project's 'ansible' file are copied over to the control node's /home/ec2-user/ directory. Ensure that the inventory.ini file is updated with the IP addresses of all managed nodes. From here, run the following command:
```
ansible-playbook playbook.yaml -i inventory.ini
```
To check that all plays have been applied, you can then connect via SSH to each managed node (after first connecting to the control node) and explore the contents of directories there.

## Running the project with Docker

Build the Docker image by running the following command:
```bash
docker build --target development --tag todo-app:development .
```

To enable hot reloading, you should use the following command to run the Docker container using a bind mount:
```bash
$ docker run --env-file .env -p 8000:5000 --mount "type=bind,source=$(pwd)/todo_app,target=/app/todo_app" todo-app:development
```

To build and run the production container, you should replace all instances of 'development' with 'production' in both of the above commands.

