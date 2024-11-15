# Projeto CRUD com Vue.js e Flask

Este projeto é uma aplicação CRUD simples utilizando **Vue.js** para o frontend e **Flask** para o backend. Ele permite gerenciar **Clientes**, **Projetos** e **Atividades** com uma interface interativa e comunicação com um banco de dados PostgreSQL.

## Tecnologias Utilizadas

### Backend (API) - Python
- **Python**: 3.12.5 (ou superior)
- **Flask**: 3.1.0
- **psycopg2**: Para interação com o PostgreSQL
- **Flask-Cors**: 5.0.0 Para permitir solicitações CORS entre o frontend (Vue.js) e o backend (Flask).
  
### Frontend - Vue.js
- **Vue.js**: 5.0.8
- **Bootstrap-Vue-3**: Para facilitar o design responsivo com componentes prontos e estilo integrado.

### Banco de Dados
- **PostgreSQL**: Para armazenar as informações de Clientes, Projetos e Atividades.

## Instalação

### Backend (API Flask)

1. Clone o repositório backend:
   ```bash
   git clone https://github.com/guilhermegielow/projetos.git
   cd projetos

    Crie um ambiente virtual e ative-o:
    
    ```bash
    cd back
    python -m venv venv
    source venv/bin/activate  # No Windows, use: venv\Scripts\activate
    ```
    
2. Instale as dependências:
    
    ```bash
    pip install -r requirements.txt
    Configure o banco de dados PostgreSQL e adicione as variáveis de ambiente necessárias para a conexão.
    ```
3. Inicie o servidor Flask:
    
    ```bash
    python back/app.py
    O backend estará disponível em http://localhost:5000.
    ```

### Frontend (VueJS)

4. Instale as dependências:
    
    ```bash
    cd frontend
    
    npm install
    ```
5. Inicie o servidor VueJs:

    ```bash
    npm run serve
    ```

6. Executar os testes com cobertura de testes da pasta de projetos
   ```bash
   pytest --cov=back/rest --cov-report=html
   ```

7. Verificar a qualidade do código python da pasta de projetos
   ```bash
   flake8 .\back\
   ```