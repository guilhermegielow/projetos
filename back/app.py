import os
import sys

from flask import Flask

from rest.clientes.clientes import clientes
from rest.projetos.projetos import projetos
from rest.atividades.atividades import atividades
from models.models import db
from config import Config
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def create_app(config_class=Config):
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(clientes)
    app.register_blueprint(projetos)
    app.register_blueprint(atividades)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
