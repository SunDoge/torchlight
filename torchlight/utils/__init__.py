import importlib


def import_function(name: str):
    module_name, function_name = name.rsplit(sep='.', maxsplit=1)
    return getattr(importlib.import_module(module_name), function_name)
