"""All exceptions used in the orbit code base are defined here."""


class OrbitException(Exception):
    """
    Base exception class.

    All Orbit-specific exceptions should subclass this class.
    """


class NonTemplatedInputDirException(OrbitException):
    """
    Exception for when a project's input dir is not templated.

    The name of the input directory should always contain a string that is
    rendered to something else, so that input_dir != output_dir.
    """


class UnknownTemplateDirException(OrbitException):
    """
    Exception for ambiguous project template directory.

    Raised when Orbit cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """

    # unused locally


class MissingProjectDir(OrbitException):
    """
    Exception for missing generated project directory.

    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """

    # unused locally


class ConfigDoesNotExistException(OrbitException):
    """
    Exception for missing config file.

    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """


class InvalidConfiguration(OrbitException):
    """
    Exception for invalid configuration file.

    Raised if the global configuration file is not valid YAML or is
    badly constructed.
    """


class UnknownRepoType(OrbitException):
    """
    Exception for unknown repo types.

    Raised if a repo's type cannot be determined.
    """


class VCSNotInstalled(OrbitException):
    """
    Exception when version control is unavailable.

    Raised if the version control system (git or hg) is not installed.
    """


class ContextDecodingException(OrbitException):
    """
    Exception for failed JSON decoding.

    Raised when a project's JSON context file can not be decoded.
    """


class OutputDirExistsException(OrbitException):
    """
    Exception for existing output directory.

    Raised when the output directory of the project exists already.
    """


class InvalidModeException(OrbitException):
    """
    Exception for incompatible modes.

    Raised when orbit is called with both `no_input==True` and
    `replay==True` at the same time.
    """


class UndefinedVariableInTemplate(OrbitException):
    """
    Exception for out-of-scope variables.

    Raised when a template uses a variable which is not defined in the
    context.
    """

    def __init__(self, message, error, context):
        """Exception for out-of-scope variables."""
        self.message = message
        self.error = error
        self.context = context

    def __str__(self):
        """Text representation of UndefinedVariableInTemplate."""
        return (
            f"{self.message}. " f"Error message: {self.error.message}. " f"Context: {self.context}"
        )


class UnknownExtension(OrbitException):
    """
    Exception for un-importable extension.

    Raised when an environment is unable to import a required extension.
    """


class RepositoryNotFound(OrbitException):
    """
    Exception for missing repo.

    Raised when the specified orbit repository doesn't exist.
    """


class RepositoryCloneFailed(OrbitException):
    """
    Exception for un-cloneable repo.

    Raised when a orbit template can't be cloned.
    """


class InvalidZipRepository(OrbitException):
    """
    Exception for bad zip repo.

    Raised when the specified orbit repository isn't a valid
    Zip archive.
    """
