import os
import sys

from flask import Blueprint, jsonify, request, abort

from models import Cliente
from models.models import db
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

clientes = Blueprint('clientes', __name__)


@clientes.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    new_cliente = Cliente(nome=data['nome'], email=data['email'], telefone=data['telefone'], cnpj=data['cnpj'])
    db.session.add(new_cliente)
    db.session.commit()
    return jsonify({"id": new_cliente.id, "nome": new_cliente.nome, "email": new_cliente.email,
                    "telefone": new_cliente.telefone, "cnpj": new_cliente.cnpj}), 201


@clientes.route('/clientes', methods=['GET'])
def get_clientes():
    clientes_list = Cliente.query.all()
    return jsonify([{"id": cliente.id, "nome": cliente.nome, "email": cliente.email, "telefone": cliente.telefone,
                     "cnpj": cliente.cnpj}
                    for cliente in clientes_list])


@clientes.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    cliente = db.session.get(Cliente, cliente_id)

    if not cliente:
        abort(404, description="Cliente não encontrado")

    return jsonify({
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
        "cnpj": cliente.cnpj
    })


@clientes.route('/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    cliente = db.session.get(Cliente, cliente_id)
    if cliente:
        data = request.get_json()
        cliente.nome = data['nome']
        cliente.telefone = data['telefone']
        cliente.email = data['email']
        cliente.cnpj = data['cnpj']
        db.session.commit()
        return jsonify(
            {"id": cliente.id, "nome": cliente.nome, "email": cliente.email, "telefone": cliente.telefone,
             "cnpj": cliente.cnpj})
    return jsonify({"message": "Cliente não encontrado"}), 404


@clientes.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    cliente = db.session.get(Cliente, cliente_id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({"message": "Cliente excluído com sucesso"})
    return jsonify({"message": "Cliente não encontrado"}), 404
