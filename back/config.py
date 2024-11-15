class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:super@localhost/projetos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
