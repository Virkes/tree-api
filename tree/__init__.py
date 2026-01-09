from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tree.app import app
from tree.db import db

def create_app():
    db.init_app(app)

    from tree.routes import nodes
    app.register_blueprint(nodes)

    return app