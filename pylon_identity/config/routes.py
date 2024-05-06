import os

from fastapi import FastAPI
from pylon.api.routes.do_login_routes import (  # Import roteador de Hearth Check
    do_login_router,
)
from pylon.api.routes.health_check_routes import (  # Import roteador de Hearth Check
    check_router,
)
from pylon.api.routes.log_routes import log_router  # Import roteador de logs
from pylon.config.helpers import settings
from pylon.utils.file_utils import (
    get_attribute,
    get_filename,
    get_files,
    get_import_module,
)


def _load_and_register_routers(app: FastAPI):
    list_modules = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navega até a raiz do projeto (supondo que a raiz seja o diretório pai do diretório do script)
    root_dir = os.path.dirname(script_dir)
    for file in get_files(root_dir, '_routes.py', True):
        filename = get_filename(file)[0]
        module_base = file.replace(os.path.sep, '.')
        module_name = module_base[:-3]
        posicao_api = module_name.rfind('api.')
        module_name = module_name[posicao_api:]
        module = get_import_module(
            f'{settings.APPLICATION_FOLDER}.{module_name}'
        )     # importlib.import_module(module_name)
        router = get_attribute(
            module, filename
        )   # getattr(obj, attr, default)
        app.include_router(router)
        list_modules.append(module)


def add_api_routes(app: FastAPI):
    _load_and_register_routers(app=app)
    app.include_router(log_router)
    app.include_router(check_router)
    app.include_router(do_login_router)
