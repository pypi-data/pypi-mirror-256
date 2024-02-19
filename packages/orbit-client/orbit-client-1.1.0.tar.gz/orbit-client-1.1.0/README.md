<h1 align="center">
    <img alt="orbit Logo" width="200px" src="https://raw.githubusercontent.com/orbit/orbit/3ac078356adf5a1a72042dfe72ebfa4a9cd5ef38/logo/orbit_medium.png">
</h1>

# Orbit

A command-line utility that creates projects from **orbits** (project templates), e.g. creating a Python package project
from a Python package project template.

## Table Of Contents

- [What is Orbit](#what-is-orbit)
- [Installation](#installation)
    - [Installing via pip](#with-pip)
    - [Installing from source](#from-source)
- [Usage](#usage)
- [Contributions](#contributing)

## What is Orbit

A command-line utility that creates projects from orbit (project templates), e.g. creating a Python package project from
a Python package project template.

## Installation

### Installing via pip

```bash
$ pip install orbit-client
```

## Usage

- Cross-platform: Windows, Mac, and Linux are officially supported.
- You don't have to know/write Python code to use Cookiecutter.
- Works with Python 3.7, 3.8, 3.9, 3.10, 3.11
- Project templates can be in any programming language or markup format:
  Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, you name it.
  You can use multiple languages in the same project template.

### For users of existing templates

- Simple command line usage:

  ```bash
  # Create project from the orbit-pypackage.git repo template
  # You'll be prompted to enter values.
  # Then it'll create your Python package in the current working directory,
  # based on those values.
  $ orbit <repo url>
  # For the sake of brevity, repos on GitHub can just use the 'gh' prefix
  $ orbit gh:audreyfeldroy/orbit-pypackage
  ```

- Use it at the command line with a local template:

  ```bash
  # Create project in the current working directory, from the local
  # orbit-pypackage/ template
  $ orbit orbit-pypackage/
  ```

- Or use it from Python:

  ```python
  from orbit.main import orbit

  # Create project from the orbit-pypackage/ template
  orbit('orbit-pypackage/')

  # Create project from the orbit-pypackage.git repo template
  orbit('<repo url>')
  ```

- Unless you suppress it with `--no-input`, you are prompted for input:
    - Prompts are the keys in `orbit.json`.
    - Default responses are the values in `orbit.json`.
    - Prompts are shown in order.
- Cross-platform support for `~/.orbitrc` files:

  ```yaml
  default_context:
    full_name: "haonv"
    email: "haonv@ftech.ai.com"
    github_username: "haonv"
  orbits_dir: "~/.orbits/"
  ```


- You can use local orbits, or remote orbits directly from Git repos or Mercurial repos on Bitbucket.
- Default context: specify key/value pairs that you want to be used as defaults whenever you generate a project.
- Inject extra context with command-line arguments:

### For template creators

- Supports unlimited levels of directory nesting.
- 100% of templating is done with Jinja2.
- Both, directory names and filenames can be templated.
  For example:

  ```py
  {{orbit.repo_name}}/{{orbit.repo_name}}/{{orbit.repo_name}}.py
  ```
- Simply define your template variables in a `orbit.json` file. You can also add human-readable questions and choices
  that will be prompted to the user for each variable using the `__prompts__` key. Those human-readable questions
  supports [`rich` markup](https://rich.readthedocs.io/en/stable/markup.html) such
  as `[bold yellow]this is bold and yellow[/]`
  For example:

  ```json
  {
    "full_name": "Audrey Roy Greenfeld",
    "email": "audreyr@gmail.com",
    "project_name": "Complexity",
    "repo_name": "complexity",
    "project_short_description": "Refreshingly simple static site generator.",
    "release_date": "2013-07-10",
    "year": "2013",
    "version": "0.1.1",
    "linting": ["ruff", "flake8", "none"],
    "__prompts__": {
      "full_name": "Provide your [bold yellow]full name[/]",
      "email": "Provide your [bold yellow]email[/]",
      "linting": {
        "__prompt__": "Which [bold yellow]linting tool[/] do you want to use?",
        "ruff": "Ruff",
        "flake8": "Flake8",
        "none": "No linting tool"
      }
    }
  }
  ```
- Pre- and post-generate hooks: Python or shell scripts to run before or after generating a project.

## Author