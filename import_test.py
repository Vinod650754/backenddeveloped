import importlib, traceback, sys

try:
    m = importlib.import_module('app')
    print('IMPORT_OK', getattr(m, '__file__', None))
except Exception:
    traceback.print_exc()
    sys.exit(1)
