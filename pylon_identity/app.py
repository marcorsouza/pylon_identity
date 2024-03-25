from fastapi import FastAPI
from pylon.server.create_app import create_app

from pylon_identity.api.admin.routes.routes import add_api_routes
from pylon_identity.api.auth.routes.routes import add_api_auth_routes

app: FastAPI = create_app(
    title='Pylon Identity API', add_routes=add_api_routes
)
add_api_auth_routes(app)


@app.get('/')
def index():
    return {'message': 'Welcome to Pylon Identity API'}
