import pkgutil
import importlib

# iterate all modules under app.models package
for module in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{module.name}")
