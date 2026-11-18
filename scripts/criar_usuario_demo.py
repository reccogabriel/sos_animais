"""
Script auxiliar: cria o usuário demonstrativo no banco de produção (Neon).

Uso (rodar UMA VEZ após o primeiro deploy e as migrações):

  vercel env pull .env.production.local   # baixa as vars de prod localmente
  python scripts/criar_usuario_demo.py

Ou via Vercel CLI no contexto de produção:

  vercel run python scripts/criar_usuario_demo.py --prod

O script não sobrescreve um usuário já existente.
Não compartilhe este arquivo com credenciais preenchidas.
"""

import os
import sys
import pathlib

# Garante que manage.py e settings.py sejam encontrados a partir da raiz.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sos_animais.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

User = get_user_model()

USUARIO = "demo"
SENHA   = os.getenv("DEMO_PASSWORD", "").strip()

if not SENHA:
    sys.exit(
        "Erro: defina a variável DEMO_PASSWORD antes de rodar este script.\n"
        "Exemplo: set DEMO_PASSWORD=SuaSenhaSegura && python scripts/criar_usuario_demo.py"
    )

if User.objects.filter(username=USUARIO).exists():
    print(f"Usuário '{USUARIO}' já existe — nenhuma alteração feita.")
else:
    User.objects.create_user(username=USUARIO, password=SENHA)
    print(f"Usuário '{USUARIO}' criado com sucesso.")
