#!/bin/bash
# build_files.sh — executado pelo Vercel durante o build via @vercel/static-build.
#
# Como é chamado:
#   O vercel.json declara este arquivo como src do builder @vercel/static-build.
#   O Vercel executa o shell script e espera encontrar os arquivos estáticos
#   no diretório configurado em config.distDir ("staticfiles").
#
# Pré-requisito: as variáveis de ambiente (SECRET_KEY, DATABASE_URL etc.)
#   devem estar configuradas no painel do Vercel antes do primeiro deploy.
#
# Migrações NÃO são executadas aqui. Execute-as manualmente após o deploy,
# com DATABASE_URL apontando explicitamente para o banco de produção.
# Consulte o README para o procedimento controlado de migração.

set -e

echo "==> Instalando dependências..."
pip install -r requirements.txt

echo "==> Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Build concluído."
