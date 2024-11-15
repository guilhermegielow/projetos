from flask import Flask, jsonify, request, abort
from models import db, Cliente, Projeto, Atividade
from config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    # Cria a instância do app Flask
    app = Flask(__name__)

    # Habilita CORS (Cross-Origin Resource Sharing)
    CORS(app)

    # Carrega a configuração a partir da classe fornecida (por padrão é Config)
    app.config.from_object(config_class)

    # Inicializa o banco de dados com a configuração do app
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

    @app.route('/clientes/<int:id>', methods=['GET'])
    def get_cliente(id):
        # Consulta o cliente pelo id
        cliente = Cliente.query.get(id)

        # Verifica se o cliente existe
        if not cliente:
            abort(404, description="Cliente não encontrado")

        # Retorna os dados do cliente em formato JSON
        return jsonify({
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "cnpj": cliente.cnpj
        })

    @app.route('/clientes/<int:id>', methods=['PUT'])
    def update_cliente(id):
        cliente = Cliente.query.get(id)
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

    @app.route('/clientes/<int:id>', methods=['DELETE'])
    def delete_cliente(id):
        cliente = Cliente.query.get(id)
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

    @app.route('/projetos/<int:id>', methods=['PUT'])
    def update_projeto(id):
        projeto = Projeto.query.get(id)
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

    @app.route('/projetos/<int:id>', methods=['DELETE'])
    def delete_projeto(id):
        projeto = Projeto.query.get(id)
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
                        "descricao": new_atividade.descricao, "data": new_atividade.data }), 201

    @app.route('/atividades', methods=['GET'])
    def get_atividades():
        atividades = Atividade.query.all()
        return jsonify([{
            "id": atividade.id,
            "projeto_id": atividade.projeto_id,
            "descricao": atividade.descricao,
            "data": atividade.data
        } for atividade in atividades])

    @app.route('/atividades/<int:id>', methods=['GET'])
    def get_atividade(id):
        # Consulta o cliente pelo id
        atividade = Atividade.query.get(id)

        # Verifica se o cliente existe
        if not atividade:
            abort(404, description="Atividade não encontrado")

        # Retorna os dados do cliente em formato JSON
        return jsonify({
            "id": atividade.id,
            "descricao": atividade.descricao,
            "data": atividade.data,
            "projeto_id": atividade.projeto_id
        })

    @app.route('/atividades/<int:id>', methods=['PUT'])
    def update_atividade(id):
        atividade = Atividade.query.get(id)
        if atividade:
            data = request.get_json()
            atividade.descricao = data['descricao']
            atividade.projeto_id = data['projeto_id']
            db.session.commit()
            return jsonify({"id": atividade.id, "descricao": atividade.descricao, "projeto_id": atividade.projeto_id})
        return jsonify({"message": "Atividade não encontrada"}), 404

    @app.route('/atividades/<int:id>', methods=['DELETE'])
    def delete_atividade(id):
        atividade = Atividade.query.get(id)
        if atividade:
            db.session.delete(atividade)
            db.session.commit()
            return jsonify({"message": "Atividade excluída com sucesso"})
        return jsonify({"message": "Atividade não encontrada"}), 404

    # Retorna o app configurado
    return app

if __name__ == '__main__':
    app = create_app()  # Cria o app com a configuração padrão (Config)
    app.run(debug=True)  # Roda o servidor Flask com o modo de debug ativado)