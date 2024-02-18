#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import shutil
import logging

from pathlib import Path
from collections import OrderedDict
from multiprocessing import cpu_count

from slpkg.checksum import Md5sum
from slpkg.configs import Configs
from slpkg.upgrade import Upgrade
from slpkg.views.views import View
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.downloader import Downloader
from slpkg.error_messages import Errors
from slpkg.views.asciibox import AsciiBox
from slpkg.logging_deps import LoggingDeps
from slpkg.repositories import Repositories
from slpkg.multi_process import MultiProcess
from slpkg.sbos.dependencies import Requires
from slpkg.logging_config import LoggingConfig


class Slackbuilds(Configs):
    """ Download build and install the SlackBuilds. """

    def __init__(self, repository: str, data: dict, slackbuilds: list, flags: list, mode: str):
        super(Configs, self).__init__()
        self.repository: str = repository
        self.data: dict = data
        self.slackbuilds: list = slackbuilds
        self.flags: list = flags
        self.mode: str = mode

        self.errors = Errors()
        self.repos = Repositories()
        self.utils = Utilities()
        self.dialogbox = DialogBox()
        self.multi_proc = MultiProcess(flags)
        self.logs_deps = LoggingDeps(repository, data)
        self.upgrade = Upgrade(repository, data)
        self.view = View(flags, repository, data)
        self.check_md5 = Md5sum(flags)
        self.download = Downloader(flags)
        self.ascii = AsciiBox()

        self.sources: dict = {}
        self.install_order: list = []
        self.dependencies: list = []
        self.slackware_command: str = ''
        self.slackware_command: str = self.installpkg
        self.progress_message: str = f'{self.cyan}Installing{self.endc}'

        self.option_for_reinstall: bool = self.utils.is_option(
            ('-r', '--reinstall'), flags)

        self.option_for_skip_installed: bool = self.utils.is_option(
            ('-k', '--skip-installed'), flags)

        self.option_for_resolve_off: bool = self.utils.is_option(
            ('-O', '--resolve-off'), flags)

        self.option_for_jobs: bool = self.utils.is_option(
            ('-j', '--jobs'), flags)

        self.slackbuilds: list = self.utils.apply_package_pattern(data, slackbuilds)

        # Patch the TAG from configs if changed.
        self.repo_tag: str = self.repos.repositories[repository]['repo_tag']
        if self.repos.repositories[repository]['patch_tag']:
            self.repo_tag: str = self.repos.repositories[repository]['repo_tag']

        logging.basicConfig(filename=LoggingConfig.log_file,
                            filemode=LoggingConfig.filemode,
                            encoding=LoggingConfig.encoding,
                            level=LoggingConfig.level)

    def execute(self) -> None:
        self.creating_dependencies_list()
        self.remove_duplicate_from_dependencies_list()
        self.choose_package_dependencies()
        self.add_dependencies_to_install_order()
        self.clean_the_main_slackbuilds()
        self.add_main_packages_to_install_order()
        self.view_slackbuilds_before_build()

        start: float = time.time()
        self.prepare_slackbuilds_for_build()
        self.download_the_sources()
        self.set_slackware_command()
        self.set_progress_message()
        self.build_and_install_the_slackbuilds()
        elapsed_time: float = time.time() - start

        self.utils.finished_time(elapsed_time)

    def creating_dependencies_list(self) -> None:
        if not self.option_for_resolve_off:
            print('\rResolving dependencies... ', end='')
            for slackbuild in self.slackbuilds:
                dependencies: tuple = Requires(self.data, slackbuild).resolve()

                for dependency in dependencies:
                    self.dependencies.append(dependency)
            print(f'{self.yellow}{self.ascii.done}{self.endc}')

    def remove_duplicate_from_dependencies_list(self) -> None:
        self.dependencies: list = list(OrderedDict.fromkeys(self.dependencies))

    def add_dependencies_to_install_order(self) -> None:
        self.install_order.extend(self.dependencies)

    def clean_the_main_slackbuilds(self) -> None:
        for dep in self.dependencies:
            if dep in self.slackbuilds:
                self.slackbuilds.remove(dep)

    def add_main_packages_to_install_order(self) -> None:
        self.install_order.extend(self.slackbuilds)

    def view_slackbuilds_before_build(self) -> None:
        if self.mode == 'build':
            self.view.build_packages(self.slackbuilds, self.dependencies)
        else:
            self.view.install_upgrade_packages(self.slackbuilds, self.dependencies, self.mode)

        self.view.question()

    def continue_build_or_install(self, name: str) -> bool:
        """ Skip installed package when the option --skip-installed is applied
            and continue to install if the package is upgradable or the --reinstall option
            applied.
        """
        if self.mode == 'build':
            return True

        if not self.utils.is_package_installed(name):
            return True

        if self.utils.is_package_installed(name) and not self.option_for_skip_installed:
            return True

        return False

    def prepare_slackbuilds_for_build(self) -> None:
        for sbo in self.install_order:
            if self.continue_build_or_install(sbo):
                build_path: Path = Path(self.build_path, sbo)

                self.utils.remove_folder_if_exists(build_path)
                location: str = self.data[sbo]['location']
                slackbuild: Path = Path(self.build_path, sbo, f'{sbo}.SlackBuild')

                # Copy slackbuilds to the build folder.
                path_repo_package: Path = Path(self.repos.repositories[self.repository]['path'], location, sbo)
                shutil.copytree(path_repo_package, build_path)

                os.chmod(slackbuild, 0o775)

                if self.os_arch == 'x86_64' and self.data[sbo]['download64']:
                    sources: tuple = self.data[sbo]['download64'].split()
                else:
                    sources: tuple = self.data[sbo]['download'].split()

                self.sources[sbo] = (sources, Path(self.build_path, sbo))

    def download_the_sources(self) -> None:
        if self.sources:
            print(f'Started to download total ({self.cyan}{len(self.sources)}{self.endc}) sources:\n')
            self.download.download(self.sources)
            print()

            self.checksum_downloaded_sources()

    def checksum_downloaded_sources(self) -> None:
        for sbo in self.install_order:
            path: Path = Path(self.build_path, sbo)

            if self.os_arch == 'x86_64' and self.data[sbo]['md5sum64']:
                checksums: list = self.data[sbo]['md5sum64'].split()
                sources: list = self.data[sbo]['download64'].split()
            else:
                checksums: list = self.data[sbo]['md5sum'].split()
                sources: list = self.data[sbo]['download'].split()

            for source, checksum in zip(sources, checksums):
                self.check_md5.md5sum(path, source, checksum)

    def build_and_install_the_slackbuilds(self) -> None:
        if self.install_order:
            print(f'Started the processing of ({self.cyan}{len(self.install_order)}{self.endc}) packages:\n')
        for sbo in self.install_order:
            if self.continue_build_or_install(sbo):
                self.patch_slackbuild_tag(sbo)
                self.build_the_script(self.build_path, sbo)

                if self.mode in ('install', 'upgrade'):
                    self.install_package(sbo)

                    if not self.option_for_resolve_off:
                        self.logs_deps.logging(sbo)
            else:
                installed_package: str = self.utils.is_package_installed(sbo)
                self.view.skipping_packages(installed_package)

    def patch_slackbuild_tag(self, sbo: str) -> None:
        sbo_script: Path = Path(self.build_path, sbo, f'{sbo}.SlackBuild')
        if sbo_script.is_file() and self.repo_tag:
            lines: list = self.utils.read_text_file(sbo_script)

            with open(sbo_script, 'w') as script:
                for line in lines:
                    if line.startswith('TAG=$'):
                        line: str = f'TAG=${{TAG:-{self.repo_tag}}}\n'
                    script.write(line)

    def install_package(self, name: str) -> None:
        package: str = self.find_package_for_install(name)
        command: str = f'{self.slackware_command} {self.tmp_path}/{package}'
        self.multi_proc.process(command, package, self.progress_message)

    def find_package_for_install(self, name: str) -> str:
        version: str = self.data[name]['version']
        pattern: str = f'{name}-{version}*{self.repo_tag}*'
        packages: list = [file.name for file in self.tmp_path.glob(pattern)]
        try:
            return max(packages)
        except ValueError:
            logger = logging.getLogger(LoggingConfig.date_time)
            logger.exception(f'{self.__class__.__name__}: '
                             f'{self.__class__.find_package_for_install.__name__}')
            self.errors.raise_error_message(f"Package '{name}' not found for install", exit_status=20)

    def build_the_script(self, path: Path, name: str) -> None:
        self.set_makeflags()
        folder: Path = Path(path, name)
        filename: str = f'{name}.SlackBuild'
        command: str = f'{folder}/./{filename}'
        self.utils.change_owner_privileges(folder)
        progress_message: str = f'{self.red}Building{self.endc}'
        self.multi_proc.process(command, filename, progress_message)

    def set_progress_message(self) -> None:
        if self.mode == 'upgrade' or self.option_for_reinstall:
            self.progress_message: str = f'{self.cyan}Upgrading{self.endc}'

    def set_slackware_command(self) -> None:
        if self.mode == 'upgrade' or self.option_for_reinstall:
            self.slackware_command: str = self.reinstall

    def set_makeflags(self) -> None:
        if self.option_for_jobs:
            os.environ['MAKEFLAGS'] = f'-j {cpu_count()}'

    def choose_package_dependencies(self) -> None:
        if self.dependencies and self.dialog:
            height: int = 10
            width: int = 70
            list_height: int = 0
            choices: list = []
            title: str = ' Choose dependencies you want to install '

            for package in self.dependencies:
                status: bool = True
                repo_ver: str = self.data[package]['version']
                description: str = self.data[package]['description']
                help_text: str = f'Description: {description}'
                installed: str = self.utils.is_package_installed(package)

                if installed:
                    status: bool = False

                if self.option_for_reinstall:
                    status: bool = True

                if self.mode == 'upgrade':
                    status: bool = True

                choices.extend(
                    [(package, repo_ver, status, help_text)]
                )
            text: str = f'There are {len(choices)} dependencies:'

            code, self.dependencies = self.dialogbox.checklist(text, title, height, width, list_height, choices)

            os.system('clear')
