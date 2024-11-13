
import os
import sys
import time
import django
import schedule
import subprocess 
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')  # Verifique se o nome do seu app raiz está correto
django.setup()

from AgendadorScripts.models import Agendamento, Scripts

def executar_script(caminho):
        
        if '.py' in caminho:

            print(f"SCI Atendimento aberto ás : {datetime.now().strftime('%H:%M')}")
            processo = subprocess.Popen(
                ["python", str(caminho)],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            process_id = processo.pid
            return process_id
        
        elif '.bat' in caminho:

            print(f"Executando script .bat às: {datetime.now().strftime('%H:%M')}")
            processo = subprocess.Popen(
                [str(caminho)],
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            process_id = processo.pid
            return process_id

def verificar_agendamentos():

    agora = datetime.now()
    agendamentos = Agendamento.objects.all()

    for agendamento in agendamentos:
        
        script = agendamento.script
        hora_inicial = agendamento.hora_inicial
        intervalo_de_repeticao = agendamento.tempo_repeticao  
        intervalo_tempo = agendamento.intervalo 

        primeira_execucao = datetime.combine(agora.date(), hora_inicial)

        if agendamento.data_agendamento is None:
            proxima_execucao = primeira_execucao
        else:
            proxima_execucao = agendamento.data_agendamento

        agora_hora_minuto = agora.replace(second=0, microsecond=0)
        proxima_execucao_hora_minuto = proxima_execucao.replace(second=0, microsecond=0)

        if agora_hora_minuto >= proxima_execucao_hora_minuto:

            executar_script(script.caminho_script)

            if intervalo_de_repeticao == 'DIA':
                proxima_execucao = agora + timedelta(days=intervalo_tempo)
            elif intervalo_de_repeticao == 'HORA':
                proxima_execucao = agora + timedelta(hours=intervalo_tempo)
            elif intervalo_de_repeticao == 'MIN':
                proxima_execucao = agora + timedelta(minutes=intervalo_tempo)

            agendamento.data_agendamento = proxima_execucao
            agendamento.save()

def iniciar_agendador():
    
    schedule.every(5).seconds.do(verificar_agendamentos)

    while True:

        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    iniciar_agendador()
