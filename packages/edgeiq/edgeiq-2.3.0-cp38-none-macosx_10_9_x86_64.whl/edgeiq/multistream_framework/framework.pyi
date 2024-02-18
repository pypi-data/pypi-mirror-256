from .._utils import gen_logger as gen_logger
from .base_process import BaseProcess as BaseProcess
from .logger import LoggerThread as LoggerThread
from .shared import Shared as Shared
from .utils import MultiprocessAppInterface as MultiprocessAppInterface
from typing import List

class MultiprocessFramework:
    def __init__(self, apps: List[MultiprocessAppInterface], args: List[tuple]) -> None: ...
    def stop(self) -> None: ...
    def start(self) -> None: ...
