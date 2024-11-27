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

## Setting up the MongoDB database

You will need to set up a MongoDB cluster, database and collection and populate the various .env files with suitable values for the connection string, database name and collection name. This can be done through the Azure portal. You should also ensure that these values are set as environment variables in your pipeline.

Azure Cosmos DB provides encryption at rest of data stored in various kinds of databases, including MongoDB, which is enabled by default in all regions. Data is periodically read from the secure storage within your account and backed up to the Azure Encrypted Blob Store. There is the option to add a second layer of encryption using customer-managed keys.

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

## Architecture Diagrams

Exported architecture diagrams for the project can be found in the diagrams subfolder. If this needs to be edited, the original diagram can be found at [this link](https://lucid.app/lucidspark/445cb0d7-f8b5-4aa5-aeae-f68559699c22/edit?invitationId=inv_7f4bbb0b-5cac-4876-aac0-1753fb1d2934&page=0_0#). Note that you need to request edit permissions.

## Running tests in Docker

Run tests in Docker using the following commands:
```bash
docker build --target test --tag todo-app:test .
docker run todo-app:test
```

## Deployment process

The Docker image will be automatically rebuilt and redeployed when changes are pushed to main. If the deployment process needs to be amended at any point, please make changes to the 'build' and 'deploy' jobs in ci-pipeline.yml.

# OAuth Authentication

We use Flask Login to authenticate users. Any new app routes will require user validation via the login_required flask login decorator. If you need to set up a new environment, you will also need to create a new OAuth app in GitLab with an appropriate callback URL, and add the client secret and client ID to the environment variables.
