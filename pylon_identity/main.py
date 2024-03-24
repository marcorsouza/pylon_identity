import uvicorn
from pylon.server.create_app import create_app

app = create_app(title='Pylon Identity API')


@app.get('/')
def index():
    return {'message': 'Welcome to Pylon Identity API'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
