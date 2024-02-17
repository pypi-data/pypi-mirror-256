import click
import sys
from json import loads, dumps
from llm.cli import get_embedding_models_with_aliases
from llm import get_embedding_model

AVAILABLE_EMBEDDING_MODELS = [
    str(model_with_aliases.model.model_id)
    for model_with_aliases in get_embedding_models_with_aliases()
]


def _embed(content, model):
    if isinstance(content, str):
        if model == "echo":
            return content
        elif model == "reverse":
            return content[::-1]
        else:
            return get_embedding_model(model).embed(content)

    elif isinstance(content, dict):
        return {k: _embed(v, model) for k, v in content.items()}
    elif isinstance(content, list):
        return [_embed(item, model) for item in content]
    else:
        return content  # Return the object as-is if it's not a string, dict, or list


@click.group()
@click.version_option()
def cli():
    """Tools for working with LLMs on JSON data"""
    pass


@cli.command()
@click.option(
    "-i",
    "--input",
    type=click.Path(exists=True, readable=True, allow_dash=True),
    help="File to embed",
)
@click.option(
    "-m",
    "--model",
    help=f"Embedding model(s) to use\n\nIssue `llm embed-models list` to list available models."
    f"\n\nCurrently installed are: {list(sorted(AVAILABLE_EMBEDDING_MODELS))}"
    f"\n\nYou can install more via `llm install ...` "
    f"\n\nYou can find available models here: "
    f"https://llm.datasette.io/en/stable/plugins/directory.html#embedding-models",
)
@click.option(
    "-j",
    "--jq",
    help=f"Embed only the keys that satisfy the given jq filter expression",
)
@click.option(
    "--in-arrays",
    is_flag=True,
    help=f"Embed text appearing in arrays too",
)
def embed(input, model, jq, in_arrays):
    """Turn a JSON of content into a JSON of embeddings."""

    if not input or input == "-":
        # Read from stdin
        for line in sys.stdin:
            content = loads(line)
            result = _embed(content, model)
            click.echo(dumps(result))
    else:
        with open(input, "r") as f:
            for line in f:
                content = loads(line)
                result = _embed(content, model)
                click.echo(dumps(result))
