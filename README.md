# microblogging-service
Итоговый проект по дополнительному курсу "Python". 

![Цветная штучка](https://img.shields.io/badge/%20Microblogging-you_like-blue)

## Запуск
1. Запустить сервисы через Docker.
    ```
    docker-compose up -d
    ```
2. Запустить миграции.
    ```
    alembic upgrade head
    ```
3. Запустить главный сервис.
    ```
    python -m app.main
    ```

Приколы:
```
flake8 --ignore=F401,F403 app
```

