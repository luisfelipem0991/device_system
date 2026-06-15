# device_systems — API REST de Gestión de Usuarios v3.0

API REST construida con **FastAPI** para la gestión del recurso `users` dentro del sistema `device_systems`. En esta versión los datos se persisten en una base de datos **SQLite** usando **SQLAlchemy ORM**, reemplazando el almacenamiento en memoria de la versión anterior.

---

## Tecnologías utilizadas

- **Python 3.13**
- **FastAPI 0.110+** — Framework web moderno y de alto rendimiento
- **Uvicorn** — Servidor ASGI para correr la aplicación
- **SQLAlchemy 2.0+** — ORM para la gestión de la base de datos
- **SQLite** — Base de datos relacional ligera (archivo local)
- **Pydantic v2** — Validación y serialización de datos
- **email-validator** — Validación de formato de correos electrónicos

---

## Estructura del proyecto

```
device_systems/
│── app/
│   │── main.py
│   │
│   │── database/
│   │   └── connection.py
│   │
│   │── models/
│   │   └── user_model.py
│   │
│   │── schemas/
│   │   └── user_schema.py
│   │
│   │── routes/
│   │   └── user_routes.py
│   │
│   │── services/
│   │   └── user_service.py
│   │
│   └── dependencies/
│       └── database_dependency.py
│
│── requirements.txt
└── README.md
```

---

## Instalación y ejecución en Windows

### 1. Clona el repositorio

```bash
git clone https://github.com/luisfelipem0991/device_system.git
cd device_system
git checkout feature/database-integration
```

### 2. Crea y activa el entorno virtual

```bash
python -m venv venv
source venv/Scripts/activate
```

> Sabrás que está activo cuando veas `(venv)` al inicio de la línea.

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecuta el servidor

```bash
uvicorn app.main:app --reload
```

Al arrancar por primera vez, FastAPI crea automáticamente el archivo `device_systems.db` con la tabla `users`.

La API quedará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Tabla de endpoints

| Método | Endpoint                        | Descripción                          | Status         |
|--------|---------------------------------|--------------------------------------|----------------|
| GET    | `/users`                        | Lista todos los usuarios             | 200 OK         |
| GET    | `/users?role=admin`             | Filtra usuarios por rol              | 200 OK         |
| GET    | `/users?is_active=true`         | Filtra usuarios por estado           | 200 OK         |
| GET    | `/users?order_by=name`          | Ordena por nombre o fecha            | 200 OK         |
| GET    | `/users/{user_id}`              | Obtiene un usuario por ID            | 200 OK         |
| POST   | `/users`                        | Registra un nuevo usuario            | 201 Created    |
| PUT    | `/users/{user_id}`              | Actualización completa               | 200 OK         |
| PATCH  | `/users/{user_id}`              | Actualización parcial                | 200 OK         |
| DELETE | `/users/{user_id}`              | Elimina un usuario                   | 204 No Content |

---

## Códigos de estado HTTP

| Código | Nombre               | Cuándo se usa                                     |
|--------|----------------------|---------------------------------------------------|
| 200    | OK                   | GET, PUT y PATCH exitosos                         |
| 201    | Created              | POST exitoso, usuario creado                      |
| 204    | No Content           | DELETE exitoso, sin cuerpo de respuesta           |
| 400    | Bad Request          | Correo duplicado, rol inválido o PATCH sin datos  |
| 404    | Not Found            | Usuario no encontrado por ID                      |
| 422    | Unprocessable Entity | Datos inválidos detectados por Pydantic           |

---

## Ejemplos de peticiones y respuestas

### POST `/users` — Crear usuario

**Body:**
```json
{
  "name": "Luis Felipe Molina",
  "email": "luis@mail.com",
  "role": "admin",
  "is_active": true
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "name": "Luis Felipe Molina",
  "email": "luis@mail.com",
  "role": "admin",
  "is_active": true,
  "created_at": "2025-06-01T10:30:00"
}
```

