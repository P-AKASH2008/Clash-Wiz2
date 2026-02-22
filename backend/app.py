from backend.extensions import create_app
from backend.routes import register_routes
from backend.config import DEBUG, HOST, PORT

app = create_app()
register_routes(app)

if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)