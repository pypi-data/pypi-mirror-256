#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Any
from pathlib import Path

from slpkg.configs import Configs
from slpkg.upgrade import Upgrade
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.views.asciibox import AsciiBox


class View(Configs):

    def __init__(self, flags=None, repository=None, data=None):
        super(Configs, self).__init__()
        if flags is None:
            flags: list = []
        self.flags: list = flags
        self.repository = repository
        self.data: dict = data

        self.utils = Utilities()
        self.dialogbox = DialogBox()
        self.ascii = AsciiBox()
        self.upgrade = Upgrade(repository, data)

        self.download_only = None
        self.summary_message: str = ''
        self.is_binary: bool = self.utils.is_binary_repo(repository)

        self.option_for_resolve_off: bool = self.utils.is_option(
            ('-O', '--resolve-off'), flags)

        self.option_for_reinstall: bool = self.utils.is_option(
            ('-r', '--reinstall'), flags)

        self.option_for_yes: bool = self.utils.is_option(
            ('-y', '--yes'), flags)

    def build_packages(self, slackbuilds: list, dependencies: list) -> None:
        mode: str = 'build'
        self.ascii.draw_package_title('The following packages will be build:',
                                      'slpkg build packages')

        for slackbuild in slackbuilds:
            self.build_package(slackbuild)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.build_package(dependency)

        self.summary(slackbuilds, dependencies, option=mode)

    def install_upgrade_packages(self, packages: list, dependencies: list, mode: str) -> None:
        title: str = 'slpkg install packages'
        if mode == 'upgrade':
            title: str = 'slpkg upgrade packages'
        self.ascii.draw_package_title('The following packages will be installed or upgraded:', title)

        for package in packages:
            self.install_upgrade_package(package)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.install_upgrade_package(dependency)

        self.summary(packages, dependencies, option=mode)

    def download_packages(self, packages: list, directory: Path) -> None:
        mode: str = 'download'
        self.download_only: Path = directory
        self.ascii.draw_package_title('The following packages will be downloaded:',
                                      'slpkg download packages')

        for package in packages:
            self.download_package(package)

        self.summary(packages, dependencies=[], option=mode)

    def remove_packages(self, packages: list, dependencies: list) -> Any:
        mode: str = 'remove'
        self.ascii.draw_package_title('The following packages will be removed:',
                                      'slpkg remove packages')
        for package in packages:
            self.remove_package(package)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for dependency in dependencies:
                self.remove_package(dependency)

        self.summary(packages, dependencies, option=mode)

    def build_package(self, package: str) -> None:
        size: str = ''
        color: str = self.yellow
        version: str = self.data[package]['version']

        if self.is_binary:
            size: str = self.utils.convert_file_sizes(int(self.data[package]['size_comp']))

        self.ascii.draw_package_line(package, version, size, color, self.repository)

    def install_upgrade_package(self, package: str) -> None:
        size: str = ''
        color: str = self.cyan
        version: str = self.data[package]['version']
        installed: str = self.utils.is_package_installed(package)
        upgradable: bool = self.upgrade.is_package_upgradeable(package)

        if self.is_binary:
            size: str = self.utils.convert_file_sizes(int(self.data[package]['size_comp']))

        if installed:
            color: str = self.grey

        if upgradable:
            color: str = self.violet
            package: str = self.build_package_and_version(package)

        if installed and self.option_for_reinstall and not upgradable:
            color: str = self.violet
            package: str = self.build_package_and_version(package)

        self.ascii.draw_package_line(package, version, size, color, self.repository)

    def download_package(self, package: str) -> None:
        size: str = ''
        color: str = self.cyan
        version: str = self.data[package]['version']

        if self.is_binary:
            size: str = self.utils.convert_file_sizes(int(self.data[package]['size_comp']))

        self.ascii.draw_package_line(package, version, size, color, self.repository)

    def remove_package(self, package: str) -> None:
        installed: str = self.utils.is_package_installed(package)
        version: str = self.utils.split_package(installed)['version']
        repo_tag: str = self.utils.split_package(installed)['tag']
        size: str = self.utils.get_file_size(Path(self.log_packages, installed))
        repository: str = repo_tag.lower().replace('_', '')

        self.ascii.draw_package_line(package, version, size, self.red, repository)

    def logs_dependencies(self, dependencies: list) -> None:
        print('The following logs will be removed:\n')
        for dep in dependencies:
            print(f'{self.yellow}{dep[0]}{self.endc}')
            self.ascii.draw_log_package(dep[1])

        print('Note: After cleaning you should remove them one by one.')

    def summary(self, packages: list, dependencies: list, option: str) -> None:
        packages.extend(dependencies)
        install = upgrade = remove = size_comp = size_uncomp = size_rmv = int()

        for pkg in packages:
            installed: str = self.utils.is_package_installed(pkg)

            if self.is_binary:
                size_comp += int(self.data[pkg]['size_comp'])
                size_uncomp += int(self.data[pkg]['size_uncomp'])

            if installed and option == 'remove':
                size_rmv += Path(self.log_packages, installed).stat().st_size

            upgradeable: bool = False
            if option != 'remove':
                upgradeable: bool = self.upgrade.is_package_upgradeable(pkg)

            if not installed:
                install += 1
            elif installed and self.option_for_reinstall:
                upgrade += 1
            elif upgradeable:
                upgrade += 1
            elif installed and option == 'remove':
                remove += 1

        self.ascii.draw_bottom_line()

        if option in ['install', 'upgrade']:
            self.set_summary_for_install_and_upgrade(install, upgrade, size_comp, size_uncomp)
        elif option == 'build':
            self.set_summary_for_build(packages)
        elif option == 'remove':
            self.set_summary_for_remove(remove, size_rmv)
        elif option == 'download':
            self.set_summary_for_download(packages, size_comp)

        print(self.summary_message)

    def set_summary_for_install_and_upgrade(self, install: int, upgrade: int, size_comp: int, size_uncomp: int) -> None:
        self.summary_message: str = (
            f'{self.grey}Total {install} packages will be '
            f'installed and {upgrade} will be upgraded, and total '
            f'{self.utils.convert_file_sizes(size_comp)} will be downloaded and '
            f'{self.utils.convert_file_sizes(size_uncomp)} will be installed.{self.endc} ')

    def set_summary_for_build(self, packages: list) -> None:
        self.summary_message: str = (
            f'{self.grey}Total {len(packages)} packages '
            f'will be build in {self.tmp_path} folder.{self.endc}')

    def set_summary_for_remove(self, remove: int, size_rmv: int) -> None:
        self.summary_message: str = (
            f'{self.grey}Total {remove} packages '
            f'will be removed and {self.utils.convert_file_sizes(size_rmv)} '
            f'of space will be freed up.{self.endc}')

    def set_summary_for_download(self, packages: list, size_comp: int) -> None:
        self.summary_message: str = (
            f'{self.grey}Total {len(packages)} packages and {self.utils.convert_file_sizes(size_comp)} '
            f'will be downloaded in {self.download_only} folder.{self.endc}'
        )

    def build_package_and_version(self, package: str) -> str:
        installed_package: str = self.utils.is_package_installed(package)
        version: str = self.utils.split_package(installed_package)['version']
        return f'{package}-{version}'

    def skipping_packages(self, filename: str) -> None:
        failed: str = f'{self.red}{self.ascii.skipped}{self.endc}'
        print(f"\r{'':>2}{self.bred}{self.ascii.bullet}{self.endc} {filename} {failed}{' ' * 17}")

    def question(self) -> None:
        if not self.option_for_yes and self.ask_question:
            answer: str = input('\nDo you want to continue? [y/N] ')
            if answer not in ['Y', 'y']:
                raise SystemExit(0)
        print()
