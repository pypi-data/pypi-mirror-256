#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import time
import shutil
import fnmatch
import logging
import subprocess
from pathlib import Path
from typing import Generator

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.views.version import Version
from slpkg.error_messages import Errors
from slpkg.repositories import Repositories
from slpkg.logging_config import LoggingConfig


class Utilities(Configs):

    def __init__(self):
        super(Configs, self).__init__()

        self.black = Blacklist()
        self.errors = Errors()
        self.repos = Repositories()
        self.stderr = None
        self.stdout = None
        self.prog_version = Version()

        self.installed_packages: dict = dict(self.all_installed())
        self.process_log_date = LoggingConfig.date.replace('/', '_')
        self.process_log_time = LoggingConfig.time.replace(':', '_')

        logging.basicConfig(filename=LoggingConfig.log_file,
                            filemode=LoggingConfig.filemode,
                            encoding=LoggingConfig.encoding,
                            level=LoggingConfig.level)

    def is_package_installed(self, name: str) -> str:
        """ Returns the installed package binary. """
        try:
            return self.installed_packages[name]
        except KeyError:
            return ''

    def all_installed(self) -> tuple:
        """ Return all installed packages from /val/log/packages folder. """
        for file in self.log_packages.glob(self.file_pattern):
            name: str = self.split_package(file.name)['name']

            if not name.startswith('.') and not self.blacklist_pattern(name):
                yield name, file.name

    @staticmethod
    def remove_file_if_exists(path: Path, file: str) -> None:
        """ Remove the old files. """
        archive: Path = Path(path, file)
        if archive.is_file():
            archive.unlink()

    @staticmethod
    def remove_folder_if_exists(folder: Path) -> None:
        """ Remove the old folders. """
        if folder.exists():
            shutil.rmtree(folder)

    @staticmethod
    def create_directory(directory: Path) -> None:
        """ Creates folder like mkdir -p. """
        if not directory.is_dir():
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def split_package(package: str) -> dict:
        """ Splits the binary package name in name, version, arch, build and tag. """
        name: str = '-'.join(package.split('-')[:-3])
        version: str = ''.join(package[len(name):].split('-')[:-2])
        arch: str = ''.join(package[len(name + version) + 2:].split('-')[:-1])
        build_tag: str = package.split('-')[-1]
        build: str = ''.join(re.findall(r'\d+', build_tag[:2]))
        pkg_tag: str = build_tag[len(build):]

        return {
            'name': name,
            'version': version,
            'arch': arch,
            'build': build,
            'tag': pkg_tag
        }

    def finished_time(self, elapsed_time: float) -> None:
        """ Printing the elapsed time. """
        print(f'\n{self.yellow}Finished:{self.endc}',
              time.strftime(f'{self.cyan}%H:%M:%S{self.endc}',
                            time.gmtime(elapsed_time)))

    def read_slackbuild_build_tag(self, sbo: str, location: str, repository: str) -> str:
        """ Returns build tag from .SlackBuild file. """
        build: str = ''
        sbo_script = Path(self.repos.repositories[repository]['path'], location, sbo, f'{sbo}.SlackBuild')

        if sbo_script.is_file():
            lines = self.read_text_file(sbo_script)

            for line in lines:
                if line.startswith('BUILD=$'):
                    build = ''.join(re.findall(r'\d+', line))
        return build

    @staticmethod
    def is_option(options: tuple, flags: list) -> bool:
        """ Returns True if option applied. """
        for option in options:
            if option in flags:
                return True

    def read_packages_from_file(self, file: Path) -> Generator:
        """ Reads name packages from file and split these to list. """
        try:
            with open(file, 'r', encoding='utf-8') as pkgs:
                packages: list = pkgs.read().splitlines()

            for package in packages:
                if package and not package.startswith('#'):
                    if '#' in package:
                        package = package.split('#')[0].strip()
                    yield package
        except FileNotFoundError:
            logger = logging.getLogger(LoggingConfig.date_time)
            logger.exception(
                f'{self.__class__.__name__}: '
                f'{self.__class__.read_packages_from_file.__name__}'
            )
            self.errors.raise_error_message(f"No such file or directory: '{file}'", exit_status=20)

    def read_text_file(self, file: Path) -> list:
        """ Reads the text file and returns it into a list. """
        try:
            with open(file, 'r', encoding='utf-8', errors='replace') as text_file:
                return text_file.readlines()
        except FileNotFoundError:
            logger = logging.getLogger(LoggingConfig.date_time)
            logger.exception(
                f'{self.__class__.__name__}: '
                f'{self.__class__.read_text_file.__name__}'
            )
            self.errors.raise_error_message(f"No such file or directory: '{file}'", exit_status=20)

    def process(self, command: str, stderr=None, stdout=None, filename=None) -> None:
        """ Handle the processes. """
        output = tee = ''
        if filename and filename.endswith('.SlackBuild') and self.process_log:
            self.header_process_log(filename)
            tee: str = (
                f' | tee -a {self.slpkg_log_path}/{filename}_'
                f'{self.process_log_date}_{self.process_log_time}.log'
            )
        try:
            output = subprocess.run(f'{command}{tee}', shell=True, stderr=stderr, stdout=stdout)
        except subprocess.CalledProcessError as error:
            logger = logging.getLogger(LoggingConfig.date_time)
            logger.exception(
                f'{self.__class__.__name__}: '
                f'{self.__class__.process.__name__}: '
                f'{error}'
            )
        except KeyboardInterrupt:
            raise SystemExit(1)

        if output.returncode != 0:
            raise SystemExit(output.returncode)

    def header_process_log(self, filename: str) -> None:
        """ Creates the build log file and the header. """
        with open(f'{self.slpkg_log_path}/{filename}_{self.process_log_date}_{self.process_log_time}.log', 'w') as f:
            f.write(f'{LoggingConfig.date_time}: {filename}: Version: {self.prog_name} {self.prog_version.version}\n')

    def get_file_size(self, file: Path) -> str:
        """ Get the local file size and converted to units. """
        size: int = file.stat().st_size
        return self.convert_file_sizes(size)

    @staticmethod
    def convert_file_sizes(size: int) -> str:
        """ Convert file sizes. """
        units: tuple = ('KB', 'MB', 'GB')
        for unit in units:
            if size < 1000:
                return f'{size:.0f} {unit}'
            size /= 1000

    @staticmethod
    def apply_package_pattern(data: dict, packages: list) -> list:
        """ If the '*' applied returns all the package names. """
        for pkg in packages:
            if pkg == '*':
                packages.remove(pkg)
                packages.extend(list(data.keys()))
        return packages

    def blacklist_pattern(self, name: str) -> bool:
        """ This module provides support for Unix shell-style wildcards. """
        blacklist: list[str] = ['%README%']
        blacklist.extend(self.black.packages())
        if [black for black in blacklist if fnmatch.fnmatch(name, black)]:
            return True

    def is_binary_repo(self, repo: str) -> bool:
        """ Returns True if the repository is binary. """
        if repo in tuple(self.repos.repositories.keys())[2:]:
            return True

    @staticmethod
    def change_owner_privileges(folder: Path) -> None:
        """ Changes the owner privileges. """
        os.chown(folder, 0, 0)
        for file in os.listdir(folder):
            os.chown(Path(folder, file), 0, 0)

    @staticmethod
    def case_insensitive_pattern_matching(packages: list, data: dict) -> list:
        """ Case-insensitive pattern matching packages. """
        repo_packages: tuple = tuple(data.keys())
        for package in packages:
            for pkg in repo_packages:
                if package.lower() == pkg.lower():
                    packages.append(pkg)
                    packages.remove(package)
                    break
        return packages
