import os
import sys

from flask import Blueprint, jsonify, request, abort

from models import Atividade
from models.models import db
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

atividades = Blueprint('atividades', __name__)


@atividades.route('/atividades', methods=['POST'])
def create_atividade():
    try:
        data = request.get_json()
        new_atividade = Atividade(
            projeto_id=data['projeto_id'],
            descricao=data['descricao']
        )
        db.session.add(new_atividade)
        db.session.commit()
        return jsonify({"id": new_atividade.id, "projeto_id": new_atividade.projeto_id,
                        "descricao": new_atividade.descricao, "data": new_atividade.data}), 201
    except Exception as e:
        abort(400, description=str(e))


@atividades.route('/atividades', methods=['GET'])
def get_atividades():
    try:
        atividades_list = Atividade.query.all()

        if not atividades_list:
            abort(404, description="Atividades não encontradas")

        return jsonify([{
            "id": atividade.id,
            "projeto_id": atividade.projeto_id,
            "cliente_id": atividade.projeto.cliente_id,
            "projeto_nome": atividade.projeto.nome,
            "cliente_nome": atividade.projeto.cliente.nome,
            "descricao": atividade.descricao,
            "data": atividade.data
        } for atividade in atividades_list])
    except Exception as e:
        abort(400, description=str(e))


@atividades.route('/atividades/<int:atividade_id>', methods=['GET'])
def get_atividade(atividade_id):
    try:
        atividade = db.session.get(Atividade, atividade_id)

        if not atividade:
            abort(404, description="Atividade não encontrada")

        return jsonify({
            "id": atividade.id,
            "descricao": atividade.descricao,
            "data": atividade.data,
            "projeto_id": atividade.projeto_id
        })
    except Exception as e:
        abort(400, description=str(e))


@atividades.route('/atividades/<int:atividade_id>', methods=['PUT'])
def update_atividade(atividade_id):
    try:
        atividade = db.session.get(Atividade, atividade_id)
        if atividade:
            data = request.get_json()
            atividade.descricao = data['descricao']
            atividade.projeto_id = data['projeto_id']
            db.session.commit()
            return jsonify({"id": atividade.id, "descricao": atividade.descricao, "projeto_id": atividade.projeto_id})
        return jsonify({"message": "Atividade não encontrada"}), 404
    except Exception as e:
        abort(400, description=str(e))


@atividades.route('/atividades/<int:atividade_id>', methods=['DELETE'])
def delete_atividade(atividade_id):
    try:
        atividade = db.session.get(Atividade, atividade_id)
        if atividade:
            db.session.delete(atividade)
            db.session.commit()
            return jsonify({"message": "Atividade excluída com sucesso"})
        return jsonify({"message": "Atividade não encontrada"}), 404
    except Exception as e:
        abort(400, description=str(e))
