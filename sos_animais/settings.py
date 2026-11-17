"""
Configurações do projeto sos_animais.

Os valores sensíveis e os que mudam entre ambientes são lidos de
variáveis de ambiente. Em desenvolvimento, eles podem ficar no arquivo
.env da raiz do projeto (copie o .env.example e preencha).

Documentação: https://docs.djangoproject.com/en/6.1/ref/settings/
"""

import os
from pathlib import Path

from django.contrib.messages import constants as message_constants
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o .env da raiz do projeto, se existir. Variáveis já definidas
# no ambiente (por exemplo, no GitHub Actions) têm prioridade.
load_dotenv(BASE_DIR / ".env")

VALORES_VERDADEIROS = {"1", "true", "sim", "yes", "on"}


def env_bool(nome, padrao=False):
    """Lê uma variável de ambiente como verdadeiro ou falso."""
    valor = os.getenv(nome)
    if valor is None or valor.strip() == "":
        return padrao
    return valor.strip().lower() in VALORES_VERDADEIROS


def env_lista(nome, padrao=""):
    """Lê uma variável de ambiente separada por vírgulas como lista."""
    valor = os.getenv(nome, padrao)
    return [item.strip() for item in valor.split(",") if item.strip()]


# Segurança

SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "A variável SECRET_KEY não foi definida. Copie o arquivo "
        ".env.example para .env e preencha a SECRET_KEY, conforme "
        "explicado no README."
    )

# Desativado por padrão. Só fica ativo com DEBUG=True no ambiente.
DEBUG = env_bool("DEBUG", padrao=False)

# Exemplo: ALLOWED_HOSTS=localhost,127.0.0.1
# Com DEBUG=True e lista vazia, o Django aceita apenas localhost.
ALLOWED_HOSTS = env_lista("ALLOWED_HOSTS")

# Exemplo: CSRF_TRUSTED_ORIGINS=https://sos-animais.exemplo.org
CSRF_TRUSTED_ORIGINS = env_lista("CSRF_TRUSTED_ORIGINS")


# Aplicação

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sos_animais.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sos_animais.wsgi.application"


# Banco de dados

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Senhas

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Autenticação

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "menu"
LOGOUT_REDIRECT_URL = "login"


# Idioma e fuso horário

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Arquivos estáticos

STATIC_URL = "static/"


# Mensagens: usa as classes de alerta do Bootstrap

MESSAGE_TAGS = {
    message_constants.ERROR: "danger",
}


# E-mail (apenas exibido no terminal, para desenvolvimento)

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
