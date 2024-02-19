"""Main `orbit` CLI."""
import collections
import json
import os
import sys

import click
from orbit import __version__
from orbit.config import get_user_config
from orbit.exceptions import (
    ContextDecodingException,
    InvalidModeException,
    InvalidZipRepository,
    OutputDirExistsException,
    RepositoryCloneFailed,
    RepositoryNotFound,
    UndefinedVariableInTemplate,
    UnknownExtension,
)
from orbit.log import configure_logger
from orbit.main import orbit


def version_msg():
    """Return the orbit version, location and Python powering it."""
    python_version = sys.version
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return f"Orbit {__version__} from {location} (Python {python_version})"


def validate_extra_context(ctx, param, value):
    """Validate extra context."""
    for string in value:
        if "=" not in string:
            raise click.BadParameter(
                f"EXTRA_CONTEXT should contain items of the form key=value; "
                f"'{string}' doesn't match that form"
            )

    # Convert tuple -- e.g.: ('program_name=foobar', 'startsecs=66')
    # to dict -- e.g.: {'program_name': 'foobar', 'startsecs': '66'}
    return collections.OrderedDict(s.split("=", 1) for s in value) or None


def list_installed_templates(default_config, passed_config_file):
    """List installed (locally cloned) templates. Use orbit --list-installed."""
    config = get_user_config(passed_config_file, default_config)
    orbit_folder = config.get("orbits_dir")
    if not os.path.exists(orbit_folder):
        click.echo(
            f"Error: Cannot list installed templates. " f"Folder does not exist: {orbit_folder}"
        )
        sys.exit(-1)

    template_names = [
        folder
        for folder in os.listdir(orbit_folder)
        if os.path.exists(os.path.join(orbit_folder, folder, "orbit.json"))
    ]
    click.echo(f"{len(template_names)} installed templates: ")
    for name in template_names:
        click.echo(f" * {name}")


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, "-V", "--version", message=version_msg())
@click.argument("template", required=False)
@click.argument("extra_context", nargs=-1, callback=validate_extra_context)
@click.option(
    "--no-input",
    is_flag=True,
    help="Do not prompt for parameters and only use orbit.json file content. "
    "Defaults to deleting any cached resources and re-downloading them. "
    "Cannot be combined with the --replay flag.",
)
@click.option(
    "-c",
    "--checkout",
    help="branch, tag or commit to checkout after git clone",
)
@click.option(
    "--directory",
    help="Directory within repo that holds orbit.json file "
    "for advanced repositories with multi templates in it",
)
@click.option("-v", "--verbose", is_flag=True, help="Print debug information", default=False)
@click.option(
    "--replay",
    is_flag=True,
    help="Do not prompt for parameters and only use information entered previously. "
    "Cannot be combined with the --no-input flag or with extra configuration passed.",
)
@click.option(
    "--replay-file",
    type=click.Path(),
    default=None,
    help="Use this file for replay instead of the default.",
)
@click.option(
    "-f",
    "--overwrite-if-exists",
    is_flag=True,
    help="Overwrite the contents of the output directory if it already exists",
)
@click.option(
    "-s",
    "--skip-if-file-exists",
    is_flag=True,
    help="Skip the files in the corresponding directories if they already exist",
    default=False,
)
@click.option(
    "-o",
    "--output-dir",
    default=".",
    type=click.Path(),
    help="Where to output the generated project dir into",
)
@click.option("--config-file", type=click.Path(), default=None, help="User configuration file")
@click.option(
    "--default-config",
    is_flag=True,
    help="Do not load a config file. Use the defaults instead",
)
@click.option(
    "--debug-file",
    type=click.Path(),
    default=None,
    help="File to be used as a stream for DEBUG logging",
)
@click.option("-l", "--list-installed", is_flag=True, help="List currently installed templates.")
@click.option(
    "--keep-project-on-failure",
    is_flag=True,
    help="Do not delete project folder on failure",
)
def main(
    template,
    extra_context,
    no_input,
    checkout,
    verbose,
    replay,
    overwrite_if_exists,
    output_dir,
    config_file,
    default_config,
    debug_file,
    directory,
    skip_if_file_exists,
    replay_file,
    list_installed,
    keep_project_on_failure,
):
    """Create a project from a orbit project template (TEMPLATE)."""
    # Commands that should work without arguments
    if list_installed:
        list_installed_templates(default_config, config_file)
        sys.exit(0)

    # Raising usage, after all commands that should work without args.
    if not template or template.lower() == "help":
        click.echo(click.get_current_context().get_help())
        sys.exit(0)

    configure_logger(stream_level="DEBUG" if verbose else "INFO", debug_file=debug_file)

    if replay_file:
        replay = replay_file

    try:
        orbit(
            template,
            checkout,
            no_input,
            extra_context=extra_context,
            replay=replay,
            overwrite_if_exists=overwrite_if_exists,
            output_dir=output_dir,
            config_file=config_file,
            default_config=default_config,
            password=os.environ.get("ORBIT_REPO_PASSWORD"),
            directory=directory,
            skip_if_file_exists=skip_if_file_exists,
            keep_project_on_failure=keep_project_on_failure,
        )
    except (
        ContextDecodingException,
        OutputDirExistsException,
        InvalidModeException,
        UnknownExtension,
        InvalidZipRepository,
        RepositoryNotFound,
        RepositoryCloneFailed,
    ) as e:
        click.echo(e)
        sys.exit(1)
    except UndefinedVariableInTemplate as undefined_err:
        click.echo(f"{undefined_err.message}")
        click.echo(f"Error message: {undefined_err.error.message}")

        context_str = json.dumps(undefined_err.context, indent=4, sort_keys=True)
        click.echo(f"Context: {context_str}")
        sys.exit(1)


if __name__ == "__main__":
    main()
