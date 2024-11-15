import pytest
from app import create_app, db

from config import TestConfig


@pytest.fixture
def setup():
    # Cria uma instância do app para testes com a configuração de teste
    app = create_app(config_class=TestConfig)

    # Cria o contexto da aplicação e o banco de dados em memória
    with app.app_context():
        db.create_all()  # Cria as tabelas
        yield app.test_client()  # Retorna o cliente de teste

        db.drop_all()  # Limpa o banco de dados após o teste


def test_create_cliente(setup):
    client = setup
    cliente_data = {
        'nome': 'Novo Cliente',
        'email': 'novocliente@teste.com',
        'telefone': '987654321',
        'cnpj': '98765432000101'
    }

    # Fazendo a requisição POST para criar um cliente
    response = client.post('/clientes', json=cliente_data)

    # Verificando se a resposta foi 201 (Created)
    assert response.status_code == 201

    # Verificando se o cliente foi criado corretamente
    json_data = response.get_json()
    assert json_data['nome'] == cliente_data['nome']
    assert json_data['email'] == cliente_data['email']
    assert json_data['telefone'] == cliente_data['telefone']
    assert json_data['cnpj'] == cliente_data['cnpj']



def test_get_clientes(setup):
    client = setup
    cliente_data = {
        'nome': 'Maria Souza',
        'email': 'maria.souza@email.com',
        'telefone': '987654321',
        'cnpj': '98765432000189'
    }
    client.post('/clientes', json=cliente_data)

    # Requisição GET para listar os clientes
    response = client.get('/clientes')

    # Verificar se o status é 200 OK
    assert response.status_code == 200

    # Verificar se o cliente criado está na resposta
    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]['nome'] == 'Maria Souza'
    assert json_data[0]['email'] == 'maria.souza@email.com'

    cliente_id = json_data[0]['id']

    response = client.get(f'/clientes/{cliente_id}')
    assert response.status_code == 200

def test_get_client_id(setup):
    client = setup
    cliente_data = {
        'nome': 'Maria Souza',
        'email': 'maria.souza@email.com',
        'telefone': '987654321',
        'cnpj': '98765432000189'
    }
    response = client.post('/clientes', json=cliente_data)
    json_data = response.get_json()
    cliente_id = json_data['id']

    response = client.get(f'/clientes/{cliente_id}')
    assert response.status_code == 200

def test_get_client_id_404(setup):
    client = setup
    response = client.get(f'/clientes/{231123}')
    assert response.status_code == 404

def test_update_cliente(setup):
    client = setup
    cliente_data = {
        'nome': 'Carlos Pereira',
        'email': 'carlos.pereira@email.com',
        'telefone': '555555555',
        'cnpj': '55555555000123'
    }
    response = client.post('/clientes', json=cliente_data)
    cliente_id = response.get_json()['id']

    # Dados para atualizar o cliente
    updated_data = {
        'nome': 'Carlos Pereira Silva',
        'email': 'carlos.silva@email.com',
        'telefone': '555555554',
        'cnpj': '55555555000124'
    }

    response = client.put(f'/clientes/{cliente_id}', json=updated_data)

    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['nome'] == 'Carlos Pereira Silva'
    assert json_data['email'] == 'carlos.silva@email.com'

def test_update_cliente_404(setup):
    client = setup
    updated_data = {
        'nome': 'Carlos Pereira Silva',
        'email': 'carlos.silva@email.com',
        'telefone': '555555554',
        'cnpj': '55555555000124'
    }
    response = client.put(f'/clientes/{2222222}', json=updated_data)

    assert response.status_code == 404

def test_delete_cliente(setup):
    client = setup
    cliente_data = {
        'nome': 'Ana Souza',
        'email': 'ana.souza@email.com',
        'telefone': '333333333',
        'cnpj': '33333333000145'
    }
    response = client.post('/clientes', json=cliente_data)
    cliente_id = response.get_json()['id']

    response = client.delete(f'/clientes/{cliente_id}')

    assert response.status_code == 200

def test_delete_cliente_404(setup):
    client = setup
    response = client.delete(f'/clientes/{123123123}')
    assert response.status_code == 404

