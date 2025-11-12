# Library Management API

API REST para la gestión de una biblioteca, desarrollada con FastAPI. Permite gestionar libros y autores con operaciones CRUD completas.

## 📋 Requisitos Previos

- Python 3.13 o superior
- Poetry (gestor de dependencias)

## 🚀 Instrucciones de Instalación

1. **Clonar el repositorio** (si aplica):
```bash
git clone https://github.com/PablitoCortes/prueba-ABPO.git
cd "prueba-ABPO"
```

2. **Instalar Poetry** (si no lo tienes instalado):
```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/Mac
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Instalar las dependencias del proyecto**:
```bash
poetry add fastapi
poetry add "uvicorn[standard]"
poetry add sqlalchemy
poetry add pydantic
poetry add python-dotenv
poetry add "python-jose[cryptography]"
poetry add "passlib[bcrypt]"
poetry add pytest --group dev

```

4. **Activar el entorno virtual**:
```bash
poetry shell
```

O si prefieres usar el entorno virtual directamente:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

5. **Inicializar la base de datos**:
La base de datos se inicializa automáticamente al ejecutar la aplicación por primera vez. El archivo `db/library.db` se creará automáticamente.

6. **Configurar variables de entorno**:
Crea un archivo `.env` en la raíz del proyecto con al menos las siguientes variables:
```bash
SECRET_KEY="cambia-este-valor-por-uno-seguro"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
Puedes generar un valor seguro para `SECRET_KEY` con `openssl rand -hex 32` o utilizando cualquier generador de cadenas aleatorias.

## ▶️ Cómo Ejecutar el Proyecto

1. **Asegúrate de estar en el entorno virtual** (ver paso 4 de instalación)

2. **Ejecutar el servidor**:
```bash
python app.py
```

O usando uvicorn directamente:
```bash
uvicorn app:app --host 0.0.0.0 --port 4000 --reload
```

3. **Acceder a la documentación interactiva**:
Una vez que el servidor esté corriendo, puedes acceder a:
- **Swagger UI**: http://localhost:4000/docs
- **ReDoc**: http://localhost:4000/redoc

El servidor estará disponible en: `http://localhost:4000`

## 📚 Ejemplos de Uso de la API

### Autenticación (Users)

#### Registrar un nuevo usuario
```bash
curl -X POST "http://localhost:4000/users/register" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"usuario_demo\",
    \"password\": \"SuperSecreto123\"
  }"
```

#### Iniciar sesión y obtener token
```bash
curl -X POST "http://localhost:4000/users/login" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"usuario_demo\",
    \"password\": \"SuperSecreto123\"
  }"
```
La respuesta devolverá un `access_token`. Guárdalo y envíalo en el header `Authorization` como `Bearer <token>` en cada petición protegida.

#### Consultar perfil autenticado
```bash
curl -X GET "http://localhost:4000/users/profile" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <token>"
```

### Autores (Authors)

#### Obtener todos los autores
```bash
curl -X GET "http://localhost:4000/authors/" \
  -H "accept: application/json"
```

#### Obtener un autor por ID
```bash
curl -X GET "http://localhost:4000/authors/1" \
  -H "accept: application/json"
```

#### Crear un nuevo autor
```bash
curl -X POST "http://localhost:4000/authors/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Gabriel García Márquez\",
    \"birth_date\": \"1927-03-06\",
    \"nationality\": \"Colombiana\"
  }"
```

#### Actualizar un autor
```bash
curl -X PUT "http://localhost:4000/authors/1" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Gabriel García Márquez\",
    \"nationality\": \"Colombiana\"
  }"
```

#### Eliminar un autor
```bash
curl -X DELETE "http://localhost:4000/authors/1" \
  -H "accept: application/json"
```

### Libros (Books)

#### Obtener todos los libros (con paginación y filtros)
```bash
# Obtener primera página (10 libros por defecto)
curl -X GET "http://localhost:4000/books/?page=1&limit=10" \
  -H "accept: application/json"

# Filtrar solo libros disponibles
curl -X GET "http://localhost:4000/books/?isAvailable=true" \
  -H "accept: application/json"

# Buscar libros por título
curl -X GET "http://localhost:4000/books/?title=Cien" \
  -H "accept: application/json"

# Combinar filtros
curl -X GET "http://localhost:4000/books/?page=1&limit=5&isAvailable=true&title=cien" \
  -H "accept: application/json"
```

#### Obtener un libro por ID
```bash
curl -X GET "http://localhost:4000/books/1" \
  -H "accept: application/json"
```

#### Crear un nuevo libro
```bash
curl -X POST "http://localhost:4000/books/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Cien años de soledad\",
    \"isbn\": \"978-84-376-0494-7\",
    \"author_id\": 1,
    \"published_year\": 1967,
    \"genre\": \"Realismo mágico\",
    \"isAvailable\": true
  }"
```

#### Actualizar un libro
```bash
curl -X PUT "http://localhost:4000/books/1" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Cien años de soledad (Edición especial)\",
    \"isAvailable\": false
  }"
```

#### Eliminar un libro
```bash
curl -X DELETE "http://localhost:4000/books/1" \
  -H "accept: application/json"
```

## 🏗️ Decisiones Técnicas

