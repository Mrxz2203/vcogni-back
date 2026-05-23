# V-COGNI · Backend

API REST del sistema de identificación de estilos cognitivos. Desarrollada con **FastAPI + SQLAlchemy + PostgreSQL**.

---

## ¿Qué hace este backend?

Gestiona la autenticación de usuarios, almacena las métricas de gaze capturadas por WebGazer.js, y clasifica el perfil cognitivo del estudiante (**Visual** o **Verbal**) usando un algoritmo basado en fijaciones y sacadas oculares.

---

## Tecnologías utilizadas

| Tecnología | Versión | Uso |
|---|---|---|
| FastAPI | 0.100+ | Framework de la API REST |
| SQLAlchemy | 2.0+ | ORM para base de datos |
| PostgreSQL | 14+ | Base de datos relacional |
| Alembic | 1.12+ | Migraciones de base de datos |
| Pydantic | 2+ | Validación de datos |
| Python-Jose | 3.3+ | Generación y verificación de JWT |
| Passlib + Bcrypt | 1.7.4 / 4.0.1 | Hashing de contraseñas |
| Uvicorn | 0.23+ | Servidor ASGI |

---

## Requisitos previos

- Python 3.10 o superior (recomendado 3.11)
- PostgreSQL 14 o superior instalado y corriendo
- pgAdmin (opcional, para visualizar la base de datos)

---

## Instalación

**1. Abre la carpeta BackCogni y crea el entorno virtual:**

```bash
cd BackCogni
python -m venv venv
```

**2. Activa el entorno virtual:**

```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

**3. Instala las dependencias:**

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt==4.0.1 python-multipart alembic pydantic pydantic-settings python-dotenv
```

**4. Configura el archivo `.env`:**

Crea un archivo `.env` en la raíz de `BackCogni/` con este contenido:

```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/vcogni_db
SECRET_KEY=clave_secreta_muy_larga_aqui_123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

Reemplaza `TU_PASSWORD` con tu contraseña de PostgreSQL.

**5. Crea la base de datos en PostgreSQL:**

Abre pgAdmin o psql y ejecuta:

```sql
CREATE DATABASE vcogni_db;
```

**6. Inicia el servidor:**

```bash
uvicorn app.main:app --reload
```

El backend estará disponible en: `http://localhost:8000`

La documentación interactiva (Swagger UI) en: `http://localhost:8000/docs`

---

## Estructura del proyecto

```
BackCogni/
├── app/
│   ├── core/
│   │   ├── config.py           ← Variables de entorno (.env)
│   │   ├── database.py         ← Conexión a PostgreSQL
│   │   └── security.py         ← JWT y bcrypt
│   ├── models/
│   │   ├── user.py             ← Tabla users
│   │   ├── session.py          ← Tabla sessions
│   │   ├── gaze_metric.py      ← Tabla gaze_metrics
│   │   └── result.py           ← Tabla results
│   ├── schemas/
│   │   ├── user.py             ← Validación registro/login
│   │   ├── session.py          ← Validación sesiones y gaze
│   │   └── result.py           ← Validación resultados
│   ├── routers/
│   │   ├── auth.py             ← POST /auth/registro y /auth/login
│   │   ├── sessions.py         ← POST /sesiones/*
│   │   └── results.py          ← GET /resultados/*
│   ├── services/
│   │   ├── auth_service.py     ← Lógica de registro y login
│   │   ├── gaze_service.py     ← Lógica de sesiones y métricas
│   │   └── ml_service.py       ← Clasificación Visual/Verbal
│   └── main.py                 ← Punto de entrada FastAPI
├── alembic/                    ← Migraciones de base de datos
├── .env                        ← Variables de entorno (no subir a git)
├── requirements.txt
└── alembic.ini
```

---

## Tablas de la base de datos

| Tabla | Descripción |
|---|---|
| `users` | Estudiantes y docentes registrados |
| `sessions` | Cada prueba biométrica realizada |
| `gaze_metrics` | Métricas oculares capturadas por WebGazer |
| `results` | Resultado de clasificación por sesión |

Las tablas se crean automáticamente al iniciar el servidor gracias a:
```python
Base.metadata.create_all(bind=engine)
```

---

## Endpoints disponibles

### Autenticación

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/auth/registro` | Registrar nuevo usuario |
| POST | `/auth/login` | Iniciar sesión · devuelve JWT |

### Sesiones

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/sesiones/iniciar` | Crear nueva sesión de prueba |
| POST | `/sesiones/guardar-gaze` | Guardar métricas de WebGazer |
| POST | `/sesiones/finalizar` | Finalizar sesión y clasificar perfil |

### Resultados

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/resultados/ultimo/{user_id}` | Último resultado del estudiante |
| GET | `/resultados/historial/{user_id}` | Historial de todas las pruebas |
| GET | `/resultados/perfil/{user_id}` | Datos del perfil del usuario |
| PUT | `/resultados/perfil/{user_id}` | Actualizar nombre y carrera |

---

## Lógica de clasificación

El perfil se clasifica en `ml_service.py` usando las métricas de gaze:

```
Perfil Visual  → duración media de fijación > 250ms Y ratio fijaciones/sacadas > 1.2
Perfil Verbal  → duración media de fijación ≤ 250ms O ratio fijaciones/sacadas ≤ 1.2
```

Esta lógica es la base para integrar el modelo **CNN + XGBoost** descrito en el paper.

---

## Roles de usuario

| Rol | Descripción |
|---|---|
| `estudiante` | Realiza pruebas biométricas y ve sus resultados |
| `docente` | Ve los resultados de sus estudiantes |
| `admin` | Gestiona usuarios e instituciones |

---

## Seguridad

- Las contraseñas se hashean con **bcrypt** antes de guardarse.
- La autenticación usa tokens **JWT** con expiración de 8 horas.
- El CORS está configurado para aceptar peticiones de `http://localhost:5173`.

---

## Comandos útiles

| Comando | Descripción |
|---|---|
| `uvicorn app.main:app --reload` | Iniciar servidor con auto-recarga |
| `uvicorn app.main:app --host 0.0.0.0` | Exponer en red local |
| `alembic revision --autogenerate -m "descripcion"` | Crear migración |
| `alembic upgrade head` | Aplicar migraciones pendientes |

---

## Notas importantes

- El archivo `.env` **no debe subirse a Git**. Agrégalo a `.gitignore`.
- Usa **bcrypt==4.0.1** y **passlib==1.7.4** para evitar errores de compatibilidad con Python 3.11+.
- Las tablas se recrean automáticamente si no existen. Si necesitas modificar una tabla existente, usa migraciones con Alembic.

---

## Autor

Desarrollado como parte del paper académico **V-COGNI: Sistema de identificación de estilos cognitivos mediante biometría ocular** · 2026