---

### GET `/users` — Listar con filtros

```
GET /users?role=admin&is_active=true&order_by=name
```

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "name": "Luis Felipe Molina",
    "email": "luis@mail.com",
    "role": "admin",
    "is_active": true,
    "created_at": "2025-06-01T10:30:00"
  }
]
```

---

### PUT `/users/{user_id}` — Actualización completa

**Body:** todos los campos son obligatorios.
```json
{
  "name": "Luis Felipe Actualizado",
  "email": "luis_nuevo@mail.com",
  "role": "support",
  "is_active": false
}
```

---

### PATCH `/users/{user_id}` — Actualización parcial

**Body:** solo los campos a modificar.
```json
{
  "role": "support"
}
```

---

### DELETE `/users/{user_id}`

**Response `204 No Content`** — Sin cuerpo de respuesta.

---

## Manejo de errores

| Escenario                      | Código | Mensaje                                              |
|--------------------------------|--------|------------------------------------------------------|
| Usuario no encontrado          | 404    | `"El usuario que buscas no existe."`                 |
| Correo duplicado               | 400    | `"Ese correo ya existe, intenta con otro."`          |
| Rol no permitido               | 400    | `"Rol '...' no permitido. Usa: admin, support, user."` |
| PATCH sin campos               | 400    | `"Debes enviar al menos un campo para actualizar."`  |
| Datos inválidos (Pydantic)     | 422    | Detalle automático de FastAPI                        |

Todos los errores retornan:
```json
{
  "detail": "Mensaje descriptivo del error"
}
```

---

## Base de datos

### Modelo `users`

| Campo        | Tipo     | Restricción                  |
|--------------|----------|------------------------------|
| `id`         | Integer  | Primary Key, autoincremental |
| `name`       | String   | Obligatorio, mín. 3 chars    |
| `email`      | String   | Único y obligatorio          |
| `role`       | String   | admin / support / user       |
| `is_active`  | Boolean  | Default `True`               |
| `created_at` | DateTime | Se asigna automáticamente    |

El archivo `device_systems.db` se genera automáticamente en la raíz del proyecto al iniciar el servidor por primera vez. Está incluido en `.gitignore` para no subirse al repositorio.

---

## Schemas Pydantic

| Schema         | Uso                              |
|----------------|----------------------------------|
| `UserCreate`   | Crear usuario (POST)             |
| `UserUpdate`   | Actualización completa (PUT)     |
| `UserPatch`    | Actualización parcial (PATCH)    |
| `UserResponse` | Respuesta de todos los endpoints |

### Validaciones
- `name`: mínimo 3 caracteres, obligatorio
- `email`: formato válido (usa `EmailStr`)
- `role`: solo permite `admin`, `support`, `user`
- `is_active`: booleano

---

## Cabeceras HTTP personalizadas

Todos los endpoints retornan:

```
X-App-Name: device_systems
X-API-Version: 3.0
```

---

## Reflexión

Migrar de listas en memoria a una base de datos real con **SQLAlchemy** fue un cambio importante en la arquitectura del proyecto. Lo más valioso fue entender cómo funciona el **ORM**: en lugar de manipular diccionarios, ahora trabajamos con objetos Python que representan filas en una tabla real, y SQLAlchemy se encarga de traducir esas operaciones a SQL.

La inyección de la sesión de base de datos con `Depends(get_db)` mantiene el código limpio y desacoplado: cada endpoint recibe su sesión, la usa y la cierra automáticamente gracias al generador `yield`. Esto evita fugas de conexión y hace el código más seguro.

La adición del campo `created_at` con `default=datetime.utcnow` también fue un buen ejemplo de cómo el modelo ORM puede manejar lógica de negocio básica sin intervención del desarrollador en cada petición.
se añadio link del video https://www.loom.com/share/581dde6e282f45e2bffb2cca87baf328
