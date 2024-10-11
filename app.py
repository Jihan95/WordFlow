"""Main app"""
from __init__ import app, bcrypt # type: ignore

@app.route("/")
def home_page():
    """Home Page"""
    return "Welcome to WordFlow!"