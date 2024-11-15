import os
import sys

from flask import Blueprint, jsonify, abort

from models import StatusProjeto
from models.models import db
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

status_projetos = Blueprint('status_projetos', __name__)


@status_projetos.route('/status_projetos', methods=['GET'])
def get_status_projetos():
    status_projetos_list = StatusProjeto.query.all()
    if not status_projetos_list:
        abort(404, description="Status dos Projetos não encontrados")
    return jsonify([{"id": status_projeto.id, "nome": status_projeto.nome}
                    for status_projeto in status_projetos_list])


@status_projetos.route('/status_projetos/<int:status_projeto_id>', methods=['GET'])
def get_status_projeto(status_projeto_id):
    status_projeto = db.session.get(StatusProjeto, status_projeto_id)

    if not status_projeto:
        abort(404, description="Status do projeto não encontrado")

    return jsonify({
        "id": status_projeto.id,
        "nome": status_projeto.nome
    })
