from fastapi import FastAPI
from pylon.config.helpers import settings
from pylon.server.create_app import create_app
from pylon.utils.file_utils import get_env_file_path

from pylon_identity.config.middlewares import add_api_middlewares
from pylon_identity.config.routes import add_api_routes

app: FastAPI = create_app(
    title=settings.APP_NAME,
    version='0.0.1',
    add_routes=add_api_routes,
    add_middlewares=add_api_middlewares,
)

file_path = get_env_file_path()
print(f'file_path => {file_path}')


@app.get('/')
def index():
    return {'message': 'Welcome to Pylon Identity API'}
