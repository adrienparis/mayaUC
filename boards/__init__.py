import sys
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

from . import *

import importlib

i = 0
for name in __all__:
    
    mod = importlib.import_module(name)
    importlib.reload(mod)
    print("reload " + module)
    reload( __all__[i] )
    i += 1