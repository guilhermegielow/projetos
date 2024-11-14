from flask import Flask, jsonify, request
from models import db, Cliente, Projeto, Atividade
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
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
        return jsonify({"id": cliente.id, "nome": cliente.nome, "email": cliente.email, "telefone": cliente.telefone,
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
    new_projeto = Projeto(nome=data['nome'])
    db.session.add(new_projeto)
    db.session.commit()
    return jsonify({"id": new_projeto.id, "nome": new_projeto.nome}), 201

@app.route('/projetos', methods=['GET'])
def get_projetos():
    projetos = Projeto.query.all()
    return jsonify([{"id": projeto.id, "nome": projeto.nome} for projeto in projetos])

@app.route('/projetos/<int:id>', methods=['PUT'])
def update_projeto(id):
    projeto = Projeto.query.get(id)
    if projeto:
        data = request.get_json()
        projeto.nome = data['nome']
        db.session.commit()
        return jsonify({"id": projeto.id, "nome": projeto.nome})
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
        cliente_id=data['clienteId'],
        projeto_id=data['projetoId'],
        descricao=data['descricao']
    )
    db.session.add(new_atividade)
    db.session.commit()
    return jsonify({"id": new_atividade.id, "clienteId": new_atividade.cliente_id,
                    "projetoId": new_atividade.projeto_id, "descricao": new_atividade.descricao}), 201

@app.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = Atividade.query.all()
    return jsonify([{
        "id": atividade.id,
        "clienteId": atividade.cliente_id,
        "projetoId": atividade.projeto_id,
        "descricao": atividade.descricao
    } for atividade in atividades])

@app.route('/atividades/<int:id>', methods=['PUT'])
def update_atividade(id):
    atividade = Atividade.query.get(id)
    if atividade:
        data = request.get_json()
        atividade.descricao = data['descricao']
        atividade.cliente_id = data['clienteId']
        atividade.projeto_id = data['projetoId']
        db.session.commit()
        return jsonify({"id": atividade.id, "descricao": atividade.descricao,
                        "clienteId": atividade.cliente_id, "projetoId": atividade.projeto_id})
    return jsonify({"message": "Atividade não encontrada"}), 404

@app.route('/atividades/<int:id>', methods=['DELETE'])
def delete_atividade(id):
    atividade = Atividade.query.get(id)
    if atividade:
        db.session.delete(atividade)
        db.session.commit()
        return jsonify({"message": "Atividade excluída com sucesso"})
    return jsonify({"message": "Atividade não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)