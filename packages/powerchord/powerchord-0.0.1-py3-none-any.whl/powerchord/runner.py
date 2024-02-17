import asyncio
import sys
import tomllib
from abc import ABC, abstractmethod
from pathlib import Path
from subprocess import PIPE

from .formatting import bright, dim, status

TaskResult = tuple[str, bool, tuple[bytes, bytes]]


class BoredomError(Exception):
    pass


class ConfigError(Exception, ABC):
    def __init__(self, config_file: Path):
        self.config_file = config_file

    @property
    @abstractmethod
    def message(self):
        pass


class PyprojectConfigError(ConfigError):
    def __init__(self, config_file: Path):
        super().__init__(config_file)

    @property
    def message(self):
        return (
            f'💀 Could not find [tool.powerchord(.*)] config in {self.config_file}.\n'
            'Currently no other configuration methods are supported.'
        )


class FailedTasksError(Exception):
    def __init__(self, failed_tasks: list[str]):
        self.failed_tasks = failed_tasks


class TaskRunner:
    def __init__(self, tasks: dict[str, str] = None, verbose: bool = False):
        if not tasks:
            raise BoredomError
        self.tasks = tasks
        self.verbose = verbose

    @classmethod
    def with_pyproject_config(cls) -> 'TaskRunner':
        pyproject_file = Path('pyproject.toml')
        try:
            with pyproject_file.open('rb') as f:
                config = tomllib.load(f).get('tool', {}).get('powerchord', {})
        except OSError:
            config = {}
        if not config:
            raise PyprojectConfigError(pyproject_file)
        return cls(**config)

    def run_tasks(self) -> None:
        results = asyncio.run(self.exec_tasks())
        for name, success, (out, err) in results:
            if (out or err) and (self.verbose or not success):
                sys.stdout.write(f'\n{status(success)} {bright(name)} report:\n')
                sys.stdout.buffer.write(out)
                sys.stdout.buffer.flush()
                sys.stderr.buffer.write(err)
                sys.stderr.buffer.flush()
        failed_tasks = [name for name, success, _ in results if not success]
        if failed_tasks:
            raise FailedTasksError(failed_tasks)

    async def exec_tasks(self) -> list[TaskResult]:
        sys.stdout.write(bright('To do:\n'))
        for name, task in self.tasks.items():
            sys.stdout.write(f'• {name}: {dim(task)}\n')
        sys.stdout.write(bright('\nResults:\n'))
        return list(await asyncio.gather(*(
            self.exec_task(name, task) for name, task in self.tasks.items()
        )))

    @staticmethod
    async def exec_task(name: str, task: str) -> TaskResult:
        proc = await asyncio.create_subprocess_shell(task, stdout=PIPE, stderr=PIPE)
        out_err = await proc.communicate()
        success = proc.returncode == 0
        sys.stdout.write(f'{status(success)} {name}\n')
        return name, success, out_err


def run_tasks() -> None:
    try:
        TaskRunner.with_pyproject_config().run_tasks()
    except ConfigError as exc:
        sys.exit(exc.message)
    except BoredomError:
        sys.stdout.write('Nothing to do. Getting bored...\n')
    except FailedTasksError as exc:
        sys.exit(f'\n💀 {bright("Failed tasks:")} {", ".join(exc.failed_tasks)}')
