# Email Auth Remote

Проект для интеграции МС рассылки с другими Django МС.

## Как пользоваться

Добавить проект в INSTALLED_APPS

```python
# File: settings.py

INSTALLED_APPS = [
    ...
    "mailing_backend",
]
```

Установить переменную EMAIL_ENDPOINT_URL

```python
# File: settings.py

EMAIL_ENDPOINT_URL = "http://localhost:8000/mailing"  # Как пример
```

## Сборка

Как собрать проект локально

```bash
python3 -m pip install build
python3 -m build 
```

### Проверка собранного пакета
```bash
python3 -m pip install twine
twine check dist/*
```

### Выкладывание проекта в PYPI
```bash
twine upload dist/*
```