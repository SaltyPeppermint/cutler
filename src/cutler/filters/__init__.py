import importlib
import inspect
import pkgutil

by_ref = {}

__all__ = []

# reexport all classes from all child modules

for _info in pkgutil.iter_modules(__path__):
    _module = importlib.import_module(f"{__name__}.{_info.name}")
    for _name, _obj in inspect.getmembers(_module, inspect.isclass):
        if _obj.__module__ == _module.__name__:
            globals()[_name] = _obj
            __all__.append(_name)
            try:
                by_ref[_obj.ref()] = _obj
            except AttributeError:
                pass

del _info, _module, _name, _obj