# Teste da criação de um projeto
def test_create_projeto(setup):
    client = setup
    cliente_data = {
        'nome': 'Carlos Souza',
        'email': 'carlos.souza@email.com',
        'telefone': '555199999',
        'cnpj': '12345000123456'
    }
    cliente_response = client.post('/clientes', json=cliente_data)
    cliente_id = cliente_response.get_json()['id']

    projeto_data = {
        'nome': 'Projeto A',
        'descricao': 'Descrição do Projeto A',
        'status_id': 1,  # Assumindo que o status 1 já existe
        'cliente_id': cliente_id
    }

    response = client.post('/projetos', json=projeto_data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['nome'] == 'Projeto A'
    assert json_data['descricao'] == 'Descrição do Projeto A'


# Teste de listagem de projetos
def test_get_projetos(setup):
    client = setup
    cliente_data = {
        'nome': 'Ana Costa',
        'email': 'ana.costa@email.com',
        'telefone': '999888777',
        'cnpj': '22233344455566'
    }
    cliente_response = client.post('/clientes', json=cliente_data)
    cliente_id = cliente_response.get_json()['id']

    client.post('/projetos', json={
        'nome': 'Projeto B',
        'descricao': 'Descrição do Projeto B',
        'status_id': 2,  # Assumindo que o status 2 já existe
        'cliente_id': cliente_id
    })

    response = client.get('/projetos')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0  # Verifica se há pelo menos um projeto na lista


# Teste para a rota POST /atividades (Criar atividade)
def test_create_atividade(setup):
    client = setup
    cliente_data = {
        'nome': 'Ricardo Martins',
        'email': 'ricardo.martins@email.com',
        'telefone': '123456789',
        'cnpj': '12345678000195'
    }
    cliente_response = client.post('/clientes', json=cliente_data)
    cliente_id = cliente_response.get_json()['id']

    # Criar um projeto antes de criar a atividade
    projeto_data = {
        'nome': 'Projeto X',
        'descricao': 'Projeto de Desenvolvimento de Software',
        'cliente_id': cliente_id,
        'status_projeto_id': 1  # Exemplo de status do projeto
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    # Dados para criar uma nova atividade
    atividade_data = {
        'descricao': 'Análise de Requisitos',
        'projeto_id': projeto_id
    }

    # Requisição POST para criar a atividade
    response = client.post('/atividades', json=atividade_data)

    # Verificar se o status é 201 (Criado)
    assert response.status_code == 201

    # Verificar se a atividade foi criada corretamente
    json_data = response.get_json()
    assert json_data['descricao'] == 'Análise de Requisitos'
    assert json_data['projeto_id'] == projeto_id
    assert 'data' in json_data  # Verificar se a data foi gerada automaticamente


# Teste para a rota GET /atividades (Listar atividades)
def test_get_atividades(setup):
    client = setup
    cliente_data = {
        'nome': 'Ana Souza',
        'email': 'ana.souza@email.com',
        'telefone': '987654321',
        'cnpj': '98765432000189'
    }
    cliente_response = client.post('/clientes', json=cliente_data)
    cliente_id = cliente_response.get_json()['id']

    projeto_data = {
        'nome': 'Projeto Y',
        'descricao': 'Desenvolvimento de Frontend',
        'cliente_id': cliente_id,
        'status_projeto_id': 1  # Exemplo de status do projeto
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    # Criar uma atividade
    atividade_data = {
        'descricao': 'Desenvolvimento da Interface',
        'projeto_id': projeto_id
    }
    client.post('/atividades', json=atividade_data)

    # Requisição GET para listar as atividades
    response = client.get('/atividades')

    # Verificar se o status é 200 OK
    assert response.status_code == 200

    # Verificar se a atividade está na resposta
    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]['descricao'] == 'Desenvolvimento da Interface'


# Teste para a rota PUT /atividades/{id} (Atualizar atividade)
def test_update_atividade(setup):
    client = setup
    cliente_data = {
        'nome': 'João Pereira',
        'email': 'joao.pereira@email.com',
        'telefone': '1122334455',
        'cnpj': '11223344000112'
    }
    cliente_response = client.post('/clientes', json=cliente_data)
    cliente_id = cliente_response.get_json()['id']

    # Criar um projeto antes de criar a atividade
    projeto_data = {
        'nome': 'Projeto Z',
        'descricao': 'Desenvolvimento de API',
        'cliente_id': cliente_id,
        'status_projeto_id': 2  # Exemplo de status do projeto
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    # Criar uma atividade
    atividade_data = {
        'descricao': 'Desenvolvimento da API REST',
        'projeto_id': projeto_id
    }
    atividade_response = client.post('/atividades', json=atividade_data)
    atividade_id = atividade_response.get_json()['id']

    # Dados para atualizar a atividade
    updated_data = {
        'descricao': 'Desenvolvimento da API RESTful'
    }

    # Requisição PUT para atualizar a atividade
    response = client.put(f'/atividades/{atividade_id}', json=updated_data)

    # Verificar se o status é 200 OK
    assert response.status_code == 200

    # Verificar se a atividade foi atualizada corretamente
    json_data = response.get_json()
    assert json_data['descricao'] == 'Desenvolvimento da API RESTful'


# Teste para a rota DELETE /atividades/{id} (Deletar atividade)
def test_delete_atividade(setup):
    client = setup
    cliente_data = {
        'nome': 'Roberta Lima',
        'email': 'roberta.lima@email.com',
        'telefone': '4433221100',
        'cnpj': '44332211000123'
    }
    cliente_response = client.post('/clientes', json=cliente_data)
    cliente_id = cliente_response.get_json()['id']

    # Criar um projeto antes de criar a atividade
    projeto_data = {
        'nome': 'Projeto W',
        'descricao': 'Desenvolvimento de Banco de Dados',
        'cliente_id': cliente_id,
        'status_projeto_id': 3  # Exemplo de status do projeto
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    # Criar uma atividade
    atividade_data = {
        'descricao': 'Modelagem do Banco de Dados',
        'projeto_id': projeto_id
    }
    atividade_response = client.post('/atividades', json=atividade_data)
    atividade_id = atividade_response.get_json()['id']

    # Requisição DELETE para deletar a atividade
    response = client.delete(f'/atividades/{atividade_id}')

    # Verificar se o status é 200 OK
    assert response.status_code == 200

    # Verificar se a atividade foi realmente deletada
    response = client.get(f'/atividades/{atividade_id}')
    assert response.status_code == 404  # A atividade não deve existir mais
