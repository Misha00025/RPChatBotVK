import inspect
import os
import sys

from app.modules.DiceModule.DicesAPI import DicesAPI
from app.modules.BaseModule.BaseAPI import BaseAPI
from app.modules.NotesModule.NotesAPI import NotesAPI
from app.modules.LocationsModule.LocationsAPI import LocationsAPI
from app.modules.AliasModule.AliasAPI import AliasAPI


def auto_load_modules_from(path, is_valid):
    """
    Import all modules from the given directory
    """
    if path[-1:] != '/':
        path += '/'
    if not os.path.exists(path):
        raise OSError("Directory does not exist: %s" % path)
    modules = []
    for f in os.listdir(path):
        # Ignore anything that isn't a .py file
        if len(f) > 3 and f[-3:] == '.py':
            modname = f[:-3]
            modpath = path[:-1] + "." + f[:-3]
            # Import the module
            __import__(modpath, globals(), locals(), [f'{modname}'])
            for name, obj in inspect.getmembers(sys.modules[modpath]):
                if inspect.isclass(obj) and name == modname:
                    module = obj()
                    if is_valid(module):
                        modules.append(module)
    return modules

def load_modules(is_valid=lambda entity: True):
    modules = []

    # modules.append(BaseAPI())
    # modules.append(CharacterAPI())
    modules.append(DicesAPI())
    modules.append(NotesAPI())
    modules.append(LocationsAPI())
    modules.append(AliasAPI())

    return modules

def load_commands(modules, is_valid=lambda entity: True) -> list:
    commands = []
    for module in modules:
        if is_valid(module):
            commands += module.commands
        else:
            print(f"Модуль '{module}' не предоставляет список команд")
    return commands

