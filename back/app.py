import os
import sys

from flask import Flask, jsonify, request, abort

from models import Cliente
from models.models import db, Atividade, Projeto
from config import Config
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def create_app(config_class=Config):
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config_class)

    db.init_app(app)

    @app.route('/clientes', methods=['POST'])
    def create_cliente():
        data = request.get_json()
        new_cliente = Cliente(nome=data['nome'], email=data['email'], telefone=data['telefone'], cnpj=data['cnpj'])
        db.session.add(new_cliente)
        db.session.commit()
        return jsonify({"id": new_cliente.id, "nome": new_cliente.nome, "email": new_cliente.email,
                        "telefone": new_cliente.telefone, "cnpj": new_cliente.cnpj}), 201

    @app.route('/clientes', methods=['GET'])
    def get_clientes():
        clientes = Cliente.query.all()
        return jsonify([{"id": cliente.id, "nome": cliente.nome, "email": cliente.email, "telefone": cliente.telefone,
                         "cnpj": cliente.cnpj}
                        for cliente in clientes])

    @app.route('/clientes/<int:cliente_id>', methods=['GET'])
    def get_cliente(cliente_id):
        cliente = Cliente.query.get(cliente_id)

        if not cliente:
            abort(404, description="Cliente não encontrado")

        return jsonify({
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "cnpj": cliente.cnpj
        })

    @app.route('/clientes/<int:cliente_id>', methods=['PUT'])
    def update_cliente(cliente_id):
        cliente = Cliente.query.get(cliente_id)
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

    @app.route('/clientes/<int:cliente_id>', methods=['DELETE'])
    def delete_cliente(cliente_id):
        cliente = Cliente.query.get(cliente_id)
        if cliente:
            db.session.delete(cliente)
            db.session.commit()
            return jsonify({"message": "Cliente excluído com sucesso"})
        return jsonify({"message": "Cliente não encontrado"}), 404

    @app.route('/projetos', methods=['POST'])
    def create_projeto():
        data = request.get_json()
        new_projeto = Projeto(nome=data['nome'], descricao=data['descricao'], cliente_id=data['cliente_id'],
                              status_projeto_id=data['status_projeto_id'])
        db.session.add(new_projeto)
        db.session.commit()
        return jsonify({"id": new_projeto.id, "nome": new_projeto.nome, "descricao": new_projeto.descricao,
                        "cliente_id": new_projeto.cliente_id, "status_projeto_id": new_projeto.status_projeto_id}), 201

    @app.route('/projetos', methods=['GET'])
    def get_projetos():
        projetos = Projeto.query.all()
        return jsonify([{"id": projeto.id, "nome": projeto.nome, "descricao": projeto.descricao,
                         "cliente_id": projeto.cliente_id, "status_projeto_id": projeto.status_projeto_id}
                        for projeto in projetos])

    @app.route('/projetos/<int:projeto_id>', methods=['PUT'])
    def update_projeto(projeto_id):
        projeto = Projeto.query.get(projeto_id)
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

    @app.route('/projetos/<int:projeto_id>', methods=['DELETE'])
    def delete_projeto(projeto_id):
        projeto = Projeto.query.get(projeto_id)
        if projeto:
            db.session.delete(projeto)
            db.session.commit()
            return jsonify({"message": "Projeto excluído com sucesso"})
        return jsonify({"message": "Projeto não encontrado"}), 404

    @app.route('/atividades', methods=['POST'])
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

    @app.route('/atividades', methods=['GET'])
    def get_atividades():
        atividades = Atividade.query.all()
        return jsonify([{
            "id": atividade.id,
            "projeto_id": atividade.projeto_id,
            "descricao": atividade.descricao,
            "data": atividade.data
        } for atividade in atividades])

    @app.route('/atividades/<int:atividade_id>', methods=['GET'])
    def get_atividade(atividade_id):
        atividade = Atividade.query.get(atividade_id)

        if not atividade:
            abort(404, description="Atividade não encontrado")

        return jsonify({
            "id": atividade.id,
            "descricao": atividade.descricao,
            "data": atividade.data,
            "projeto_id": atividade.projeto_id
        })

    @app.route('/atividades/<int:atividade_id>', methods=['PUT'])
    def update_atividade(atividade_id):
        atividade = Atividade.query.get(atividade_id)
        if atividade:
            data = request.get_json()
            atividade.descricao = data['descricao']
            atividade.projeto_id = data['projeto_id']
            db.session.commit()
            return jsonify({"id": atividade.id, "descricao": atividade.descricao, "projeto_id": atividade.projeto_id})
        return jsonify({"message": "Atividade não encontrada"}), 404

    @app.route('/atividades/<int:atividade_id>', methods=['DELETE'])
    def delete_atividade(atividade_id):
        atividade = Atividade.query.get(atividade_id)
        if atividade:
            db.session.delete(atividade)
            db.session.commit()
            return jsonify({"message": "Atividade excluída com sucesso"})
        return jsonify({"message": "Atividade não encontrada"}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
