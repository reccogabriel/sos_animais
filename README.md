# SOS Animais de Olímpia — MVP

Sistema web para apoiar o registro e o acompanhamento de animais, adoções, devoluções, doações e despesas da SOS Animais de Olímpia.

## Objetivo do MVP

Oferecer uma ferramenta simples e acessível para a equipe da ONG registrar informações essenciais sobre animais e processos de adoção, reduzindo o uso de controles dispersos e apoiando a organização das ações de proteção animal.

## Escopo inicial

O MVP contempla:

- Cadastro de animais.
- Registro de adoções e devoluções.
- Registro de doações e despesas.
- Histórico básico de saúde do animal.
- Autenticação de usuários da equipe.
- Interface adaptada para uso em celular.

O pagamento online de doações não faz parte do escopo inicial. O alerta de vacina é um requisito desejável e poderá ser implementado em uma iteração posterior.

## Tecnologias

- Python 3.12
- Django 5.0
- PostgreSQL
- Bootstrap 5.3
- GitHub para controle de versão

## Estrutura do projeto

```text
sos_animais/
├── core/
│   ├── templates/
│   │   └── core/
│   │       ├── login.html
│   │       ├── menu.html
│   │       ├── formulario_adocao.html
│   │       └── resultado_adocao.html
│   ├── views.py
│   └── urls.py
├── sos_animais/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Depois, acesse:

```text
http://127.0.0.1:8000/
```

## Status do projeto

O projeto está em desenvolvimento. O protótipo inicial apresenta o fluxo de simulação de adoção para validação de usabilidade; a gravação definitiva de adoções e a integração com o banco de dados serão implementadas nas próximas etapas.
