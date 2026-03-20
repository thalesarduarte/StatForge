# StatForge

StatForge e um hub gamer multi-jogos com core compartilhado e modulos independentes por jogo. A plataforma foi organizada para escalar sem acoplamento indevido entre regras de Overwatch, Valorant, CS2, LoL e Fortnite.

## Stack

- Frontend: React, Vite, TypeScript, Tailwind CSS, React Router, TanStack Query e base shadcn/ui
- Backend: FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Alembic e JWT
- Infra: Docker, Docker Compose e configuracao por `.env`

## Arquitetura

```text
backend/
  app/
    api/
      routes/
      responses.py
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
      lol/
      fortnite/
frontend/
  src/
    app/
    components/
    pages/
    services/
    types/
    utils/
    features/
      core/
      overwatch/
      valorant/
      cs2/
      lol/
      fortnite/
```

## Principios adotados

- Tudo que e global da plataforma fica no core compartilhado.
- Tudo que e especifico de jogo fica dentro de `backend/app/modules/<game>` e `frontend/src/features/<game>`.
- Rotas, services, schemas, integracoes e componentes de cada jogo evoluem sem contaminar outros modulos.
- Responses da API seguem envelope padronizado.
- Frontend e backend continuam desacoplados e preparados para crescimento independente.

## Core compartilhado

Dominios cobertos na base atual:

- autenticacao JWT
- usuarios
- perfis publicos
- comentarios
- likes em comentarios
- seguir jogadores
- favoritos
- badges
- times / clas
- torneios
- feed de atividade
- painel admin inicial

## Modulos por jogo

### Overwatch

- perfil do jogador
- ranks
- heroes
- mapas
- modos
- estatisticas por role
- estatisticas por heroi
- comparacao entre jogadores
- main hero
- historico recente

### Valorant

- perfil do jogador
- rank
- agents
- mapas
- armas
- HS%
- KDA
- winrate
- comparacao entre jogadores
- historico recente

### CS2

- perfil do jogador
- rank / elo
- KD
- HS%
- ADR
- mapas
- armas
- comparacao entre jogadores
- historico recente

### LoL

- perfil do invocador
- elo
- champions
- roles
- KDA
- winrate
- historico recente
- comparacao entre jogadores

### Fortnite

- perfil
- partidas
- vitorias
- kills
- KD
- modos
- historico
- comparacao entre jogadores

## Backend

Padrao de endpoints por modulo:

- `GET /api/v1/modules/<game>/overview/{handle}`
- `GET /api/v1/modules/<game>/compare/{left}/{right}`
- `GET /api/v1/modules/<game>/reference-data`
- `GET /api/v1/modules/<game>/history/{handle}`

Rotas centrais relevantes:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/users`
- `GET/POST /api/v1/profiles`
- `GET/POST /api/v1/comments`
- `GET/POST /api/v1/comment-likes`
- `GET/POST /api/v1/favorites`
- `GET/POST /api/v1/follows`
- `GET/POST /api/v1/teams`
- `GET/POST /api/v1/tournaments`
- `GET/POST /api/v1/badges`
- `GET /api/v1/activity/feed`
- `GET /api/v1/admin/summary`

### Modelagem principal

Tabelas compartilhadas previstas na base:

- `users`
- `profiles`
- `comments`
- `comment_likes`
- `favorites`
- `follows`
- `activity_events`
- `teams`
- `tournaments`
- `badges`
- `game_profiles`
- `game_stats`
- `game_matches`

Tabelas modulares:

- `overwatch_profiles`
- `valorant_profiles`
- `cs2_profiles`
- `lol_profiles`
- `fortnite_profiles`

## Frontend

O frontend foi reorganizado como hub multi-game:

- dashboard central com pilares do core
- navegacao por modulo
- pagina separada para cada jogo
- hooks e services isolados por modulo
- renderer compartilhado para paginas de jogo
- integracao pronta para TanStack Query com fallback local

## Ambiente local

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

## Docker

```powershell
docker compose up --build
```

## Estado atual

- frontend multi-game refatorado e compilando em build de producao
- backend reorganizado com envelopes padronizados e novos modulos
- validacao automatica do backend ainda depende de executar o interpretador Python fora das restricoes do sandbox

## Proximos passos naturais

1. Persistir de fato favoritos, feed, historico e comparativos com dados reais.
2. Adicionar testes automatizados de API e frontend.
3. Introduzir integracoes reais por provider em cada modulo.
4. Publicar a base no GitHub e configurar CI.
