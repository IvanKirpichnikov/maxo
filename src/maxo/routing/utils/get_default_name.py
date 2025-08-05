from maxo._internal.get_caller_module import get_caller_module


def get_router_default_name() -> str:
    return get_caller_module(2).__name__
