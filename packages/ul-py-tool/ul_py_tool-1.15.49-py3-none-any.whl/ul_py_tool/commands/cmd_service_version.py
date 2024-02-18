import argparse
import os.path
from datetime import datetime
from enum import Enum
from typing import Tuple

from ul_py_tool.commands.cmd import Cmd
from ul_py_tool.utils.arg_file_exists import arg_file_exists
from ul_py_tool.utils.colors import FG_GREEN, NC
from ul_py_tool.utils.step import Stepper
from ul_py_tool.utils.write_stdout import write_stdout


class CmdServiceVersionType(Enum):
    PATCH = 'patch'
    MINOR = 'minor'
    MAJOR = 'major'


class CmdServiceVersion(Cmd):
    service_version_file: str
    type: CmdServiceVersionType

    @staticmethod
    def add_parser_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--service-version-file', dest='service_version_file', type=arg_file_exists, default=os.path.join(os.getcwd(), '.service-version'), required=False)

    def _increase_version(self) -> str:
        write_stdout(f'read "{self.service_version_file}"')
        with open(self.service_version_file, 'rt') as f:
            version = f.read()

        version_segm: Tuple[int, int, int] = tuple(int(v) for v in version.split('.'))  # type: ignore

        if self.type is CmdServiceVersionType.PATCH:
            new_version_segm = (version_segm[0], version_segm[1], version_segm[2] + 1)
            write_stdout(f'{version} -> {new_version_segm[0]}.{new_version_segm[1]}.{FG_GREEN}{new_version_segm[2]}{NC}')
        elif self.type is CmdServiceVersionType.MINOR:
            new_version_segm = (version_segm[0], version_segm[1] + 1, 0)
            write_stdout(f'{version} -> {new_version_segm[0]}.{FG_GREEN}{new_version_segm[1]}.{new_version_segm[2]}{NC}')
        elif self.type is CmdServiceVersionType.MAJOR:
            new_version_segm = (version_segm[0] + 1, 0, 0)
            write_stdout(f'{version} -> {FG_GREEN}{new_version_segm[0]}.{new_version_segm[1]}.{new_version_segm[2]}{NC}')
        else:
            raise NotImplementedError(f'type {self.type} was not implemented for increasing version command')
        new_version = ".".join(str(i) for i in new_version_segm)

        with open(self.service_version_file, 'wt') as f:
            f.write(new_version)
            write_stdout(f'Changes saved to {self.service_version_file}')

        return new_version

    def run(self) -> None:
        stepper = Stepper()

        with stepper.step('INCREASE VERSION', print_error=True):
            new_version = self._increase_version()

        files_to_add = [self.service_version_file]

        with stepper.step('GIT') as stp:
            stp.run_cmd(['git', 'reset'])
            stp.run_cmd(['git', 'add', *files_to_add])
            stp.run_cmd(['git', 'commit', '-m', new_version])
            stp.run_cmd(['git', 'tag', new_version])


class CmdServiceVersionMinor(CmdServiceVersion):
    type: CmdServiceVersionType = CmdServiceVersionType.MINOR


class CmdServiceVersionPatch(CmdServiceVersion):
    type: CmdServiceVersionType = CmdServiceVersionType.PATCH


class CmdServiceVersionMajor(CmdServiceVersion):
    type: CmdServiceVersionType = CmdServiceVersionType.MAJOR
