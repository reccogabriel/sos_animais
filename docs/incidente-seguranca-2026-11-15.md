# Incidente de segurança: banco local e .env publicados no histórico

| Item | Situação |
| --- | --- |
| Data da exposição | 15/11/2026, commit `5fc6a81` ("Envio completo MVP ao GitHubS") |
| Remoção do rastreamento | commit `c8e5bf1` |
| Situação atual | Arquivos fora da versão atual, mas **ainda acessíveis no histórico público** |
| Reescrita do histórico | **Não realizada.** Depende de aprovação prévia do responsável pelo repositório |

## O que aconteceu

O primeiro envio do projeto ao GitHub incluiu arquivos que deveriam ficar
apenas no computador do desenvolvedor:

- `db.sqlite3`, o banco de dados local;
- `.env`, o arquivo de configuração local;
- arquivos `__pycache__/*.pyc`, sem dados sensíveis.

O commit `c8e5bf1` tirou esses arquivos do rastreamento e criou o
`.gitignore`. Porém remover um arquivo em um commit novo **não apaga as
versões antigas**: qualquer pessoa ainda consegue abrir o commit `5fc6a81`
e baixar os arquivos.

## O que ficou exposto

**No `db.sqlite3`:**

- uma conta de superusuário (administrador), com nome de usuário e e-mail
  do desenvolvedor;
- o hash da senha dessa conta. O algoritmo é PBKDF2-SHA256 com 1.500.000
  iterações. A senha não aparece em texto, mas o hash permite tentativas
  de adivinhação fora do sistema, sem limite de tentativas. Senhas fracas
  ou reaproveitadas de outros serviços correm risco;
- um registro de sessão de login. Ele só tem efeito no banco local do
  desenvolvedor, e o risco é baixo.

**No `.env`:**

- `SECRET_KEY` com um texto de exemplo ("sua-chave-secreta..."), e não uma
  chave real;
- `DEBUG=True`.

Não foram encontrados dados de animais, adotantes ou doadores.

## Ações já realizadas

1. Os arquivos não estão mais na versão atual do repositório
   (commit `c8e5bf1`).
2. O `.gitignore` cobre banco SQLite (incluindo os arquivos `-wal` e
   `-shm`), `.env`, cópias de segurança e caches.
3. Foi criado o `.env.example`, sem valores reais, para que ninguém precise
   versionar o `.env`.
4. O `settings.py` deixou de ter `DEBUG = True` fixo e passou a exigir
   `SECRET_KEY` definida no ambiente.

## Ações pendentes

- [ ] **Trocar a senha da conta de superusuário exposta.** Se a mesma
      senha for usada em outro serviço (e-mail, GitHub etc.), trocá-la lá
      também.
- [ ] No computador do desenvolvedor, apagar as sessões antigas:
      `python manage.py shell -c "from django.contrib.sessions.models import Session; Session.objects.all().delete()"`.
- [ ] Gerar uma `SECRET_KEY` nova e aleatória no `.env` local (veja o
      `.env.example`).
- [ ] Verificar no GitHub se existem forks ou cópias do repositório. Uma
      reescrita do histórico não alcança essas cópias.
- [ ] **Decidir** sobre a reescrita do histórico (por exemplo, com
      `git filter-repo`) para remover `db.sqlite3` e `.env` de todos os
      commits. Essa ação muda os identificadores dos commits publicados e
      exige que todos os colaboradores clonem o repositório de novo. **Só
      deve ser feita com aprovação prévia do responsável.** Mesmo depois
      dela, é preciso considerar que os dados já podem ter sido copiados.
      Por isso a troca de senha é a ação principal.

## Como evitar que se repita

- Conferir `git status` antes de cada commit e nunca usar `git add .`
  sem revisar a lista.
- Manter `.env` e `db.sqlite3` sempre fora do Git (já garantido pelo
  `.gitignore`).
- Usar apenas dados fictícios no banco local de desenvolvimento.
