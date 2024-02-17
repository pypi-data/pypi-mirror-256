import pytest
from json import dumps, loads, load
from click.testing import CliRunner
from jsonllm.cli import cli


def test_cli_embed_echo(simplejson):
    injsonstr = dumps(simplejson)
    runner = CliRunner()
    result = runner.invoke(cli, ["embed", "-m", "echo"], input=injsonstr)
    assert result.exit_code == 0

    resjson = loads(result.output)
    assert resjson == simplejson


def test_cli_embed_reverse():
    injsonstr = dumps({"key": "value", "list": ["example", "test"]})
    runner = CliRunner()
    result = runner.invoke(cli, ["embed", "-m", "reverse"], input=injsonstr)
    assert result.exit_code == 0

    resjson = loads(result.output)
    assert resjson == {"key": "eulav", "list": ["elpmaxe", "tset"]}
