import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import create_app
from config import TestConfig
from models.models import db


@pytest.fixture
def setup():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()
        yield app.test_client()

        db.drop_all()


def test_create_cliente(setup):
    client = setup
    cliente_data = {
        'nome': 'Novo Cliente',
        'email': 'novocliente@teste.com',
        'telefone': '987654321',
        'cnpj': '98765432000101'
    }

    response = client.post('/clientes', json=cliente_data)

    assert response.status_code == 201

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

    response = client.get('/clientes')

    assert response.status_code == 200

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