### Framework: FastAPI
Se eligió **FastAPI** como framework principal por las siguientes razones:
- **Alto rendimiento**: Basado en Starlette y Pydantic, comparable a Node.js y Go
- **Documentación automática**: Genera documentación interactiva (Swagger/OpenAPI) automáticamente
- **Validación de datos integrada**: Usa Pydantic para validación y serialización automática
- **Type hints nativos**: Soporte completo para anotaciones de tipo de Python
- **Async/await**: Soporte nativo para operaciones asíncronas

### Base de Datos: SQLite con SQLAlchemy ORM
- **SQLite**: Ademas de ser requisito para esta prueba, se ha elegido SQLite por su simplicidad para desarrollo y pruebas. No requiere configuración de servidor, es ligera y suficiente para proyectos de tamaño medio
- **SQLAlchemy ORM**: Proporciona una capa de abstracción que facilita el mantenimiento del código y permite migrar a otras bases de datos (PostgreSQL, MySQL) en el futuro sin cambios mayores

### Arquitectura en Capas
Se implementó una arquitectura en capas para separar responsabilidades:

```
routes/          → Endpoints HTTP, manejo de requests/responses
services/        → Lógica de negocio y reglas de dominio
models/          → Modelos de base de datos (SQLAlchemy)
schemas/         → Esquemas de validación (Pydantic)
db/              → Configuración de base de datos
```

**Ventajas**:
- **Separación de responsabilidades**: Cada capa tiene un propósito claro
- **Mantenibilidad**: Cambios en una capa no afectan directamente a otras
- **Testabilidad**: Fácil de testear cada capa de forma independiente
- **Escalabilidad**: Fácil agregar nuevas funcionalidades sin afectar código existente

### Validación con Pydantic
- **Schemas separados**: `CreateBookSchema`, `UpdateBookSchema`, `BookOut` para diferentes contextos
- **Validación automática**: FastAPI valida automáticamente los datos de entrada usando los schemas
- **Documentación automática**: Los schemas se reflejan automáticamente en la documentación de la API

### Manejo de Excepciones Personalizado
Se crearon excepciones personalizadas (`NotFoundError`, `BadRequestError`) para:
- **Consistencia**: Manejo uniforme de errores en toda la aplicación
- **Claridad**: Mensajes de error más descriptivos y específicos
- **Mantenibilidad**: Centralizar la lógica de manejo de errores

### Optimización de Queries
- **joinedload**: Se utiliza `joinedload(Book.author)` para evitar el problema N+1 en las consultas, cargando la relación con el autor en una sola query
- **Filtros opcionales**: Los endpoints de listado soportan filtros (disponibilidad, título) para reducir la cantidad de datos transferidos

### Gestión de Dependencias: Poetry
- **Reproducibilidad**: Garantiza que todos los desarrolladores usen las mismas versiones de dependencias
- **Manejo de entornos**: Facilita la gestión de entornos virtuales
- **Lock file**: `poetry.lock` asegura instalaciones consistentes

### Paginación
Los endpoints de listado implementan paginación para:
- **Rendimiento**: Evitar cargar grandes cantidades de datos de una vez
- **Experiencia de usuario**: Mejor respuesta en aplicaciones cliente
- **Escalabilidad**: Preparado para manejar grandes volúmenes de datos

### Configuración del Servidor
- **Host 0.0.0.0**: Permite acceso desde cualquier interfaz de red
- **Puerto 4000**: Puerto personalizado para evitar conflictos
- **Reload automático**: Modo desarrollo con recarga automática al detectar cambios

### Autenticación y Seguridad
- **OAuth2 con JWT**: Se utiliza `OAuth2PasswordBearer` para extraer el token y `python-jose` para firmarlo/verificarlo (`core/auth.py`)
- **Tokens configurables**: Duración (`ACCESS_TOKEN_EXPIRE_MINUTES`), algoritmo (`ALGORITHM`) y clave (`SECRET_KEY`) provienen de variables de entorno
- **Contraseñas hasheadas**: `passlib[bcrypt]` gestiona el hashing y verificación de contraseñas (`core/security.py`)
- **Usuarios persistidos**: El modelo `User` en `models/user_model.py` almacena credenciales y permite ampliar la lógica de roles o permisos
- **Protección de rutas**: Los routers `author_router.py` y `book_router.py` usan `Depends(get_current_user)` para exigir autenticación en todas las operaciones CRUD

## 🧪 Testing

El proyecto incluye tests en la carpeta `tests/`. Para ejecutarlos:

```bash
pytest
```

## 📝 Estructura del Proyecto

```
prueba ABPO/
├── app.py                 # Punto de entrada de la aplicación
├── db/
│   └── db.py             # Configuración de base de datos
├── models/               # Modelos SQLAlchemy
│   ├── author_model.py
│   └── book_model.py
├── routes/               # Endpoints de la API
│   ├── author_router.py
│   └── book_router.py
├── schemas/              # Schemas Pydantic
│   ├── author_schema.py
│   └── book_schema.py
├── services/             # Lógica de negocio
│   ├── authors/
│   │   └── author_services.py
│   ├── books/
│   │   └── book_services.py
│   └── exceptions.py
├── tests/                # Tests
│   ├── author_tests.py
│   └── book_tests.py
└── pyproject.toml        # Configuración de Poetry
```

## 📄 Licencia

Este proyecto es parte de una prueba técnica.

