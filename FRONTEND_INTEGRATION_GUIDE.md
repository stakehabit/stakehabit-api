# Frontend and Coding Agent Integration Guide

This document is intended as a handoff guide for the frontend developer and any coding agent that needs to integrate with StakeHabit API.

## Base URL

- Local development: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication model

The API uses JWT bearer tokens.

1. Register or log in to receive a token.
2. Store the token in memory or in your app state.
3. Send it as:

```http
Authorization: Bearer <token>
```

### Login example

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### Expected response

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

## Core endpoints

### Auth
- `POST /register`
- `POST /login`
- `GET /me`

### Habits
- `GET /habits`
- `POST /habits`
- `GET /habits/{id}`
- `PATCH /habits/{id}`
- `DELETE /habits/{id}`
- `POST /habits/{id}/checkins`
- `GET /habits/{id}/streak`

### Pools
- `GET /pools`
- `POST /pools`
- `GET /pools/{pool_id}`
- `POST /pools/{pool_id}/join`
- `GET /pools/{pool_id}/participants`
- `POST /pools/{pool_id}/checkin`
- `GET /pools/{pool_id}/checkins/{wallet_address}`

## Request and response notes

### Habit payload

```json
{
  "title": "Exercise",
  "frequency": "daily",
  "target_days_per_week": 5,
  "is_active": true
}
```

### Pool payload

```json
{
  "title": "Streak Pool",
  "description": "Daily goals with shared stakes",
  "duration": 14,
  "stake_amount": "10.0000000",
  "currency": "USD",
  "max_participants": 5,
  "winner_split": 80,
  "charity": "help",
  "creator_address": "GABCDEF1234567890"
}
```

### Pool join payload

```json
{
  "wallet_address": "GUSER0000000001"
}
```

### Pool check-in payload

```json
{
  "wallet_address": "GUSER0000000001",
  "check_in_date": "2026-07-13"
}
```

## CORS and local development

The backend currently allows cross-origin requests from any origin for local development. If a frontend runs on a different port, it should be able to call the API without extra server-side changes.

## Important implementation details

- Protected routes require a bearer token.
- Pool participation is keyed by `wallet_address`, not by the authenticated user email.
- Duplicate pool joins and duplicate check-ins for the same day are rejected with a `400` response.
- Use the `/docs` page as the live reference for request and response bodies while developing.

## Suggested integration checklist

- [ ] Store the JWT token after login.
- [ ] Attach the token to protected requests.
- [ ] Fetch habits and render streaks from the habit endpoints.
- [ ] Use the pool endpoints for creating and joining challenge pools.
- [ ] Handle `401` and `400` responses with clear user feedback.
- [ ] Keep the frontend in sync with the documented API contract when new fields are added.
