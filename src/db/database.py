



TORTOISE_ORM = {
    "connections": {
         "default": "sqlite://manager.sqlite3"
    },
    "apps": {
        "contact": {
            "models": [
                 "src.db.models", "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}