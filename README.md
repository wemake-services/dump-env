# A utility tool to create ``.env`` files

[![Build Status](https://travis-ci.org/sobolevn/dump-env.svg?branch=master)](https://travis-ci.org/sobolevn/dump-env) [![Coverage](https://coveralls.io/repos/github/sobolevn/dump-env/badge.svg?branch=master)](https://coveralls.io/github/sobolevn/dump-env?branch=master) [![Python Version](https://img.shields.io/pypi/pyversions/dump-env.svg)](https://https://pypi.org/project/dump-env/) [![Docs](https://readthedocs.org/projects/dump-env/badge/?version=latest)](http://dump-env.readthedocs.io/en/latest/?badge=latest)

`dump-env` takes an `.env.template` file and some optional environmental variables to create a new `.env` file from these two sources. No external dependencies are used.


## Why?

Why do we need such a tool? Well, this tool is very helpful when your CI is building `docker` (or other) images.
[Previously](https://github.com/wemake-services/wemake-django-template/blob/6a7ab060e8435fd855cd806706c5d1b5a9e76d12/%7B%7Bcookiecutter.project_name%7D%7D/.gitlab-ci.yml#L25) we had some complex logic of encrypting and decrypting files, importing secret keys and so on.
Now we can just create secret variables for our CI, add some prefix to it, and use `dump-env` to make our life easier.


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


## Installation

```bash
$ pip install dump-env
```

## Creating secret variables in some CIs

- `travis`: [docs](https://docs.travis-ci.com/user/environment-variables/#Defining-encrypted-variables-in-.travis.yml)
- `gitlab-ci`: [docs](https://docs.gitlab.com/ce/ci/variables/README.html#secret-variables)
