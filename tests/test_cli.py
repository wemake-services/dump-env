# -*- coding: utf-8 -*-

import delegator


def test_simple_usage(monkeypatch):
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    result = delegator.run('dump-env -p SOM_TT_')
    assert result.out == 'VALUE=1\n'


def test_both_options(monkeypatch, env_file):
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    result = delegator.run('dump-env -p SOM_TT_ -t ' + env_file)
    assert result.out == 'NORMAL_KEY=SOMEVALUE\nVALUE=1\n'


def test_simple_usage_file_output(monkeypatch, tmpdir):
    monkeypatch.setenv('SOM_TT_VALUE', '1')

    file_ = tmpdir.mkdir('tests').join('.env')
    filename = file_.strpath

    delegator.run('dump-env -p SOM_TT_ > ' + filename)

    with open(filename) as f:
        assert f.read() == 'VALUE=1\n'
