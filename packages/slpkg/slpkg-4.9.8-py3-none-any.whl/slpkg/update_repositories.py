#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path
from multiprocessing import Process, Queue

from slpkg.configs import Configs
from slpkg.views.views import View
from slpkg.repo_info import RepoInfo
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.progress_bar import ProgressBar
from slpkg.install_data import InstallData
from slpkg.repositories import Repositories
from slpkg.check_updates import CheckUpdates
from slpkg.sbos.sbo_generate import SBoGenerate
from slpkg.models.models import session as Session
from slpkg.models.models import (SBoTable, PonceTable,
                                 BinariesTable, LastRepoUpdated)


class UpdateRepositories(Configs):
    """ Updates the local repositories and install the data
        into the database.
    """

    def __init__(self, flags: list, repository: str):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repository: str = repository

        self.session = Session
        self.view = View(flags)
        self.repos = Repositories()
        self.progress = ProgressBar()
        self.utils = Utilities()
        self.data = InstallData()
        self.generate = SBoGenerate()
        self.check_updates = CheckUpdates(flags, repository)
        self.download = Downloader(flags)
        self.repo_info = RepoInfo(flags, repository)

        self.repos_for_update: dict = {}

        self.is_binary: bool = self.utils.is_binary_repo(repository)

        self.option_for_repository: bool = self.utils.is_option(
            ('-o', '--repository='), flags)

        self.option_for_install_data: bool = self.utils.is_option(
            ('-a', '--install-data'), flags)

    def update_the_repositories(self) -> None:
        if not any(list(self.repos_for_update.values())):
            self.view.question()
            for repo in self.repos_for_update:
                self.repos_for_update[repo] = True
        else:
            print()

        repositories: dict = {
            self.repos.sbo_repo_name: self.sbo_repository,
            self.repos.ponce_repo_name: self.ponce_repository,
            self.repos.slack_repo_name: self.slack_repository,
            self.repos.slack_extra_repo_name: self.slack_extra_repository,
            self.repos.slack_patches_repo_name: self.slack_patches_repository,
            self.repos.alien_repo_name: self.alien_repository,
            self.repos.multilib_repo_name: self.multilib_repository,
            self.repos.restricted_repo_name: self.restricted_repository,
            self.repos.gnome_repo_name: self.gnome_repository,
            self.repos.msb_repo_name: self.msb_repository,
            self.repos.csb_repo_name: self.csb_repository,
            self.repos.conraid_repo_name: self.conraid_repository,
            self.repos.slackdce_repo_name: self.slackdce_repository,
            self.repos.slackonly_repo_name: self.slackonly_repository,
            self.repos.salixos_repo_name: self.salixos_repository,
            self.repos.salixos_extra_repo_name: self.salixos_extra_repository,
            self.repos.salixos_patches_repo_name: self.salixos_patches_repository,
            self.repos.slackel_repo_name: self.slackel_repository,
            self.repos.slint_repo_name: self.slint_repository,
            self.repos.pprkut_repo_name: self.pprkut_repository
        }

        if self.option_for_repository:
            if not self.option_for_install_data:
                self.view_downloading_message(self.repository)
            repositories[self.repository]()
        else:
            for repo, update in self.repos_for_update.items():
                if update:
                    if not self.option_for_install_data:
                        self.view_downloading_message(repo)
                    repositories[repo]()
        print()

    def view_downloading_message(self, repo: str) -> None:
        print(f"Downloading the '{self.green}{repo}{self.endc}' repository "
              f"in the '{self.repos.repositories[repo]['path']}' folder, please wait...\n")

    def slack_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.slack_repo_path)

            self.utils.remove_file_if_exists(self.repos.slack_repo_path, self.repos.slack_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slack_repo_path, self.repos.slack_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slack_repo_path, self.repos.slack_repo_checksums)

            if self.repos.slack_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.slack_repo_mirror[0]} '
                    f'{self.repos.slack_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.slack_repo_mirror[0]}{self.repos.slack_repo_changelog}'
                packages: str = f'{self.repos.slack_repo_mirror[0]}{self.repos.slack_repo_packages}'
                checksums: str = f'{self.repos.slack_repo_mirror[0]}{self.repos.slack_repo_checksums}'

                urls[self.repos.slack_repo_name] = ((changelog, packages, checksums), self.repos.slack_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.slack_repo_name)
        self.delete_last_updated(self.repos.slack_repo_name)
        self.data.install_slack_data()

    def slack_extra_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.slack_extra_repo_path)

            self.utils.remove_file_if_exists(self.repos.slack_extra_repo_path, self.repos.slack_extra_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slack_extra_repo_path, self.repos.slack_extra_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slack_extra_repo_path, self.repos.slack_extra_repo_checksums)

            changelog: str = f'{self.repos.slack_extra_repo_mirror[0]}{self.repos.slack_extra_repo_changelog}'

            if self.repos.slack_extra_repo_local[0].startswith('file'):
                urls[self.repos.slack_extra_repo_name] = ((changelog,), self.repos.slack_extra_repo_path)
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.slack_extra_repo_mirror)} '
                    f'{self.repos.slack_extra_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                packages: str = f'{"".join(self.repos.slack_extra_repo_mirror)}{self.repos.slack_extra_repo_packages}'
                checksums: str = f'{"".join(self.repos.slack_extra_repo_mirror)}{self.repos.slack_extra_repo_checksums}'
                urls[self.repos.slack_extra_repo_name] = ((changelog, packages, checksums),
                                                          self.repos.slack_extra_repo_path)

            self.download.download(urls)
            print()

        self.delete_bin_database_data(self.repos.slack_extra_repo_name)
        self.delete_last_updated(self.repos.slack_extra_repo_name)
        self.data.install_slack_extra_data()

    def slack_patches_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.slack_patches_repo_path)

            self.utils.remove_file_if_exists(self.repos.slack_patches_repo_path,
                                             self.repos.slack_patches_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slack_patches_repo_path,
                                             self.repos.slack_patches_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slack_patches_repo_path,
                                             self.repos.slack_patches_repo_checksums)

            changelog: str = f'{self.repos.slack_patches_repo_mirror[0]}{self.repos.slack_patches_repo_changelog}'

            if self.repos.slack_patches_repo_local[0].startswith('file'):
                urls[self.repos.slack_patches_repo_name] = ((changelog,), self.repos.slack_patches_repo_path)
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.slack_patches_repo_mirror)} '
                    f'{self.repos.slack_patches_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                packages: str = (f'{"".join(self.repos.slack_patches_repo_mirror)}'
                                 f'{self.repos.slack_patches_repo_packages}')
                checksums: str = (f'{"".join(self.repos.slack_patches_repo_mirror)}'
                                  f'{self.repos.slack_patches_repo_checksums}')

                urls[self.repos.slack_patches_repo_name] = ((changelog, packages, checksums),
                                                            self.repos.slack_patches_repo_path)

            self.download.download(urls)
            print()

        self.delete_bin_database_data(self.repos.slack_patches_repo_name)
        self.delete_last_updated(self.repos.slack_patches_repo_name)
        self.data.install_slack_patches_data()

    def alien_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.alien_repo_path)

            self.utils.remove_file_if_exists(self.repos.alien_repo_path, self.repos.alien_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.alien_repo_path, self.repos.alien_repo_packages)
            self.utils.remove_file_if_exists(self.repos.alien_repo_path, self.repos.alien_repo_checksums)

            changelog: str = f'{self.repos.alien_repo_mirror[0]}{self.repos.alien_repo_changelog}'

            if self.repos.alien_repo_local[0].startswith('file'):
                urls[self.repos.alien_repo_name] = ((changelog,), self.repos.alien_repo_path)
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.alien_repo_mirror)} '
                    f'{self.repos.alien_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                packages: str = f'{"".join(self.repos.alien_repo_mirror)}{self.repos.alien_repo_packages}'
                checksums: str = f'{"".join(self.repos.alien_repo_mirror)}{self.repos.alien_repo_checksums}'

                urls[self.repos.alien_repo_name] = ((changelog, packages, checksums),
                                                    self.repos.alien_repo_path)

            self.download.download(urls)
            print()

        self.delete_bin_database_data(self.repos.alien_repo_name)
        self.delete_last_updated(self.repos.alien_repo_name)
        self.data.install_alien_data()

    def multilib_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.multilib_repo_path)

            self.utils.remove_file_if_exists(self.repos.multilib_repo_path, self.repos.multilib_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.multilib_repo_path, self.repos.multilib_repo_packages)
            self.utils.remove_file_if_exists(self.repos.multilib_repo_path, self.repos.multilib_repo_checksums)

            changelog: str = f'{self.repos.multilib_repo_mirror[0]}{self.repos.multilib_repo_changelog}'

            if self.repos.multilib_repo_local[0].startswith('file'):
                urls[self.repos.multilib_repo_name] = ((changelog,), self.repos.multilib_repo_path)
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.multilib_repo_mirror)} '
                    f'{self.repos.multilib_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                packages: str = f'{"".join(self.repos.multilib_repo_mirror)}{self.repos.multilib_repo_packages}'
                checksums: str = f'{"".join(self.repos.multilib_repo_mirror)}{self.repos.multilib_repo_checksums}'

                urls[self.repos.multilib_repo_name] = ((changelog, packages, checksums),
                                                       self.repos.multilib_repo_path)

            self.download.download(urls)
            print()

        self.delete_bin_database_data(self.repos.multilib_repo_name)
        self.delete_last_updated(self.repos.multilib_repo_name)
        self.data.install_multilib_data()

    def restricted_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.restricted_repo_path)

            self.utils.remove_file_if_exists(self.repos.restricted_repo_path, self.repos.restricted_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.restricted_repo_path, self.repos.restricted_repo_packages)
            self.utils.remove_file_if_exists(self.repos.restricted_repo_path, self.repos.restricted_repo_checksums)

            changelog: str = f'{self.repos.restricted_repo_mirror[0]}{self.repos.restricted_repo_changelog}'

            if self.repos.restricted_repo_local[0].startswith('file'):
                urls[self.repos.restricted_repo_name] = ((changelog,), self.repos.restricted_repo_path)
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.restricted_repo_mirror)} '
                    f'{self.repos.restricted_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                packages: str = f'{"".join(self.repos.restricted_repo_mirror)}{self.repos.restricted_repo_packages}'
                checksums: str = f'{"".join(self.repos.restricted_repo_mirror)}{self.repos.restricted_repo_checksums}'

                urls[self.repos.restricted_repo_name] = ((changelog, packages, checksums),
                                                         self.repos.restricted_repo_path)

            self.download.download(urls)
            print()

        self.delete_bin_database_data(self.repos.restricted_repo_name)
        self.delete_last_updated(self.repos.restricted_repo_name)
        self.data.install_restricted_data()

    def gnome_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.gnome_repo_path)

            self.utils.remove_file_if_exists(self.repos.gnome_repo_path, self.repos.gnome_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.gnome_repo_path, self.repos.gnome_repo_packages)
            self.utils.remove_file_if_exists(self.repos.gnome_repo_path, self.repos.gnome_repo_checksums)

            if self.repos.gnome_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.gnome_repo_mirror[0]} '
                    f'{self.repos.gnome_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.gnome_repo_mirror[0]}{self.repos.gnome_repo_changelog}'
                packages: str = f'{self.repos.gnome_repo_mirror[0]}{self.repos.gnome_repo_packages}'
                checksums: str = f'{self.repos.gnome_repo_mirror[0]}{self.repos.gnome_repo_checksums}'

                urls[self.repos.gnome_repo_name] = ((changelog, packages, checksums), self.repos.gnome_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.gnome_repo_name)
        self.delete_last_updated(self.repos.gnome_repo_name)
        self.data.install_gnome_data()

    def msb_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.msb_repo_path)

            self.utils.remove_file_if_exists(self.repos.msb_repo_path, self.repos.msb_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.msb_repo_path, self.repos.msb_repo_packages)
            self.utils.remove_file_if_exists(self.repos.msb_repo_path, self.repos.msb_repo_checksums)

            changelog: str = f'{self.repos.msb_repo_mirror[0]}{self.repos.msb_repo_changelog}'

            if self.repos.msb_repo_local[0].startswith('file'):
                urls[self.repos.msb_repo_name] = ((changelog,), self.repos.msb_repo_path)
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.msb_repo_mirror)} '
                    f'{self.repos.msb_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                packages: str = f'{"".join(self.repos.msb_repo_mirror)}{self.repos.msb_repo_packages}'
                checksums: str = f'{"".join(self.repos.msb_repo_mirror)}{self.repos.msb_repo_checksums}'

                urls[self.repos.msb_repo_name] = ((changelog, packages, checksums), self.repos.msb_repo_path)

            self.download.download(urls)
            print()

        self.delete_bin_database_data(self.repos.msb_repo_name)
        self.delete_last_updated(self.repos.msb_repo_name)
        self.data.install_msb_data()

    def csb_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.csb_repo_path)

            self.utils.remove_file_if_exists(self.repos.csb_repo_path, self.repos.csb_repo_packages)
            self.utils.remove_file_if_exists(self.repos.csb_repo_path, self.repos.csb_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.csb_repo_path, self.repos.csb_repo_checksums)

            if self.repos.csb_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.csb_repo_mirror)} '
                    f'{self.repos.csb_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{"".join(self.repos.csb_repo_mirror)}{self.repos.csb_repo_changelog}'
                packages: str = f'{"".join(self.repos.csb_repo_mirror)}{self.repos.csb_repo_packages}'
                checksums: str = f'{"".join(self.repos.csb_repo_mirror)}{self.repos.csb_repo_checksums}'

                urls[self.repos.csb_repo_name] = ((changelog, packages, checksums), self.repos.csb_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.csb_repo_name)
        self.delete_last_updated(self.repos.csb_repo_name)
        self.data.install_csb_data()

    def conraid_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.conraid_repo_path)

            self.utils.remove_file_if_exists(self.repos.conraid_repo_path, self.repos.conraid_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.conraid_repo_path, self.repos.conraid_repo_packages)
            self.utils.remove_file_if_exists(self.repos.conraid_repo_path, self.repos.conraid_repo_checksums)

            if self.repos.conraid_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.conraid_repo_mirror[0]} '
                    f'{self.repos.conraid_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.conraid_repo_mirror[0]}{self.repos.conraid_repo_changelog}'
                packages: str = f'{self.repos.conraid_repo_mirror[0]}{self.repos.conraid_repo_packages}'
                checksums: str = f'{self.repos.conraid_repo_mirror[0]}{self.repos.conraid_repo_checksums}'

                urls[self.repos.conraid_repo_name] = ((changelog, packages, checksums), self.repos.conraid_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.conraid_repo_name)
        self.delete_last_updated(self.repos.conraid_repo_name)
        self.data.install_conraid_data()

    def slackdce_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.slackdce_repo_path)

            self.utils.remove_file_if_exists(self.repos.slackdce_repo_path, self.repos.slackdce_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slackdce_repo_path, self.repos.slackdce_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slackdce_repo_path, self.repos.slackdce_repo_checksums)

            if self.repos.slackdce_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.slackdce_repo_mirror[0]} '
                    f'{self.repos.slackdce_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.slackdce_repo_mirror[0]}{self.repos.slackdce_repo_changelog}'
                packages: str = f'{self.repos.slackdce_repo_mirror[0]}{self.repos.slackdce_repo_packages}'
                checksums: str = f'{self.repos.slackdce_repo_mirror[0]}{self.repos.slackdce_repo_checksums}'

                urls[self.repos.slackdce_repo_name] = ((changelog, packages, checksums), self.repos.slackdce_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.slackdce_repo_name)
        self.delete_last_updated(self.repos.slackdce_repo_name)
        self.data.install_slackdce_data()

    def slackonly_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.slackonly_repo_path)

            self.utils.remove_file_if_exists(self.repos.slackonly_repo_path, self.repos.slackonly_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slackonly_repo_path, self.repos.slackonly_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slackonly_repo_path, self.repos.slackonly_repo_checksums)

            if self.repos.slackonly_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.slackonly_repo_mirror[0]} '
                    f'{self.repos.slackonly_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.slackonly_repo_mirror[0]}{self.repos.slackonly_repo_changelog}'
                packages: str = f'{self.repos.slackonly_repo_mirror[0]}{self.repos.slackonly_repo_packages}'
                checksums: str = f'{self.repos.slackonly_repo_mirror[0]}{self.repos.slackonly_repo_checksums}'

                urls[self.repos.slackonly_repo_name] = ((changelog, packages, checksums),
                                                        self.repos.slackonly_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.slackonly_repo_name)
        self.delete_last_updated(self.repos.slackonly_repo_name)
        self.data.install_slackonly_data()

    def salixos_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.salixos_repo_path)

            self.utils.remove_file_if_exists(self.repos.salixos_repo_path, self.repos.salixos_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.salixos_repo_path, self.repos.salixos_repo_packages)
            self.utils.remove_file_if_exists(self.repos.salixos_repo_path, self.repos.salixos_repo_checksums)

            if self.repos.salixos_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.salixos_repo_mirror[0]} '
                    f'{self.repos.salixos_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.salixos_repo_mirror[0]}{self.repos.salixos_repo_changelog}'
                packages: str = f'{self.repos.salixos_repo_mirror[0]}{self.repos.salixos_repo_packages}'
                checksums: str = f'{self.repos.salixos_repo_mirror[0]}{self.repos.salixos_repo_checksums}'

                urls[self.repos.salixos_repo_name] = ((changelog, packages, checksums), self.repos.salixos_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.salixos_repo_name)
        self.delete_last_updated(self.repos.salixos_repo_name)
        self.data.install_salixos_data()

    def salixos_extra_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.salixos_extra_repo_path)

            self.utils.remove_file_if_exists(self.repos.salixos_extra_repo_path,
                                             self.repos.salixos_extra_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.salixos_extra_repo_path,
                                             self.repos.salixos_extra_repo_packages)
            self.utils.remove_file_if_exists(self.repos.salixos_extra_repo_path,
                                             self.repos.salixos_extra_repo_checksums)

            changelog: str = f'{self.repos.salixos_extra_repo_mirror[0]}{self.repos.salixos_extra_repo_changelog}'

            if self.repos.salixos_extra_repo_local[0].startswith('file'):
                urls[self.repos.salixos_extra_repo_name] = ((changelog,), self.repos.salixos_extra_repo_path)
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.salixos_extra_repo_mirror)} '
                    f'{self.repos.salixos_extra_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                packages: str = f'{"".join(self.repos.salixos_extra_repo_mirror)}' \
                                f'{self.repos.salixos_extra_repo_packages}'
                checksums: str = (f'{"".join(self.repos.salixos_extra_repo_mirror)}'
                                  f'{self.repos.salixos_extra_repo_checksums}')

                urls[self.repos.salixos_extra_repo_name] = ((changelog, packages, checksums),
                                                            self.repos.salixos_extra_repo_path)

            self.download.download(urls)
            print()

        self.delete_bin_database_data(self.repos.salixos_extra_repo_name)
        self.delete_last_updated(self.repos.salixos_extra_repo_name)
        self.data.install_salixos_extra_data()

    def salixos_patches_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.slack_patches_repo_path)

            self.utils.remove_file_if_exists(self.repos.salixos_patches_repo_path,
                                             self.repos.salixos_patches_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.salixos_patches_repo_path,
                                             self.repos.salixos_patches_repo_packages)
            self.utils.remove_file_if_exists(self.repos.salixos_patches_repo_path,
                                             self.repos.salixos_patches_repo_checksums)

            changelog: str = f'{self.repos.salixos_patches_repo_mirror[0]}{self.repos.salixos_patches_repo_changelog}'

            if self.repos.salixos_patches_repo_local[0].startswith('file'):
                urls[self.repos.salixos_patches_repo_name] = ((changelog,), self.repos.salixos_patches_repo_path)
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {"".join(self.repos.salixos_patches_repo_mirror)} '
                    f'{self.repos.salixos_patches_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                packages: str = (f'{"".join(self.repos.salixos_patches_repo_mirror)}'
                                 f'{self.repos.salixos_patches_repo_packages}')
                checksums: str = (f'{"".join(self.repos.salixos_patches_repo_mirror)}'
                                  f'{self.repos.salixos_patches_repo_checksums}')

                urls[self.repos.salixos_patches_repo_name] = ((changelog, packages, checksums),
                                                              self.repos.salixos_patches_repo_path)

            self.download.download(urls)
            print()

        self.delete_bin_database_data(self.repos.salixos_patches_repo_name)
        self.delete_last_updated(self.repos.salixos_patches_repo_name)
        self.data.install_salixos_patches_data()

    def slackel_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.slackel_repo_path)

            self.utils.remove_file_if_exists(self.repos.slackel_repo_path, self.repos.slackel_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slackel_repo_path, self.repos.slackel_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slackel_repo_path, self.repos.slackel_repo_checksums)

            if self.repos.slackel_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.slackel_repo_mirror[0]} '
                    f'{self.repos.slackel_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.slackel_repo_mirror[0]}{self.repos.slackel_repo_changelog}'
                packages: str = f'{self.repos.slackel_repo_mirror[0]}{self.repos.slackel_repo_packages}'
                checksums: str = f'{self.repos.slackel_repo_mirror[0]}{self.repos.slackel_repo_checksums}'

                urls[self.repos.slackel_repo_name] = ((changelog, packages, checksums), self.repos.slackel_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.slackel_repo_name)
        self.delete_last_updated(self.repos.slackel_repo_name)
        self.data.install_slackel_data()

    def slint_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.slint_repo_path)

            self.utils.remove_file_if_exists(self.repos.slint_repo_path, self.repos.slint_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slint_repo_path, self.repos.slint_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slint_repo_path, self.repos.slint_repo_checksums)

            if self.repos.slint_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.slint_repo_mirror[0]} '
                    f'{self.repos.slint_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.slint_repo_mirror[0]}{self.repos.slint_repo_changelog}'
                packages: str = f'{self.repos.slint_repo_mirror[0]}{self.repos.slint_repo_packages}'
                checksums: str = f'{self.repos.slint_repo_mirror[0]}{self.repos.slint_repo_checksums}'

                urls[self.repos.slint_repo_name] = ((changelog, packages, checksums), self.repos.slint_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.slint_repo_name)
        self.delete_last_updated(self.repos.slint_repo_name)
        self.data.install_slint_data()

    def pprkut_repository(self) -> None:
        if not self.option_for_install_data:
            urls: dict = {}
            self.utils.create_directory(self.repos.pprkut_repo_path)

            self.utils.remove_file_if_exists(self.repos.pprkut_repo_path, self.repos.pprkut_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.pprkut_repo_path, self.repos.pprkut_repo_packages)
            self.utils.remove_file_if_exists(self.repos.pprkut_repo_path, self.repos.pprkut_repo_checksums)

            if self.repos.pprkut_repo_local[0].startswith('file'):
                lftp_command: str = (
                    f'lftp {self.lftp_mirror_options} {self.repos.pprkut_repo_mirror[0]} '
                    f'{self.repos.pprkut_repo_path}'
                )
                self.utils.process(lftp_command)
            else:
                changelog: str = f'{self.repos.pprkut_repo_mirror[0]}{self.repos.pprkut_repo_changelog}'
                packages: str = f'{self.repos.pprkut_repo_mirror[0]}{self.repos.pprkut_repo_packages}'
                checksums: str = f'{self.repos.pprkut_repo_mirror[0]}{self.repos.pprkut_repo_checksums}'

                urls[self.repos.pprkut_repo_name] = ((changelog, packages, checksums), self.repos.pprkut_repo_path)

                self.download.download(urls)
                print()

        self.delete_bin_database_data(self.repos.pprkut_repo_name)
        self.delete_last_updated(self.repos.pprkut_repo_name)
        self.data.install_pprkut_data()

    def ponce_repository(self) -> None:
        """ Update the slackbuild repositories. """
        if not self.option_for_install_data:
            self.utils.create_directory(self.repos.ponce_repo_path)
            self.utils.remove_file_if_exists(self.repos.ponce_repo_path, self.repos.ponce_repo_slackbuilds)
            self.utils.remove_file_if_exists(self.repos.ponce_repo_path, self.repos.ponce_repo_changelog)

            lftp_command: str = (f'lftp {self.lftp_mirror_options} {self.lftp_exclude} '
                                 f'{self.repos.ponce_repo_mirror[0]} {self.repos.ponce_repo_path}')

            self.utils.process(lftp_command)

        # It checks if there is the SLACKBUILDS.TXT file, otherwise going to create it.
        if not Path(self.repos.ponce_repo_path, self.repos.ponce_repo_slackbuilds).is_file():
            self.generate.slackbuild_file(self.repos.ponce_repo_path, self.repos.ponce_repo_slackbuilds)

        self.delete_last_updated(self.repos.ponce_repo_name)
        self.delete_ponce_database_data()
        self.data.install_ponce_data()

    def sbo_repository(self) -> None:
        if not self.option_for_install_data:
            self.utils.create_directory(self.repos.sbo_repo_path)
            self.utils.remove_file_if_exists(self.repos.sbo_repo_path, self.repos.sbo_repo_slackbuilds)
            self.utils.remove_file_if_exists(self.repos.sbo_repo_path, self.repos.sbo_repo_changelog)

            lftp_command: str = (f'lftp {self.lftp_mirror_options} {self.lftp_exclude} '
                                 f'{self.repos.sbo_repo_mirror[0]} {self.repos.sbo_repo_path}')

            self.utils.process(lftp_command)

        # It checks if there is the SLACKBUILDS.TXT file, otherwise going to create it.
        if not Path(self.repos.sbo_repo_path, self.repos.sbo_repo_slackbuilds).is_file():
            self.generate.slackbuild_file(self.repos.sbo_repo_path, self.repos.sbo_repo_slackbuilds)

        self.delete_last_updated(self.repos.sbo_repo_name)
        self.delete_sbo_database_data()
        self.data.install_sbo_data()

    def check_for_updates(self, queue) -> dict:
        compare: dict = self.check_updates.check_the_repositories()
        self.check_updates.view_messages(compare)

        return queue.put(compare)

    def repositories(self) -> None:
        queue = Queue()
        message: str = 'Checking for news, please wait...'

        # Starting multiprocessing
        process_1 = Process(target=self.check_for_updates, args=(queue,))
        process_2 = Process(target=self.progress.progress_bar, args=(message,))

        process_1.start()
        process_2.start()

        # Wait until process 1 finish
        process_1.join()

        # Terminate process 2 if process 1 finished
        if not process_1.is_alive():
            process_2.terminate()

        # Restore the terminal cursor
        print('\x1b[?25h', self.endc, end='')
        self.repos_for_update: dict = queue.get()
        self.update_the_repositories()

    def delete_sbo_database_data(self) -> None:
        """ Delete all the data from a table of the database. """
        self.session.query(SBoTable).delete()
        self.session.commit()

    def delete_ponce_database_data(self) -> None:
        self.session.query(PonceTable).delete()
        self.session.commit()

    def delete_bin_database_data(self, repo: str) -> None:
        """ Delete the repository data from a table of the database. """
        self.session.query(BinariesTable).where(BinariesTable.repo == repo).delete()
        self.session.commit()

    def delete_last_updated(self, repo: str) -> None:
        """ Deletes the last updated date. """
        self.session.query(LastRepoUpdated).where(LastRepoUpdated.repo == repo).delete()
        self.session.commit()
