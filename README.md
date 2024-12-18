# webtest

1
```bash
cd webtest
```
2
```bash
pip install -r requirements.txt
```
3
```bash
flask --app main.py run
```

### Нужно вписать в __init__.py свое имя базы данных, пароль и порт (порт по умолчанию 5432):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://имябазыданных:пароль@localhost:порт"
    app.config['SQLALCHEMY_BINDS'] = {
        "auth": "postgresql://имябазыданных:пароль@localhost:порт/auth"
    }
### В моем случае "postgresql://postgres:qwerty@localhost:5432"
