from fastapi import FastAPI
from pylon.api.routes.log_routes import log_router  # Import roteador de logs

from pylon_identity.api.admin.routes.application_routes import (  # Import roteador de aplicações
    application_router,
)
from pylon_identity.api.admin.routes.role_routes import (  # Import roteador de regras
    role_router,
)
from pylon_identity.api.admin.routes.task_routes import (  # Import roteador de tarefas
    task_router,
)
from pylon_identity.api.admin.routes.user_routes import (  # Import roteador de usuarios
    user_router,
)

"""
def add_api_routes2(app: FastAPI):
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
     # Navega até a raiz do projeto (supondo que a raiz seja o diretório pai do diretório do script)
    root_dir = os.path.dirname(script_dir)
    
    for file in get_files(os.path.join(root_dir, api_folder), '_routes.py', True):
    
    # Lista todos os arquivos no diretório de rotas
    for file in os.listdir(routes_directory):
        if file.endswith("_routes.py"):  # Filtra por arquivos de rotas
            module_name = file[:-3]  # Remove a extensão '.py'
            module_path = f"{base_import_path}.{module_name}"
            module = importlib.import_module(module_path)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, "include_router"):
                    # Assume que o objeto tem um método 'include_router'
                    app.include_router(attr)
"""


def add_api_routes(app: FastAPI):
    app.include_router(user_router)
    app.include_router(application_router)
    app.include_router(role_router)
    app.include_router(task_router)
    app.include_router(log_router)
