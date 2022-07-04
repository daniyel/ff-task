# Peter Park Task

## Setup development environment

### Requirements

- Install [pipenv](https://pipenv.pypa.io/en/latest/)

## Installing dependencies

To install dependencies run:

```sh
shell> pipenv install <package>
```

and for development dependencies:

```sh
shell> pipenv install <package> --dev
```

## Run project

```sh
shell> set FLASK_APP=app/app.py python3 -m flask run
```

## Testing

### Running tests

Install nose2 first as `pip install nose2` and run `nose2` from root folder.

### Running coverage

To run the coverage execute: `coverage run <test_file_name>` and to generate report run `coverage report app/**/*.py`.

## Linting

Fix pylint issues with:

```sh
> autopep8 --in-place --aggressive --recursive .
```
