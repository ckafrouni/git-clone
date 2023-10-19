# GIT CLONE: g

## Description
This project is an attempt at cloning the git command line tool in Python.

The CLI is built using the [Click](https://click.palletsprojects.com/en/8.1.x/) library.
I haven't setup the project as a package yet, so the CLI can be run using the following command:

```bash
python -m cli.main <command> <options> <args>
```

## Usage
As this is a work in progress, the usage is limited. So far, the following commands are supported:

```bash
g init

g add <file>
g add <directory>
```

