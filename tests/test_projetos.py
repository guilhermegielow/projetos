import pytest
import sys
import os

from back.models import StatusProjeto

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
        'status_projeto_id': 1,
        'cliente_id': cliente_id
    }

    response = client.post('/projetos', json=projeto_data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['nome'] == 'Projeto A'
    assert json_data['descricao'] == 'Descrição do Projeto A'


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
        'status_projeto_id': 2,
        'cliente_id': cliente_id
    })

    response = client.get('/projetos')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0


def test_get_projetos_abertos(setup):
    client = setup

    status_projeto = StatusProjeto(id=1, nome='Planejamento')
    db.session.add(status_projeto)
    db.session.commit()

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

    response = client.get('/projetos/abertos')

    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0


def test_update_projeto(setup):
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
        'nome': 'teste',
        'descricao': 'descricao_teste',
        'cliente_id': cliente_id,
        'status_projeto_id': 1
    }

    response = client.post('/projetos', json=projeto_data)
    projeto_id = response.get_json()['id']

    updated_data = {
        'nome': 'nome',
        'descricao': 'teste',
        'cliente_id': cliente_id,
        'status_projeto_id': 2
    }

    response = client.put(f'/projetos/{projeto_id}', json=updated_data)

    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data['nome'] == 'nome'
    assert json_data['descricao'] == 'teste'
    assert json_data['status_projeto_id'] == 2


def test_update_projeto_404(setup):
    client = setup
    updated_data = {
        'nome': 'nome',
        'descricao': 'teste',
        'cliente_id': '222',
        'status_projeto_id': 2
    }
    response = client.put(f'/projetos/{2222222}', json=updated_data)

    assert response.status_code == 404


def test_delete_projeto(setup):
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
        'nome': 'teste',
        'descricao': 'descricao_teste',
        'cliente_id': cliente_id,
        'status_projeto_id': 1
    }

    response = client.post('/projetos', json=projeto_data)
    projeto_id = response.get_json()['id']

    response = client.delete(f'/projetos/{projeto_id}')

    assert response.status_code == 200


def test_delete_projetos_404(setup):
    client = setup
    response = client.delete(f'/projetos/{123123123}')
    assert response.status_code == 404