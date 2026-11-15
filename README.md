# SOS Animais de Olímpia — MVP

Projeto acadêmico de sistema web para apoiar a organização dos registros da SOS Animais de Olímpia.

O desenvolvimento prioriza uma interface simples, voltada ao uso em celular por uma equipe com tempo limitado e diferentes níveis de familiaridade digital.

## Objetivo

Centralizar informações sobre animais, adoções, devoluções, doações e despesas, reduzindo a dispersão dos registros e apoiando o trabalho da organização.

## Estado atual da implementação

Implementado:

- Fluxo de login utilizando a autenticação do Django.
- Menu principal e formulário demonstrativo de adoção.
- Validação dos campos do formulário e apresentação do resultado da simulação.
- Modelo Animal com nome, espécie, porte, data de entrada, situação, observações e datas de controle.
- Migração inicial do modelo Animal.
- Sete testes automatizados de validação, comportamento e persistência do modelo.
- Regras de exclusão de arquivos locais pelo .gitignore.

Limitações:

- O formulário de adoção utiliza animais fictícios e armazena o resultado na sessão.
- A simulação não grava uma adoção nem altera a situação de um animal.
- O modelo Animal ainda não está conectado a uma tela própria de cadastro.
- A existência do modelo não equivale à implementação completa do cadastro.
- Não há medição de cobertura nem pipeline de integração contínua configurado.
- A validação com a comunidade ainda não possui resultados registrados.

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

## Ambiente observado no desenvolvimento

Versões informadas pelo terminal do ambiente local:

- Python 3.15.2.
- Django 6.1.3.
- Banco SQLite.
- Dependências registradas em requirements.txt.

O planejamento anterior previa Python 3.12, Django 5.0 e PostgreSQL.
A implementação local utiliza um ambiente diferente, cuja padronização
ainda deverá ser revisada antes da configuração de CI e da implantação.

As versões acima são registros do ambiente local. A instalação em um
ambiente limpo e a disponibilidade das versões nas fontes de pacotes
ainda não foram verificadas.

A interface foi planejada com Bootstrap 5.3.

## Estrutura principal

```text
core/
    migrations/
    templates/
    models.py
    tests.py
    urls.py
    views.py
sos_animais/
    settings.py
    urls.py
    wsgi.py
manage.py
requirements.txt
README.md
.gitignore
```

## Preparação de um ambiente local no Windows

Os comandos abaixo descrevem o procedimento previsto.
A reprodução completa em um ambiente limpo ainda precisa ser validada.

Com o Python adequado instalado, abra o PowerShell na raiz do projeto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Antes de executar a aplicação, confira em sos_animais/settings.py quais
variáveis de ambiente são utilizadas. Quando necessário, configure-as
localmente. O arquivo .env não é distribuído no repositório, e ainda
não há um .env.example.

Não utilize credenciais de produção no ambiente acadêmico.

## Execução local

Após instalar as dependências e configurar o ambiente:

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

Com o ambiente virtual ativo:

```powershell
python manage.py test core --verbosity 2
```

São sete testes: seis testes de comportamento e validação sem acesso
ao banco e um teste de integração entre o modelo e o banco.

Cenários:

- Representação textual.
- Valores padrão.
- Nome obrigatório.
- Espécie inválida.
- Situação inválida.
- Observações opcionais.
- Gravação e recuperação do animal.

Na execução local após a integração do PR #2, os sete testes passaram.
O executor utilizou um banco SQLite separado, em memória.

Os testes de validação chamam clean_fields() explicitamente.
Eles não demonstram validação automática em toda chamada de save().

## Versionamento e revisão

As alterações são desenvolvidas em branches e propostas à main por
Pull Requests, com registro de auto-revisão técnica.

O histórico inclui commits específicos para modelo, migração,
organização do repositório, testes e dependências.

## Proteção de arquivos locais

O .gitignore exclui do novo rastreamento:

- Ambientes virtuais.
- Caches do Python.
- Banco SQLite local.
- Arquivos .env.
- Logs.

Ignorar ou remover um arquivo do rastreamento não elimina versões
anteriores do histórico. Não publique dados pessoais reais, senhas
ou tokens.

## Próximos passos

- Verificar a instalação em ambiente limpo e padronizar as versões.
- Documentar as variáveis necessárias em um .env.example sem segredos.
- Implementar as telas de cadastro de animais.
- Implementar a persistência e as regras de adoção e devolução.
- Ampliar os testes e medir a cobertura.
- Configurar integração contínua.
- Realizar duas rodadas de validação com a comunidade, mediante
  agendamento e concordância dos participantes.

## Autorrevisão técnica do MVP

### Arquitetura e separação de responsabilidades

O modelo Animal e sua migração constituem a estrutura inicial de
persistência. Sua existência não representa a conclusão do cadastro
em tela nem a integração com o fluxo demonstrativo de adoção.

O formulário demonstrativo permanece em core/views.py. Como melhoria
de organização, está prevista sua extração para core/forms.py,
separando a definição dos campos e suas validações da coordenação
das requisições. Essa refatoração ainda não foi realizada.

### Legibilidade e manutenção

A documentação distingue funcionalidades implementadas, planejadas
e demonstrativas. Essa separação evita interpretar o resultado da
simulação como uma adoção efetivamente registrada.

As próximas alterações devem manter nomes descritivos e testes
compatíveis com as responsabilidades de cada componente.

### Segurança e proteção de dados

O protótipo demonstrativo deve utilizar dados fictícios. Não devem
ser publicados dados pessoais reais, credenciais ou tokens.

O .gitignore não substitui a verificação dos arquivos e do histórico
antes da publicação. Remover um arquivo do rastreamento atual não
elimina suas versões anteriores.

A existência de login não comprova, isoladamente, a proteção de todas
as rotas. A verificação de acesso sem autenticação às telas internas
permanece como atividade de revisão e teste.

### Limites desta revisão

Este registro apresenta uma análise técnica do estado documentado
do projeto e oportunidades de melhoria. Não comprova auditoria de
segurança, revisão independente, execução de novos testes ou
implementação das melhorias propostas.