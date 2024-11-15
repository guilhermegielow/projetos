import os
import sys

from flask import Blueprint, jsonify, request, abort

from models import Atividade
from models.models import db
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

atividades = Blueprint('atividades', __name__)


@atividades.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()
    new_atividade = Atividade(
        projeto_id=data['projeto_id'],
        descricao=data['descricao']
    )
    db.session.add(new_atividade)
    db.session.commit()
    return jsonify({"id": new_atividade.id, "projeto_id": new_atividade.projeto_id,
                    "descricao": new_atividade.descricao, "data": new_atividade.data}), 201


@atividades.route('/atividades', methods=['GET'])
def get_atividades():
    atividades_list = Atividade.query.all()
    return jsonify([{
        "id": atividade.id,
        "projeto_id": atividade.projeto_id,
        "descricao": atividade.descricao,
        "data": atividade.data
    } for atividade in atividades_list])


@atividades.route('/atividades/<int:atividade_id>', methods=['GET'])
def get_atividade(atividade_id):
    atividade = db.session.get(Atividade, atividade_id)

    if not atividade:
        abort(404, description="Atividade não encontrado")

    return jsonify({
        "id": atividade.id,
        "descricao": atividade.descricao,
        "data": atividade.data,
        "projeto_id": atividade.projeto_id
    })


@atividades.route('/atividades/<int:atividade_id>', methods=['PUT'])
def update_atividade(atividade_id):
    atividade = db.session.get(Atividade, atividade_id)
    if atividade:
        data = request.get_json()
        atividade.descricao = data['descricao']
        atividade.projeto_id = data['projeto_id']
        db.session.commit()
        return jsonify({"id": atividade.id, "descricao": atividade.descricao, "projeto_id": atividade.projeto_id})
    return jsonify({"message": "Atividade não encontrada"}), 404


@atividades.route('/atividades/<int:atividade_id>', methods=['DELETE'])
def delete_atividade(atividade_id):
    atividade = db.session.get(Atividade, atividade_id)
    if atividade:
        db.session.delete(atividade)
        db.session.commit()
        return jsonify({"message": "Atividade excluída com sucesso"})
    return jsonify({"message": "Atividade não encontrada"}), 404
