import os
import sys

from flask import Blueprint, jsonify, request

from models import Projeto
from models.models import db
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

CONCLUIDO = 4
CANCELADO = 5

projetos = Blueprint('projetos', __name__)


@projetos.route('/projetos', methods=['POST'])
def create_projeto():
    data = request.get_json()
    new_projeto = Projeto(nome=data['nome'], descricao=data['descricao'], cliente_id=data['cliente_id'],
                          status_projeto_id=data['status_projeto_id'])
    db.session.add(new_projeto)
    db.session.commit()
    return jsonify({"id": new_projeto.id, "nome": new_projeto.nome, "descricao": new_projeto.descricao,
                    "cliente_id": new_projeto.cliente_id, "status_projeto_id": new_projeto.status_projeto_id}), 201


@projetos.route('/projetos', methods=['GET'])
def get_projetos():
    projetos_list = Projeto.query.all()
    return jsonify([{"id": projeto.id, "nome": projeto.nome, "descricao": projeto.descricao,
                     "cliente_id": projeto.cliente_id, "status_projeto_id": projeto.status_projeto_id}
                    for projeto in projetos_list])


@projetos.route('/projetos/abertos', methods=['GET'])
def get_projetos_abertos():
    projetos_base_list = Projeto.query.filter(
        Projeto.status_projeto_id != CONCLUIDO and Projeto.status_projeto_id != CANCELADO).all()

    projetos_list = []
    for projeto in projetos_base_list:
        projeto_info = {
            'id': projeto.id,
            'nome': projeto.nome,
            'cliente': projeto.cliente.nome,
            'status': projeto.status_projeto.nome,
            'atividades': [{'id': atividade.id, 'descricao': atividade.descricao} for atividade in projeto.atividades]
        }
        projetos_list.append(projeto_info)

    return jsonify(projetos_list)


@projetos.route('/projetos/<int:projeto_id>', methods=['PUT'])
def update_projeto(projeto_id):
    projeto = db.session.get(Projeto, projeto_id)
    if projeto:
        data = request.get_json()
        projeto.nome = data['nome']
        projeto.descricao = data['descricao']
        projeto.cliente_id = data['cliente_id']
        projeto.status_projeto_id = data['status_projeto_id']
        db.session.commit()
        return jsonify({"id": projeto.id, "nome": projeto.nome, "descricao": projeto.descricao,
                        "cliente_id": projeto.cliente_id, "status_projeto_id": projeto.status_projeto_id})
    return jsonify({"message": "Projeto não encontrado"}), 404


@projetos.route('/projetos/<int:projeto_id>', methods=['DELETE'])
def delete_projeto(projeto_id):
    projeto = db.session.get(Projeto, projeto_id)
    if projeto:
        db.session.delete(projeto)
        db.session.commit()
        return jsonify({"message": "Projeto excluído com sucesso"})
    return jsonify({"message": "Projeto não encontrado"}), 404
