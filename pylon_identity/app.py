from pylon.server.create_app import create_app

app = create_app(title='Pylon Identity API')


@app.get('/')
def index():
    return {'message': 'Welcome to Pylon Identity API'}
