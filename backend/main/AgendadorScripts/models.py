from django.db import models

class Scripts(models.Model):

    nome = models.CharField(
        "Nome do Script", 
        max_length = 100,
        blank = False,
        null = False,
        help_text = "Apelido ou nome do script a ser executado."
    )

    responsavel = models.CharField(
        "Responsável", 
        max_length = 100,
        blank = True,
        help_text = "Responsável pelo Script"
    )

    caminho_script = models.CharField(
        "Caminho do Script", 
        max_length = 255,
        blank = False,
        null = False,
        help_text = "Caminho completo do script a ser executado."
    )
    
    class Meta:

        verbose_name = "Script"
        verbose_name_plural = "Scripts"

    def __str__(self):
        return self.nome

class Agendamento(models.Model):

    FREQUENCIA_CHOICES = [
        ('U', 'Uma vez'),
        ('D', 'Diário'),
        ('S', 'Semanal'),
        ('M', 'Mensal'),
    ]

    TEMPO_REPETICAO_CHOICES = [
        ('DIA', 'Dia(s)'),
        ('HORA', 'Hora(s)'),
        ('MIN', 'Minuto(s)'),
    ]

    script = models.ForeignKey(
        Scripts, 
        on_delete = models.CASCADE, 
        related_name = "agendamentos", 
        null = True
    )

    frequencia = models.CharField(
        "Frequência",
        max_length = 1, 
        choices = FREQUENCIA_CHOICES
    )

    tempo_repeticao = models.CharField(
        "Intervalo de Repetição",
        max_length = 4,
        choices = TEMPO_REPETICAO_CHOICES,
        blank = True,
        null = True,
        help_text = "Especifique o intervalo caso a frequência seja repetitiva (ex.: a cada X horas)."
    )

    intervalo = models.PositiveIntegerField(
        "Intervalo(X)",
        blank = True,
        null = True,
        help_text = "Número de horas, minutos ou dias de repetição."
    )

    hora_inicial = models.TimeField(
        "Hora Inicial",
        blank = True, 
        null = True,
        help_text = "Horário da primeira execução do Script."
    )

    hora_final = models.TimeField(
        "Hora Final",
        blank = True, 
        null = True,
        help_text = "Horário da última execução do Script."
    )

    data_agendamento = models.DateTimeField(
        "Data e Hora da Proxima Execução", 
        blank = True, 
        null = True,
        help_text = "Data: Ano-Mês-Dia"
    )

    class Meta:

        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"{self.get_frequencia_display()} - {self.script.caminho_script}"
