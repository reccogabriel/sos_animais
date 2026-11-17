# SOS Animais de Olímpia: MVP

[![CI](https://github.com/reccogabriel/sos_animais/actions/workflows/ci.yml/badge.svg)](https://github.com/reccogabriel/sos_animais/actions/workflows/ci.yml)

Projeto acadêmico de sistema web para apoiar a organização dos registros da SOS Animais de Olímpia.

O desenvolvimento prioriza uma interface simples, voltada ao uso em celular por uma equipe com tempo limitado e diferentes níveis de familiaridade digital.

> **Aviso de segurança.** O primeiro commit do repositório publicou por engano
> o banco local e o arquivo `.env`. Os detalhes e as ações pendentes estão em
> [docs/incidente-seguranca-2026-11-15.md](docs/incidente-seguranca-2026-11-15.md).

## Objetivo

Centralizar informações sobre animais, adoções, devoluções, doações e despesas, reduzindo a dispersão dos registros e apoiando o trabalho da organização.

## Estado atual da implementação

Implementado:

- Login e logout com a autenticação do Django. O login respeita o
  parâmetro `?next=` apenas para endereços do próprio site, e o logout
  funciona somente por POST.
- Menu principal. As funcionalidades que ainda não existem aparecem como
  botões desativados, marcados como "em desenvolvimento".
- Formulário demonstrativo de adoção, com validação dos campos e tela de
  resultado da simulação.
- Validação de telefone brasileiro: DDD e número (10 ou 11 dígitos),
  aceitando apenas dígitos, espaços, parênteses, hífen e `+55` opcional.
- Modelo Animal com nome, espécie, porte, data de entrada, situação, observações e datas de controle.
- Migração inicial do modelo Animal.
- 34 testes automatizados (detalhes abaixo).
- Integração contínua com GitHub Actions.
- Configuração por variáveis de ambiente, com `.env.example`.
- Idioma `pt-br` e fuso horário `America/Sao_Paulo`.

Limitações:

- O formulário de adoção usa dois animais fictícios, fixos no código. Ele
  não consulta o cadastro nem o status dos animais no banco.
- A simulação não grava uma adoção nem altera a situação de um animal.
- Os dados da simulação ficam na sessão somente até a tela de resultado
  ser exibida. Depois disso, são apagados.
- O modelo Animal ainda não está conectado a uma tela própria de cadastro
  e não está registrado no admin.
- A existência do modelo não equivale à implementação completa do cadastro.
- Não existem modelos nem telas de adoção real, devolução, doação, despesa
  ou histórico de saúde.
- Não há medição de cobertura de testes.
- A validação com a comunidade ainda não possui resultados registrados.
- A configuração atual é para desenvolvimento. Antes de publicar o
  sistema, é preciso resolver os avisos de `python manage.py check --deploy`.

## Escopo planejado

- Cadastro e acompanhamento de animais.
- Registro de adoções e devoluções.
- Registro de doações e despesas.
- Histórico de saúde dos animais.
- Autenticação da equipe.
- Interface adequada ao uso em celular.

O pagamento online de doações está fora do escopo.
O alerta de vacina é desejável e poderá ser desenvolvido posteriormente.

## Arquitetura

Aplicação monolítica em camadas, com responsabilidades distribuídas entre modelos, formulários, views e templates do Django.

O formulário demonstrativo permanece definido em core/views.py.

## Versões utilizadas

| Componente | Versão | Observação |
| --- | --- | --- |
| Python | 3.12 ou mais recente | Exigência do Django 6.1. Verificado no CI com 3.12, 3.13 e 3.14 |
| Django | 6.1.3 | Fixado em `requirements.txt` |
| Banco | SQLite | Arquivo local `db.sqlite3`, fora do Git |
| Bootstrap | 5.3.0 (somente CSS) | Carregado por CDN em `base.html` |

O planejamento inicial previa Python 3.12, Django 5.0 e PostgreSQL. A
implementação adotou o **Django 6.1.3**, e essa é a versão oficial do
projeto. O código usa recursos do Django 6 (por exemplo, a configuração
`MAILERS`) e não é compatível com o Django 5.0.

O ambiente local do autor registrou Python 3.15.2. Essa versão não faz
parte da verificação automática do CI. Qualquer versão a partir da 3.12
listada acima pode ser usada.

## Estrutura principal

```text
.github/
    workflows/
        ci.yml
core/
    migrations/
    templates/
    models.py
    tests.py
    urls.py
    views.py
docs/
    incidente-seguranca-2026-11-15.md
sos_animais/
    settings.py
    urls.py
    wsgi.py
.env.example
.gitignore
manage.py
requirements.txt
README.md
```

## Preparação de um ambiente local no Windows

Com o Python 3.12 ou mais recente instalado, abra o PowerShell na raiz do projeto.

1. Crie e ative o ambiente virtual, e instale as dependências:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Crie o arquivo `.env` a partir do modelo:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Gere uma chave secreta:

   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. Abra o `.env`, cole a chave gerada depois de `SECRET_KEY=` e, para
   desenvolvimento no seu computador, mude para `DEBUG=True`.

Variáveis disponíveis (todas descritas no `.env.example`):

| Variável | Obrigatória | Padrão | Para que serve |
| --- | --- | --- | --- |
| `SECRET_KEY` | Sim | nenhum | Chave de criptografia do Django. Sem ela, o sistema não inicia |
| `DEBUG` | Não | `False` | Mostra páginas de erro detalhadas. Use `True` só localmente |
| `ALLOWED_HOSTS` | Não | vazio | Endereços aceitos, separados por vírgula |
| `CSRF_TRUSTED_ORIGINS` | Não | vazio | Origens HTTPS confiáveis, para quando o sistema for publicado |

O arquivo `.env` não deve ser enviado ao GitHub (ele está no `.gitignore`).
Não utilize credenciais de produção no ambiente acadêmico.

## Execução local

Após instalar as dependências e configurar o `.env`:

```powershell
python manage.py migrate
python manage.py check
python manage.py createsuperuser
python manage.py runserver
```

O comando createsuperuser é necessário apenas quando ainda não houver
um usuário apropriado para acessar o fluxo autenticado.

Acesse no navegador:

```text
http://127.0.0.1:8000/
```

O servidor iniciado por runserver é destinado ao desenvolvimento local.

## Testes automatizados

Com o ambiente virtual ativo e o `.env` configurado:

```powershell
python manage.py test core --verbosity 2
```

São 34 testes, divididos em grupos:

| Grupo | Quantidade | O que verifica |
| --- | --- | --- |
| `AnimalValidacaoTests` | 6 | Texto do animal, valores padrão, nome obrigatório, espécie e situação inválidas, observações opcionais |
| `AnimalPersistenciaTests` | 1 | Gravação e leitura de um animal no banco |
| `LoginTests` | 7 | Página de login, senha errada, login correto, `?next=` interno, `?next=` externo ignorado, usuário já logado |
| `AcessoProtegidoTests` | 5 | Páginas que exigem login, menu sem links vazios, logout por POST, logout por GET recusado |
| `AdocaoFormularioTests` | 7 | Campos obrigatórios, nome só com espaços, animal fora da lista, data futura, telefones válidos e inválidos |
| `AdocaoFluxoTests` | 5 | Aviso de dados fictícios, erro de validação, tela de resultado, limpeza da sessão, nenhuma gravação nas tabelas do sistema |
| `ConfiguracaoTests` | 3 | Leitura de `DEBUG` e `ALLOWED_HOSTS` a partir do ambiente |

Os testes de validação do modelo chamam clean_fields() explicitamente.
Eles não demonstram validação automática em toda chamada de save().

O teste de "nenhuma gravação" registra todos os comandos enviados ao banco
durante a simulação e confirma que só a tabela de sessões do Django recebe
escrita.

## Integração contínua

O workflow `.github/workflows/ci.yml` roda a cada push na `main` e em cada
Pull Request, com Python 3.12, 3.13 e 3.14. Ele:

1. instala as dependências do `requirements.txt`;
2. executa `python manage.py check`;
3. executa `python manage.py makemigrations --check --dry-run`, que falha
   se houver alteração de modelo sem migração;
4. executa os testes.

## Versionamento e revisão

As alterações são desenvolvidas em branches e propostas à main por
Pull Requests, com registro de auto-revisão técnica.

O histórico inclui commits específicos para modelo, migração,
organização do repositório, testes e dependências.

## Proteção de arquivos locais

O .gitignore exclui do novo rastreamento:

- Ambientes virtuais.
- Caches do Python.
- Banco SQLite local e seus arquivos auxiliares.
- Arquivos .env (o `.env.example` continua versionado).
- Cópias de segurança e relatórios de testes.
- Logs.

Ignorar ou remover um arquivo do rastreamento não elimina versões
anteriores do histórico. Foi exatamente isso que aconteceu no primeiro
commit; veja o [registro do incidente](docs/incidente-seguranca-2026-11-15.md).
Não publique dados pessoais reais, senhas ou tokens.

## Próximos passos

- Concluir as ações pendentes do incidente de segurança.
- Registrar o modelo Animal no admin e implementar as telas de cadastro e consulta.
- Implementar a persistência e as regras de adoção e devolução.
- Implementar o registro de doações e despesas.
- Medir a cobertura dos testes.
- Preparar a configuração de implantação (`check --deploy`).
- Realizar duas rodadas de validação com a comunidade, mediante
  agendamento e concordância dos participantes.
