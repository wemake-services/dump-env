# A utility tool to create ``.env`` files

[![Build Status](https://travis-ci.org/sobolevn/dump-env.svg?branch=master)](https://travis-ci.org/sobolevn/dump-env) [![Coverage](https://coveralls.io/repos/github/sobolevn/dump-env/badge.svg?branch=master)](https://coveralls.io/github/sobolevn/dump-env?branch=master) [![Python Version](https://img.shields.io/pypi/pyversions/dump-env.svg)](https://pypi.org/project/dump-env/) [![Docs](https://readthedocs.org/projects/dump-env/badge/?version=latest)](http://dump-env.readthedocs.io/en/latest/?badge=latest) [![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

`dump-env` takes an `.env.template` file and some optional environmental variables to create a new `.env` file from these two sources. No external dependencies are used.


## Why?

Why do we need such a tool? Well, this tool is very helpful when your CI is building `docker` (or other) images.
[Previously](https://github.com/wemake-services/wemake-django-template/blob/6a7ab060e8435fd855cd806706c5d1b5a9e76d12/%7B%7Bcookiecutter.project_name%7D%7D/.gitlab-ci.yml#L25) we had some complex logic of encrypting and decrypting files, importing secret keys and so on.
Now we can just create secret variables for our CI, add some prefix to it, and use `dump-env` to make our life easier.


## Requirements

* Python (3.6, 3.7)


## Quickstart

This quick demo will demonstrate the main and the only purpose of `dump-env`:

```bash
$ dump-env --template=.env.template --prefix='SECRET_ENV_' > .env
```

This command will:

1. take `.env.template`
2. parse its keys and values
3. read and all the variables from the environment starting with `SECRET_ENV_`
4. remove this prefix
5. mix it all together, where environment variables could override ones with the same name from the template
6. sort keys in alphabetic order
7. dump all the keys and values into the `.env` file


## Advanced Usage
```bash
$ dump-env -t .env.template -p 'SECRET_ENV_' -p 'ANOTHER_SECRET_ENV_' > .env
```

This command will do pretty much the same thing as with one prefix. But, it will replace multiple prefixes.
Further prefixes always replace previous ones if they are the same.
For example
```bash
$ export SECRET_TOKEN='very secret string'
$ export SECRET_ANSWER='13'
$ export ANOTHER_SECRET_ENV_ANSWER='42'
$ export ANOTHER_SECRET_ENV_VALUE='0'
$ dump-env -p SECRET_ -p ANOTHER_SECRET_ENV_
ANSWER=42
TOKEN=very secret string
VALUE=0
```


## Installation

```bash
$ pip install dump-env
```

## Creating secret variables in some CIs

- `travis`: [docs](https://docs.travis-ci.com/user/environment-variables/#Defining-encrypted-variables-in-.travis.yml)
- `gitlab-ci`: [docs](https://docs.gitlab.com/ce/ci/variables/README.html#secret-variables)
