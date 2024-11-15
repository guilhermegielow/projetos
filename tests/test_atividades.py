import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'back')))

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

    projeto_data = {
        'nome': 'Projeto X',
        'descricao': 'Projeto de Desenvolvimento de Software',
        'cliente_id': cliente_id,
        'status_projeto_id': 1
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    atividade_data = {
        'descricao': 'Análise de Requisitos',
        'projeto_id': projeto_id
    }

    response = client.post('/atividades', json=atividade_data)

    assert response.status_code == 201

    json_data = response.get_json()
    assert json_data['descricao'] == 'Análise de Requisitos'
    assert json_data['projeto_id'] == projeto_id
    assert 'data' in json_data


def test_get_atividade_id(setup):
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
        'status_projeto_id': 1
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    # Dados para criar uma nova atividade
    atividade_data = {
        'descricao': 'Análise de Requisitos',
        'projeto_id': projeto_id
    }

    response = client.post('/atividades', json=atividade_data)
    atividade_id = response.get_json()['id']

    response = client.get(f'/atividades/{atividade_id}')
    assert response.status_code == 200


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
        'status_projeto_id': 1
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    atividade_data = {
        'descricao': 'Desenvolvimento da Interface',
        'projeto_id': projeto_id
    }
    client.post('/atividades', json=atividade_data)

    response = client.get('/atividades')

    assert response.status_code == 200

    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]['descricao'] == 'Desenvolvimento da Interface'


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

    projeto_data = {
        'nome': 'Projeto Z',
        'descricao': 'Desenvolvimento de API',
        'cliente_id': cliente_id,
        'status_projeto_id': 2
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    atividade_data = {
        'descricao': 'Desenvolvimento da API REST',
        'projeto_id': projeto_id
    }
    atividade_response = client.post('/atividades', json=atividade_data)
    atividade_id = atividade_response.get_json()['id']

    updated_data = {
        'descricao': 'Desenvolvimento da API RESTful',
        'projeto_id': projeto_id
    }

    response = client.put(f'/atividades/{atividade_id}', json=updated_data)

    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['descricao'] == 'Desenvolvimento da API RESTful'


def test_update_atividade_404(setup):
    client = setup
    updated_data = {
        'descricao': 'Desenvolvimento da API RESTful',
        'projeto_id': 1
    }
    response = client.put(f'/atividades/{2222222}', json=updated_data)

    assert response.status_code == 404


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

    projeto_data = {
        'nome': 'Projeto W',
        'descricao': 'Desenvolvimento de Banco de Dados',
        'cliente_id': cliente_id,
        'status_projeto_id': 3
    }
    projeto_response = client.post('/projetos', json=projeto_data)
    projeto_id = projeto_response.get_json()['id']

    atividade_data = {
        'descricao': 'Modelagem do Banco de Dados',
        'projeto_id': projeto_id
    }
    atividade_response = client.post('/atividades', json=atividade_data)
    atividade_id = atividade_response.get_json()['id']

    response = client.delete(f'/atividades/{atividade_id}')

    assert response.status_code == 200

    response = client.get(f'/atividades/{atividade_id}')
    assert response.status_code == 404


def test_delete_atividade_404(setup):
    client = setup

    response = client.delete(f'/atividades/{123123123}')

    assert response.status_code == 404


def test_get_atividade_404(setup):
    client = setup
    response = client.get(f'/atividades')
    assert response.status_code == 404
