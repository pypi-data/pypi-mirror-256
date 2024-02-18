#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
from pathlib import Path
from collections import OrderedDict

from slpkg.configs import Configs
from slpkg.checksum import Md5sum
from slpkg.upgrade import Upgrade
from slpkg.views.views import View
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.downloader import Downloader
from slpkg.views.asciibox import AsciiBox
from slpkg.logging_deps import LoggingDeps
from slpkg.repositories import Repositories
from slpkg.multi_process import MultiProcess
from slpkg.binaries.required import Required


class Packages(Configs):

    def __init__(self, repository: str, data: dict, packages: list, flags: list, mode: str):
        super(Configs, self).__init__()
        self.data: dict = data
        self.packages: list = packages
        self.flags: list = flags
        self.mode: str = mode

        self.utils = Utilities()
        self.repos = Repositories()
        self.dialogbox = DialogBox()
        self.multi_proc = MultiProcess(flags)
        self.logs_deps = LoggingDeps(repository, data)
        self.upgrade = Upgrade(repository, data)
        self.view = View(flags, repository, data)
        self.check_md5 = Md5sum(flags)
        self.download = Downloader(flags)
        self.ascii = AsciiBox()

        self.dependencies: list = []
        self.install_order: list = []
        self.binary_packages: list = []
        self.slackware_command: str = self.installpkg
        self.progress_message: str = f'{self.cyan}Installing{self.endc}'

        self.option_for_reinstall: bool = self.utils.is_option(
            ('-r', '--reinstall'), flags)

        self.option_for_skip_installed: bool = self.utils.is_option(
            ('-k', '--skip-installed'), flags)

        self.option_for_resolve_off: bool = self.utils.is_option(
            ('-O', '--resolve-off'), flags)

        self.packages: list = self.utils.apply_package_pattern(data, packages)

    def execute(self) -> None:
        # self.creating_dependencies_list()
        self.creating_dependencies_list()
        self.remove_duplicate_from_dependencies_list()
        self.choose_package_dependencies()
        self.add_dependencies_to_install_order()
        self.clean_the_main_slackbuilds()
        self.add_main_packages_to_install_order()

        self.view.install_upgrade_packages(self.packages, self.dependencies, self.mode)
        self.view.question()

        start: float = time.time()
        self.crating_the_package_urls_list()
        self.checksum_binary_packages()
        self.set_slackware_command()
        self.set_progress_message()
        self.install_packages()
        elapsed_time: float = time.time() - start

        self.utils.finished_time(elapsed_time)

    def creating_dependencies_list(self) -> None:
        if not self.option_for_resolve_off:
            print('\rResolving dependencies... ', end='')
            for package in self.packages:
                dependencies: tuple = Required(self.data, package).resolve()

                for dependency in dependencies:
                    self.dependencies.append(dependency)
            print(f'{self.yellow}{self.ascii.done}{self.endc}')

    def remove_duplicate_from_dependencies_list(self) -> None:
        if self.dependencies:
            self.dependencies: list = list(OrderedDict.fromkeys(self.dependencies))

    def add_dependencies_to_install_order(self) -> None:
        self.install_order.extend(self.dependencies)

    def clean_the_main_slackbuilds(self) -> None:
        for dependency in self.dependencies:
            if dependency in self.packages:
                self.packages.remove(dependency)

    def add_main_packages_to_install_order(self) -> None:
        self.install_order.extend(self.packages)

    def crating_the_package_urls_list(self) -> None:
        packages: dict = {}

        for pkg in self.install_order:
            if self.continue_to_install(pkg):
                package: str = self.data[pkg]['package']
                mirror: str = self.data[pkg]['mirror']
                location: str = self.data[pkg]['location']
                url: list = [f'{mirror}{location}/{package}']

                packages[pkg] = (url, self.tmp_slpkg)

                self.binary_packages.append(package)
                self.utils.remove_file_if_exists(self.tmp_slpkg, package)
            else:
                installed_package: str = self.utils.is_package_installed(pkg)
                self.view.skipping_packages(installed_package)

        self.download_the_binary_packages(packages)

    def download_the_binary_packages(self, packages: dict) -> None:
        if packages:
            print(f'Started to download total ({self.cyan}{len(packages)}{self.endc}) packages:\n')
            self.download.download(packages)
            print()

    def continue_to_install(self, name: str) -> bool:
        """ Skip installed package when the option --skip-installed is applied
            and continue to install if the package is upgradable or the --reinstall option
            applied.
         """
        if not self.utils.is_package_installed(name):
            return True

        if self.utils.is_package_installed(name) and not self.option_for_skip_installed:
            return True

        return False

    def checksum_binary_packages(self) -> None:
        for package in self.binary_packages:
            name: str = self.utils.split_package(Path(package).stem)['name']
            pkg_checksum: str = self.data[name]['checksum']
            self.check_md5.md5sum(self.tmp_slpkg, package, pkg_checksum)

    def install_packages(self) -> None:
        if self.binary_packages:
            print(f'Started the processing of ({self.cyan}{len(self.binary_packages)}{self.endc}) packages:\n')
        for package in self.binary_packages:
            command: str = f'{self.slackware_command} {self.tmp_slpkg}/{package}'
            self.multi_proc.process(command, package, self.progress_message)

            if not self.option_for_resolve_off:
                name: str = self.utils.split_package(Path(package).stem)['name']
                self.logs_deps.logging(name)

    def set_progress_message(self) -> None:
        if self.mode == 'upgrade' or self.option_for_reinstall:
            self.progress_message: str = f'{self.cyan}Upgrading{self.endc}'

    def set_slackware_command(self) -> None:
        if self.mode == 'upgrade' or self.option_for_reinstall:
            self.slackware_command: str = self.reinstall

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
                help_text: str = f'Package: {package} {repo_ver}'
                installed: str = self.utils.is_package_installed(package)

                if installed:
                    status: bool = False

                if self.option_for_reinstall:
                    status: bool = True

                if self.mode == 'upgrade':
                    status: bool = True

                choices.extend([(package, repo_ver, status, help_text)])

            text: str = f'There are {len(choices)} dependencies:'
            code, self.dependencies = self.dialogbox.checklist(text, title, height, width, list_height, choices)

            os.system('clear')
