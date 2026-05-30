# device_systems — API REST de Gestión de Usuarios

API REST desarrollada con **FastAPI** para administrar el recurso `users` en el sistema `device_systems`. El proyecto aplica validación con Pydantic v2, uso de path y query parameters, response models y cabeceras HTTP personalizadas.

---

## Estructura del proyecto

```
device_systems/
│── app/
│   │── main.py
│   │── schemas/
│   │   └── user_schema.py
│   └── routes/
│       └── user_routes.py
│── requirements.txt
└── README.md
```

---

## Instalación de dependencias

Clona el repositorio e instala las dependencias:

```bash
git clone https://github.com/tu-usuario/device_systems.git
cd device_systems
pip install -r requirements.txt
```

Contenido del `requirements.txt`:

```
fastapi
uvicorn
pydantic[email]
```

---

## Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Documentación interactiva (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Tabla de endpoints

| Método | Endpoint               | Descripción                          |
|--------|------------------------|--------------------------------------|
| GET    | `/users`               | Lista todos los usuarios             |
| GET    | `/users/{user_id}`     | Obtiene un usuario por su ID         |
| GET    | `/users?role=admin`    | Filtra usuarios por rol              |
| GET    | `/users?is_active=true`| Filtra usuarios por estado activo    |
| POST   | `/users`               | Registra un nuevo usuario            |

---

## Cabeceras HTTP personalizadas

Todos los endpoints retornan las siguientes cabeceras personalizadas:

```
X-App-Name: device_systems
X-API-Version: 1.0
```

---

## Reflexión sobre el uso de FastAPI para construir APIs REST

Este taller me ayudó a comprender por qué **FastAPI** se ha vuelto tan popular para construir APIs en Python. Lo más destacable es su enfoque minimalista: con muy pocas líneas se obtiene un servidor funcional, con documentación automática en `/docs` lista para usar desde el primer momento.

La parte que más me aportó fue trabajar con **Pydantic v2** para la validación. Definir las reglas dentro del schema (tipo de dato, longitud, formato de correo) y que el framework las aplique automáticamente elimina una cantidad enorme de código repetitivo y reduce el margen de error humano.

En cuanto al diseño de endpoints, entendí con claridad cuándo conviene usar **Path Parameters** y cuándo **Query Parameters**: los path params identifican un recurso concreto, los query params sirven para aplicar filtros sobre una colección. Esta distinción, que parece simple, tiene un impacto directo en qué tan intuitiva y predecible resulta la API para quien la consuma. Finalmente, los **Response Models** me mostraron una forma elegante de separar los datos internos del sistema de lo que realmente necesita ver el cliente.

---

## Video de sustentación

