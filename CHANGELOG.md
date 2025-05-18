# dump-env changelog

We follow semantic versioning.


## Version 1.6.0

### Features

- Drops `python3.9` support
- Adds `python3.13` support
- Adds support for multiline values


## Version 1.5.0

### Features

- Drops `python3.7` and `python3.8` support
- Adds `python3.11` and `python3.12` official support

### Misc

- Updates multiple dev dependencies


## Version 1.4.0

### Features

- Drops `python3.6` support

### Misc

- Updates `poetry` to `>=1.2`


## Version 1.3.0

### Features

- Adds `python3.9` support
- Adds `--source` flag

### Misc

- Moves to Github Actions
- Bumps a lot of dev dependencies


## Version 1.2.0

### Features

- Adds `python3.8` support


## Version 1.1.1

### Bugfixes

- Outputs errors to `stderr` instead of `stdout`


## Version 1.1.0

### Features

- Adds `--strict` option to fail the command if some keys are not present

### Misc

- Updates `wemake-python-styleguide` to the latest version


## Version 1.0.0

### Breaking changes

- Dropped `python2` support

### Features

- Adds multiple `-p` flags

### Misc

- Updates dependencies
- Enables dependabot
- Improves testing and type checking
- Improves docs
- Adds `CONTRIBUTING.md`
- Fixes `sphinx` and `readthedocs` builds


## Version 0.2.1

### Features

- Adds `pyroma` to check package metadata

### Bugfixes

- Fixes `pypi` readme rendering by providing `pypandoc`
- Changes how version are deployed from `travis`
- `wheel` is now universal


## Version 0.2.0

### Features

- Refactors `Env` class to be a function
- We are now using `python3.5` for tests
- We are now using `md` version of `README` file. New PyPI allows that!
- Updates how linting works


## Version 0.1.1

### Bugfixes

- Fixes [#1](https://github.com/sobolevn/dump-env/issues/1) when prefix was replaced multiple times in a string


## Version 0.1.0

- Initial release
