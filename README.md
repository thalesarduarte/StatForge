# StatForge

StatForge e uma plataforma gamer modular para acompanhar perfis de jogadores, estatisticas, rankings, comparacoes, comentarios da comunidade, times, torneios, badges e integracoes com multiplos jogos.

## Stack

- Frontend: React, Vite, TypeScript, Tailwind CSS, React Router, TanStack Query, base shadcn/ui
- Backend: FastAPI, SQLAlchemy, Pydantic, PostgreSQL, Alembic, JWT Authentication
- Infra: Docker, Docker Compose, variaveis de ambiente por app

## Estrutura

```text
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
    repositories/
    utils/
    modules/
      overwatch/
      valorant/
      cs2/
frontend/
  src/
    app/
    pages/
    components/
    services/
    hooks/
    types/
    utils/
    features/
      core/
      overwatch/
      valorant/
      cs2/
```

## Regras de arquitetura

- Tudo que e global da plataforma fica no core compartilhado.
- Tudo que e especifico de cada jogo fica isolado dentro de `backend/app/modules/<game>` e `frontend/src/features/<game>`.
- Frontend e backend ficam desacoplados para crescimento independente.
- Modelos compartilhados de dados cobrem a plataforma base; extensoes especificas de jogo ficam em tabelas proprias por modulo.

## Core compartilhado

- Autenticacao com JWT
- Usuarios e perfis publicos
- Comentarios, likes e follows
- Favoritos e feed preparados para expansao
- Times, clas e torneios
- Badges e painel admin inicial

## Modelagem inicial

Tabelas compartilhadas criadas no bootstrap:

- `users`
- `profiles`
- `comments`
- `comment_likes`
- `follows`
- `teams`
- `tournaments`
- `badges`
- `game_profiles`
- `game_stats`
- `game_matches`

Tabelas modulares iniciais:

- `overwatch_profiles`
- `valorant_profiles`
- `cs2_profiles`

## Backend

Principais rotas REST iniciais:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET/POST /api/v1/profiles`
- `GET/POST /api/v1/comments`
- `GET/POST /api/v1/follows`
- `GET/POST /api/v1/teams`
- `GET/POST /api/v1/tournaments`
- `GET/POST /api/v1/badges`
- `GET /api/v1/admin/summary`
- `GET /api/v1/modules/overwatch/profiles/{handle}`
- `GET /api/v1/modules/valorant/profiles/{handle}`
- `GET /api/v1/modules/cs2/profiles/{handle}`

## Frontend

O frontend inicia com:

- dashboard core da plataforma
- paginas independentes por jogo
- layout compartilhado e componentes base reutilizaveis
- cliente HTTP centralizado
- preparacao para consumo da API com TanStack Query

## Ambiente local

### Backend

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker compose up --build
```

## Proximos passos recomendados

1. Conectar as rotas modulares a provedores reais por jogo.
2. Criar persistencia para favoritos, activity feed e memberships de times.
3. Adicionar testes automatizados de API e frontend.
4. Evoluir o admin para moderacao e curadoria de integracoes.
