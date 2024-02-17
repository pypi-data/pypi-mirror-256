<p align="center">

[//]: # (<p align="center">)

[//]: # (   <img width="50%" height="40%" src="https://th.bing.com/th/id/OIP.Er8SBUDGYYFbqBisj0qifwHaE8?rs=1&pid=ImgDetMain" alt="Logo">)

[//]: # (  </p>)

  <h1 align="center">jsonllm</h1>
  <p align="center">
  <strong>Tools for working with LLMs on JSON data</strong>
    <br> <br />
    <a href="#usage"><strong> Usage </strong></a> |
    <a href="#installation"><strong> Installation </strong></a> |
    <a href="#why"><strong> Why</strong></a> |
    <a href="#how"><strong> How </strong></a>
   </p>
<p align="center">

<p align="center">
<a href="https://pypi.org/project/jsonllm/"><img src="https://img.shields.io/pypi/v/jsonllm?label=PyPI"></a>
<a href="https://github.com/Florents-Tselai/jsonllm/actions/workflows/test.yml?branch=mainline"><img src="https://github.com/Florents-Tselai/jsonllm/actions/workflows/test.yml/badge.svg"></a>
<a href="https://codecov.io/gh/Florents-Tselai/jsonllm"><img src="https://codecov.io/gh/Florents-Tselai/jsonllm/branch/main/graph/badge.svg"></a>  
<a href="https://opensource.org/licenses/MIT license"><img src="https://img.shields.io/badge/MIT license.0-blue.svg"></a>
<a href="https://github.com/Florents-Tselai/jsonllm/releases"><img src="https://img.shields.io/github/v/release/Florents-Tselai/jsonllm?include_prereleases&label=changelog"></a>

## Usage

```bash
Usage: jsonllm [OPTIONS] COMMAND [ARGS]...

  Tools for working with LLMs on JSON data

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  embed  Turn a JSON of content into a JSON of embeddings.

```

```bash
Usage: jsonllm embed [OPTIONS]

  Turn a JSON of content into a JSON of embeddings.

Options:
  -i, --input PATH  File to embed
  -m, --model TEXT  Embedding model(s) to use
                    
                    Issue `llm embed-models list` to list available models.
                    
                    Currently installed are: ['3-large', '3-large-1024',
                    '3-large-256', '3-small', '3-small-512', 'ada-002',
                    'clip', 'jina-embeddings-v2-base-en', 'jina-
                    embeddings-v2-large-en', 'jina-embeddings-v2-small-en',
                    'onnx-bge-base', 'onnx-bge-large', 'onnx-bge-micro',
                    'onnx-bge-small', 'onnx-gte-tiny', 'onnx-minilm-l12',
                    'onnx-minilm-l6', 'sentence-transformers/all-MiniLM-L6-v2']
                    
                    You can install more via `llm install ...`
                    
                    You can find available models here: https://llm.datasette.io/en/stable/plugins/directory.html#embedding-models
  -j, --jq TEXT     Embed only the keys that satisfy the given jq filter
                    expression
  --in-arrays       Embed text appearing in arrays too
  --help            Show this message and exit.

```

```sql
CREATE TABLE people (data JSONB);
```

```bash
python tests/gen_people.py 100 |\
jsonllm embed -m clip -j '.name'
psql -c "\COPY people(data) FROM stdin"
```

```bash
echo '{"hello": "world"}' | jsonllm embed -m clip
```

## Installation

```bash
pip install jsonllm
```

### Available Models

Available embedding models
are those provided and installed via the `llm` package.

- **[llm-sentence-transformers](https://github.com/simonw/llm-sentence-transformers)** adds support for embeddings using
  the [sentence-transformers](https://www.sbert.net/) library, which provides
  access to [a wide range](https://www.sbert.net/docs/pretrained_models.html) of
  embedding models.
- **[llm-clip](https://github.com/simonw/llm-clip)** provides
  the [CLIP](https://openai.com/research/clip) model, which can be used to embed
  images and text in the same vector space, enabling text search against images.
  See [Build an image search engine with llm-clip](https://simonwillison.net/2023/Sep/12/llm-clip-and-chat/)
  for more on this plugin.
- **[llm-embed-jina](https://github.com/simonw/llm-embed-jina)** provides Jina
  AI's [8K text embedding models](https://jina.ai/news/jina-ai-launches-worlds-first-open-source-8k-text-embedding-rivaling-openai/).
- **[llm-embed-onnx](https://github.com/simonw/llm-embed-onnx)** provides seven
  embedding models that can be executed using the ONNX model framework.

```bash
llm install llm-sentence-transformers
llm install llm-clip
llm install llm-embed-jina
llm install llm-embed-onnx
```

For an up-to-date list
check [here](https://llm.datasette.io/en/stable/plugins/directory.html#embedding-models)

## Why

There are now plenty of tools providing ways of getting embeddings out of a
corpus of text.
Some even can generate embeddings from JSON documents,
but they treat JSON as simple text too.

That is rarely the case though; JSON documents have structure and semantics
depending on their application in context.
Most importantly though it's data exchange format and a data aggregation tool.
Aggregation in the sense of getting data from A to B.

In my case point A was a JSON object created by an SQL query from a Postgres
database, piped through `jsonllm` and pushed into another Postgres instance
specifically designed for AI-related experiments.

## How

`jsonllm` traverses a JSON object recursively,
and replaces text values with their embeddings array.

Other data types are not modified at all and the overall
object structure is not changed.

## Development

```bash
pip install -e '.[test]'
pytest
```
