
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

def executar_script(script):
        
        if '.py' in script.caminho_script:

            print(f"Script '.py' {script.nome} aberto no horário: {datetime.now().strftime('%H:%M')}")
            processo = subprocess.Popen(
                ["python", str(script.caminho_script)],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            process_id = processo.pid
            return process_id
        
        elif '.bat' in script.caminho_script:

            print(f"Script '.bat' {script.nome} aberto no horário: {datetime.now().strftime('%H:%M')}")

            comando = f'start cmd /c "{script.caminho_script}"'

            processo = subprocess.Popen(
                comando, 
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
        hora_final = agendamento.hora_final

        # primeira_execucao = datetime.combine(agora.date(), hora_inicial)

        if agendamento.data_agendamento is None:

            amanha = datetime.now().date() + timedelta(days=1)
            proxima_execucao = datetime.combine(amanha, hora_inicial)

        else:
            
            proxima_execucao = agendamento.data_agendamento

        agora_hora_minuto = agora.replace(second=0, microsecond=0)
        proxima_execucao_hora_minuto = proxima_execucao.replace(second=0, microsecond=0)

        if hora_final:

            if agora_hora_minuto >= datetime.combine(agora.date(), hora_inicial) and agora_hora_minuto <= datetime.combine(agora.date(), hora_final):
            
                if not agendamento.data_agendamento: 

                    executar_script(script)

                    if intervalo_de_repeticao == 'DIA':
                        proxima_execucao = agora + timedelta(days=intervalo_tempo)
                    elif intervalo_de_repeticao == 'HORA':
                        proxima_execucao = agora + timedelta(hours=intervalo_tempo)
                    elif intervalo_de_repeticao == 'MIN':
                        proxima_execucao = agora + timedelta(minutes=intervalo_tempo)

                    agendamento.data_agendamento = proxima_execucao
                    agendamento.save()

                elif agora_hora_minuto == proxima_execucao_hora_minuto:

                    executar_script(script)

                    if intervalo_de_repeticao == 'DIA':
                        proxima_execucao = agora + timedelta(days=intervalo_tempo)
                    elif intervalo_de_repeticao == 'HORA':
                        proxima_execucao = agora + timedelta(hours=intervalo_tempo)
                    elif intervalo_de_repeticao == 'MIN':
                        proxima_execucao = agora + timedelta(minutes=intervalo_tempo)

                    agendamento.data_agendamento = proxima_execucao
                    agendamento.save()
                
            else:
                
                amanha = datetime.now().date() + timedelta(days=1)
                agendamento.data_agendamento = datetime.combine(amanha, hora_inicial)
                agendamento.save() 

        elif agora_hora_minuto >= proxima_execucao_hora_minuto:

            executar_script(script)

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
