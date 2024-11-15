import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import create_app
from config import TestConfig
from models.models import db, StatusProjeto


@pytest.fixture
def setup():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()
        yield app.test_client()

        db.drop_all()


def test_get_status_projetos(setup):
    client = setup
    status_projeto = StatusProjeto(id=1, nome='Planejamento')
    db.session.add(status_projeto)
    db.session.commit()

    response = client.get('/status_projetos')

    assert response.status_code == 200

    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]['id'] == 1
    assert json_data[0]['nome'] == 'Planejamento'


def test_get_client_id(setup):
    client = setup
    status_projeto = StatusProjeto(id=1, nome='Planejamento')
    db.session.add(status_projeto)
    db.session.commit()

    response = client.get(f'/status_projetos/{1}')
    assert response.status_code == 200


def test_get_status_projeto_id_404(setup):
    client = setup
    response = client.get(f'/status_projetos/{231123}')
    assert response.status_code == 404


def test_get_status_projeto_404(setup):
    client = setup
    response = client.get(f'/status_projetos')
    assert response.status_code == 404
