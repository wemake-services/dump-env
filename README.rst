A utility tool to create ``.env`` files
---------------------------------------

.. image:: https://travis-ci.org/sobolevn/dump-env.svg?branch=master
     :target: https://travis-ci.org/sobolevn/dump-env

.. image:: https://coveralls.io/repos/github/sobolevn/dump-env/badge.svg?branch=master
     :target: https://coveralls.io/github/sobolevn/dump-env?branch=master

.. image:: https://badge.fury.io/py/dump-env.svg
     :target: http://badge.fury.io/py/dump-env

.. image:: https://img.shields.io/pypi/pyversions/dump-env.svg
     :target: https://pypi.python.org/pypi/dump-env

.. image:: https://readthedocs.org/projects/dump-env/badge/?version=latest
      :target: http://dump-env.readthedocs.io/en/latest/?badge=latest

``dump-env`` takes an ``.env.template`` file and some optional environmental variables to create a new ``.env`` file from these two sources.

Quickstart
~~~~~~~~~~

This quick demo will demonstrate the main and the only purpose of ``dump-env``:

.. code:: bash

    $ dump-env --template=.env.template --prefix='SECRET_ENV_' > .env

This command will:

1. take ``.env.template``
2. parse its keys and values
3. read and all the variables from the environment starting with ``SECRET_ENV_``
4. remove this prefix
5. mix it all together, where environment variables could override ones with the same name from the template
6. sort keys in alphabetic order
7. dump all the keys and values into the ``.env`` file

Installation
~~~~~~~~~~~~

.. code:: bash

    $ pip install dump-env

Why?
~~~~

Why do we need such a tool? Well, this tool is very helpful when your CI is building ``docker`` (or other) images.
`Previously <https://github.com/wemake-services/wemake-django-template/blob/6a7ab060e8435fd855cd806706c5d1b5a9e76d12/%7B%7Bcookiecutter.project_name%7D%7D/.gitlab-ci.yml#L25>`_ we had some complex logic of encrypting and decrypting files, importing secret keys and so on.
Now we can just create secret variables for our CI, add some prefix to it, and use ``dump-env`` to make our life easier.

Creating secret variables in some CIs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``travis``: `docs <https://docs.travis-ci.com/user/environment-variables/#Defining-encrypted-variables-in-.travis.yml>`_
- ``gitlab-ci``: `docs <https://docs.gitlab.com/ce/ci/variables/README.html#secret-variables>`_
