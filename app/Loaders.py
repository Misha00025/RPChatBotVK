import inspect
import os
import sys

from app.modules.CharactersModule.CharacterAPI import CharacterAPI
from app.modules.DiceModule import DicesAPI
from app.modules.BaseModule import BaseAPI
from app.modules.NotesModule.NotesAPI import NotesAPI


def auto_load_modules_from(path, is_valid=lambda entity: True):
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

    modules.append(BaseAPI.BaseAPI())
    # modules.append(CharacterAPI())
    modules.append(DicesAPI.DicesAPI())
    modules.append(NotesAPI())

    return modules

def load_commands(modules, is_valid=lambda entity: True) -> [str]:
    commands = []
    for module in modules:
        if is_valid(module):
            commands += module.commands
        else:
            print(f"Модуль '{module}' не предоставляет список команд")
    return commands