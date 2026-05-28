# taller-sesion-02

Este repositorio incluye una API en `backend` construida con **Python + FastAPI** que implementa un caso de uso con **JWT**.

## Estructura

- `backend/`: aplicación FastAPI administrada con Poetry.
- `docker-compose.yml`: despliegue local con Docker.

## Endpoints

### 1) Generar token

- **POST** `/token`
- Body JSON:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Respuesta exitosa:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 2) Refrescar token

- **POST** `/token/refresh`
- Body JSON:

```json
{
  "token": "<jwt>"
}
```

Respuesta exitosa:

```json
{
  "access_token": "<jwt_nuevo>",
  "token_type": "bearer",
  "expires_in": 300
}
```

## Uso con Poetry

Requisitos: Python 3.11+ y Poetry.

```bash
cd backend
export SECRET_KEY="una-clave-secreta-de-al-menos-32-caracteres"
poetry install
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API quedará disponible en `http://localhost:8000`.

Variables de entorno opcionales:

- `SECRET_KEY` (obligatoria, mínimo 32 caracteres, clave de firmado JWT)
- `ADMIN_USERNAME` (por defecto `admin`)
- `ADMIN_PASSWORD` (por defecto `admin123`)

## Uso con Docker

Desde la raíz del proyecto:

```bash
export SECRET_KEY="una-clave-secreta-de-al-menos-32-caracteres"
docker compose up --build
```

La API quedará disponible en `http://localhost:8000`.
