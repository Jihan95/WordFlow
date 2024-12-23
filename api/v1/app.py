"""Main app"""
from api.v1 import app, bcrypt # type: ignore
from flask import jsonify
from models import storage # type: ignore
from api.v1.views import app_views # type: ignore

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(e):
    """ close the storage """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Custom 404 error page """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = 'localhost'
    port = 5000
    app.run(host=host, port=port, threaded=True, debug=True)
