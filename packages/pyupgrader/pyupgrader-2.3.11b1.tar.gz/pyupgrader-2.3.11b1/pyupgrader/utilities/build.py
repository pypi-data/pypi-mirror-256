"""
This module provides the functionality to build a project into a pyupgrader project.
It is intended to be used by the command line tool.

Classes:
- Builder: Builds a project into a pyupgrader project

Exceptions:
- FolderCreationError: Raised when there is an error creating a folder
- ConfigError: Raised when there is an error with the config file
- HashDBError: Raised when there is an error with the hash database
- PathError: Raised when there is an error with a path
"""

import os
import shutil
import logging
from pyupgrader.utilities import helper, hashing

LOGGER = logging.getLogger(__name__)


class FolderCreationError(Exception):
    """Raised when there is an error creating a folder"""


class ConfigError(Exception):
    """Raised when there is an error with the config file"""


class HashDBError(Exception):
    """Raised when there is an error with the hash database"""


class PathError(Exception):
    """Raised when there is an error with a path"""


class Builder:
    """
    Builds a project into a pyupgrader project

    Attributes:
    - project_path: str
        Path to the project folder.
    - exclude_envs: bool
        Whether to exclude common virtual environment folders.
    - exclude_hidden: bool
        Whether to exclude hidden files and folders.
    - exclude_patterns: list
        List of patterns to exclude from the hash database.
    - exclude_paths: list
        List of absolute paths to exclude from the hash database.

    Methods:
    - build(): Builds the project into a pyupgrader project.
    """

    def __init__(
        self,
        project_path: str,
        exclude_envs: bool = False,
        exclude_hidden: bool = False,
        exclude_patterns: list = None,
        exclude_paths: list = None,
    ):

        self.project_path = project_path
        self.exclude_envs = exclude_envs
        self.exclude_hidden = exclude_hidden
        self.exclude_patterns = [] if exclude_patterns is None else exclude_patterns
        self.exclude_paths = [] if exclude_paths is None else exclude_paths

        self.env_names = [
            ".venv",
            "venv",
            "env",
            ".env",
            ".virtualenv",
            "virtualenv",
            "conda",
            ".conda",
            "condaenv",
            ".condaenv",
            "pipenv",
            ".pipenv",
            "poetry",
            ".poetry",
            "pyenv",
            ".pyenv",
        ]

        self._pyudpdate_folder = None
        self._config_path = None
        self._hash_db_path = None

    def build(self):
        """Builds a project into a pyupgrader project"""
        self._validate_paths()

        LOGGER.info("Building Project...")

        try:
            self._create_pyupgrader_folder()
        except Exception as error:
            raise FolderCreationError("Failed to create .pyupgrader folde") from error

        try:
            self._create_config_file()
        except Exception as error:
            raise ConfigError("Failed to create config file") from error

        try:
            self._create_hash_db()
        except Exception as error:
            raise HashDBError("Failed to create hash database") from error

        LOGGER.info("Project built at '%s'", self._pyudpdate_folder)
        LOGGER.info("Don't forget to configure the config file in the .pyupgrader folder.")

    def _validate_paths(self):
        """Validates and set paths"""
        if self.project_path is None:
            raise PathError("Folder path not set")
        if self.exclude_paths is None:
            raise PathError("Exclude paths not set")

        if not os.path.exists(self.project_path):
            raise PathError(f'Folder "{self.project_path}" does not exist')
        if self.project_path in self.exclude_paths:
            raise PathError("Folder path cannot be excluded")

        self.project_path = helper.normalize_paths(self.project_path)
        self.exclude_paths = helper.normalize_paths(self.exclude_paths)

        self._pyudpdate_folder = os.path.join(self.project_path, ".pyupgrader")
        self._config_path = os.path.join(self._pyudpdate_folder, "config.yaml")
        self._hash_db_path = os.path.join(self._pyudpdate_folder, "hashes.db")

    def _create_pyupgrader_folder(self):
        """Creates the .pyupgrader folder"""
        if os.path.exists(self._pyudpdate_folder):
            LOGGER.warning("Folder '%s' already exists! Deleting it...", self._pyudpdate_folder)
            shutil.rmtree(self._pyudpdate_folder)

        LOGGER.info("Creating folder at '%s'", self._pyudpdate_folder)
        os.mkdir(self._pyudpdate_folder)

    def _create_config_file(self):
        """Creates the config file"""
        LOGGER.info("Creating config file at '%s'", self._config_path)
        config = helper.Config()

        default_data = config.default_config_data
        default_data["hash_db"] = os.path.basename(self._hash_db_path)
        config.write_yaml(self._config_path, default_data)
        try:
            config.load_yaml(self._config_path)
        except ValueError as error:
            raise ConfigError("Failed to validate config file") from error

    def _create_hash_db(self):
        """Creates the hash database"""
        LOGGER.info("Creating hash database at '%s'", self._hash_db_path)
        hasher = hashing.Hasher(project_name=os.path.basename(self.project_path))

        self.exclude_paths.append(self._pyudpdate_folder)
        self.exclude_patterns.append(r".*/__pycache__/.*")

        if self.exclude_hidden:
            self.exclude_patterns.append(r".*/\..*")
        if self.exclude_envs:
            self.exclude_paths += [os.path.join(self.project_path, path) for path in self.env_names]

        hasher.create_hash_db(
            self.project_path, self._hash_db_path, self.exclude_paths, self.exclude_patterns
        )
