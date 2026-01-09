from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nodes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

ROOT_NODE_ID = 1