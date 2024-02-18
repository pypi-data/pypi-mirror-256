#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import logging
from pathlib import Path
from multiprocessing import Process
from urllib3.exceptions import HTTPError
from urllib3 import PoolManager, ProxyManager, make_headers

from slpkg.configs import Configs
from slpkg.repo_info import RepoInfo
from slpkg.utilities import Utilities
from slpkg.progress_bar import ProgressBar
from slpkg.repositories import Repositories
from slpkg.logging_config import LoggingConfig


class CheckUpdates(Configs):
    """ Check for changes in the ChangeLog file. """

    def __init__(self, flags: list, repository: str):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repository: str = repository

        self.utils = Utilities()
        self.progress = ProgressBar()
        self.repos = Repositories()
        self.repo_info = RepoInfo(flags, repository)

        self.compare: dict = {}

        self.http = PoolManager(timeout=self.urllib_timeout)
        self.proxy_default_headers = make_headers(
            proxy_basic_auth=f'{self.proxy_username}:{self.proxy_password}')

        self.is_binary: bool = self.utils.is_binary_repo(repository)

        self.option_for_repository: bool = self.utils.is_option(
            ('-o', '--repository='), flags)

        logging.basicConfig(filename=LoggingConfig.log_file,
                            filemode=LoggingConfig.filemode,
                            encoding=LoggingConfig.encoding,
                            level=LoggingConfig.level)

    def check_the_repositories(self) -> dict:
        if self.option_for_repository:
            self.check_updates_for_repository()
        else:
            self.check_updates_for_repositories()

        return self.compare

    def check_updates_for_repository(self) -> None:
        sbo_repository: dict = {
            self.repos.sbo_repo_name: self.sbo_repository,
            self.repos.ponce_repo_name: self.ponce_repository
        }

        if self.is_binary:
            self.binary_repository(self.repository)
        else:
            sbo_repository[self.repository]()

    def check_updates_for_repositories(self) -> None:
        if self.repos.sbo_repo:
            self.sbo_repository()

        if self.repos.ponce_repo:
            self.ponce_repository()

        for repo in list(self.repos.repositories.keys())[2:]:
            if self.repos.repositories[repo]['enable']:
                self.binary_repository(repo)

    def binary_repository(self, repo: str) -> None:
        local_chg_txt: Path = Path(self.repos.repositories[repo]['path'],
                                   self.repos.repositories[repo]['changelog_txt'])
        repo_chg_txt: str = (f"{self.repos.repositories[repo]['mirror'][0]}"
                             f"{self.repos.repositories[repo]['changelog_txt']}")
        self.compare[repo] = self.compare_the_changelogs(local_chg_txt, repo_chg_txt)

    def sbo_repository(self) -> None:
        local_chg_txt: Path = Path(self.repos.sbo_repo_path, self.repos.sbo_repo_changelog)
        repo_chg_txt: str = f'{self.repos.sbo_repo_mirror[0]}{self.repos.sbo_repo_changelog}'
        self.compare[self.repos.sbo_repo_name] = self.compare_the_changelogs(local_chg_txt, repo_chg_txt)

    def ponce_repository(self) -> None:
        local_chg_txt: Path = Path(self.repos.ponce_repo_path, self.repos.ponce_repo_changelog)
        repo_chg_txt: str = f'{self.repos.ponce_repo_mirror[0]}{self.repos.ponce_repo_changelog}'
        self.compare[self.repos.ponce_repo_name] = self.compare_the_changelogs(local_chg_txt, repo_chg_txt)

    def compare_the_changelogs(self, local_chg_txt: Path, repo_chg_txt: str) -> bool:
        local_size: int = 0
        repo_size: int = 0

        if self.proxy_address.startswith('http'):
            self.set_http_proxy_server()

        if self.proxy_address.startswith('socks'):
            self.set_socks_proxy_server()

        # Get local changelog file size.
        if local_chg_txt.is_file():
            local_size: int = int(os.stat(local_chg_txt).st_size)

        try:  # Get repository changelog file size.
            repo = self.http.request(
                'GET', repo_chg_txt,
                retries=self.urllib_retries,
                redirect=self.urllib_redirect
            )
            repo_size: int = int(repo.headers.get('content-length', 0))
        except KeyboardInterrupt:
            raise SystemExit(1)
        except HTTPError:
            self.error_connect_message(repo_chg_txt)

        # Return False if repository changelog file size failed to get a value.
        if repo_size == 0:
            return False

        logger = logging.getLogger(LoggingConfig.date_time)
        logger.info(f'{self.__class__.__name__}: '
                    f'{self.__class__.compare_the_changelogs.__name__}: '
                    f'{local_chg_txt=}, {local_size=}, '
                    f'{repo_chg_txt=}, {repo_size=}, '
                    f'{local_size != repo_size}')

        return local_size != repo_size

    def error_connect_message(self, repo_chg_txt: str) -> None:
        print(f'\n\n{self.endc}{self.prog_name}: {self.bred}Error:{self.endc} '
              f'Failed to connect to {repo_chg_txt}\n')

    def set_http_proxy_server(self) -> None:
        self.http = ProxyManager(f'{self.proxy_address}', headers=self.proxy_default_headers)

    def set_socks_proxy_server(self) -> None:
        try:  # Try to import PySocks if it's installed.
            from urllib3.contrib.socks import SOCKSProxyManager
        except (ModuleNotFoundError, ImportError) as error:
            print(error)
        # https://urllib3.readthedocs.io/en/stable/advanced-usage.html#socks-proxies
        self.http = SOCKSProxyManager(f'{self.proxy_address}', headers=self.proxy_default_headers)

    def check_for_updates(self) -> None:
        self.check_the_repositories()
        self.view_messages(self.compare)

    def view_messages(self, compare: dict) -> None:
        print()
        repo_for_update: list = []
        for repo, comp in compare.items():
            if comp:
                repo_for_update.append(repo)

        if repo_for_update:
            print(f"\n{self.endc}There are new updates available for the "
                  f"repositories: \n")
            for repo in repo_for_update:
                repo_length: int = max(len(name) for name in repo_for_update)
                print(f'> {self.bgreen}{repo:<{repo_length}}{self.endc} Last Updated: '
                      f"'{self.repo_info.last_repository_updated(repo)}'")
        else:
            print(f'\n{self.endc}{self.yellow}No updated packages since the last check.{self.endc}')

    def updates(self) -> None:
        message: str = 'Checking for news, please wait...'

        # Starting multiprocessing
        process_1 = Process(target=self.check_for_updates)
        process_2 = Process(target=self.progress.progress_bar, args=(message,))

        process_1.start()
        process_2.start()

        # Wait until process 1 finish
        process_1.join()

        # Terminate process 2 if process 1 finished
        if not process_1.is_alive():
            process_2.terminate()

        # Restore the terminal cursor
        print('\x1b[?25h', self.endc)
