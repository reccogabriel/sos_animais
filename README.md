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

Aplicação monolítica em camadas, com responsabilidades distribuídas entre modelos, formulários, views e templ