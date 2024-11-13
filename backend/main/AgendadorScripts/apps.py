import threading
from django.apps import AppConfig

class AgendadorscriptsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AgendadorScripts'

    def ready(self):

        def start_agendamento():
            
            from . import agendamento
            agendamento.iniciar_agendador()

        thread = threading.Thread(target=start_agendamento)
        thread.daemon = True
        thread.start()
