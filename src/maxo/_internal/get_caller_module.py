import inspect
import sys
from types import ModuleType


def get_caller_module(stack_offset: int) -> ModuleType:
    return sys.modules[inspect.stack()[stack_offset].frame.f_globals["__name__"]]
