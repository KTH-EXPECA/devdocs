# Editing documentation

## Overview

This website is built from Markdown-formatted text files using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), an extended version of the base [MkDocs](https://www.mkdocs.org/) framework. It is automatically built from the `master` branch of the source repository [KTH-EXPECA/devdocs](https://github.com/KTH-EXPECA/devdocs) using a GitHub Action whenever new commits are pushed.

## Editing pages

Each page in this website corresponds to a Markdown file under the `docs/` directory, or any of its subdirectories.
Simply edit or create files to modify the content of the documentation.

### Setting titles

By default, page titles in the navigation sections in the top bar and sidebar are set from the first top-level markdown heading of the file.
That is, a file beginning with 

``` markdown
# This is a top-level heading
```

will show up as `This is a top-level heading` in the navigation sections.

This behavior can be overridden in multiple ways:

- By setting a different title inside a YAML header at the top of the file.
    For instance:

    ``` markdown
    ---
    title: Different title
    ...

    # This is a top-level heading
    ```

    Makes the file show up as `Different title`, instead of `This is a top-level heading`.

- By not including a top-level heading in the file.
    This will cause the MkDocs to create a name from its filename.
    For instance, a file called `different_title.md` without a top-level heading will show up as `Different title` in the navigation.

- Using the `awesome-pages` plugin; see the [section below](#setting-section-titles) for details.

## Editing sections

Sections in MkDocs simply correspond to subdirectories inside the `docs/` directory.
Simply create directories and modify their content to create and re-organize sections.

### Setting the order of pages inside a section

By default, MkDocs orders pages alphabetically inside sections.
Since this is usually not what we want, we use the `awesome-pages` plugin to specify custom orderings.
Configuring the order of subpages and subsections inside a secion is done then by creating special `.page` in the corresponding directory; this file is actually a YAML file which should have the following structure:

``` yaml
---
nav:
  - first_page.md
  - second_page.md
  - section
...
```

Pages and sections will then appear in the navigation in the order specified in the corresponding `.page` file for their parent section.
*Hint:* The wildcard `...` can be used as a catch-all to allow MkDocs to automatically order any pages and sections that are not explicitly declared in the `.pages` file.

### Setting section titles

Sections titles can be set in two ways:

- By default, MkDocs creates names from the directory name.
    A directory called `a_section` thus creates a section called `A section`.

- Using the `awesome-pages` plugin, section (and page) names can be customized by prepending the desired name in the corresponding `.pages` file like so:

    ``` yaml
    ---
    nav:
      - First page: first_page_with_a_weird_filename.md
      - First section: section_number1
    ...
    ```

## Previewing the website

You can use Docker to run a local copy of the documentation website to preview your changes while editing.
Included in the documentation repository is a `./docker` directory containing a `docker-compose.yml` file which builds and deploys a containerized instance of the website listening on [localhost:8000](http://localhost:8000).

To run this container, you will first need to install [Docker](https://docs.docker.com/engine/install) and [docker-compose](https://docs.docker.com/compose/install/).
Next, run `docker-compose` from the root of the repository:

``` console
$ docker-compose -f docker/docker-compose.yml up --build --remove-orphans
Building mkdocs
Sending build context to Docker daemon  3.072kB
Step 1/2 : FROM squidfunk/mkdocs-material
 ---> 4b50acece4f3
Step 2/2 : RUN pip install mkdocs-awesome-pages-plugin
 ---> Using cache
 ---> 2a3f1835ca41
Successfully built 2a3f1835ca41
Successfully tagged docker_mkdocs:latest
Starting docker_mkdocs_1 ... done
Attaching to docker_mkdocs_1
mkdocs_1  | INFO    -  Building documentation... 
mkdocs_1  | WARNING -  Config value: 'dev_addr'. Warning: The use of the IP address '0.0.0.0' suggests a production environment or the use of a proxy to connect to the MkDocs server. However, the MkDocs' server is intended for local development purposes only. Please use a third party production-ready server instead. 
mkdocs_1  | INFO    -  Cleaning site directory 
mkdocs_1  | INFO    -  Documentation built in 0.32 seconds 
mkdocs_1  | [I 210727 08:29:39 server:335] Serving on http://0.0.0.0:8000
mkdocs_1  | [I 210727 08:29:39 handlers:62] Start watching changes
mkdocs_1  | [I 210727 08:29:39 handlers:64] Start detecting changes
```

To shut down the container, simply press `Ctrl+C` on the same terminal; alternatively, from another terminal at the root of the repository, you can run:

``` console
$ docker-compose -f docker/docker-compose.yml down
Stopping docker_mkdocs_1 ... done
Removing docker_mkdocs_1 ... done
Removing network docker_default
```

## Adding plugins

There exist a multitude of plugins for MkDocs available online; many of which are potentially useful for this documentation.
[See here](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins) for a list of available plugins.

To use plugins with the website, a couple of steps need to be followed:

1. Add the plugins to the preview Docker container image.
: Edit the `docker/Dockerfile` file, and add the desired plugins to the line starting with `RUN pip install ...`.
    You will need to shutdown and re-build the Docker container image if it was already running.

    ``` Dockerfile
    FROM squidfunk/mkdocs-material
    RUN pip install <plugin1> <plugin2> ... <pluginN>
    ```

    

2. Add the plugins to the automated CI build configuration.
: This needs to be done so that the plugins are included when the website is automatically built by the GitHub Action.
    Edit the `.github/workflows/ci.yml` file and add the desired plugins to the line starting with `- run: pip install ...`, e.g.:

    ``` yaml
    - run: pip install <plugin1> <plugin2> ... <pluginN>
    ```

3. Make sure the plugin is enabled.
: Edit the `mkdocs.yml` file, adding the corresponding entries to the `plugins` list entry (if no `plugins` entry exist, you need to create it).
    For example:

    ``` yaml
    plugins:
      - <plugin1>
      - <plugin2>
      - ...
      - <pluginN>
    ```

4. Finally, configure the plugin; follow the specific instructions for each plugin to configure it.
