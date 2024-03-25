from pylon.server.create_app import create_app

from pylon_identity.api.routes.routes import add_api_routes

app = create_app(title='Pylon Identity API', add_routes=add_api_routes)


@app.get('/')
def index():
    return {'message': 'Welcome to Pylon Identity API'}
