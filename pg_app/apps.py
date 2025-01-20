from django.apps import AppConfig


class PgAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pg_app'

    def ready(self):
        import pg_app.signals
