from ast import ast
from object import object
from typing import List, Dict, Tuple


class EnvironmentEnclosed:
    def __init__(self):
        self.store: Dict[str, object.Object] = {}

    def get(self, name: str) -> Tuple[object.Object, bool]:
        obj = self.store.get(name, 'error')
        if obj != 'error':
            return obj, True
        else:
            return object.Object(), False

    def set(self, name: str, val: object.Object):
        self.store[name] = val
        return val


class Environment:
    def __init__(self, outer: EnvironmentEnclosed):
        self.store: Dict[str, object.Object] = {}
        self.outer = outer

    def get(self, name: str) -> Tuple[object.Object, bool]:
        obj = self.store.get(name, 'error')
        if obj == 'error' and self.outer is not None:
            obj, ok = self.outer.get(name)
            return obj, ok
        elif obj != 'error':
            return obj, True
        else:
            return object.Object(), False

    def set(self, name: str, val: object.Object):
        self.store[name] = val
        return val


def new_environment() -> Environment:
    return Environment(outer=None)


def new_enclosed_environment(outer: EnvironmentEnclosed) -> Environment:
    env = new_environment()
    env.outer = outer
    return env
