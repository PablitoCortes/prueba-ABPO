# Tests Unitarios

Este directorio contiene los tests unitarios del proyecto.

## Estructura de Tests

- `conftest.py`: Configuración compartida de pytest (fixtures, base de datos de prueba)
- `test_author_services.py`: Tests unitarios para los servicios de autores
- `test_book_services.py`: Tests unitarios para los servicios de libros
- `test_api_endpoints.py`: Tests de integración para los endpoints de la API

## Ejecutar Tests

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar tests con más detalle
```bash
pytest -v
```

### Ejecutar tests con cobertura
```bash
pytest --cov=. --cov-report=html
```

### Ejecutar un archivo específico
```bash
pytest tests/test_author_services.py
```

### Ejecutar un test específico
```bash
pytest tests/test_author_services.py::TestAuthorServices::test_create_author_success
```

### Ejecutar tests en modo watch (requiere pytest-watch)
```bash
ptw
```

## Configuración

Los tests usan una base de datos SQLite en memoria (`:memory:`) que se crea y destruye para cada test, asegurando aislamiento completo entre tests.

## Fixtures Disponibles

- `db_session`: Sesión de base de datos de prueba
- `client`: Cliente de prueba de FastAPI
- `test_user_token`: Token de autenticación para tests que requieren autenticación

## Notas

- Los tests de endpoints requieren autenticación, por lo que usan el fixture `test_user_token`
- Cada test tiene su propia base de datos limpia
- Los tests están organizados por clases que agrupan tests relacionados

