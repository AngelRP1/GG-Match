# GG-Match: Auth & Teams Service

Este repositorio contiene el microservicio de Autenticación y Gestión de Usuarios para el proyecto **GG-Match**, desarrollado con un enfoque de arquitectura escalable.

## Arquitectura y Stack Tecnológico

El servicio está completamente dockerizado y aislado, garantizando un entorno agnóstico al sistema operativo.

* **Backend:** Python 3.11 con FastAPI.
* **Base de Datos:** PostgreSQL 15 (vía SQLAlchemy ORM).
* **Seguridad:** Encriptación de contraseñas con `bcrypt` (Passlib) y control de sesiones mediante Tokens JWT (JSON Web Tokens) bajo el estándar OAuth2.
* **Infraestructura:** Docker & Docker Compose.

## ¿Cómo levantar el entorno local?

El proyecto utiliza contenedores para orquestar la API junto con su base de datos. Para iniciar el sistema completo:

1. Clona el repositorio.
2. Posiciónate en la carpeta raíz (`/GG-Match`).
3. Ejecuta el siguiente comando para construir las imágenes y levantar la red:

\`\`\`bash
docker compose up -d --build
\`\`\`

## Documentación de la API

FastAPI autogenera la documentación interactiva en tiempo real. Una vez que los contenedores estén corriendo, puedes probar los endpoints accediendo a:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoints Principales:
* `GET /` - Health check del servidor y conexión a base de datos.
* `POST /usuarios/` - Creación de nuevos usuarios con hash de contraseña.
* `POST /login` - Generación de Token JWT para acceso autorizado.