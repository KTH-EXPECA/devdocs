# Documentation for the Testbed

## Getting started

Documentation is built using [mkdocs-material](https://squidfunk.github.io/mkdocs-material/).
Each Markdown file in `./docs` corresponds to a page.

Easiest way to write and preview is by running the official Docker container:

```bash
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

The live preview will then be served at [localhost:8000](https://localhost:8000).

## Deploying

To deploy the documentation site, first build a static version of the documentation:

```bash
docker run --rm -it -v ${PWD}:/docs squidfunk/mkdocs-material build .
```

The output of this command can then be served using an HTTP server such as NGINX.