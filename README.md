# Projeto CRUD com Vue.js e Flask

Este projeto é uma aplicação CRUD simples utilizando **Vue.js** para o frontend e **Flask** para o backend. Ele permite gerenciar **Clientes**, **Projetos**, **Atividades** e **Status_Projeto** com uma interface interativa e comunicação com um banco de dados PostgreSQL.

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
- **PostgreSQL**: Para armazenar as informações de Clientes, Projetos, Atividades e Status de Projeto.

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
8. Diagrama de classes
```bash
+-------------------+           +-------------------+          +-------------------+
|     Atividade     |           |      Cliente      |          |      Projeto      |
+-------------------+           +-------------------+          +-------------------+
| - id: integer     |           | - id: integer     |          | - id: integer     |
| - descricao: text |           | - nome: string    |          | - nome: string    |
| - data: timestamp |           | - email: string   |          | - descricao: text |
| - projeto_id: int | --------> | - telefone: string| <------->| - cliente_id: int |
+-------------------+           | - cnpj: string    |          | - status_projeto_id|
                                +-------------------+          +-------------------+
                                                              |    ^                
                                                              |    |                
                                                     +------------------------+
                                                     |    StatusProjeto       |
                                                     +------------------------+
                                                     | - id: integer          |
                                                     | - nome: string         |
                                                     +------------------------+
```
9. Criação da base de dados
```bash
CREATE TABLE IF NOT EXISTS public.atividades
(
    id integer NOT NULL DEFAULT nextval('atividades_id_seq'::regclass),
    descricao text COLLATE pg_catalog."default" NOT NULL,
    data timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    projeto_id integer NOT NULL,
    CONSTRAINT atividades_pkey PRIMARY KEY (id),
    CONSTRAINT atividades_projeto_id_fkey FOREIGN KEY (projeto_id)
        REFERENCES public.projetos (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
); 
CREATE TABLE IF NOT EXISTS public.clientes
(
    id integer NOT NULL DEFAULT nextval('clientes_id_seq'::regclass),
    nome character varying(255) COLLATE pg_catalog."default" NOT NULL,
    email character varying(255) COLLATE pg_catalog."default",
    telefone character varying(15) COLLATE pg_catalog."default",
    cnpj character varying(14) COLLATE pg_catalog."default",
    CONSTRAINT clientes_pkey PRIMARY KEY (id),
    CONSTRAINT clientes_email_key UNIQUE (email),
    CONSTRAINT unique_cnpj UNIQUE (cnpj)
); 
CREATE TABLE IF NOT EXISTS public.projetos
(
    id integer NOT NULL DEFAULT nextval('projetos_id_seq'::regclass),
    nome character varying(255) COLLATE pg_catalog."default" NOT NULL,
    descricao text COLLATE pg_catalog."default",
    cliente_id integer NOT NULL,
    status_projeto_id integer,
    CONSTRAINT projetos_pkey PRIMARY KEY (id),
    CONSTRAINT fk_status_projeto FOREIGN KEY (status_projeto_id)
        REFERENCES public.status_projeto (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT projetos_cliente_id_fkey FOREIGN KEY (cliente_id)
        REFERENCES public.clientes (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE;  
CREATE TABLE IF NOT EXISTS public.status_projeto
(
    id integer NOT NULL DEFAULT nextval('status_projeto_id_seq'::regclass),
    nome character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT status_projeto_pkey PRIMARY KEY (id)
);
```